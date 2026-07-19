from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from adaptive_learning.application_service import ApplicationService
from adaptive_learning.asset_reference import issue_asset_reference, parse_asset_reference
from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_validation import load_pack, load_pack_for_review

from v03_helpers import approved_scopes, png_bytes, write_manifest, write_pack


class Format03ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "pack"
        self.root.mkdir()
        self.data = write_pack(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def rewrite(self) -> None:
        write_manifest(self.root, self.data)

    def assert_invalid(self, fragment: str | None = None) -> None:
        with self.assertRaises(LearningError) as caught:
            load_pack(self.root)
        self.assertEqual(caught.exception.code, "PACK_VALIDATION_FAILED")
        if fragment:
            self.assertIn(fragment, caught.exception.message)

    def replace_asset(self, content: bytes) -> None:
        (self.root / "assets" / "figure-t1.png").write_bytes(content)
        self.data["assets"][0]["content_sha256"] = hashlib.sha256(content).hexdigest()
        self.rewrite()

    def add_asset(self, identifier: str, content: bytes) -> None:
        path = f"assets/{identifier}.png"
        (self.root / path).write_bytes(content)
        item = copy.deepcopy(self.data["assets"][0])
        item.update(
            {
                "id": identifier,
                "path": path,
                "content_sha256": hashlib.sha256(content).hexdigest(),
                "official_figure_id": identifier.upper(),
            }
        )
        self.data["assets"].append(item)
        self.data["questions"][0]["asset_ids"].append(identifier)

    def test_exact_dispatch_and_closed_asset_shapes(self) -> None:
        pack = load_pack(self.root)
        self.assertEqual(pack.format_version, "0.3")
        self.data["assets"][0]["unexpected"] = True
        self.rewrite()
        self.assert_invalid("unknown fields")
        self.data["format_version"] = "0.3.0"
        self.rewrite()
        self.assert_invalid("exactly")

    def test_pending_pack_is_reviewable_but_not_installable(self) -> None:
        self.data["approval"] = {
            "status": "pending",
            "reviewed_by": None,
            "reviewed_at": None,
            "review_scope": [],
        }
        self.rewrite()
        self.assertEqual(load_pack_for_review(self.root).approval["status"], "pending")
        self.assert_invalid("approved")

    def test_approval_requires_every_exact_scope(self) -> None:
        self.data["approval"]["review_scope"] = approved_scopes()[:-1]
        self.rewrite()
        self.assert_invalid("every accepted review scope")

    def test_missing_and_undeclared_assets_are_rejected(self) -> None:
        (self.root / "assets" / "figure-t1.png").unlink()
        self.assert_invalid("readable pack file")
        write_pack(self.root, content=png_bytes(marker=b"restored"))
        (self.root / "assets" / "extra.png").write_bytes(png_bytes(marker=b"extra"))
        self.assert_invalid("only pack.json")

    def test_asset_paths_reject_traversal_absolute_backslash_case_and_duplicates(self) -> None:
        mutations = (
            "../figure.png",
            str((self.root / "assets" / "figure-t1.png").resolve()),
            "assets\\figure-t1.png",
            "assets/FIGURE-T1.png",
        )
        for value in mutations:
            with self.subTest(value=value):
                original = self.data["assets"][0]["path"]
                self.data["assets"][0]["path"] = value
                self.rewrite()
                self.assert_invalid()
                self.data["assets"][0]["path"] = original
        self.add_asset("asset-two", png_bytes(marker=b"two"))
        self.data["assets"][1]["path"] = "assets/figure-t1.png"
        self.rewrite()
        self.assert_invalid("unique")

    def test_symlink_or_hardlink_alias_is_rejected_when_supported(self) -> None:
        alias = self.root / "assets" / "alias.png"
        try:
            os.link(self.root / "assets" / "figure-t1.png", alias)
        except OSError:
            self.skipTest("Hard links are unavailable on this filesystem")
        item = copy.deepcopy(self.data["assets"][0])
        item.update({"id": "asset-alias", "path": "assets/alias.png"})
        self.data["assets"].append(item)
        self.data["questions"][0]["asset_ids"].append("asset-alias")
        self.rewrite()
        self.assert_invalid()

    def test_duplicate_ids_hashes_and_raw_bytes_are_rejected(self) -> None:
        content = png_bytes(marker=b"two")
        self.add_asset("asset-two", content)
        self.data["assets"][1]["id"] = "asset-t1"
        self.rewrite()
        self.assert_invalid("Duplicate asset ID")
        self.data["assets"][1]["id"] = "asset-two"
        self.data["assets"][1]["content_sha256"] = self.data["assets"][0]["content_sha256"]
        self.rewrite()
        self.assert_invalid("hashes must be unique")
        (self.root / "assets" / "asset-two.png").write_bytes((self.root / "assets" / "figure-t1.png").read_bytes())
        self.rewrite()
        self.assert_invalid()

    def test_only_png_media_type_and_signature_are_accepted(self) -> None:
        self.data["assets"][0]["media_type"] = "image/jpeg"
        self.rewrite()
        self.assert_invalid("image/png")
        self.data["assets"][0]["media_type"] = "image/png"
        broken = b"not-png"
        self.replace_asset(broken)
        self.assert_invalid("signature")

    def test_png_framing_crc_and_trailing_data_are_rejected(self) -> None:
        valid = png_bytes()
        for broken in (valid[:-3], valid[:29] + bytes([valid[29] ^ 1]) + valid[30:], valid + b"trailing"):
            with self.subTest(length=len(broken)):
                self.replace_asset(broken)
                self.assert_invalid()

    def test_png_dimensions_and_declared_dimensions_are_bounded(self) -> None:
        self.data["assets"][0]["width"] = 3
        self.rewrite()
        self.assert_invalid("dimensions do not match")
        large = png_bytes(width=4097, height=1)
        self.replace_asset(large)
        self.data["assets"][0].update({"width": 4097, "height": 1})
        self.rewrite()
        self.assert_invalid("dimensions are outside")

    def test_asset_digest_and_individual_size_are_enforced(self) -> None:
        self.data["assets"][0]["content_sha256"] = "0" * 64
        self.rewrite()
        self.assert_invalid("does not match")
        oversized = png_bytes(marker=b"x" * (2 * 1024 * 1024))
        self.replace_asset(oversized)
        self.assert_invalid("2 MiB")

    def test_asset_count_and_total_size_are_enforced(self) -> None:
        for index in range(16):
            self.add_asset(f"asset-{index}", png_bytes(marker=f"{index}".encode()))
        self.rewrite()
        self.assert_invalid("between 1 and 16")

        self.tearDown()
        self.setUp()
        for index in range(5):
            self.add_asset(f"large-{index}", png_bytes(marker=bytes([65 + index]) * 1_800_000))
        self.rewrite()
        self.assert_invalid("8 MiB")

    def test_question_and_lesson_asset_references_must_resolve(self) -> None:
        self.data["questions"][0]["asset_ids"] = ["missing"]
        self.rewrite()
        self.assert_invalid("Question Q1")
        self.data["questions"][0]["asset_ids"] = ["asset-t1"]
        self.data["lessons"][0]["asset_ids"] = ["missing"]
        self.rewrite()
        self.assert_invalid("Lesson lesson-figure")

    def test_figure_mentions_require_a_matching_mapping_and_assets_must_be_used(self) -> None:
        self.data["questions"][0]["asset_ids"] = []
        self.rewrite()
        self.assert_invalid("official figure")
        for question in self.data["questions"]:
            question["asset_ids"] = []
            question["prompt"] = "No figure is named."
        self.rewrite()
        self.assert_invalid("Every asset")

    def test_source_and_rights_references_must_resolve(self) -> None:
        for field, value in (("source_id", "missing"), ("rights_id", "missing"), ("accessibility_rights_id", "missing")):
            with self.subTest(field=field):
                original = self.data["assets"][0][field]
                self.data["assets"][0][field] = value
                self.rewrite()
                self.assert_invalid()
                self.data["assets"][0][field] = original

    def test_accessibility_fields_are_nonempty_and_trimmed(self) -> None:
        for field in ("caption", "alt_text", "terminal_fallback"):
            with self.subTest(field=field):
                original = self.data["assets"][0][field]
                self.data["assets"][0][field] = " "
                self.rewrite()
                self.assert_invalid("non-empty")
                self.data["assets"][0][field] = original

    def test_answer_marker_and_complete_keyed_option_lint(self) -> None:
        self.data["assets"][0]["alt_text"] = "The answer is B."
        self.rewrite()
        self.assert_invalid("answer marker")
        self.data["assets"][0]["alt_text"] = "Neutral start; KEY PHRASE B1; neutral end."
        self.rewrite()
        self.assert_invalid("complete keyed option")

    def test_shared_asset_across_three_questions_and_optional_derivation(self) -> None:
        pack = load_pack(self.root)
        self.assertEqual([question.asset_ids for question in pack.questions], [("asset-t1",)] * 3)
        self.data["assets"][0]["derivation"] = {
            "kind": "format_conversion",
            "source_media_type": "image/svg+xml",
            "source_content_sha256": "a" * 64,
            "process": "Deterministic synthetic test process",
            "fidelity_review_required": True,
        }
        self.rewrite()
        self.assertIsNotNone(load_pack(self.root).assets[0].derivation)

    def test_digest_binds_asset_bytes_accessibility_and_asset_order(self) -> None:
        original = digest_pack(load_pack(self.root))
        changed = png_bytes(marker=b"changed")
        self.replace_asset(changed)
        byte_digest = digest_pack(load_pack(self.root))
        self.assertNotEqual(original, byte_digest)
        self.data["assets"][0]["alt_text"] += " Additional neutral detail."
        self.rewrite()
        accessibility_digest = digest_pack(load_pack(self.root))
        self.assertNotEqual(byte_digest, accessibility_digest)
        self.add_asset("asset-two", png_bytes(marker=b"two"))
        self.rewrite()
        ordered = digest_pack(load_pack(self.root))
        self.data["assets"].reverse()
        self.rewrite()
        self.assertNotEqual(ordered, digest_pack(load_pack(self.root)))


class Format03WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        base = Path(self.temporary.name)
        self.pack_path = base / "pack"
        self.pack_path.mkdir()
        self.data = write_pack(self.pack_path)
        self.service = ApplicationService(base / "user-data")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def install_and_start(self) -> tuple[str, dict[str, object]]:
        self.service.pack_install(self.pack_path)
        learner = self.service.learner_initialize("Learner")
        started = self.service.study_start(learner["learner_id"], "format-03-test", "0.3.0")
        return learner["learner_id"], started

    def test_health_validate_and_install_have_additive_asset_summaries(self) -> None:
        health = self.service.system_health()
        self.assertEqual(health["pack_format_versions"], ["0.1", "0.2", "0.3"])
        self.assertTrue(health["capabilities"]["static_local_assets"])
        self.assertEqual(health["capabilities"]["supported_asset_media_types"], ["image/png"])
        validated = self.service.pack_validate(self.pack_path)
        installed = self.service.pack_install(self.pack_path)
        self.assertEqual(validated["asset_summary"]["asset_count"], 1)
        self.assertEqual(installed["asset_summary"]["integrity_status"], "validated")

    def test_question_descriptor_is_answer_safe_json_and_core_referenced(self) -> None:
        _, started = self.install_and_start()
        self.assertNotIn("assets", started["lessons"][0])
        shown = self.service.study_next(started["session_id"])
        question = shown["question"]
        self.assertNotIn("correct_option_ids", question)
        self.assertNotIn("explanation", question)
        descriptor = question["assets"][0]
        self.assertTrue(descriptor["asset_ref"].startswith("ala-pack-asset-v1:"))
        claims = parse_asset_reference(descriptor["asset_ref"])
        self.assertEqual((claims.pack_id, claims.pack_version, claims.asset_id), ("format-03-test", "0.3.0", "asset-t1"))
        self.assertEqual(self.service.resolve_asset_reference(descriptor["asset_ref"]).read_bytes(), png_bytes())
        json.dumps(shown)

    def test_malformed_stale_and_unknown_asset_references_are_rejected(self) -> None:
        _, started = self.install_and_start()
        descriptor = self.service.study_next(started["session_id"])["question"]["assets"][0]
        with self.assertRaises(LearningError):
            self.service.resolve_asset_reference("ala-pack-asset-v1:not-valid-json")
        claims = parse_asset_reference(descriptor["asset_ref"])
        stale = issue_asset_reference(claims.pack_id, claims.pack_version, "0" * 64, claims.asset_id)
        with self.assertRaises(LearningError) as caught:
            self.service.resolve_asset_reference(stale)
        self.assertEqual(caught.exception.code, "ASSET_REFERENCE_STALE")
        unknown = issue_asset_reference(claims.pack_id, claims.pack_version, claims.pack_digest, "missing")
        with self.assertRaises(LearningError):
            self.service.resolve_asset_reference(unknown)

    def test_resolver_rejects_an_installed_path_outside_the_store(self) -> None:
        _, started = self.install_and_start()
        descriptor = self.service.study_next(started["session_id"])["question"]["assets"][0]
        with self.service.storage.transaction() as connection:
            connection.execute(
                "UPDATE installed_packs SET install_path = ? WHERE pack_id = ?",
                (str(self.pack_path), "format-03-test"),
            )
        with self.assertRaises(LearningError) as caught:
            self.service.resolve_asset_reference(descriptor["asset_ref"])
        self.assertEqual(caught.exception.code, "PACK_PATH_INVALID")

    def test_restart_reconstructs_descriptor_and_challenge_is_unchanged(self) -> None:
        learner_id, started = self.install_and_start()
        first = self.service.study_next(started["session_id"])
        restarted = ApplicationService(self.service.storage.user_data_path)
        resumed = restarted.study_start(learner_id, "format-03-test", "0.3.0")
        second = restarted.study_next(resumed["session_id"])
        self.assertEqual(first["question"]["assets"], second["question"]["assets"])
        challenge = restarted.question_challenge(resumed["session_id"], second["presentation_id"], "Figure inaccessible")
        self.assertTrue(challenge["quarantined"])

    def test_submit_keeps_scoring_and_attempt_immutability_and_adds_figure_reference(self) -> None:
        _, started = self.install_and_start()
        shown = self.service.study_next(started["session_id"])
        result = self.service.study_submit(started["session_id"], shown["presentation_id"], ["B"], 4)
        self.assertTrue(result["is_correct"])
        self.assertEqual(result["figure_references"][0]["asset_id"], "asset-t1")
        with self.assertRaises(LearningError) as caught:
            self.service.study_submit(started["session_id"], shown["presentation_id"], ["A"], 4)
        self.assertEqual(caught.exception.code, "ATTEMPT_CONFLICT")

    def test_same_identity_changed_content_conflicts(self) -> None:
        self.service.pack_install(self.pack_path)
        changed = png_bytes(marker=b"changed")
        (self.pack_path / "assets" / "figure-t1.png").write_bytes(changed)
        self.data["assets"][0]["content_sha256"] = hashlib.sha256(changed).hexdigest()
        write_manifest(self.pack_path, self.data)
        with self.assertRaises(LearningError) as caught:
            self.service.pack_install(self.pack_path)
        self.assertEqual(caught.exception.code, "PACK_VERSION_CONFLICT")

    def test_core_asset_workflow_has_no_network_dependency(self) -> None:
        source = Path(__file__).parents[1] / "src" / "adaptive_learning"
        combined = "\n".join(path.read_text(encoding="utf-8") for path in source.glob("*.py"))
        for forbidden in ("import requests", "import urllib", "import httpx", "import socket"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
