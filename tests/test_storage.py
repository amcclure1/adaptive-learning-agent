from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from adaptive_learning.schema import APPROVED_TABLES
from adaptive_learning.storage import Storage


class StorageTests(unittest.TestCase):
    def test_clean_creation_has_exact_schema_and_foreign_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            storage = Storage(Path(temporary) / "user-data")
            with storage.read() as connection:
                tables = {
                    row["name"]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                    )
                }
                version = connection.execute(
                    "SELECT value FROM schema_meta WHERE key = 'schema_version'"
                ).fetchone()["value"]
                foreign_keys = connection.execute("PRAGMA foreign_keys").fetchone()[0]

            self.assertEqual(tables, APPROVED_TABLES)
            self.assertEqual(version, "1")
            self.assertEqual(foreign_keys, 1)

    def test_transaction_rolls_back_on_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            storage = Storage(temporary)
            with self.assertRaises(RuntimeError):
                with storage.transaction() as connection:
                    connection.execute(
                        "INSERT INTO learners VALUES (?, ?, ?)",
                        ("learner-1", "Alex", "2026-01-01T00:00:00.000000Z"),
                    )
                    raise RuntimeError("stop")
            with storage.read() as connection:
                count = connection.execute("SELECT count(*) FROM learners").fetchone()[0]
            self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
