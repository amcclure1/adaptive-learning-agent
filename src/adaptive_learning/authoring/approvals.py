"""Immutable human decisions, applicability, revocation, and impact analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError

from .schemas import APPROVAL_TYPES, REVIEW_TYPES, seal_record
from .workspace import all_stored_records, find_record, reference, store_immutable


TARGET_TYPES = {
    "source_approval": {"source"},
    "claim_approval": {"claim"},
    "question_content_approval": {"question"},
    "answer_uniqueness_approval": {"question"},
    "pack_release_approval": {"release_candidate"},
}


def create_decision(
    workspace: Path,
    *,
    decision_id: str,
    decision_type: str,
    target: dict[str, Any],
    dependency_digests: list[str],
    prerequisite_decisions: list[dict[str, Any]],
    decision: str,
    reviewer: dict[str, str],
    scope: list[str],
    findings: list[dict[str, str]],
    conditions: list[str],
    decided_at: str,
    record_kind: str = "decision",
    supersedes_decision_id: str | None = None,
    revokes_decision_id: str | None = None,
) -> dict[str, Any]:
    is_approval = decision_type in APPROVAL_TYPES
    if not is_approval and decision_type not in REVIEW_TYPES:
        raise LearningError("AUTHORING_APPROVAL_INVALID", "The decision type is unsupported.")
    target_record, _, _ = find_record(workspace, target)
    if is_approval and target_record["artifact_type"] not in TARGET_TYPES[decision_type]:
        raise LearningError("AUTHORING_APPROVAL_INVALID", "The approval type cannot target this artifact type.")
    if target_record["status"] in {"draft", "stale", "superseded", "invalidated", "rejected"}:
        raise LearningError("AUTHORING_APPROVAL_INVALID", "Approvals and reviews require a current immutable target.")
    if reviewer["identity"] == target_record["author"]["identity"]:
        raise LearningError("REVIEWER_CONFLICT", "An artifact author cannot approve or review the same artifact.")
    if decision_type == "answer_uniqueness_approval" and reviewer["identity"] == target_record["author"]["identity"]:
        raise LearningError("REVIEWER_CONFLICT", "A material question author cannot approve answer uniqueness.")
    for prerequisite in prerequisite_decisions:
        prior, _, _ = find_record(workspace, prerequisite)
        if prior["artifact_type"] not in {"approval", "review"}:
            raise LearningError("AUTHORING_APPROVAL_INVALID", "Prerequisite decisions must reference an approval or review.")
    artifact_type = "approval" if is_approval else "review"
    record: dict[str, Any] = {
        "schema_version": f"ala.authoring.{artifact_type}.v1",
        "artifact_id": decision_id,
        "artifact_type": artifact_type,
        "revision": 1,
        "status": "active",
        "created_at": decided_at,
        "modified_at": decided_at,
        "author": {"identity": reviewer["identity"], "identity_type": "human", "role": reviewer["role"]},
        "supersedes": None,
        f"{artifact_type}_id": decision_id,
        f"{artifact_type}_type": decision_type,
        "record_kind": record_kind,
        "target": target,
        "dependency_digests": sorted(set(dependency_digests)),
        "prerequisite_decisions": prerequisite_decisions,
        "decision": decision,
        "reviewer": reviewer,
        "scope": scope,
        "findings": findings,
        "conditions": conditions,
        "decided_at": decided_at,
        "supersedes_decision_id": supersedes_decision_id,
        "revokes_decision_id": revokes_decision_id,
        "canonical_digest": "0" * 64,
    }
    sealed = seal_record(record)
    return store_immutable(workspace, sealed)


def _decisions(workspace: Path) -> list[dict[str, Any]]:
    return [record for record, _, _ in all_stored_records(workspace) if record["artifact_type"] in {"approval", "review"}]


def current_decision(
    workspace: Path,
    *,
    target: dict[str, Any],
    decision_type: str,
    require_approved: bool = True,
) -> dict[str, Any] | None:
    type_field = "approval_type" if decision_type in APPROVAL_TYPES else "review_type"
    candidates = [
        item for item in _decisions(workspace)
        if item.get(type_field) == decision_type and item["record_kind"] == "decision" and item["target"] == target
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item["decided_at"], item["artifact_id"]))
    current = candidates[-1]
    later = _decisions(workspace)
    if any(
        item["record_kind"] in {"revocation", "supersession"}
        and (item.get("revokes_decision_id") == current["artifact_id"] or item.get("supersedes_decision_id") == current["artifact_id"])
        for item in later
    ):
        return None
    if require_approved and current["decision"] != "approved":
        return None
    return current


MATERIAL_FIELDS = {
    "source": {
        "title", "publisher", "canonical_url", "source_category", "authority_tier", "rights_reuse",
        "intended_uses", "retrieved_on", "published_or_updated_on", "source_revision",
        "retained_snapshot", "freshness_policy", "prohibited_disposition",
    },
    "claim": {
        "statement", "category", "source_references", "applicability", "scope", "region_sensitivity",
        "account_configuration_sensitivity", "time_sensitivity", "freshness_horizon", "derived_from",
        "decision_criterion",
    },
    "lesson": {"objective_ids", "prerequisite_bridge_ids", "claim_references", "markdown_path", "markdown_sha256", "learner_citations", "intended_depth"},
    "question": {
        "specification_reference", "question_type", "required_selection_count", "stem", "options",
        "keyed_option_ids", "learner_explanation", "option_rationales", "requirement_option_matrix",
        "supporting_claim_references", "objective_references", "blueprint_references",
        "source_citation_projection",
    },
    "release_candidate": {"compiler_version", "project", "selection_digest", "source_workspace_commit", "compiled_pack", "compiler_input_digest", "compiler_output_digest"},
}
INVALIDATED_TYPES = {
    "source": ["source_approval", "claim_approval", "question_content_approval", "answer_uniqueness_approval", "pack_release_approval"],
    "claim": ["claim_approval", "question_content_approval", "answer_uniqueness_approval", "pack_release_approval"],
    "lesson": ["lesson_content_review", "pack_release_approval"],
    "question": ["question_content_approval", "answer_uniqueness_approval", "pack_release_approval"],
    "release_candidate": ["pack_release_approval"],
}


def impact_analysis(workspace: Path, old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    if old["artifact_id"] != new["artifact_id"] or old["artifact_type"] != new["artifact_type"]:
        raise LearningError("AUTHORING_IMPACT_INVALID", "Impact analysis requires the same stable artifact identity.")
    artifact_type = old["artifact_type"]
    changed = sorted(field for field in MATERIAL_FIELDS.get(artifact_type, set()) if old.get(field) != new.get(field))
    old_digest = old["canonical_digest"]
    directly_applicable = [item for item in _decisions(workspace) if item["target"] == reference(old)]
    dependent = [item for item in _decisions(workspace) if old_digest in item["dependency_digests"]]
    affected = sorted({item["artifact_id"] for item in directly_applicable + dependent})
    return {
        "artifact_id": old["artifact_id"],
        "artifact_type": artifact_type,
        "old_digest": old_digest,
        "new_digest": new["canonical_digest"],
        "material_fields_changed": changed,
        "invalidated_decision_types": INVALIDATED_TYPES.get(artifact_type, []) if changed or old_digest != new["canonical_digest"] else [],
        "affected_historical_decision_ids": affected,
        "historical_records_preserved": True,
    }
