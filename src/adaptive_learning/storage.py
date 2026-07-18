"""SQLite connection, schema, and explicit transaction management."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .errors import LearningError
from .schema import APPROVED_TABLES, SCHEMA_SQL, SCHEMA_VERSION


class Storage:
    def __init__(self, user_data_path: str | Path) -> None:
        try:
            self.user_data_path = Path(user_data_path).expanduser().resolve(strict=False)
        except (OSError, RuntimeError, TypeError, ValueError) as exc:
            raise LearningError("DATA_PATH_INVALID", "The user-data path is invalid.") from exc
        self.user_data_path.mkdir(parents=True, exist_ok=True)
        if not self.user_data_path.is_dir():
            raise LearningError("DATA_PATH_INVALID", "The user-data path must be a directory.")
        self.database_path = self.user_data_path / "learner.sqlite3"
        self.pack_store_path = self.user_data_path / "packs"
        self.pack_store_path.mkdir(exist_ok=True)
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            connection.close()
            raise LearningError("DATABASE_CONFIGURATION_FAILED", "SQLite foreign keys could not be enabled.")
        return connection

    def _initialize(self) -> None:
        connection = self.connect()
        try:
            connection.executescript(SCHEMA_SQL)
            version_row = connection.execute(
                "SELECT value FROM schema_meta WHERE key = 'schema_version'"
            ).fetchone()
            if version_row is None or version_row["value"] != SCHEMA_VERSION:
                raise LearningError("SCHEMA_VERSION_UNSUPPORTED", "The SQLite schema version is unsupported.")
            actual_tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                )
            }
            if actual_tables != APPROVED_TABLES:
                raise LearningError("SCHEMA_UNEXPECTED", "The database contains an unexpected application table.")
        finally:
            connection.close()

    @contextmanager
    def read(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()
