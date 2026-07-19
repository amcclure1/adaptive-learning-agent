"""Deterministic authored-content validation and authority-free reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError

from .approvals import current_decision
from .schemas import seal_record, validate_record
from .workspace import all_stored_records, atomic_write, reference, store_immutable
from .canonical import canonical_json_file_bytes


VALIDATOR_VERSION = "1.0.0"
RULE_SET_ID = "ala-authoring-workspace"
RULE_SET_VERSION = "1"


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: str
    blocking: bool
    artifact: str
    field: str
    message: str


def _finding(code: str, artifact: str, field: str, message: str, *, severity: str = "error", blocking: bool = True) -> Finding:
    return Finding(code, severity, blocking, artifact, field, message)


def _key(record: dict[str, Any]) -> tuple[str, str, int, str]:
    return record["artifact_type"], record["artifact_id"], record["revision"], record["canonical_digest"]


def _source_reference_key(item: dict[str, Any]) -> tuple[str, str, int, str]:
    return "source", item["source_id"], item["revision"], item["canonical_digest"]


def _schema_finding_code(error: LearningError) -> str:
    field = error.details.get("field", "") if error.details else ""
    message = error.message.lower()
    if "missing fields" in message:
        return "FIELD_MISSING"
    if "unknown fields" in message:
        return "FIELD_UNKNOWN"
    if "canonical_digest" in field or "digest" in message:
        return "DIGEST_MISMATCH"
    if field.endswith("revision") or "revision" in message:
        return "REVISION_INVALID"
    if "artifact-id" in message or field.endswith("_id"):
        return "ID_INVALID"
    if "source_category" in field or "source_category" in message:
        return "SOURCE_CATEGORY_INVALID"
    if "option_rationales" in field or "rationale" in message:
        return "RATIONALE_MISSING"
    if "requirement_option_matrix" in field or "matrix" in message:
        return "REQUIREMENT_MATRIX_INCOMPLETE"
    if "selection count" in message or "key count" in message:
        return "SELECTION_COUNT_MISMATCH"
    return "SCHEMA_INVALID"


def validate_workspace(
    workspace: Path,
    *,
    as_of: str,
    workspace_commit: str,
    validation_id: str | None = None,
    executed_at: str | None = None,
    persist: bool = False,
) -> dict[str, Any]:
    """Validate every stored authoring artifact; no finding implies human approval."""

    try:
        cutoff = date.fromisoformat(as_of)
    except ValueError as exc:
        raise LearningError("AUTHORING_VALIDATION_INVALID", "as_of must be an ISO calendar date.") from exc
    stored = all_stored_records(workspace)
    findings: list[Finding] = []
    valid: list[tuple[dict[str, Any], str | None, Path]] = []
    for record, markdown, path in stored:
        try:
            validate_record(record, markdown=markdown)
            valid.append((record, markdown, path))
        except LearningError as exc:
            findings.append(_finding(_schema_finding_code(exc), str(record.get("artifact_id", path.name)), exc.details.get("field", "$") if exc.details else "$", exc.message))
    index = {_key(record): record for record, _, _ in valid}
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record, _, _ in valid:
        by_type.setdefault(record["artifact_type"], []).append(record)

    def resolve(ref: dict[str, Any], artifact: str, field: str) -> dict[str, Any] | None:
        key = (ref.get("artifact_type"), ref.get("artifact_id"), ref.get("revision"), ref.get("canonical_digest"))
        result = index.get(key)
        if result is None:
            findings.append(_finding("REFERENCE_MISSING", artifact, field, "The exact referenced artifact is missing or mismatched."))
        return result

    for source in by_type.get("source", []):
        artifact = source["artifact_id"]
        if source["source_category"] == "prohibited_material" or source["authority_tier"] == "excluded" or source["rights_reuse"] == "prohibited":
            findings.append(_finding("SOURCE_PROHIBITED", artifact, "source_category", "Prohibited or excluded sources cannot support authored content."))
        if source["rights_reuse"] == "unresolved":
            findings.append(_finding("SOURCE_RIGHTS_UNRESOLVED", artifact, "rights_reuse", "Unresolved source rights block compilation."))
        if source["status"] != "draft" and current_decision(workspace, target=reference(source), decision_type="source_approval") is None:
            findings.append(_finding("SOURCE_APPROVAL_MISSING", artifact, "review_state", "A current source approval over this exact digest is required."))

    for claim in by_type.get("claim", []):
        artifact = claim["artifact_id"]
        horizon = claim["freshness_horizon"]["valid_through"]
        if claim["status"] == "stale" or claim["invalidation_state"]["status"] != "current" or (horizon is not None and date.fromisoformat(horizon) < cutoff):
            findings.append(_finding("CLAIM_STALE", artifact, "freshness_horizon", "The claim is stale, invalidated, or outside its freshness horizon."))
        for index_value, source_ref in enumerate(claim["source_references"]):
            source = index.get(_source_reference_key(source_ref))
            if source is None:
                findings.append(_finding("REFERENCE_MISSING", artifact, f"source_references[{index_value}]", "The exact source reference is missing or mismatched."))
            elif claim["status"] != "draft" and current_decision(workspace, target=reference(source), decision_type="source_approval") is None:
                findings.append(_finding("SOURCE_APPROVAL_MISSING", artifact, f"source_references[{index_value}]", "The claim depends on an unapproved source."))
        if claim["category"] == "derived_recommendation":
            if not claim["derived_from"]:
                findings.append(_finding("DERIVED_PREMISE_MISSING", artifact, "derived_from", "A derived recommendation requires approved premise claims."))
            for index_value, premise_ref in enumerate(claim["derived_from"]):
                premise = resolve(premise_ref, artifact, f"derived_from[{index_value}]")
                if claim["status"] != "draft" and premise is not None and current_decision(workspace, target=reference(premise), decision_type="claim_approval") is None:
                    findings.append(_finding("CLAIM_APPROVAL_MISSING", artifact, f"derived_from[{index_value}]", "A premise claim lacks current approval."))
        if claim["status"] != "draft" and current_decision(workspace, target=reference(claim), decision_type="claim_approval") is None:
            findings.append(_finding("CLAIM_APPROVAL_MISSING", artifact, "human_review_state", "A current claim approval over this exact digest is required."))

    claim_graph = {
        _key(claim): [
            (ref["artifact_type"], ref["artifact_id"], ref["revision"], ref["canonical_digest"])
            for ref in claim["derived_from"]
        ]
        for claim in by_type.get("claim", [])
    }
    visiting: set[tuple[str, str, int, str]] = set()
    visited: set[tuple[str, str, int, str]] = set()

    def visit_claim(node: tuple[str, str, int, str]) -> None:
        if node in visiting:
            findings.append(_finding("DERIVED_PREMISE_CYCLE", node[1], "derived_from", "Derived claim references must be acyclic."))
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in claim_graph.get(node, []):
            visit_claim(dependency)
        visiting.remove(node)
        visited.add(node)

    for claim_key in claim_graph:
        visit_claim(claim_key)

    lesson_markdown = {record["artifact_id"]: markdown for record, markdown, _ in valid if record["artifact_type"] == "lesson"}
    for lesson in by_type.get("lesson", []):
        artifact = lesson["artifact_id"]
        if lesson["status"] == "draft":
            continue
        if lesson["status"] != "active":
            findings.append(_finding("DRAFT_CONTENT", artifact, "status", "Only active immutable lessons are compilation eligible."))
        for index_value, claim_ref in enumerate(lesson["claim_references"]):
            claim = resolve(claim_ref, artifact, f"claim_references[{index_value}]")
            if claim is not None and current_decision(workspace, target=reference(claim), decision_type="claim_approval") is None:
                findings.append(_finding("LESSON_UNAPPROVED_CLAIM", artifact, f"claim_references[{index_value}]", "The lesson uses an unapproved claim."))
        if current_decision(workspace, target=reference(lesson), decision_type="lesson_content_review") is None:
            findings.append(_finding("LESSON_REVIEW_MISSING", artifact, "content_review_state", "A current lesson-content review is required."))
        if lesson_markdown.get(artifact) is None:
            findings.append(_finding("LESSON_MARKDOWN_MISSING", artifact, "markdown_path", "The lesson Markdown is missing."))

    for spec in by_type.get("question_spec", []):
        if spec["status"] == "draft":
            continue
        if spec["status"] != "active":
            findings.append(_finding("DRAFT_CONTENT", spec["artifact_id"], "status", "Only active immutable question specifications are eligible."))
        if current_decision(workspace, target=reference(spec), decision_type="question_spec_design_review") is None:
            findings.append(_finding("QUESTION_SPEC_REVIEW_MISSING", spec["artifact_id"], "design_review_state", "A current design review is required."))

    for question in by_type.get("question", []):
        artifact = question["artifact_id"]
        if question["status"] == "draft":
            continue
        if question["status"] != "active":
            findings.append(_finding("DRAFT_CONTENT", artifact, "status", "Only active immutable questions are compilation eligible."))
        resolve(question["specification_reference"], artifact, "specification_reference")
        for index_value, claim_ref in enumerate(question["supporting_claim_references"]):
            claim = resolve(claim_ref, artifact, f"supporting_claim_references[{index_value}]")
            if claim is not None and current_decision(workspace, target=reference(claim), decision_type="claim_approval") is None:
                findings.append(_finding("CLAIM_APPROVAL_MISSING", artifact, f"supporting_claim_references[{index_value}]", "The question uses an unapproved claim."))
        if len(question["option_rationales"]) != len(question["options"]):
            findings.append(_finding("RATIONALE_MISSING", artifact, "option_rationales", "Every option requires one internal rationale."))
        if not question["requirement_option_matrix"]:
            findings.append(_finding("REQUIREMENT_MATRIX_INCOMPLETE", artifact, "requirement_option_matrix", "A complete requirement-option matrix is required."))
        if len(question["keyed_option_ids"]) != question["required_selection_count"]:
            findings.append(_finding("SELECTION_COUNT_MISMATCH", artifact, "required_selection_count", "Selection count must match keyed-option count."))
        required = (
            ("question_originality_review", "ORIGINALITY_REVIEW_MISSING", "originality_review_state"),
            ("question_content_approval", "QUESTION_CONTENT_APPROVAL_MISSING", "content_review_state"),
            ("answer_uniqueness_approval", "UNIQUENESS_APPROVAL_MISSING", "answer_uniqueness_state"),
        )
        for decision_type, code, field in required:
            if current_decision(workspace, target=reference(question), decision_type=decision_type) is None:
                findings.append(_finding(code, artifact, field, f"A current {decision_type} decision is required."))

    for decision in by_type.get("approval", []) + by_type.get("review", []):
        target = resolve(decision["target"], decision["artifact_id"], "target")
        if target is not None and target.get("author", {}).get("identity") == decision["reviewer"]["identity"]:
            findings.append(_finding("REVIEWER_CONFLICT", decision["artifact_id"], "reviewer.identity", "An artifact author cannot approve the same artifact."))

    project_records = by_type.get("project", [])
    if len(project_records) != 1:
        findings.append(_finding("PROJECT_COUNT_INVALID", "workspace", "project.json", "Exactly one project record is required."))
    elif project_records:
        scope = project_records[0]["pilot_scope"]
        objective_ids = set(scope["objective_ids"])
        for claim in by_type.get("claim", []):
            unknown_objectives = sorted(set(claim["scope"]["objective_ids"]) - objective_ids)
            if unknown_objectives:
                findings.append(_finding("OBJECTIVE_MAPPING_INVALID", claim["artifact_id"], "scope.objective_ids", "Claim objective mappings must be declared by the project."))
        if "claim_count_range" in scope and by_type.get("claim"):
            claim_count = len(by_type["claim"])
            if not scope["claim_count_range"]["minimum"] <= claim_count <= scope["claim_count_range"]["maximum"]:
                findings.append(_finding("DECLARED_CLAIM_RANGE_MISMATCH", project_records[0]["artifact_id"], "pilot_scope.claim_count_range", "Stored claim count is outside the declared project range."))
        active_lessons = [item for item in by_type.get("lesson", []) if item["status"] == "active"]
        active_questions = [item for item in by_type.get("question", []) if item["status"] == "active"]
        mix = {
            "single_response": sum(item["question_type"] == "single_response" for item in active_questions),
            "multiple_response": sum(item["question_type"] == "multiple_response" for item in active_questions),
        }
        authored_delivery_content = bool(by_type.get("lesson") or by_type.get("question"))
        if authored_delivery_content and (len(active_lessons) != scope["lesson_count"] or len(active_questions) != scope["question_count"] or mix != scope["response_mix"]):
            findings.append(_finding("DECLARED_SCOPE_MISMATCH", project_records[0]["artifact_id"], "pilot_scope", "Active content counts do not match the declared generic project scope."))

    result = "failed" if any(item.blocking for item in findings) else "passed"
    checked = sorted((reference(record) for record, _, _ in valid if record["artifact_type"] != "validation_report"), key=lambda item: (item["artifact_type"], item["artifact_id"], item["revision"], item["canonical_digest"]))
    payload = {"result": result, "findings": [asdict(item) for item in findings], "checked_artifacts": checked, "human_approval_implication": "none"}
    if validation_id is None:
        return payload
    if executed_at is None:
        raise LearningError("AUTHORING_VALIDATION_INVALID", "Persisted validation reports require executed_at.")
    report = seal_record({
        "schema_version": "ala.authoring.validation-report.v1",
        "artifact_id": validation_id,
        "artifact_type": "validation_report",
        "revision": 1,
        "status": "immutable",
        "created_at": executed_at,
        "modified_at": executed_at,
        "author": {"identity": "ala-authoring-validator", "identity_type": "service", "role": "deterministic_validator"},
        "supersedes": None,
        "validation_id": validation_id,
        "validator_name": "adaptive-learning-authoring-validator",
        "validator_version": VALIDATOR_VERSION,
        "rule_set_id": RULE_SET_ID,
        "rule_set_version": RULE_SET_VERSION,
        "executed_at": executed_at,
        "workspace_commit": workspace_commit,
        "checked_artifacts": checked,
        "findings": [asdict(item) for item in findings],
        "result": result,
        "human_approval_implication": "none",
        "output_digest": "0" * 64,
        "canonical_digest": "0" * 64,
    })
    if persist:
        path = workspace / "validations" / "reports" / f"{validation_id}.json"
        store_immutable(workspace, report, path=path)
    return report


def validate_release_evidence(record: dict[str, Any], *, candidate: dict[str, Any] | None = None) -> dict[str, Any]:
    validate_record(record)
    findings: list[Finding] = []
    if candidate is not None:
        for field in ("compiled_pack", "compiler_input_digest", "compiler_output_digest", "source_workspace_commit"):
            if record[field] != candidate[field]:
                findings.append(_finding("RELEASE_EVIDENCE_MISMATCH", record["artifact_id"], field, "Final evidence does not match candidate evidence."))
    return {"result": "failed" if findings else "passed", "findings": [asdict(item) for item in findings], "human_approval_implication": "none"}
