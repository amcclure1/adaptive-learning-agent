from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACK_MANIFEST = REPOSITORY_ROOT / "packs" / "amateur-extra-e1a" / "pack.json"
GOLDEN_FIXTURE = REPOSITORY_ROOT / "tests" / "fixtures" / "amateur-extra-e1a-approved.json"


def official_projection(manifest: dict[str, object]) -> list[dict[str, object]]:
    projected = []
    for question in manifest["questions"]:
        locator = re.search(r"(\[[^]]+\])$", question["source_question_ref"]["locator"])
        if locator is None:
            raise AssertionError(f"{question['id']} has no printed locator")
        projected.append(
            {
                "id": question["official_question_id"],
                "prompt": question["prompt"],
                "options": question["options"],
                "correct_option_ids": question["correct_option_ids"],
                "printed_locator": locator.group(1),
            }
        )
    return projected


def assert_matches_approved(test: unittest.TestCase, manifest: dict[str, object]) -> None:
    golden = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))
    questions = official_projection(manifest)
    test.assertEqual(len(questions), 11)
    test.assertEqual(len({item["id"] for item in questions}), 11)
    test.assertEqual(questions, golden["questions"])


class ApprovedE1AGoldenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(PACK_MANIFEST.read_text(encoding="utf-8"))

    def test_pack_exactly_matches_approved_transcription(self) -> None:
        golden = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(golden["fixture_type"], "approved_transcription")
        self.assertEqual(golden["reviewed_by"], "Anthony McClure")
        assert_matches_approved(self, self.manifest)

    def test_every_required_official_mutation_breaks_comparison(self) -> None:
        mutations = {
            "omitted question": lambda item: item["questions"].pop(),
            "extra question": lambda item: item["questions"].append(copy.deepcopy(item["questions"][-1]) | {"id": "E1A12", "official_question_id": "E1A12"}),
            "duplicate ID": lambda item: item["questions"][1].update({"official_question_id": "E1A01"}),
            "changed prompt": lambda item: item["questions"][0].update({"prompt": item["questions"][0]["prompt"][:-1] + "!"}),
            "changed Unicode": lambda item: item["questions"][5]["options"][3].update({"text": item["questions"][5]["options"][3]["text"].replace("’", "'")}),
            "reordered options": lambda item: item["questions"][0]["options"].reverse(),
            "changed option": lambda item: item["questions"][0]["options"][0].update({"text": "Changed"}),
            "changed key": lambda item: item["questions"][0].update({"correct_option_ids": ["A"]}),
            "changed locator": lambda item: item["questions"][0]["source_question_ref"].update({"locator": "E1A01 (D) [97.305]"}),
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                changed = copy.deepcopy(self.manifest)
                mutation(changed)
                with self.assertRaises(AssertionError):
                    assert_matches_approved(self, changed)


if __name__ == "__main__":
    unittest.main()
