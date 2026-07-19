"""Bounded JSON-compatible authoring operations, separate from learner tools."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack

from .approvals import create_decision, impact_analysis
from .canonical import artifact_digest, canonical_json_file_bytes
from .compiler import compile_candidate, finalize_release_evidence, load_candidate_pack, validate_selection
from .schemas import ID_RE, validate_record
from .validation import validate_release_evidence, validate_workspace
from .verification import (
    add_finding,
    compare_runs,
    create_resolution,
    create_verification_run,
    experiment_metrics,
    finalize_verification_run,
    register_consulted_source,
    verification_eligibility,
)
from .workspace import (
    atomic_write,
    draft_path,
    find_record,
    freeze_revision,
    initialize_workspace,
    project_path,
    read_json,
    read_record,
    write_draft,
)


class AuthoringOperations:
    """Confined authoring facade with no shell, network, install, or publication surface."""

    def __init__(self, authoring_root: str | Path) -> None:
        self.authoring_root = Path(authoring_root).resolve()

    def _workspace(self, project_id: str) -> Path:
        workspace = project_path(self.authoring_root, project_id)
        if not workspace.is_dir():
            raise LearningError("WORKSPACE_NOT_FOUND", "The authoring project does not exist.")
        return workspace

    def initialize_project(self, request: dict[str, Any]) -> dict[str, Any]:
        required = {"project_id", "title", "created_at", "workspace_commit", "pilot_scope", "author"}
        self._closed(request, required)
        return initialize_workspace(self.authoring_root, **request)

    def validate_project(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "as_of", "workspace_commit", "validation_id", "executed_at", "persist"})
        return validate_workspace(self._workspace(request["project_id"]), **{key: value for key, value in request.items() if key != "project_id"})

    def add_or_update_draft(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "record", "expected_prior_digest", "markdown"})
        record = write_draft(
            self._workspace(request["project_id"]), request["record"],
            expected_prior_digest=request["expected_prior_digest"], markdown=request["markdown"],
        )
        return {"artifact": record, "changed": True, "approval_granted": False}

    def freeze_draft(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "artifact_type", "artifact_id", "expected_draft_digest", "modified_at"})
        record = freeze_revision(self._workspace(request["project_id"]), request["artifact_type"], request["artifact_id"], expected_draft_digest=request["expected_draft_digest"], modified_at=request["modified_at"])
        return {"artifact": record, "immutable": True, "approval_granted": False}

    def calculate_artifact_digest(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"record", "markdown"})
        return {"canonical_digest": artifact_digest(request["record"], markdown_path=request["record"].get("markdown_path"), markdown=request["markdown"])}

    def create_decision(self, request: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "project_id", "decision_id", "decision_type", "target", "dependency_digests",
            "prerequisite_decisions", "decision", "reviewer", "scope", "findings", "conditions",
            "decided_at", "record_kind", "supersedes_decision_id", "revokes_decision_id",
        }
        self._closed(request, allowed)
        payload = dict(request)
        workspace = self._workspace(payload.pop("project_id"))
        return {"decision": create_decision(workspace, **payload), "human_action_recorded": True}

    def analyze_impact(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "old", "new"})
        return impact_analysis(self._workspace(request["project_id"]), request["old"], request["new"])

    def create_verification_run(self, request: dict[str, Any]) -> dict[str, Any]:
        fields = {"project_id", "verification_id", "target_workspace_commit", "verifier", "model", "research_date", "target_artifacts", "architecture_references", "verification_scope", "deterministic_validation_report", "created_at"}
        self._closed(request, fields)
        payload = dict(request)
        workspace = self._workspace(payload.pop("project_id"))
        return {"verification_run": create_verification_run(workspace, **payload), "approval_granted": False}

    def register_verification_source(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "verification_id", "expected_run_digest", "source", "modified_at"})
        payload = dict(request)
        workspace = self._workspace(payload.pop("project_id"))
        return {"verification_run": register_consulted_source(workspace, **payload), "network_accessed": False}

    def add_verification_finding(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "verification_id", "finding"})
        return {"finding": add_finding(self._workspace(request["project_id"]), verification_id=request["verification_id"], finding=request["finding"]), "approval_granted": False}

    def finalize_verification_run(self, request: dict[str, Any]) -> dict[str, Any]:
        fields = {"project_id", "verification_id", "expected_run_digest", "finding_references", "artifact_dispositions", "unresolved_questions", "completed_at"}
        self._closed(request, fields)
        payload = dict(request)
        workspace = self._workspace(payload.pop("project_id"))
        return {"verification_run": finalize_verification_run(workspace, **payload), "approval_granted": False}

    def verification_eligibility(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "target", "require_approved_premises"})
        return verification_eligibility(self._workspace(request["project_id"]), target=request["target"], require_approved_premises=request["require_approved_premises"])

    def create_finding_resolution(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "record"})
        return {"resolution": create_resolution(self._workspace(request["project_id"]), request["record"]), "finding_closed": False, "approval_granted": False}

    def compare_verification_runs(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "earlier_run", "later_run"})
        return compare_runs(self._workspace(request["project_id"]), earlier_run=request["earlier_run"], later_run=request["later_run"])

    def generate_experiment_metrics(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "run_references"})
        return experiment_metrics(self._workspace(request["project_id"]), run_references=request["run_references"])

    def store_selection(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "selection"})
        selection = validate_selection(request["selection"])
        selection_id = selection["selection_id"]
        if not isinstance(selection_id, str) or not ID_RE.fullmatch(selection_id):
            raise LearningError("AUTHORING_ID_INVALID", "selection_id is invalid.")
        path = self._workspace(request["project_id"]) / "release" / "selections" / f"{selection_id}.json"
        atomic_write(path, canonical_json_file_bytes(selection), expected_absent=True)
        return {"selection_id": selection_id, "path": f"release/selections/{selection_id}.json"}

    def validate_release_candidate(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "candidate_id"})
        workspace = self._workspace(request["project_id"])
        candidate_record, _, _ = read_record(workspace / "release" / "candidates" / f"{request['candidate_id']}.json")
        pack = load_candidate_pack(workspace / candidate_record["compiled_pack"]["relative_output_path"])
        digest = digest_pack(pack)
        if digest != candidate_record["compiled_pack"]["digest"]:
            raise LearningError("RELEASE_EVIDENCE_MISMATCH", "Candidate pack digest does not match its record.")
        return {"result": "passed", "candidate_pack_digest": digest, "human_approval_implication": "none"}

    def compile_approved_project(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "selection_id", "candidate_id", "evidence_id"})
        workspace = self._workspace(request["project_id"])
        selection_id = request["selection_id"]
        if not isinstance(selection_id, str) or not ID_RE.fullmatch(selection_id):
            raise LearningError("AUTHORING_ID_INVALID", "selection_id is invalid.")
        selection = read_json(workspace / "release" / "selections" / f"{selection_id}.json")
        return compile_candidate(workspace, selection, candidate_id=request["candidate_id"], evidence_id=request["evidence_id"])

    def generate_release_evidence(self, request: dict[str, Any]) -> dict[str, Any]:
        self._closed(request, {"project_id", "candidate_evidence", "release_approval", "final_evidence_id", "finalized_at"})
        result = finalize_release_evidence(
            self._workspace(request["project_id"]), candidate_evidence=request["candidate_evidence"],
            release_approval=request["release_approval"], final_evidence_id=request["final_evidence_id"],
            finalized_at=request["finalized_at"],
        )
        return {"release_evidence": result, "installed": False, "published": False}

    @staticmethod
    def _closed(request: dict[str, Any], fields: set[str]) -> None:
        if not isinstance(request, dict) or set(request) != fields:
            unknown = sorted(set(request) - fields) if isinstance(request, dict) else []
            missing = sorted(fields - set(request)) if isinstance(request, dict) else sorted(fields)
            raise LearningError("AUTHORING_REQUEST_INVALID", f"The request must be closed; unknown={unknown}, missing={missing}.")
