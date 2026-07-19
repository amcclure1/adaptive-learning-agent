from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from adaptive_learning.authoring.approvals import current_decision, impact_analysis
from adaptive_learning.authoring.canonical import artifact_digest, canonical_json_bytes, markdown_digest, normalize_markdown, portable_relative_path
from adaptive_learning.authoring.compiler import EXCLUSIONS
from adaptive_learning.authoring.schemas import seal_record, validate_record
from adaptive_learning.authoring.validation import validate_release_evidence
from adaptive_learning.authoring.workspace import DIRECTORIES, atomic_write, draft_path, read_record, reference, revision_path, store_immutable, workspace_lock
from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_validation import load_pack
from adaptive_learning.schema import APPROVED_TABLES, SCHEMA_VERSION
from adaptive_learning.tool_contract import ToolContract

from authoring_helpers import (
    COMMIT,
    REVIEW_TIMESTAMP,
    TIMESTAMP,
    build_approved_workspace,
    claim_record,
    common,
    decide,
    draft_and_freeze,
    lesson_record,
    project_request,
    question_record,
    reviewer,
    source_record,
    specification_record,
)
from adaptive_learning.authoring.operations import AuthoringOperations


class AuthoringInfrastructureTests(unittest.TestCase):
    def initialize(self, root: Path, project_id: str = "synthetic-authoring"):
        ops = AuthoringOperations(root / "authoring")
        result = ops.initialize_project(project_request(project_id))
        return ops, result, root / "authoring" / project_id

    def compile_fixture(self, root: Path, candidate_id: str = "cand-synthetic", evidence_id: str = "evidence-synthetic"):
        fixture = build_approved_workspace(root)
        result = fixture["ops"].compile_approved_project({
            "project_id": fixture["project_id"], "selection_id": "selection-synthetic",
            "candidate_id": candidate_id, "evidence_id": evidence_id,
        })
        return fixture, result

    def revoke(self, fixture, prior: dict, decision_type: str, decision_id: str) -> dict:
        return fixture["ops"].create_decision({
            "project_id": fixture["project_id"], "decision_id": decision_id,
            "decision_type": decision_type, "target": prior["target"],
            "dependency_digests": [prior["canonical_digest"]], "prerequisite_decisions": [reference(prior)],
            "decision": "revoked", "reviewer": reviewer("revoker", "independent_revoker"),
            "scope": ["revocation"], "findings": [], "conditions": [],
            "decided_at": "2030-01-05T00:00:00Z", "record_kind": "revocation",
            "supersedes_decision_id": None, "revokes_decision_id": prior["artifact_id"],
        })["decision"]

    def test_01_workspace_initialization(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, result, workspace = self.initialize(Path(temporary))
            self.assertEqual(result["project"]["canonical_digest"], artifact_digest(result["project"]))
            expected_directories = {prefix for item in DIRECTORIES for prefix in ["/".join(item.split("/")[:index]) for index in range(1, len(item.split("/")) + 1)]}
            self.assertEqual({item.relative_to(workspace).as_posix() for item in workspace.rglob("*") if item.is_dir()}, expected_directories)
            self.assertEqual([item.name for item in workspace.rglob("*.json")], ["project.json"])

    def test_02_unsafe_project_id_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops = AuthoringOperations(Path(temporary) / "authoring")
            for project_id in ("../escape", "Upper", "a_b", "C:drive"):
                request = project_request()
                request["project_id"] = project_id
                with self.subTest(project_id=project_id), self.assertRaises(LearningError):
                    ops.initialize_project(request)

    def test_03_initialization_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            with self.assertRaisesRegex(LearningError, "already exists"):
                ops.initialize_project(project_request())

    def test_04_closed_schema_rejection(self) -> None:
        record = source_record("src-test")
        record["unknown"] = True
        record["canonical_digest"] = artifact_digest(record)
        with self.assertRaisesRegex(LearningError, "unknown fields"):
            validate_record(record)

    def test_05_canonical_json_golden_output(self) -> None:
        value = {"z": "Cafe\u0301\r\nline", "a": [True, 2, None]}
        self.assertEqual(canonical_json_bytes(value), '{"a":[true,2,null],"z":"Café\\nline"}'.encode())

    def test_06_canonical_markdown_golden_output(self) -> None:
        self.assertEqual(normalize_markdown("Cafe\u0301\r\n\r\n"), "Café\n")
        self.assertEqual(markdown_digest("Cafe\u0301\r\n"), markdown_digest("Café\n\n"))

    def test_07_digest_domain_separation(self) -> None:
        source = {"schema_version": "test.v1", "artifact_type": "source", "value": "same"}
        claim = {"schema_version": "test.v1", "artifact_type": "claim", "value": "same"}
        self.assertNotEqual(artifact_digest(source), artifact_digest(claim))

    def test_08_semantic_array_order_is_stable_and_preserved(self) -> None:
        first = {"schema_version": "test.v1", "artifact_type": "claim", "values": ["a", "b"]}
        second = {"schema_version": "test.v1", "artifact_type": "claim", "values": ["b", "a"]}
        self.assertNotEqual(artifact_digest(first), artifact_digest(second))
        self.assertEqual(artifact_digest(first), artifact_digest(copy.deepcopy(first)))

    def test_09_float_numbers_are_rejected(self) -> None:
        with self.assertRaisesRegex(LearningError, "Floating-point"):
            canonical_json_bytes({"value": 1.5})

    def test_10_artifact_revision_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            first = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            draft_path = root / "authoring/synthetic-authoring/sources/drafts/src-test.json"
            draft = json.loads(draft_path.read_text(encoding="utf-8"))
            draft["title"] = "Changed synthetic title"
            draft["modified_at"] = "2030-01-03T00:00:00Z"
            updated = ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": draft, "expected_prior_digest": draft["canonical_digest"], "markdown": None})["artifact"]
            second = ops.freeze_draft({"project_id": "synthetic-authoring", "artifact_type": "source", "artifact_id": "src-test", "expected_draft_digest": updated["canonical_digest"], "modified_at": "2030-01-04T00:00:00Z"})["artifact"]
            self.assertEqual(second["revision"], 2)
            self.assertEqual(second["supersedes"], reference(first))

    def test_11_stale_draft_write_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            record = source_record("src-test")
            first = ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": record, "expected_prior_digest": None, "markdown": None})["artifact"]
            with self.assertRaisesRegex(LearningError, "expected prior"):
                ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": first, "expected_prior_digest": "f" * 64, "markdown": None})

    def test_12_missing_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            selection = copy.deepcopy(fixture["selection"])
            selection["claim_references"][0]["canonical_digest"] = "f" * 64
            selection["selection_id"] = "selection-missing"
            fixture["ops"].store_selection({"project_id": fixture["project_id"], "selection": selection})
            with self.assertRaisesRegex(LearningError, "missing|match"):
                fixture["ops"].compile_approved_project({"project_id": fixture["project_id"], "selection_id": "selection-missing", "candidate_id": "cand-missing", "evidence_id": "evidence-missing"})

    def test_13_invalid_source_category(self) -> None:
        record = source_record("src-test", category="invented")
        with self.assertRaisesRegex(LearningError, "source_category"):
            seal_record(record)

    def test_14_prohibited_source_category(self) -> None:
        record = source_record("src-test", category="prohibited_material")
        record.update({"authority_tier": "excluded", "rights_reuse": "prohibited", "intended_uses": [], "prohibited_disposition": {"reason": "Synthetic prohibited input", "content_retained": False, "downstream_use": "none"}})
        self.assertEqual(seal_record(record)["source_category"], "prohibited_material")

    def test_15_stale_claim_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            claim = claim_record(source)
            claim["freshness_horizon"]["valid_through"] = "2029-01-01"
            draft_and_freeze(ops, "synthetic-authoring", claim)
            result = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("CLAIM_STALE", {item["code"] for item in result["findings"]})

    def test_15a_superseded_latest_revision_is_historical_not_current(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            current = draft_and_freeze(ops, "synthetic-authoring", claim_record(source, claim_id="clm-current"))
            retired = draft_and_freeze(ops, "synthetic-authoring", claim_record(source, claim_id="clm-retired"))
            superseded = copy.deepcopy(retired)
            superseded.update({"revision": 2, "status": "superseded", "modified_at": "2030-01-05T00:00:00Z", "supersedes": reference(retired), "canonical_digest": "0" * 64})
            superseded = seal_record(superseded)
            workspace = root / "authoring/synthetic-authoring"
            store_immutable(workspace, superseded, path=revision_path(workspace, "claim", superseded["artifact_id"], 2))

            result = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-06", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            codes = {item["code"] for item in result["findings"]}
            checked = {(item["artifact_type"], item["artifact_id"], item["revision"]) for item in result["checked_artifacts"]}
            self.assertNotIn("CLAIM_STALE", codes)
            self.assertNotIn("DECLARED_CLAIM_RANGE_MISMATCH", codes)
            self.assertIn(("claim", current["artifact_id"], current["revision"]), checked)
            self.assertFalse(any(item[1] == retired["artifact_id"] for item in checked))

    def test_16_unapproved_source_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            result = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("SOURCE_APPROVAL_MISSING", {item["code"] for item in result["findings"]})

    def test_17_unapproved_claim_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            decide(ops, "synthetic-authoring", "apr-source", "source_approval", source, "source-reviewer")
            draft_and_freeze(ops, "synthetic-authoring", claim_record(source))
            result = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("CLAIM_APPROVAL_MISSING", {item["code"] for item in result["findings"]})

    def test_18_derived_claim_missing_premises(self) -> None:
        record = claim_record({"artifact_id": "src-test", "revision": 1, "canonical_digest": "a" * 64})
        record.update({"category": "derived_recommendation", "decision_criterion": "Synthetic priority", "derived_from": []})
        with self.assertRaisesRegex(LearningError, "premise"):
            seal_record(record)

    def test_19_lesson_using_unapproved_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ops, _, _ = self.initialize(root)
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            claim = draft_and_freeze(ops, "synthetic-authoring", claim_record(source))
            lesson, markdown = lesson_record(claim, source)
            draft_and_freeze(ops, "synthetic-authoring", lesson, markdown)
            result = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("LESSON_UNAPPROVED_CLAIM", {item["code"] for item in result["findings"]})

    def test_20_invalid_selection_count(self) -> None:
        spec = specification_record()
        spec["response_design"]["required_selection_count"] = 2
        with self.assertRaisesRegex(LearningError, "selection count"):
            seal_record(spec)

    def test_21_missing_distractor_rationale(self) -> None:
        source = {"artifact_id": "src-test", "revision": 1, "canonical_digest": "a" * 64}
        claim = seal_record(claim_record(source))
        spec = seal_record(specification_record())
        question = question_record(spec, claim, source)
        question["option_rationales"].pop()
        with self.assertRaisesRegex(LearningError, "rationale"):
            seal_record(question)

    def test_22_incomplete_requirement_matrix(self) -> None:
        source = {"artifact_id": "src-test", "revision": 1, "canonical_digest": "a" * 64}
        claim = seal_record(claim_record(source))
        spec = seal_record(specification_record())
        question = question_record(spec, claim, source)
        question["requirement_option_matrix"][0]["cells"].pop()
        with self.assertRaisesRegex(LearningError, "cover every option"):
            seal_record(question)

    def test_23_missing_originality_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            prior = next(item for item in fixture["reviews"] if item["review_type"] == "question_originality_review")
            self.revoke(fixture, prior, "question_originality_review", "rev-originality-revoke")
            result = fixture["ops"].validate_project({"project_id": fixture["project_id"], "as_of": "2030-01-06", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("ORIGINALITY_REVIEW_MISSING", {item["code"] for item in result["findings"]})

    def test_24_missing_content_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            prior = next(item for item in fixture["approvals"] if item["approval_type"] == "question_content_approval")
            self.revoke(fixture, prior, "question_content_approval", "apr-content-revoke")
            result = fixture["ops"].validate_project({"project_id": fixture["project_id"], "as_of": "2030-01-06", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("QUESTION_CONTENT_APPROVAL_MISSING", {item["code"] for item in result["findings"]})

    def test_25_missing_uniqueness_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            prior = next(item for item in fixture["approvals"] if item["approval_type"] == "answer_uniqueness_approval")
            self.revoke(fixture, prior, "answer_uniqueness_approval", "apr-uniqueness-revoke")
            result = fixture["ops"].validate_project({"project_id": fixture["project_id"], "as_of": "2030-01-06", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("UNIQUENESS_APPROVAL_MISSING", {item["code"] for item in result["findings"]})

    def test_26_author_self_approval_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            with self.assertRaisesRegex(LearningError, "author"):
                decide(ops, "synthetic-authoring", "apr-source", "source_approval", source, "source-author")

    def test_27_question_author_uniqueness_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            with self.assertRaisesRegex(LearningError, "author"):
                decide(fixture["ops"], fixture["project_id"], "apr-conflict", "answer_uniqueness_approval", fixture["question"], "question-author")

    def test_28_approval_digest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            source = draft_and_freeze(ops, "synthetic-authoring", source_record("src-test"))
            target = reference(source)
            target["canonical_digest"] = "f" * 64
            request = {"project_id": "synthetic-authoring", "decision_id": "apr-bad", "decision_type": "source_approval", "target": target, "dependency_digests": [], "prerequisite_decisions": [], "decision": "approved", "reviewer": reviewer("reviewer", "source_reviewer"), "scope": ["test"], "findings": [], "conditions": [], "decided_at": REVIEW_TIMESTAMP, "record_kind": "decision", "supersedes_decision_id": None, "revokes_decision_id": None}
            with self.assertRaisesRegex(LearningError, "match"):
                ops.create_decision(request)

    def test_29_approval_is_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            source = fixture["sources"][0]
            with self.assertRaisesRegex(LearningError, "already exists"):
                decide(fixture["ops"], fixture["project_id"], "apr-source-pool", "source_approval", source, "another-reviewer")

    def test_30_revocation_is_a_new_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            prior = fixture["approvals"][0]
            request = {"project_id": fixture["project_id"], "decision_id": "apr-source-revoke", "decision_type": "source_approval", "target": reference(fixture["sources"][0]), "dependency_digests": [prior["canonical_digest"]], "prerequisite_decisions": [reference(prior)], "decision": "revoked", "reviewer": reviewer("revoker", "source_reviewer"), "scope": ["revocation"], "findings": [], "conditions": [], "decided_at": "2030-01-05T00:00:00Z", "record_kind": "revocation", "supersedes_decision_id": None, "revokes_decision_id": prior["artifact_id"]}
            revocation = fixture["ops"].create_decision(request)["decision"]
            self.assertNotEqual(prior["canonical_digest"], revocation["canonical_digest"])
            self.assertIsNone(current_decision(fixture["workspace"], target=reference(fixture["sources"][0]), decision_type="source_approval"))

    def test_31_source_change_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            changed = dict(fixture["sources"][0]); changed["title"] = "Changed"; changed["canonical_digest"] = artifact_digest(changed)
            impact = impact_analysis(fixture["workspace"], fixture["sources"][0], changed)
            self.assertIn("source_approval", impact["invalidated_decision_types"])

    def test_32_claim_change_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            changed = copy.deepcopy(fixture["claim"]); changed["statement"] += " Changed."; changed["canonical_digest"] = artifact_digest(changed)
            self.assertIn("claim_approval", impact_analysis(fixture["workspace"], fixture["claim"], changed)["invalidated_decision_types"])

    def test_33_question_change_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            changed = copy.deepcopy(fixture["question"]); changed["stem"] += " Changed."; changed["canonical_digest"] = artifact_digest(changed)
            result = impact_analysis(fixture["workspace"], fixture["question"], changed)
            self.assertIn("question_content_approval", result["invalidated_decision_types"])

    def test_34_uniqueness_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            changed = copy.deepcopy(fixture["question"]); changed["keyed_option_ids"] = ["b"]; changed["canonical_digest"] = artifact_digest(changed)
            self.assertIn("answer_uniqueness_approval", impact_analysis(fixture["workspace"], fixture["question"], changed)["invalidated_decision_types"])

    def test_35_release_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, result = self.compile_fixture(Path(temporary))
            candidate = result["candidate"]
            changed = copy.deepcopy(candidate); changed["compiler_output_digest"] = "f" * 64; changed["canonical_digest"] = artifact_digest(changed)
            self.assertIn("pack_release_approval", impact_analysis(Path(temporary) / "authoring/synthetic-authoring", candidate, changed)["invalidated_decision_types"])

    def test_36_compile_draft_or_mismatched_reference_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            draft, _ = read_record(draft_path(fixture["workspace"], "lesson", fixture["lesson"]["artifact_id"]))
            selection = copy.deepcopy(fixture["selection"]); selection["selection_id"] = "selection-draft"; selection["lesson_references"] = [reference(draft)]; selection["lesson_projections"][0]["lesson_reference"] = reference(draft)
            fixture["ops"].store_selection({"project_id": fixture["project_id"], "selection": selection})
            with self.assertRaisesRegex(LearningError, "Draft"):
                fixture["ops"].compile_approved_project({"project_id": fixture["project_id"], "selection_id": "selection-draft", "candidate_id": "cand-draft", "evidence_id": "evidence-draft"})

    def test_37_compile_stale_dependency_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            stale = copy.deepcopy(fixture["claim"])
            stale.update({"revision": 2, "status": "stale", "modified_at": "2030-01-05T00:00:00Z", "supersedes": reference(fixture["claim"]), "canonical_digest": "0" * 64})
            stale = seal_record(stale)
            store_immutable(fixture["workspace"], stale, path=revision_path(fixture["workspace"], "claim", stale["artifact_id"], 2))
            selection = copy.deepcopy(fixture["selection"]); selection["selection_id"] = "selection-stale"; selection["claim_references"] = [reference(stale)]
            fixture["ops"].store_selection({"project_id": fixture["project_id"], "selection": selection})
            with self.assertRaisesRegex(LearningError, "stale"):
                fixture["ops"].compile_approved_project({"project_id": fixture["project_id"], "selection_id": "selection-stale", "candidate_id": "cand-stale", "evidence_id": "evidence-stale"})

    def test_38_format_02_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture, result = self.compile_fixture(Path(temporary))
            pack = json.loads((fixture["workspace"] / result["candidate_path"] / "pack.json").read_text(encoding="utf-8"))
            self.assertEqual(pack["format_version"], "0.2")
            self.assertEqual(pack["lessons"][0]["path"], "lessons/synthetic.md")
            self.assertEqual(pack["questions"][0]["correct_option_ids"], ["a"])
            self.assertIn("pattern two does not", pack["questions"][0]["explanation"])

    def test_39_internal_fields_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture, result = self.compile_fixture(Path(temporary))
            text = (fixture["workspace"] / result["candidate_path"] / "pack.json").read_text(encoding="utf-8")
            for forbidden in ("option_rationales", "requirement_option_matrix", "supporting_claim_references", "conflict_of_interest", "originality_review_state"):
                self.assertNotIn(forbidden, text)
            self.assertEqual(result["release_evidence"]["exclusions"], EXCLUSIONS)

    def test_40_repeated_compilation_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            _, result_a = self.compile_fixture(Path(first))
            _, result_b = self.compile_fixture(Path(second))
            self.assertEqual(result_a["candidate_pack_digest"], result_b["candidate_pack_digest"])
            self.assertEqual(result_a["release_evidence"]["canonical_digest"], result_b["release_evidence"]["canonical_digest"])

    def test_41_changed_input_changes_output_digest(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            _, result_a = self.compile_fixture(Path(first))
            fixture = build_approved_workspace(Path(second))
            selection = copy.deepcopy(fixture["selection"]); selection["selection_id"] = "selection-changed"; selection["pack"]["title"] = "Changed synthetic pack"
            fixture["ops"].store_selection({"project_id": fixture["project_id"], "selection": selection})
            result_b = fixture["ops"].compile_approved_project({"project_id": fixture["project_id"], "selection_id": "selection-changed", "candidate_id": "cand-synthetic", "evidence_id": "evidence-synthetic"})
            self.assertNotEqual(result_a["candidate_pack_digest"], result_b["candidate_pack_digest"])
            self.assertNotEqual(result_a["release_evidence"]["canonical_digest"], result_b["release_evidence"]["canonical_digest"])

    def test_42_release_evidence_completeness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, result = self.compile_fixture(Path(temporary))
            evidence = result["release_evidence"]
            expected = {"project", "compiler_version", "source_workspace_commit", "assessment_blueprint", "learning_architecture", "realization_plan", "source_records", "approved_claims", "lessons", "question_specifications", "approved_final_questions", "approval_records", "validation_reports", "compiled_pack", "compiler_input_digest", "compiler_output_digest", "compilation_timestamp", "release_review_approval"}
            self.assertTrue(expected <= set(evidence))

    def test_43_release_evidence_mismatch_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, result = self.compile_fixture(Path(temporary))
            changed = copy.deepcopy(result["release_evidence"]); changed["compiled_pack"]["digest"] = "f" * 64; changed["canonical_digest"] = artifact_digest(changed)
            validation = validate_release_evidence(changed, candidate=result["release_evidence"])
            self.assertEqual(validation["result"], "failed")

    def test_44_sqlite_schema_remains_one_without_authoring_tables(self) -> None:
        self.assertEqual(SCHEMA_VERSION, "1")
        self.assertFalse(any("author" in table for table in APPROVED_TABLES))

    def test_45_learner_operation_count_is_unchanged(self) -> None:
        contract = ToolContract(mock.Mock())
        self.assertEqual(len(contract.tool_names), 10)
        self.assertFalse(any(name.startswith("authoring") for name in contract.tool_names))

    def test_46_pack_parser_behavior_is_unchanged(self) -> None:
        fixture = Path(__file__).resolve().parents[1] / "packs" / "fixture-basics"
        self.assertEqual(digest_pack(load_pack(fixture)), "12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf")

    def test_47_no_network_dependency_and_json_serializable_results(self) -> None:
        source_root = Path(__file__).resolve().parents[1] / "src/adaptive_learning/authoring"
        text = "\n".join(path.read_text(encoding="utf-8") for path in source_root.glob("*.py"))
        for forbidden in ("import requests", "import socket", "urllib.request", "http.client"):
            self.assertNotIn(forbidden, text)
        with tempfile.TemporaryDirectory() as temporary:
            _, result = self.compile_fixture(Path(temporary))
            json.dumps(result)

    def test_48_portable_path_behavior(self) -> None:
        self.assertEqual(portable_relative_path("lessons/test.md"), "lessons/test.md")
        for invalid in ("../test.md", "C:/test.md", "lessons\\test.md", "/absolute.md"):
            with self.subTest(invalid=invalid), self.assertRaises(LearningError):
                portable_relative_path(invalid)

    def test_49_atomic_write_failure_preserves_prior_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            path.write_bytes(b"prior\n")
            with mock.patch("adaptive_learning.authoring.workspace.os.replace", side_effect=OSError("synthetic failure")), self.assertRaises(OSError):
                atomic_write(path, b"changed\n")
            self.assertEqual(path.read_bytes(), b"prior\n")
            self.assertEqual(list(Path(temporary).glob("*.tmp")), [])

    def test_50_workspace_lock_contention_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, _, workspace = self.initialize(Path(temporary))
            with workspace_lock(workspace):
                with self.assertRaisesRegex(LearningError, "already being mutated"):
                    with workspace_lock(workspace):
                        pass

    def test_51_structured_per_option_teaching_escalates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            selection = copy.deepcopy(fixture["selection"]); selection["selection_id"] = "selection-format-four"; selection["requires_structured_option_teaching"] = True
            with self.assertRaisesRegex(LearningError, "format 0.4"):
                fixture["ops"].store_selection({"project_id": fixture["project_id"], "selection": selection})

    def test_52_candidate_is_not_installable_or_approved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture, result = self.compile_fixture(Path(temporary))
            manifest = json.loads((fixture["workspace"] / result["candidate_path"] / "pack.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["approval"]["status"], "pending")
            self.assertFalse(result["human_approval_granted"])

    def test_53_pack_release_approval_and_final_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture, result = self.compile_fixture(Path(temporary))
            approval = decide(
                fixture["ops"], fixture["project_id"], "apr-pack-release", "pack_release_approval",
                result["candidate"], "release-reviewer", [result["release_evidence"]["canonical_digest"]],
                [reference(item) for item in [*fixture["approvals"], *fixture["reviews"]]],
            )
            final = fixture["ops"].generate_release_evidence({
                "project_id": fixture["project_id"], "candidate_evidence": result["release_evidence"],
                "release_approval": approval, "final_evidence_id": "evidence-final",
                "finalized_at": "2030-01-06T00:00:00Z",
            })["release_evidence"]
            self.assertEqual(final["phase"], "final")
            self.assertEqual(final["release_review_approval"], reference(approval))

    def test_54_candidate_failure_rolls_back_all_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_approved_workspace(Path(temporary))
            real_atomic_write = atomic_write
            calls = 0

            def fail_second(path, content, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("synthetic evidence-write failure")
                return real_atomic_write(path, content, **kwargs)

            with mock.patch("adaptive_learning.authoring.compiler.atomic_write", side_effect=fail_second), self.assertRaises(OSError):
                fixture["ops"].compile_approved_project({"project_id": fixture["project_id"], "selection_id": "selection-synthetic", "candidate_id": "cand-rollback", "evidence_id": "evidence-rollback"})
            self.assertFalse((fixture["workspace"] / "release/candidates/cand-rollback-pack").exists())
            self.assertFalse((fixture["workspace"] / "release/candidates/cand-rollback.json").exists())
            self.assertFalse((fixture["workspace"] / "release/evidence/evidence-rollback.json").exists())

    def test_55_project_v2_binds_workspace_commit_and_claim_range(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, result, _ = self.initialize(Path(temporary))
            project = result["project"]
            self.assertEqual(project["schema_version"], "ala.authoring.project.v2")
            self.assertEqual(project["workspace_commit"], COMMIT)
            self.assertEqual(project["pilot_scope"]["claim_count_range"], {"minimum": 1, "maximum": 2})
            validation = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertEqual(validation["result"], "passed")

    def test_56_project_v1_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, result, _ = self.initialize(Path(temporary))
            project = copy.deepcopy(result["project"])
            project["schema_version"] = "ala.authoring.project.v1"
            project.pop("workspace_commit")
            project["pilot_scope"].pop("claim_count_range")
            project = seal_record(project)
            self.assertEqual(validate_record(project)["schema_version"], "ala.authoring.project.v1")

    def test_57_draft_source_and_claim_references_are_validated_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            source = ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": source_record("src-test"), "expected_prior_digest": None, "markdown": None})["artifact"]
            ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": claim_record(source), "expected_prior_digest": None, "markdown": None})
            validation = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertEqual(validation["result"], "passed")
            self.assertFalse({"SOURCE_APPROVAL_MISSING", "CLAIM_APPROVAL_MISSING"} & {item["code"] for item in validation["findings"]})

    def test_58_missing_draft_source_reference_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ops, _, _ = self.initialize(Path(temporary))
            source = seal_record(source_record("src-test"))
            claim = claim_record(source)
            claim["source_references"][0]["canonical_digest"] = "f" * 64
            ops.add_or_update_draft({"project_id": "synthetic-authoring", "record": claim, "expected_prior_digest": None, "markdown": None})
            validation = ops.validate_project({"project_id": "synthetic-authoring", "as_of": "2030-01-01", "workspace_commit": COMMIT, "validation_id": None, "executed_at": None, "persist": False})
            self.assertIn("REFERENCE_MISSING", {item["code"] for item in validation["findings"]})


if __name__ == "__main__":
    unittest.main()
