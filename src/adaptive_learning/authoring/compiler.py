"""Deterministic authored-content projection to the unchanged format-0.2 pack."""

from __future__ import annotations

import os
import shutil
import tempfile
import json
from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_digest import normalize_value
from adaptive_learning.pack_validation import _load_v02

from .approvals import current_decision
from .canonical import artifact_digest, canonical_json_bytes, canonical_json_file_bytes, digest_file_set, normalize_markdown, portable_relative_path
from .schemas import SHA256_RE, seal_record, validate_reference
from .validation import validate_release_evidence
from .workspace import atomic_write, find_record, read_record, reference, store_immutable, workspace_lock


AUTHORING_COMPILER_VERSION = "1.0.0+ala-authoring-compiler-v1"
SELECTION_FIELDS = {
    "schema_version", "selection_id", "project", "assessment_blueprint", "learning_architecture",
    "realization_plan", "source_references", "claim_references", "lesson_references",
    "question_specification_references", "question_references", "approval_references",
    "review_references", "validation_report_references", "source_projections", "lesson_projections",
    "question_projections", "pack", "target_pack_format", "compilation_timestamp",
    "source_workspace_commit", "requires_structured_option_teaching",
}
EXCLUSIONS = [
    "claims", "internal_locators", "requirement_option_matrices", "internal_rationales",
    "originality_findings", "uniqueness_findings", "conflict_declarations", "private_notes",
    "reviewer_details",
]
SOURCE_TYPE_MAP = {
    "official_question_pool", "official_errata", "regulation", "official_guidance",
}


def load_candidate_pack(path: Path):
    """Use the existing format-0.2 implementation's explicit internal approval-skip hook."""

    try:
        manifest = normalize_value(json.loads((path / "pack.json").read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LearningError("PACK_VALIDATION_FAILED", "Candidate pack.json is not readable UTF-8 JSON.") from exc
    return _load_v02(path.resolve(), manifest, skip_approval=True)


def _closed(value: Any, label: str, fields: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LearningError("AUTHORING_SELECTION_INVALID", f"{label} must be an object.")
    unknown = set(value) - fields
    missing = fields - set(value)
    if unknown or missing:
        raise LearningError("AUTHORING_SELECTION_INVALID", f"{label} must be closed; unknown={sorted(unknown)}, missing={sorted(missing)}.")
    return value


def _design_reference(value: Any, label: str) -> dict[str, Any]:
    record = _closed(value, label, {"version", "path", "canonical_digest"})
    if not isinstance(record["version"], str) or not record["version"] or not isinstance(record["canonical_digest"], str) or not SHA256_RE.fullmatch(record["canonical_digest"]):
        raise LearningError("AUTHORING_SELECTION_INVALID", f"{label} version or digest is invalid.")
    portable_relative_path(record["path"])
    return record


def validate_selection(selection: dict[str, Any]) -> dict[str, Any]:
    selection = _closed(selection, "selection", SELECTION_FIELDS)
    if selection["schema_version"] != "ala.authoring.selection.v1":
        raise LearningError("SCHEMA_UNSUPPORTED", "The selection schema is unsupported.")
    if selection["target_pack_format"] != "0.2":
        raise LearningError("TARGET_FORMAT_INELIGIBLE", "This implementation compiles only unchanged format 0.2.")
    if selection["requires_structured_option_teaching"] is not False:
        raise LearningError("FORMAT_0_4_REQUIRED", "Structured per-option learner teaching requires a separately proposed format 0.4.")
    if not isinstance(selection["source_workspace_commit"], str) or len(selection["source_workspace_commit"]) != 40 or any(character not in "0123456789abcdef" for character in selection["source_workspace_commit"]):
        raise LearningError("AUTHORING_SELECTION_INVALID", "source_workspace_commit must be a full lowercase Git commit.")
    for field in ("assessment_blueprint", "learning_architecture", "realization_plan"):
        _design_reference(selection[field], field)
    for field, expected_type in (
        ("source_references", "source"), ("claim_references", "claim"), ("lesson_references", "lesson"),
        ("question_specification_references", "question_spec"), ("question_references", "question"),
        ("approval_references", "approval"), ("review_references", "review"),
        ("validation_report_references", "validation_report"),
    ):
        if not isinstance(selection[field], list):
            raise LearningError("AUTHORING_SELECTION_INVALID", f"{field} must be an array.")
        for index, item in enumerate(selection[field]):
            validate_reference(item, f"{field}[{index}]", expected_type=expected_type)
    validate_reference(selection["project"], "project", expected_type="project")
    if not isinstance(selection["source_projections"], list) or not isinstance(selection["lesson_projections"], list) or not isinstance(selection["question_projections"], list):
        raise LearningError("AUTHORING_SELECTION_INVALID", "Projection mappings must be arrays.")
    for index, item in enumerate(selection["source_projections"]):
        projection = _closed(item, f"source_projections[{index}]", {"source_reference", "pack_source_id", "pack_source_type", "rights_id"})
        validate_reference(projection["source_reference"], f"source_projections[{index}].source_reference", expected_type="source")
        if projection["pack_source_type"] not in SOURCE_TYPE_MAP:
            raise LearningError("PROHIBITED_SOURCE", "A source projection uses an unsupported format-0.2 source class.")
    for index, item in enumerate(selection["lesson_projections"]):
        projection = _closed(item, f"lesson_projections[{index}]", {"lesson_reference", "title", "path", "rights_id"})
        validate_reference(projection["lesson_reference"], f"lesson_projections[{index}].lesson_reference", expected_type="lesson")
        portable_relative_path(projection["path"])
    for index, item in enumerate(selection["question_projections"]):
        projection = _closed(item, f"question_projections[{index}]", {"question_reference", "tags", "question_rights_id", "explanation_rights_id"})
        validate_reference(projection["question_reference"], f"question_projections[{index}].question_reference", expected_type="question")
    pack = _closed(selection["pack"], "pack", {"pack_id", "version", "title", "language", "tags", "objectives", "assessment_pool", "rights", "notice_markdown"})
    if not isinstance(pack["objectives"], list) or not isinstance(pack["rights"], list) or not isinstance(pack["tags"], list):
        raise LearningError("AUTHORING_SELECTION_INVALID", "Pack objectives, rights, and tags must be arrays.")
    return selection


def _selection_digest(selection: dict[str, Any]) -> str:
    pseudo = {
        "schema_version": "ala.authoring.selection.v1", "artifact_type": "compiler_input_manifest",
        "selection": selection,
    }
    return artifact_digest(pseudo)


def _resolve_all(workspace: Path, references: list[dict[str, Any]]) -> list[tuple[dict[str, Any], str | None]]:
    return [(record, markdown) for record, markdown, _ in (find_record(workspace, item) for item in references)]


def _ref_key(item: dict[str, Any]) -> tuple[str, str, int, str]:
    return item["artifact_type"], item["artifact_id"], item["revision"], item["canonical_digest"]


def _sorted_refs(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = [_ref_key(item) for item in items]
    if len(set(keys)) != len(keys):
        raise LearningError("AUTHORING_SELECTION_INVALID", "Artifact-reference sets must not contain duplicates.")
    return sorted(items, key=_ref_key)


def _require_decision(workspace: Path, record: dict[str, Any], decision_type: str) -> dict[str, Any]:
    decision = current_decision(workspace, target=reference(record), decision_type=decision_type)
    if decision is None:
        raise LearningError("APPROVAL_MISSING", f"{record['artifact_id']} lacks current {decision_type}.")
    return decision


def _project_source(source: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
    if source["source_category"] == "prohibited_material" or source["authority_tier"] == "excluded" or source["rights_reuse"] in {"prohibited", "unresolved", "analysis_only", "style_evidence_only"}:
        raise LearningError("PROHIBITED_SOURCE", "A selected source is prohibited or ineligible for learner projection.")
    result: dict[str, Any] = {
        "id": projection["pack_source_id"],
        "type": projection["pack_source_type"],
        "title": source["title"],
        "publisher": source["publisher"],
        "url": source["canonical_url"],
        "retrieved_on": source["retrieved_on"],
        "snapshot_retained": source["retained_snapshot"]["retained"],
        "rights_id": projection["rights_id"],
    }
    if source["source_revision"] is not None:
        result["revision"] = source["source_revision"]
    if source["published_or_updated_on"] is not None:
        result["effective_from"] = source["published_or_updated_on"]
    if source["retained_snapshot"]["retained"]:
        result["content_sha256"] = source["retained_snapshot"]["content_sha256"]
    return result


def compile_candidate(
    workspace: Path,
    selection: dict[str, Any],
    *,
    candidate_id: str,
    evidence_id: str,
) -> dict[str, Any]:
    selection = validate_selection(selection)
    project, _, _ = find_record(workspace, selection["project"])
    sources = _resolve_all(workspace, selection["source_references"])
    claims = _resolve_all(workspace, selection["claim_references"])
    lessons = _resolve_all(workspace, selection["lesson_references"])
    specifications = _resolve_all(workspace, selection["question_specification_references"])
    questions = _resolve_all(workspace, selection["question_references"])
    approvals = _resolve_all(workspace, selection["approval_references"])
    reviews = _resolve_all(workspace, selection["review_references"])
    reports = _resolve_all(workspace, selection["validation_report_references"])
    for record, _ in [*sources, *claims, *lessons, *specifications, *questions]:
        if record["status"] != "active":
            raise LearningError("STALE_DEPENDENCY", "Draft, stale, superseded, invalidated, or rejected content cannot compile.")
    required_decisions: list[dict[str, Any]] = []
    for source, _ in sources:
        required_decisions.append(_require_decision(workspace, source, "source_approval"))
    for claim, _ in claims:
        if claim["invalidation_state"]["status"] != "current":
            raise LearningError("STALE_DEPENDENCY", "A selected claim is not current.")
        required_decisions.append(_require_decision(workspace, claim, "claim_approval"))
    for lesson, _ in lessons:
        required_decisions.append(_require_decision(workspace, lesson, "lesson_content_review"))
    for spec, _ in specifications:
        required_decisions.append(_require_decision(workspace, spec, "question_spec_design_review"))
    for question, _ in questions:
        required_decisions.append(_require_decision(workspace, question, "question_originality_review"))
        required_decisions.append(_require_decision(workspace, question, "question_content_approval"))
        required_decisions.append(_require_decision(workspace, question, "answer_uniqueness_approval"))
    selected_decision_refs = {_ref_key(reference(item)) for item, _ in [*approvals, *reviews]}
    if any(_ref_key(reference(item)) not in selected_decision_refs for item in required_decisions):
        raise LearningError("APPROVAL_MISSING", "The selection omits a required current approval or review record.")
    selected_dependency_digests = {
        item["canonical_digest"] for item, _ in [*sources, *claims, *lessons, *specifications, *questions, *approvals, *reviews]
    }
    for decision in required_decisions:
        if not set(decision["dependency_digests"]) <= selected_dependency_digests:
            raise LearningError("STALE_DEPENDENCY", "A required decision dependency is absent or stale.")
    for report, _ in reports:
        if report["result"] != "passed" or report["workspace_commit"] != selection["source_workspace_commit"]:
            raise LearningError("VALIDATION_FAILED", "A selected validation report failed or targets another workspace commit.")
        checked = {_ref_key(item) for item in report["checked_artifacts"]}
        required_checked = {_ref_key(item) for item in [selection["project"], *selection["source_references"], *selection["claim_references"], *selection["lesson_references"], *selection["question_specification_references"], *selection["question_references"], *selection["approval_references"], *selection["review_references"]]}
        if not required_checked <= checked:
            raise LearningError("VALIDATION_FAILED", "A selected validation report does not cover every compiler input.")
    scope = project["pilot_scope"]
    mix = {
        "single_response": sum(question["question_type"] == "single_response" for question, _ in questions),
        "multiple_response": sum(question["question_type"] == "multiple_response" for question, _ in questions),
    }
    if len(lessons) != scope["lesson_count"] or len(questions) != scope["question_count"] or mix != scope["response_mix"]:
        raise LearningError("COUNT_MISMATCH", "Selected content does not match the project's declared counts and response mix.")

    source_by_ref = {_ref_key(projection["source_reference"]): projection for projection in selection["source_projections"]}
    pack_source_ids: dict[str, str] = {}
    pack_sources = []
    for source, _ in sources:
        projection = source_by_ref.get(_ref_key(reference(source)))
        if projection is None:
            raise LearningError("PROJECTION_VIOLATION", "Every selected source requires one explicit projection.")
        pack_source_ids[source["artifact_id"]] = projection["pack_source_id"]
        pack_sources.append(_project_source(source, projection))

    lesson_projection_by_ref = {_ref_key(item["lesson_reference"]): item for item in selection["lesson_projections"]}
    pack_lessons: list[dict[str, Any]] = []
    lesson_files: dict[str, bytes] = {}
    for lesson, markdown in lessons:
        projection = lesson_projection_by_ref.get(_ref_key(reference(lesson)))
        if projection is None or markdown is None:
            raise LearningError("PROJECTION_VIOLATION", "Every lesson requires a projection and Markdown.")
        path = projection["path"]
        citations = [{"source_id": pack_source_ids[item["source_id"]], "locator": item["locator"]} for item in lesson["learner_citations"]]
        pack_lessons.append({
            "id": lesson["artifact_id"], "title": projection["title"], "path": path,
            "objective_ids": lesson["objective_ids"], "rights_id": projection["rights_id"], "citations": citations,
        })
        lesson_files[path] = normalize_markdown(markdown).encode("utf-8")

    question_projection_by_ref = {_ref_key(item["question_reference"]): item for item in selection["question_projections"]}
    pack_questions = []
    for question, _ in questions:
        projection = question_projection_by_ref.get(_ref_key(reference(question)))
        if projection is None:
            raise LearningError("PROJECTION_VIOLATION", "Every question requires one explicit projection.")
        citations = [{"source_id": pack_source_ids[item["source_id"]], "locator": item["locator"]} for item in question["source_citation_projection"]]
        pack_questions.append({
            "id": question["artifact_id"], "type": question["question_type"], "origin": "generated",
            "objective_id": question["objective_references"]["primary"], "tags": projection["tags"],
            "prompt": question["stem"],
            "options": [{"id": item["option_id"], "text": item["text"]} for item in question["options"]],
            "correct_option_ids": question["keyed_option_ids"],
            "question_rights_id": projection["question_rights_id"],
            "explanation": question["learner_explanation"],
            "explanation_rights_id": projection["explanation_rights_id"],
            "explanation_citations": citations,
        })
    pack_config = selection["pack"]
    manifest: dict[str, Any] = {
        "format_version": "0.2", "pack_id": pack_config["pack_id"], "version": pack_config["version"],
        "title": pack_config["title"], "language": pack_config["language"], "tags": pack_config["tags"],
        "assessment_pool": pack_config["assessment_pool"], "rights": pack_config["rights"],
        "sources": pack_sources, "objectives": pack_config["objectives"], "lessons": pack_lessons,
        "questions": pack_questions,
        "approval": {
            "status": "pending", "reviewed_by": "Pending pack-release review",
            "reviewed_at": selection["compilation_timestamp"],
            "review_scope": ["lessons", "explanations", "citations", "rights_metadata"],
            "notes": "Candidate only; compilation grants no approval.",
        },
    }
    files: dict[str, bytes] = {"pack.json": canonical_json_file_bytes(manifest), **lesson_files}
    if pack_config["notice_markdown"] is not None:
        files["NOTICE.md"] = normalize_markdown(pack_config["notice_markdown"]).encode("utf-8")
    output_root = workspace / "release" / "candidates"
    output_path = output_root / f"{candidate_id}-pack"
    candidate_record_path = output_root / f"{candidate_id}.json"
    evidence_path = workspace / "release" / "evidence" / f"{evidence_id}.json"
    if output_path.exists() or candidate_record_path.exists() or evidence_path.exists():
        raise LearningError("OUTPUT_CONFLICT", "Candidate output or evidence already exists.")
    temporary = Path(tempfile.mkdtemp(prefix=f".{candidate_id}.", dir=output_root))
    try:
        for relative, content in files.items():
            path = temporary.joinpath(*relative.split("/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        pack = load_candidate_pack(temporary)
        pack_digest = digest_pack(pack)
        output_digest = digest_file_set(files)
        selection_digest = _selection_digest(selection)
        compiler_input_digest = artifact_digest({
            "schema_version": "ala.authoring.compiler-input.v1", "artifact_type": "compiler_input_manifest",
            "selection_digest": selection_digest, "compiler_version": AUTHORING_COMPILER_VERSION,
            "selected_digests": sorted(item[0]["canonical_digest"] for item in [*sources, *claims, *lessons, *specifications, *questions, *approvals, *reviews, *reports]),
        })
        candidate = seal_record({
            "schema_version": "ala.authoring.release-candidate.v1", "artifact_id": candidate_id,
            "artifact_type": "release_candidate", "revision": 1, "status": "immutable",
            "created_at": selection["compilation_timestamp"], "modified_at": selection["compilation_timestamp"],
            "author": {"identity": "ala-authoring-compiler", "identity_type": "service", "role": "deterministic_compiler"},
            "supersedes": None, "candidate_id": candidate_id, "compiler_version": AUTHORING_COMPILER_VERSION,
            "project": reference(project), "selection_digest": selection_digest,
            "source_workspace_commit": selection["source_workspace_commit"],
            "compiled_pack": {"pack_id": pack.pack_id, "version": pack.version, "target_format": "0.2", "relative_output_path": f"release/candidates/{candidate_id}-pack", "digest": pack_digest},
            "compiler_input_digest": compiler_input_digest, "compiler_output_digest": output_digest,
            "compilation_timestamp": selection["compilation_timestamp"], "canonical_digest": "0" * 64,
        })
        evidence = seal_record({
            "schema_version": "ala.release-evidence/1", "artifact_id": evidence_id,
            "artifact_type": "release_evidence", "revision": 1, "status": "immutable",
            "created_at": selection["compilation_timestamp"], "modified_at": selection["compilation_timestamp"],
            "author": {"identity": "ala-authoring-compiler", "identity_type": "service", "role": "release_evidence_generator"},
            "supersedes": None, "phase": "candidate", "project": reference(project),
            "compiler_version": AUTHORING_COMPILER_VERSION, "source_workspace_commit": selection["source_workspace_commit"],
            "assessment_blueprint": selection["assessment_blueprint"], "learning_architecture": selection["learning_architecture"],
            "realization_plan": selection["realization_plan"],
            "source_records": _sorted_refs(selection["source_references"]), "approved_claims": _sorted_refs(selection["claim_references"]),
            "lessons": _sorted_refs(selection["lesson_references"]), "question_specifications": _sorted_refs(selection["question_specification_references"]),
            "approved_final_questions": _sorted_refs(selection["question_references"]),
            "approval_records": _sorted_refs([*selection["approval_references"], *selection["review_references"]]),
            "validation_reports": _sorted_refs(selection["validation_report_references"]), "compiled_pack": candidate["compiled_pack"],
            "compilation_timestamp": selection["compilation_timestamp"], "compiler_input_digest": compiler_input_digest,
            "compiler_output_digest": output_digest, "candidate_manifest": None, "release_review_approval": None,
            "exclusions": EXCLUSIONS, "canonical_digest": "0" * 64,
        })
        validate_release_evidence(evidence)
        with workspace_lock(workspace):
            os.replace(temporary, output_path)
            atomic_write(candidate_record_path, canonical_json_file_bytes(candidate), expected_absent=True)
            atomic_write(evidence_path, canonical_json_file_bytes(evidence), expected_absent=True)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return {
        "compiler_version": AUTHORING_COMPILER_VERSION, "project_id": project["project_id"],
        "source_workspace_commit": selection["source_workspace_commit"], "target_format": "0.2",
        "candidate_path": f"release/candidates/{candidate_id}-pack", "candidate_pack_digest": pack_digest,
        "candidate": candidate, "release_evidence": evidence, "human_approval_granted": False,
    }


def finalize_release_evidence(
    workspace: Path,
    *,
    candidate_evidence: dict[str, Any],
    release_approval: dict[str, Any],
    final_evidence_id: str,
    finalized_at: str,
) -> dict[str, Any]:
    if candidate_evidence["phase"] != "candidate" or release_approval["approval_type"] != "pack_release_approval" or release_approval["decision"] != "approved":
        raise LearningError("APPROVAL_MISSING", "Final evidence requires approved pack-release review of candidate evidence.")
    candidate_record, _, _ = find_record(workspace, release_approval["target"])
    if candidate_record["artifact_type"] != "release_candidate" or candidate_evidence["compiled_pack"] != candidate_record["compiled_pack"] or candidate_evidence["canonical_digest"] not in release_approval["dependency_digests"]:
        raise LearningError("RELEASE_EVIDENCE_MISMATCH", "The pack-release approval does not bind this candidate and evidence digest.")
    final = dict(candidate_evidence)
    final.update({
        "artifact_id": final_evidence_id, "revision": 1, "status": "immutable", "created_at": finalized_at,
        "modified_at": finalized_at, "supersedes": None, "phase": "final",
        "candidate_manifest": reference(candidate_evidence), "release_review_approval": reference(release_approval),
        "canonical_digest": "0" * 64,
    })
    final = seal_record(final)
    result = validate_release_evidence(final, candidate=candidate_evidence)
    if result["result"] != "passed":
        raise LearningError("RELEASE_EVIDENCE_MISMATCH", "Final release evidence does not match candidate evidence.")
    return store_immutable(workspace, final, path=workspace / "release" / "evidence" / f"{final_evidence_id}.json")
