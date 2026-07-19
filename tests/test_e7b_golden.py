from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_validation import load_pack, load_pack_for_review


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "packs" / "amateur-extra-e7b"
GOLDEN_PATH = ROOT / "tests" / "fixtures" / "amateur-extra-e7b-official.json"
DRAFT_DIGEST = "9c43be04bc38910f12ddf1d90eb62e69cd916ed06fccf44c0770e6fbf2218d43"


def official_records(pack) -> list[dict[str, object]]:
    records = []
    for question in pack.questions:
        records.append(
            {
                "id": question.official_question_id,
                "prompt": question.prompt,
                "options": [{"id": option.option_id, "text": option.text} for option in question.options],
                "correct_option_ids": list(question.correct_option_ids),
                "printed_locator": question.source_question_reference.locator,
            }
        )
    return records


class PendingE7BGoldenTests(unittest.TestCase):
    def test_pending_pack_matches_exact_official_question_golden(self) -> None:
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        pack = load_pack_for_review(PACK_PATH)
        self.assertEqual(official_records(pack), golden["questions"])
        self.assertEqual([question.question_id for question in pack.questions], ["E7B10", "E7B11", "E7B12"])
        self.assertEqual([question.asset_ids for question in pack.questions], [("asset-figure-e7-1",)] * 3)

    def test_exact_asset_and_source_mapping_match_golden(self) -> None:
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        pack = load_pack_for_review(PACK_PATH)
        asset = pack.assets[0]
        expected = golden["asset"]
        self.assertEqual(asset.official_figure_id, expected["official_figure_id"])
        self.assertEqual(asset.media_type, expected["media_type"])
        self.assertEqual((asset.width, asset.height), (expected["width"], expected["height"]))
        self.assertEqual(len(asset.content), expected["byte_length"])
        self.assertEqual(hashlib.sha256(asset.content).hexdigest(), expected["content_sha256"])
        source = pack.source("ncvec-extra-pool-docx-fourth-errata")
        self.assertEqual(source.content_sha256, golden["source"]["content_sha256"])

    def test_pending_draft_digest_is_stable_and_public_load_is_blocked(self) -> None:
        pack = load_pack_for_review(PACK_PATH)
        self.assertEqual(digest_pack(pack), DRAFT_DIGEST)
        with self.assertRaises(LearningError) as caught:
            load_pack(PACK_PATH)
        self.assertIn("approved", caught.exception.message)

    def test_golden_comparison_detects_every_official_field_class(self) -> None:
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))["questions"]
        mutations = []
        missing = copy.deepcopy(golden)
        missing.pop()
        mutations.append(missing)
        extra = copy.deepcopy(golden)
        extra.append(copy.deepcopy(extra[-1]))
        mutations.append(extra)
        for field in ("id", "prompt", "correct_option_ids", "printed_locator"):
            changed = copy.deepcopy(golden)
            changed[0][field] = ["A"] if field == "correct_option_ids" else f"changed-{field}"
            mutations.append(changed)
        reordered = copy.deepcopy(golden)
        reordered[0]["options"].reverse()
        mutations.append(reordered)
        option_text = copy.deepcopy(golden)
        option_text[0]["options"][0]["text"] += "."
        mutations.append(option_text)
        for candidate in mutations:
            with self.subTest(candidate=candidate):
                self.assertNotEqual(candidate, golden)


if __name__ == "__main__":
    unittest.main()
