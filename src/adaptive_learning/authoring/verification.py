"""Deterministic records and fail-closed gates for independent AI verification.

Research happens outside this module. The bounded operations only accept, validate,
persist, compare, and evaluate source-grounded evidence.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError

from .canonical import canonical_json_file_bytes
from .schemas import ID_RE, VERIFICATION_DISPOSITIONS, VERIFICATION_SEVERITIES, seal_record
from .workspace import all_stored_records, atomic_write, find_record, read_record, reference, store_immutable
from .self_audit import author_self_audit_eligibility


PROTOCOL_VERSION = "ala-independent-ai-verification-1"
BLOCKING_DISPOSITIONS = {"revision_required", "blocked", "unable_to_verify"}


def _reference_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return item.get("artifact_id"), item.get("artifact_type"), item.get("revision"), item.get("canonical_digest")


def _run_path(workspace: Path, verification_id: str) -> Path:
    if not isinstance(verification_id, str) or not ID_RE.fullmatch(verification_id):
        raise LearningError("AUTHORING_ID_INVALID", "verification_id is invalid.")
    return workspace / "verifications" / "runs" / f"{verification_id}.json"


def _load_run(workspace: Path, verification_id: str) -> dict[str, Any]:
    record, _ = read_record(_run_path(workspace, verification_id))
    if record["artifact_type"] != "ai_verification_run":
        raise LearningError("VERIFICATION_RUN_INVALID", "The record is not an AI verification run.")
    return record


def _all(workspace: Path, artifact_type: str) -> list[dict[str, Any]]:
    return [record for record, _, _ in all_stored_records(workspace) if record["artifact_type"] == artifact_type]


def create_verification_run(
    workspace: Path,
    *,
    verification_id: str,
    target_workspace_commit: str,
    verifier: dict[str, Any],
    model: dict[str, Any],
    research_date: str,
    target_artifacts: list[dict[str, Any]],
    architecture_references: list[dict[str, Any]],
    verification_scope: list[str],
    deterministic_validation_report: dict[str, Any],
    created_at: str,
) -> dict[str, Any]:
    project = next((item for item in _all(workspace, "project")), None)
    if project is None:
        raise LearningError("VERIFICATION_RUN_INVALID", "The workspace project record is missing.")
    validation, _, _ = find_record(workspace, deterministic_validation_report)
    if validation["artifact_type"] != "validation_report" or validation["result"] != "passed":
        raise LearningError("DETERMINISTIC_VALIDATION_REQUIRED", "A passing deterministic validation report is required before AI verification.")
    checked = {_reference_key(item) for item in validation["checked_artifacts"]}
    for target in target_artifacts:
        target_record, _, _ = find_record(workspace, target)
        if target_record["artifact_type"] in {"source", "claim", "lesson", "question_spec", "question"}:
            audit = author_self_audit_eligibility(workspace, target=target, target_workspace_commit=target_workspace_commit)
            if not audit["eligible"]:
                raise LearningError("AUTHOR_SELF_AUDIT_REQUIRED", "A completed exact-digest author self-audit is required before independent verification.", details=audit)
        if _reference_key(target) not in checked:
            raise LearningError("DETERMINISTIC_VALIDATION_STALE", "The validation report does not cover an exact verification target.")
        if target_record["author"]["identity"] == verifier.get("identity"):
            raise LearningError("VERIFIER_CONFLICT", "The artifact author cannot independently verify the same artifact.")
    empty_dispositions = {item: 0 for item in VERIFICATION_DISPOSITIONS}
    empty_severities = {item: 0 for item in VERIFICATION_SEVERITIES}
    record = seal_record({
        "schema_version": "ala.authoring.ai-verification-run.v1",
        "artifact_id": verification_id,
        "artifact_type": "ai_verification_run",
        "revision": 1,
        "status": "draft",
        "created_at": created_at,
        "modified_at": created_at,
        "author": {"identity": verifier["identity"], "identity_type": verifier["identity_type"], "role": "independent_ai_verifier"},
        "supersedes": None,
        "verification_id": verification_id,
        "protocol_version": PROTOCOL_VERSION,
        "target_project_id": project["project_id"],
        "target_workspace_commit": target_workspace_commit,
        "verifier": verifier,
        "model": model,
        "research_date": research_date,
        "target_artifacts": target_artifacts,
        "architecture_references": architecture_references,
        "verification_scope": sorted(set(verification_scope)),
        "deterministic_validation_report": deterministic_validation_report,
        "independently_accessed_sources": [],
        "finding_references": [],
        "artifact_dispositions": [],
        "summary_counts": {"total_artifacts": len(target_artifacts), "total_findings": 0, "blocking_findings": 0, "by_disposition": empty_dispositions, "by_severity": empty_severities},
        "unresolved_questions": [],
        "completion_status": "in_progress",
        "human_approval_implication": "none",
        "canonical_digest": "0" * 64,
    })
    atomic_write(_run_path(workspace, verification_id), canonical_json_file_bytes(record), expected_absent=True)
    return record


def register_consulted_source(workspace: Path, *, verification_id: str, expected_run_digest: str, source: dict[str, Any], modified_at: str) -> dict[str, Any]:
    run = _load_run(workspace, verification_id)
    if run["completion_status"] != "in_progress" or run["canonical_digest"] != expected_run_digest:
        raise LearningError("WORKSPACE_CONFLICT", "The verification run is finalized or its expected digest is stale.")
    if any(item["source_id"] == source.get("source_id") for item in run["independently_accessed_sources"]):
        raise LearningError("VERIFICATION_SOURCE_DUPLICATE", "The consulted source is already registered.")
    changed = dict(run)
    changed["modified_at"] = modified_at
    changed["independently_accessed_sources"] = [*run["independently_accessed_sources"], source]
    sealed = seal_record(changed)
    atomic_write(_run_path(workspace, verification_id), canonical_json_file_bytes(sealed))
    return sealed


def add_finding(workspace: Path, *, verification_id: str, finding: dict[str, Any]) -> dict[str, Any]:
    run = _load_run(workspace, verification_id)
    if run["completion_status"] != "in_progress":
        raise LearningError("VERIFICATION_RUN_FINAL", "A finalized verification run cannot accept findings.")
    if finding.get("verification_id") != verification_id or finding.get("target") not in run["target_artifacts"]:
        raise LearningError("VERIFICATION_FINDING_INVALID", "The finding must target an exact artifact in its verification run.")
    record = seal_record(finding)
    path = workspace / "verifications" / "findings" / f"{record['finding_id']}.json"
    return store_immutable(workspace, record, path=path)


def finalize_verification_run(
    workspace: Path,
    *,
    verification_id: str,
    expected_run_digest: str,
    finding_references: list[dict[str, Any]],
    artifact_dispositions: list[dict[str, Any]],
    unresolved_questions: list[str],
    completed_at: str,
) -> dict[str, Any]:
    run = _load_run(workspace, verification_id)
    if run["completion_status"] != "in_progress" or run["canonical_digest"] != expected_run_digest:
        raise LearningError("WORKSPACE_CONFLICT", "The verification run is finalized or its expected digest is stale.")
    if {_reference_key(item) for item in run["target_artifacts"]} != {_reference_key(item["target"]) for item in artifact_dispositions}:
        raise LearningError("VERIFICATION_INCOMPLETE", "Every target requires exactly one artifact disposition.")
    if len(artifact_dispositions) != len(run["target_artifacts"]):
        raise LearningError("VERIFICATION_INCOMPLETE", "Duplicate artifact dispositions are forbidden.")
    findings: list[dict[str, Any]] = []
    for item in finding_references:
        finding, _, _ = find_record(workspace, item)
        if finding["artifact_type"] != "verification_finding" or finding["verification_id"] != verification_id:
            raise LearningError("VERIFICATION_FINDING_INVALID", "A referenced finding belongs to another run.")
        findings.append(finding)
    finding_ids = {item["finding_id"] for item in findings}
    for disposition in artifact_dispositions:
        if not set(disposition["finding_ids"]) <= finding_ids:
            raise LearningError("VERIFICATION_FINDING_INVALID", "A disposition references an unknown finding.")
        target_findings = {item["finding_id"] for item in findings if item["target"] == disposition["target"]}
        if set(disposition["finding_ids"]) != target_findings:
            raise LearningError("VERIFICATION_FINDING_INVALID", "A disposition must enumerate every finding for its target.")
        if disposition["disposition"] in {"verified", "verified_with_nonblocking_note"} and any(item["blocking"] for item in findings if item["target"] == disposition["target"]):
            raise LearningError("VERIFICATION_BLOCKING_FINDING", "A verified disposition cannot retain a blocking finding.")
    dispositions = Counter(item["disposition"] for item in artifact_dispositions)
    severities = Counter(item["severity"] for item in findings)
    changed = dict(run)
    changed.update({
        "status": "immutable",
        "modified_at": completed_at,
        "finding_references": finding_references,
        "artifact_dispositions": artifact_dispositions,
        "summary_counts": {
            "total_artifacts": len(run["target_artifacts"]),
            "total_findings": len(findings),
            "blocking_findings": sum(item["blocking"] for item in findings),
            "by_disposition": {item: dispositions[item] for item in VERIFICATION_DISPOSITIONS},
            "by_severity": {item: severities[item] for item in VERIFICATION_SEVERITIES},
        },
        "unresolved_questions": unresolved_questions,
        "completion_status": "completed",
    })
    sealed = seal_record(changed)
    atomic_write(_run_path(workspace, verification_id), canonical_json_file_bytes(sealed))
    return sealed


def verification_eligibility(workspace: Path, *, target: dict[str, Any], require_approved_premises: bool = False) -> dict[str, Any]:
    target_record, _, _ = find_record(workspace, target)
    runs = [item for item in _all(workspace, "ai_verification_run") if item["completion_status"] == "completed" and target in item["target_artifacts"]]
    runs.sort(key=lambda item: (item["modified_at"], item["artifact_id"]))
    reasons: list[str] = []
    selected = runs[-1] if runs else None
    disposition = None
    if selected is None:
        reasons.append("verification_missing")
    else:
        disposition = next(item for item in selected["artifact_dispositions"] if item["target"] == target)
        if disposition["disposition"] in BLOCKING_DISPOSITIONS:
            reasons.append(f"disposition_{disposition['disposition']}")
        findings = {item["artifact_id"]: item for item in _all(workspace, "verification_finding")}
        for finding_id in disposition["finding_ids"]:
            finding = findings.get(finding_id)
            if finding is None or finding["blocking"] or finding["finding_status"] in {"open", "disputed"} and finding["severity"] in {"critical", "high", "medium"}:
                reasons.append(f"blocking_finding_{finding_id}")
    if require_approved_premises and target_record["artifact_type"] == "claim" and target_record.get("category") == "derived_recommendation":
        from .approvals import current_decision
        for premise in target_record["derived_from"]:
            premise_result = verification_eligibility(workspace, target=premise)
            if not premise_result["eligible"]:
                reasons.append(f"premise_unverified_{premise['artifact_id']}")
            if current_decision(workspace, target=premise, decision_type="claim_approval") is None:
                reasons.append(f"premise_unapproved_{premise['artifact_id']}")
    return {
        "target": target,
        "eligible": not reasons,
        "verification_run": reference(selected) if selected else None,
        "disposition": disposition["disposition"] if disposition else None,
        "reasons": sorted(set(reasons)),
        "human_approval_granted": False,
    }


def assert_human_review_eligible(workspace: Path, *, target: dict[str, Any], decision_type: str, reviewer_identity: str) -> None:
    result = verification_eligibility(workspace, target=target, require_approved_premises=decision_type == "claim_approval")
    if not result["eligible"]:
        raise LearningError("AI_VERIFICATION_REQUIRED", "Current independent AI verification is required before human approval.", details=result)
    run, _, _ = find_record(workspace, result["verification_run"])
    if run["verifier"]["identity"] == reviewer_identity:
        raise LearningError("REVIEWER_CONFLICT", "The AI verifier cannot be listed as the human approver.")


def create_resolution(workspace: Path, record: dict[str, Any]) -> dict[str, Any]:
    finding, _, _ = find_record(workspace, record["finding"])
    if finding["artifact_type"] != "verification_finding":
        raise LearningError("FINDING_RESOLUTION_INVALID", "The resolution must reference a verification finding.")
    find_record(workspace, record["old_artifact"])
    find_record(workspace, record["new_artifact"])
    sealed = seal_record(record)
    path = workspace / "verifications" / "resolutions" / f"{sealed['resolution_id']}.json"
    return store_immutable(workspace, sealed, path=path)


def compare_runs(workspace: Path, *, earlier_run: dict[str, Any], later_run: dict[str, Any]) -> dict[str, Any]:
    earlier, _, _ = find_record(workspace, earlier_run)
    later, _, _ = find_record(workspace, later_run)
    if earlier["artifact_type"] != "ai_verification_run" or later["artifact_type"] != "ai_verification_run":
        raise LearningError("VERIFICATION_COMPARISON_INVALID", "Comparison requires two verification runs.")
    return {
        "earlier_run": earlier_run,
        "later_run": later_run,
        "finding_delta": later["summary_counts"]["total_findings"] - earlier["summary_counts"]["total_findings"],
        "blocking_delta": later["summary_counts"]["blocking_findings"] - earlier["summary_counts"]["blocking_findings"],
        "severity_delta": {item: later["summary_counts"]["by_severity"][item] - earlier["summary_counts"]["by_severity"][item] for item in VERIFICATION_SEVERITIES},
        "disposition_delta": {item: later["summary_counts"]["by_disposition"][item] - earlier["summary_counts"]["by_disposition"][item] for item in VERIFICATION_DISPOSITIONS},
        "human_approval_implication": "none",
    }


def experiment_metrics(workspace: Path, *, run_references: list[dict[str, Any]]) -> dict[str, Any]:
    runs = []
    for item in run_references:
        run, _, _ = find_record(workspace, item)
        if run["artifact_type"] != "ai_verification_run" or run["completion_status"] != "completed":
            raise LearningError("VERIFICATION_METRICS_INVALID", "Metrics require completed verification runs.")
        runs.append(run)
    findings_by_id = {item["artifact_id"]: item for item in _all(workspace, "verification_finding")}
    selected_findings = [findings_by_id[ref["artifact_id"]] for run in runs for ref in run["finding_references"]]
    selected_ids = {item["artifact_id"] for item in selected_findings}
    resolutions = [item for item in _all(workspace, "finding_resolution") if item["finding"]["artifact_id"] in selected_ids]

    def semantic_key(item: dict[str, Any]) -> tuple[Any, ...]:
        source = item["supporting_source"]
        dependencies = tuple(sorted((dep["artifact_type"], dep["artifact_id"]) for dep in item["affected_dependencies"]))
        return (
            item["target"]["artifact_type"], item["target"]["artifact_id"], item["disputed_field"],
            item["disputed_language"], item["category"], item["severity"], source["canonical_url"],
            source["locator"], item["explanation"], item["required_action"], item["suggested_revision"],
            dependencies, item["confidence"], item["blocking"],
        )

    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for finding in selected_findings:
        groups.setdefault(semantic_key(finding), []).append(finding)
    logical = [items[0] for items in groups.values()]
    exact_duplicate_count = sum(
        len(items) - len({(item["target"]["revision"], item["target"]["canonical_digest"]) for item in items})
        for items in groups.values()
    )
    repeated_changed_target_count = sum(
        max(0, len({(item["target"]["revision"], item["target"]["canonical_digest"]) for item in items}) - 1)
        for items in groups.values()
    )
    def counts(items: list[dict[str, Any]], field: str, vocabulary: set[str] | None = None) -> dict[str, int]:
        counter = Counter(item[field] if field != "artifact_type" else item["target"]["artifact_type"] for item in items)
        keys = sorted(vocabulary or set(counter))
        return {key: counter[key] for key in keys}
    latest = runs[-1] if runs else None
    return {
        "run_count": len(runs),
        "target_artifact_count": sum(item["summary_counts"]["total_artifacts"] for item in runs),
        "stored_finding_record_count": len(selected_findings),
        "logical_finding_count": len(logical),
        "exact_duplicate_record_count": exact_duplicate_count,
        "repeated_on_changed_target_count": repeated_changed_target_count,
        "superseding_finding_record_count": sum(item["supersedes"] is not None for item in selected_findings),
        "resolution_record_count": len(resolutions),
        "stored_by_severity": counts(selected_findings, "severity", VERIFICATION_SEVERITIES),
        "logical_by_severity": counts(logical, "severity", VERIFICATION_SEVERITIES),
        "stored_by_category": counts(selected_findings, "category"),
        "logical_by_category": counts(logical, "category"),
        "stored_by_artifact_type": counts(selected_findings, "artifact_type"),
        "logical_by_artifact_type": counts(logical, "artifact_type"),
        "response_by_disposition": dict(sorted(Counter(item["response_disposition"] for item in resolutions).items())),
        "residual_finding_record_count": latest["summary_counts"]["total_findings"] if latest else 0,
        "per_run": [{"verification_id": item["verification_id"], "stored_finding_record_count": item["summary_counts"]["total_findings"], "blocking_finding_record_count": item["summary_counts"]["blocking_findings"]} for item in runs],
        "research_capabilities": sorted({"public_web" if item["independently_accessed_sources"] else "none" for item in runs}),
        "human_approval_implication": "none",
    }
