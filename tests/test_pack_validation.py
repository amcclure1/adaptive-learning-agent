from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from adaptive_learning.errors import LearningError
from adaptive_learning.pack_digest import digest_pack
from adaptive_learning.pack_validation import load_pack


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PACK = REPOSITORY_ROOT / "packs" / "fixture-basics"


class PackValidationTests(unittest.TestCase):
    def copy_fixture(self, destination: Path) -> Path:
        pack_path = destination / "fixture"
        shutil.copytree(FIXTURE_PACK, pack_path)
        return pack_path

    def test_fixture_shape_and_digest_are_stable(self) -> None:
        pack = load_pack(FIXTURE_PACK)

        self.assertEqual(pack.format_version, "0.1")
        self.assertEqual(len(pack.objectives), 2)
        self.assertEqual(len(pack.questions), 5)
        self.assertEqual(sum(q.question_type == "single_response" for q in pack.questions), 3)
        self.assertEqual(sum(q.question_type == "multiple_response" for q in pack.questions), 2)
        self.assertEqual(digest_pack(pack), digest_pack(load_pack(FIXTURE_PACK)))

    def test_rejects_path_traversal_in_lesson(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack_path = self.copy_fixture(root)
            record = json.loads((pack_path / "pack.json").read_text(encoding="utf-8"))
            record["lesson"] = "../lesson.md"
            (pack_path / "pack.json").write_text(json.dumps(record), encoding="utf-8")

            with self.assertRaisesRegex(LearningError, "relative Markdown"):
                load_pack(pack_path)

    def test_rejects_unknown_fields_at_each_record_level(self) -> None:
        mutations = [
            lambda record: record.update({"surprise": True}),
            lambda record: record["objectives"][0].update({"surprise": True}),
            lambda record: record["questions"][0].update({"surprise": True}),
            lambda record: record["questions"][0]["options"][0].update({"surprise": True}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                pack_path = self.copy_fixture(Path(temporary))
                manifest = pack_path / "pack.json"
                record = json.loads(manifest.read_text(encoding="utf-8"))
                mutation(record)
                manifest.write_text(json.dumps(record), encoding="utf-8")
                with self.assertRaisesRegex(LearningError, "unknown fields"):
                    load_pack(pack_path)

    def test_rejects_unknown_correct_option(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pack_path = self.copy_fixture(Path(temporary))
            manifest = pack_path / "pack.json"
            record = json.loads(manifest.read_text(encoding="utf-8"))
            record["questions"][0]["correct_option_ids"] = ["missing"]
            manifest.write_text(json.dumps(record), encoding="utf-8")

            with self.assertRaisesRegex(LearningError, "unknown correct option"):
                load_pack(pack_path)


if __name__ == "__main__":
    unittest.main()
