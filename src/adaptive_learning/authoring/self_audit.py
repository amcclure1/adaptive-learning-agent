"""Immutable first-pass author self-audit records and exact-digest eligibility."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError

from .schemas import seal_record
from .workspace import all_stored_records, find_record, reference, store_immutable


PROTOCOL_VERSION = "ala-author-first-pass-quality-1"


def create_author_self_audit(workspace: Path, record: dict[str, Any]) -> dict[str, Any]:
    project = next((item for item, _, _ in all_stored_records(workspace) if item["artifact_type"] == "project"), None)
    if project is None or record.get("target_project_id") != project["project_id"]:
        raise LearningError("AUTHOR_SELF_AUDIT_INVALID", "The self-audit must identify its workspace project.")
    if record.get("protocol_version") != PROTOCOL_VERSION:
        raise LearningError("AUTHOR_SELF_AUDIT_INVALID", "The self-audit protocol version is unsupported.")
    author = record.get("author", {})
    for target in record.get("target_artifacts", []):
        artifact, _, _ = find_record(workspace, target)
        if artifact["artifact_type"] not in {"source", "claim", "lesson", "question_spec", "question"}:
            raise LearningError("AUTHOR_SELF_AUDIT_INVALID", "Only authored-content artifacts may be self-audited.")
        if artifact["author"]["identity"] != author.get("identity"):
            raise LearningError("AUTHOR_SELF_AUDIT_CONFLICT", "The recorded author must be the author of every target.")
    sealed = seal_record(record)
    return store_immutable(workspace, sealed, path=workspace / "self-audits" / "records" / f"{sealed['audit_id']}.json")


def author_self_audit_eligibility(workspace: Path, *, target: dict[str, Any], target_workspace_commit: str) -> dict[str, Any]:
    find_record(workspace, target)
    audits = [
        item for item, _, _ in all_stored_records(workspace)
        if item["artifact_type"] == "author_self_audit" and target in item["target_artifacts"]
    ]
    audits.sort(key=lambda item: (item["modified_at"], item["artifact_id"]))
    completed = [item for item in audits if item["completion_status"] == "completed" and item["target_workspace_commit"] == target_workspace_commit]
    selected = completed[-1] if completed else None
    reasons = []
    if selected is None:
        if audits and any(item["completion_status"] == "completed" for item in audits):
            reasons.append("author_self_audit_workspace_commit_stale")
        else:
            reasons.append("author_self_audit_missing" if not audits else "author_self_audit_incomplete")
    return {
        "target": target,
        "eligible": not reasons,
        "author_self_audit": reference(selected) if selected else None,
        "reasons": reasons,
        "human_approval_granted": False,
    }
