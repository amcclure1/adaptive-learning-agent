from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from adaptive_learning.authoring.operations import AuthoringOperations
from adaptive_learning.authoring.schemas import seal_record, validate_record
from adaptive_learning.authoring.workspace import draft_path, read_record, reference
from adaptive_learning.errors import LearningError
from adaptive_learning.schema import SCHEMA_VERSION
from adaptive_learning.tool_contract import ToolContract

from authoring_helpers import COMMIT, REVIEW_TIMESTAMP, TIMESTAMP, author, project_request, reviewer, source_record


class IndependentVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.ops = AuthoringOperations(self.root / "authoring")
        self.project_id = "verification-test"
        self.project = self.ops.initialize_project(project_request(self.project_id))["project"]
        draft = self.ops.add_or_update_draft({"project_id": self.project_id, "record": source_record("src-verify"), "expected_prior_digest": None, "markdown": None})["artifact"]
        self.source = self.ops.freeze_draft({"project_id": self.project_id, "artifact_type": "source", "artifact_id": "src-verify", "expected_draft_digest": draft["canonical_digest"], "modified_at": REVIEW_TIMESTAMP})["artifact"]

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _report(self, suffix: str = "one") -> dict:
        return self.ops.validate_project({"project_id": self.project_id, "as_of": "2030-01-02", "workspace_commit": COMMIT, "validation_id": f"val-{suffix}", "executed_at": REVIEW_TIMESTAMP, "persist": True})

    def _architectures(self) -> list[dict]:
        return [{"artifact_id": name, **self.project["pilot_scope"][name]} for name in ("assessment_blueprint", "learning_architecture", "realization_plan")]

    def _start(self, run_id: str, target: dict | None = None, report: dict | None = None, verifier_id: str = "independent-verifier") -> dict:
        target = target or self.source
        report = report or self._report(run_id)
        return self.ops.create_verification_run({
            "project_id": self.project_id, "verification_id": run_id, "target_workspace_commit": COMMIT,
            "verifier": {"identity": verifier_id, "identity_type": "model", "role": "independent_ai_verifier", "invocation_id": f"inv-{run_id}"},
            "model": {"provider": "test-provider", "model_id": "test-model", "configuration": {"temperature": 0}, "reproducibility_notes": "Fresh synthetic invocation."},
            "research_date": "2030-01-02", "target_artifacts": [reference(target)],
            "architecture_references": self._architectures(), "verification_scope": ["full_statement", "source_grounding"],
            "deterministic_validation_report": reference(report), "created_at": REVIEW_TIMESTAMP,
        })["verification_run"]

    def _finding(self, run: dict, finding_id: str = "finding-one", *, severity: str = "medium", blocking: bool = True, status: str = "open") -> dict:
        return {
            "schema_version": "ala.authoring.verification-finding.v1", "artifact_id": finding_id,
            "artifact_type": "verification_finding", "revision": 1, "status": "immutable",
            "created_at": REVIEW_TIMESTAMP, "modified_at": REVIEW_TIMESTAMP,
            "author": {"identity": run["verifier"]["identity"], "identity_type": "model", "role": "independent_ai_verifier"},
            "supersedes": None, "finding_id": finding_id, "verification_id": run["verification_id"],
            "target": reference(self.source), "disputed_field": "title", "disputed_language": self.source["title"],
            "category": "source_mismatch", "severity": severity,
            "supporting_source": {"title": "Official synthetic authority", "publisher": "Synthetic Publisher", "canonical_url": "https://example.invalid/official", "accessed_on": "2030-01-02", "locator": "section one"},
            "explanation": "The exact statement is not supported by the cited section.", "required_action": "Use the precise source section.",
            "suggested_revision": "Replace the locator.", "affected_dependencies": [], "confidence": "high",
            "blocking": blocking, "finding_status": status, "canonical_digest": "0" * 64,
        }

    def _finalize(self, run: dict, *, finding: dict | None = None, disposition: str = "verified") -> dict:
        refs = []
        ids = []
        if finding is not None:
            stored = self.ops.add_verification_finding({"project_id": self.project_id, "verification_id": run["verification_id"], "finding": finding})["finding"]
            refs = [reference(stored)]
            ids = [stored["finding_id"]]
        return self.ops.finalize_verification_run({
            "project_id": self.project_id, "verification_id": run["verification_id"], "expected_run_digest": run["canonical_digest"],
            "finding_references": refs, "artifact_dispositions": [{"target": reference(self.source), "disposition": disposition, "finding_ids": ids, "notes": None}],
            "unresolved_questions": [], "completed_at": REVIEW_TIMESTAMP,
        })["verification_run"]

    def _human_decision(self, reviewer_id: str = "human-reviewer") -> dict:
        return self.ops.create_decision({
            "project_id": self.project_id, "decision_id": "apr-source", "decision_type": "source_approval", "target": reference(self.source),
            "dependency_digests": [], "prerequisite_decisions": [], "decision": "approved", "reviewer": reviewer(reviewer_id, "source_reviewer"),
            "scope": ["source"], "findings": [], "conditions": [], "decided_at": REVIEW_TIMESTAMP, "record_kind": "decision",
            "supersedes_decision_id": None, "revokes_decision_id": None,
        })

    def test_closed_verification_schemas_and_json_serialization(self) -> None:
        run = self._start("verify-schema")
        validate_record(run)
        bad = dict(run)
        bad["unknown"] = True
        with self.assertRaises(LearningError):
            validate_record(bad)
        json.dumps(run)

    def test_exact_target_digest_binding_and_stale_validation_rejection(self) -> None:
        report = self._report("stale")
        target = reference(self.source)
        target["canonical_digest"] = "f" * 64
        with self.assertRaises(LearningError):
            self._start("verify-stale", target=target, report=report)

    def test_human_approval_blocked_without_verification(self) -> None:
        with self.assertRaisesRegex(LearningError, "verification"):
            self._human_decision()

    def test_blocking_finding_prevents_eligibility_and_approval(self) -> None:
        run = self._start("verify-block")
        final = self._finalize(run, finding=self._finding(run), disposition="revision_required")
        result = self.ops.verification_eligibility({"project_id": self.project_id, "target": reference(self.source), "require_approved_premises": False})
        self.assertFalse(result["eligible"])
        self.assertEqual(final["human_approval_implication"], "none")
        with self.assertRaises(LearningError):
            self._human_decision()

    def test_low_nonblocking_note_can_proceed_but_never_approves(self) -> None:
        run = self._start("verify-note")
        finding = self._finding(run, severity="low", blocking=False)
        final = self._finalize(run, finding=finding, disposition="verified_with_nonblocking_note")
        result = self.ops.verification_eligibility({"project_id": self.project_id, "target": reference(self.source), "require_approved_premises": False})
        self.assertTrue(result["eligible"])
        self.assertFalse(result["human_approval_granted"])
        self.assertFalse("approval" in final)

    def test_revised_artifact_invalidates_prior_verification(self) -> None:
        self._finalize(self._start("verify-old"))
        workspace = self.root / "authoring" / self.project_id
        current_draft, _ = read_record(draft_path(workspace, "source", "src-verify"))
        changed = copy.deepcopy(current_draft)
        changed["title"] = "Revised synthetic source"
        changed["modified_at"] = "2030-01-03T00:00:00Z"
        draft = self.ops.add_or_update_draft({"project_id": self.project_id, "record": changed, "expected_prior_digest": current_draft["canonical_digest"], "markdown": None})["artifact"]
        revised = self.ops.freeze_draft({"project_id": self.project_id, "artifact_type": "source", "artifact_id": "src-verify", "expected_draft_digest": draft["canonical_digest"], "modified_at": "2030-01-03T00:00:00Z"})["artifact"]
        result = self.ops.verification_eligibility({"project_id": self.project_id, "target": reference(revised), "require_approved_premises": False})
        self.assertFalse(result["eligible"])
        self.assertIn("verification_missing", result["reasons"])

    def test_finding_resolution_links_old_and_new_but_does_not_self_close(self) -> None:
        run = self._start("verify-resolution")
        finding = self.ops.add_verification_finding({"project_id": self.project_id, "verification_id": run["verification_id"], "finding": self._finding(run)})["finding"]
        record = seal_record({
            "schema_version": "ala.authoring.finding-resolution.v1", "artifact_id": "resolution-one", "artifact_type": "finding_resolution",
            "revision": 1, "status": "immutable", "created_at": REVIEW_TIMESTAMP, "modified_at": REVIEW_TIMESTAMP,
            "author": author("source-author", "artifact_author"), "supersedes": None, "resolution_id": "resolution-one",
            "finding": reference(finding), "old_artifact": reference(self.source), "new_artifact": reference(self.source),
            "author_response": "Accepted for a future revision.", "change_summary": "No silent mutation was made.",
            "response_disposition": "accepted", "supporting_source_changes": [], "resolved_at": REVIEW_TIMESTAMP, "canonical_digest": "0" * 64,
        })
        result = self.ops.create_finding_resolution({"project_id": self.project_id, "record": record})
        self.assertFalse(result["finding_closed"])

    def test_disputed_finding_remains_blocking(self) -> None:
        run = self._start("verify-disputed")
        final = self._finalize(run, finding=self._finding(run, status="disputed"), disposition="revision_required")
        self.assertEqual(final["summary_counts"]["blocking_findings"], 1)

    def test_verifier_cannot_be_human_approver(self) -> None:
        self._finalize(self._start("verify-conflict", verifier_id="same-identity"))
        with self.assertRaisesRegex(LearningError, "verifier"):
            self._human_decision("same-identity")

    def test_compare_runs_and_metrics(self) -> None:
        first = self._finalize(self._start("verify-first"))
        second = self._finalize(self._start("verify-second"))
        comparison = self.ops.compare_verification_runs({"project_id": self.project_id, "earlier_run": reference(first), "later_run": reference(second)})
        metrics = self.ops.generate_experiment_metrics({"project_id": self.project_id, "run_references": [reference(first), reference(second)]})
        self.assertEqual(comparison["finding_delta"], 0)
        self.assertEqual(metrics["run_count"], 2)
        self.assertEqual(metrics["human_approval_implication"], "none")

    def test_consulted_source_registration_is_bounded_and_offline(self) -> None:
        run = self._start("verify-source")
        result = self.ops.register_verification_source({
            "project_id": self.project_id, "verification_id": run["verification_id"], "expected_run_digest": run["canonical_digest"],
            "source": {"source_id": "src-consulted", "title": "Consulted source", "publisher": "Synthetic Publisher", "canonical_url": "https://example.invalid/consulted", "accessed_on": "2030-01-02", "locators": ["section one"]},
            "modified_at": REVIEW_TIMESTAMP,
        })
        self.assertFalse(result["network_accessed"])
        self.assertEqual(len(result["verification_run"]["independently_accessed_sources"]), 1)

    def test_runtime_boundaries_remain_unchanged(self) -> None:
        self.assertEqual(SCHEMA_VERSION, "1")
        contract = ToolContract.__new__(ToolContract)
        class Service:
            pass
        service = Service()
        for name in ("system_health", "learner_initialize", "pack_validate", "pack_install", "study_start", "study_next", "study_submit", "study_status", "study_finish", "question_challenge"):
            setattr(service, name, lambda **_: {})
        ToolContract.__init__(contract, service)
        self.assertEqual(len(contract.tool_names), 10)
        source = (Path(__file__).parents[1] / "src" / "adaptive_learning" / "authoring" / "verification.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("hermes", source)
        self.assertNotIn("mcp", source)
        self.assertNotIn("requests", source)


if __name__ == "__main__":
    unittest.main()
