from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from adaptive_learning.application_service import ApplicationService
from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_validation import load_pack
from adaptive_learning.time_and_ids import TimeAndIds


def manifest() -> dict[str, object]:
    return {
        "format_version": "0.2",
        "pack_id": "synthetic-sourced",
        "version": "0.2.0-test",
        "title": "Synthetic sourced test pack",
        "language": "en-US",
        "tags": ["synthetic"],
        "assessment_pool": {
            "id": "synthetic-pool",
            "title": "Synthetic Pool",
            "publisher": "Test Publisher",
            "effective_from": "2026-01-01",
            "effective_through": "2026-12-31",
            "source_id": "pool-source",
            "errata_revision": "revision-1",
            "errata_source_id": "errata-source",
            "withdrawn_official_question_ids": [],
        },
        "rights": [
            {
                "id": "pool-rights",
                "scope": "official_question_pool_content",
                "status": "public_domain",
                "basis_source_id": "errata-source",
                "covered_material": ["wording", "choices", "answer_keys", "identifiers"],
            },
            {
                "id": "original-rights",
                "scope": "original_lessons_and_explanations",
                "status": "licensed",
                "license_expression": "CC-BY-4.0",
                "copyright_holder": "Test contributors",
            },
            {"id": "reference-rights", "scope": "external_official_sources", "status": "reference_only"},
        ],
        "sources": [
            {
                "id": "pool-source",
                "type": "official_question_pool",
                "title": "Synthetic Official Pool",
                "publisher": "Test Publisher",
                "url": "https://example.invalid/pool.pdf",
                "retrieved_on": "2026-07-18",
                "revision": "revision-1",
                "snapshot_retained": True,
                "content_sha256": "a" * 64,
                "rights_id": "pool-rights",
            },
            {
                "id": "errata-source",
                "type": "official_errata",
                "title": "Synthetic Errata",
                "publisher": "Test Publisher",
                "url": "https://example.invalid/errata",
                "retrieved_on": "2026-07-18",
                "revision": "revision-1",
                "snapshot_retained": False,
                "rights_id": "reference-rights",
            },
            {
                "id": "rule-source",
                "type": "regulation",
                "title": "Synthetic Regulation",
                "publisher": "Test Publisher",
                "url": "https://example.invalid/rule",
                "retrieved_on": "2026-07-18",
                "snapshot_retained": False,
                "rights_id": "reference-rights",
            },
        ],
        "objectives": [
            {"id": "objective-one", "title": "First objective"},
            {"id": "objective-two", "title": "Second objective"},
        ],
        "lessons": [
            {
                "id": "lesson-one",
                "title": "First lesson",
                "path": "lessons/01-first.md",
                "objective_ids": ["objective-one"],
                "rights_id": "original-rights",
                "citations": [{"source_id": "rule-source", "locator": "section 1"}],
            },
            {
                "id": "lesson-two",
                "title": "Second lesson",
                "path": "lessons/02-second.md",
                "objective_ids": ["objective-two"],
                "rights_id": "original-rights",
                "citations": [{"source_id": "rule-source", "locator": "section 2"}],
            },
        ],
        "questions": [
            {
                "id": "Q01",
                "type": "single_response",
                "origin": "official_pool",
                "official_question_id": "Q01",
                "pool_id": "synthetic-pool",
                "source_question_ref": {"source_id": "pool-source", "locator": "Q01 page 1"},
                "objective_id": "objective-one",
                "tags": ["synthetic"],
                "prompt": "Which choice is correct?",
                "options": [{"id": "A", "text": "Correct"}, {"id": "B", "text": "Incorrect"}],
                "correct_option_ids": ["A"],
                "question_rights_id": "pool-rights",
                "explanation": "The regulation supports A.",
                "explanation_rights_id": "original-rights",
                "explanation_citations": [{"source_id": "rule-source", "locator": "section 1"}],
            },
            {
                "id": "Q02",
                "type": "single_response",
                "origin": "official_pool",
                "official_question_id": "Q02",
                "pool_id": "synthetic-pool",
                "source_question_ref": {"source_id": "pool-source", "locator": "Q02 page 1"},
                "objective_id": "objective-two",
                "tags": ["synthetic"],
                "prompt": "Which second choice is correct?",
                "options": [{"id": "A", "text": "Incorrect"}, {"id": "B", "text": "Correct"}],
                "correct_option_ids": ["B"],
                "question_rights_id": "pool-rights",
                "explanation": "The regulation supports B.",
                "explanation_rights_id": "original-rights",
                "explanation_citations": [{"source_id": "rule-source", "locator": "section 2"}],
            },
        ],
        "approval": {
            "status": "approved",
            "reviewed_by": "Synthetic fixture reviewer",
            "reviewed_at": "2026-07-18T12:00:00Z",
            "review_scope": ["official_wording", "answer_keys", "lessons", "citations"],
        },
    }


class Format02Tests(unittest.TestCase):
    def make_pack(self, root: Path, record: dict[str, object] | None = None) -> Path:
        pack = root / "pack"
        (pack / "lessons").mkdir(parents=True)
        (pack / "lessons" / "01-first.md").write_text("# First\n\nOriginal lesson one.\n", encoding="utf-8")
        (pack / "lessons" / "02-second.md").write_text("# Second\n\nOriginal lesson two.\n", encoding="utf-8")
        (pack / "pack.json").write_text(json.dumps(record or manifest()), encoding="utf-8")
        return pack

    def mutate(self, root: Path, mutation) -> Path:
        record = copy.deepcopy(manifest())
        mutation(record)
        return self.make_pack(root, record)

    def test_valid_pack_loads_with_ordered_lessons_and_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pack_path = self.make_pack(Path(temporary))
            pack = load_pack(pack_path)
            self.assertEqual([item.lesson_id for item in pack.lessons], ["lesson-one", "lesson-two"])
            self.assertEqual(pack.questions[0].official_question_id, "Q01")
            self.assertEqual(pack.sources[0].content_sha256, "a" * 64)
            self.assertEqual(digest_pack(pack), digest_pack(load_pack(pack_path)))

    def test_format_01_digest_remains_at_its_golden_value(self) -> None:
        fixture = Path(__file__).resolve().parents[1] / "packs" / "fixture-basics"
        self.assertEqual(digest_pack(load_pack(fixture)), "12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf")

    def test_closed_records_reject_unknown_fields(self) -> None:
        for mutation in (
            lambda item: item.update({"unknown": True}),
            lambda item: item["sources"][0].update({"unknown": True}),
            lambda item: item["lessons"][0].update({"unknown": True}),
            lambda item: item["approval"].update({"unknown": True}),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaisesRegex(LearningError, "unknown fields"):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_snapshot_digest_is_strictly_conditional(self) -> None:
        mutations = (
            lambda item: item["sources"][0].pop("content_sha256"),
            lambda item: item["sources"][1].update({"content_sha256": "b" * 64}),
            lambda item: item["sources"][0].update({"content_sha256": "A" * 64}),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaisesRegex(LearningError, "content_sha256"):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_paths_and_declared_file_set_are_confined(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(LearningError):
                load_pack(self.mutate(root, lambda item: item["lessons"][0].update({"path": "../escape.md"})))
        with tempfile.TemporaryDirectory() as temporary:
            pack = self.make_pack(Path(temporary))
            (pack / "extra.txt").write_text("unexpected", encoding="utf-8")
            with self.assertRaisesRegex(LearningError, "may contain only"):
                load_pack(pack)

    def test_dangling_source_objective_and_rights_references_fail(self) -> None:
        mutations = (
            lambda item: item["lessons"][0]["citations"][0].update({"source_id": "missing"}),
            lambda item: item["questions"][0].update({"objective_id": "missing"}),
            lambda item: item["lessons"][0].update({"rights_id": "pool-rights"}),
            lambda item: item.update({"rights": []}),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaises(LearningError):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_pool_errata_and_withdrawal_rules_are_enforced(self) -> None:
        mutations = (
            lambda item: item["assessment_pool"].update({"source_id": "rule-source"}),
            lambda item: item["assessment_pool"].update({"errata_source_id": "rule-source"}),
            lambda item: item["assessment_pool"]["withdrawn_official_question_ids"].append("Q01"),
            lambda item: item["assessment_pool"].update({"effective_from": "2027-01-01", "effective_through": "2026-01-01"}),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaises(LearningError):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_official_and_generated_origin_shapes_are_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(LearningError):
                load_pack(self.mutate(Path(temporary), lambda item: item["questions"][0].update({"origin": "generated"})))
        with tempfile.TemporaryDirectory() as temporary:
            record = manifest()
            question = record["questions"][0]
            for field in ("official_question_id", "pool_id", "source_question_ref"):
                question.pop(field)
            question["origin"] = "generated"
            question["question_rights_id"] = "original-rights"
            pack = load_pack(self.make_pack(Path(temporary), record))
            self.assertEqual(pack.questions[0].origin, "generated")
        mutations = (
            lambda item: item["questions"][0].pop("official_question_id"),
            lambda item: item["questions"][0].pop("pool_id"),
            lambda item: item["questions"][0].pop("source_question_ref"),
            lambda item: item["questions"][1].update({"id": "Q01", "official_question_id": "Q01", "source_question_ref": {"source_id": "pool-source", "locator": "Q01 page 1"}}),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaises(LearningError):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_approval_must_be_approved_structured_and_scoped(self) -> None:
        mutations = (
            lambda item: item["approval"].update({"status": "draft"}),
            lambda item: item["approval"].update({"reviewed_at": "yesterday"}),
            lambda item: item["approval"].update({"review_scope": ["invented"]}),
            lambda item: item["approval"].update({"review_scope": []}),
            lambda item: item.pop("approval"),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaises(LearningError):
                    load_pack(self.mutate(Path(temporary), mutation))

    def test_digest_binds_manifest_lesson_order_content_and_notice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline_path = self.make_pack(root / "a")
            baseline = digest_pack(load_pack(baseline_path))
            changed_path = self.make_pack(root / "b")
            (changed_path / "lessons" / "01-first.md").write_text("# Changed\n", encoding="utf-8")
            self.assertNotEqual(baseline, digest_pack(load_pack(changed_path)))
            notice_path = self.make_pack(root / "c")
            (notice_path / "NOTICE.md").write_text("Rights notice\n", encoding="utf-8")
            self.assertNotEqual(baseline, digest_pack(load_pack(notice_path)))
            reordered = manifest()
            reordered["lessons"].reverse()
            self.assertNotEqual(baseline, digest_pack(load_pack(self.make_pack(root / "d", reordered))))
            source_changed = manifest()
            source_changed["sources"][2]["retrieved_on"] = "2026-07-17"
            self.assertNotEqual(baseline, digest_pack(load_pack(self.make_pack(root / "e", source_changed))))

    def test_invalid_citation_locators_are_rejected(self) -> None:
        for locator in ("https://example.invalid/rule", "line one\nline two", "\x01section"):
            with self.subTest(locator=locator), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaisesRegex(LearningError, "locator"):
                    load_pack(self.mutate(Path(temporary), lambda item: item["lessons"][0]["citations"][0].update({"locator": locator})))

    def test_contract_outputs_add_provenance_without_pre_answer_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack_path = self.make_pack(root / "source")
            service = ApplicationService(root / "data", time_and_ids=TimeAndIds())
            validation = service.pack_validate(pack_path)
            self.assertEqual(validation["question_origins"], {"official_pool": 2, "generated": 0})
            service.pack_install(pack_path)
            learner = service.learner_initialize("Learner")
            started = service.study_start(learner["learner_id"], "synthetic-sourced", "0.2.0-test")
            self.assertEqual(len(started["lessons"]), 2)
            presented = service.study_next(started["session_id"])
            self.assertEqual(presented["question"]["official_question_id"], "Q01")
            self.assertNotIn("correct_option_ids", presented["question"])
            self.assertNotIn("explanation_citations", presented["question"])
            feedback = service.study_submit(started["session_id"], presented["presentation_id"], ["A"], 3)
            self.assertEqual(feedback["provenance"]["explanation_citations"][0]["source_id"], "rule-source")
            restarted = ApplicationService(root / "data")
            resumed = restarted.study_start(learner["learner_id"], "synthetic-sourced", "0.2.0-test")
            self.assertTrue(resumed["resumed"])
            second = restarted.study_next(started["session_id"])
            challenge = restarted.question_challenge(started["session_id"], second["presentation_id"], "Synthetic challenge")
            self.assertTrue(challenge["quarantined"])


if __name__ == "__main__":
    unittest.main()
