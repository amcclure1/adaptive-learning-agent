"""Deterministic version-0.1 learning operations."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

from .errors import LearningError, require
from .pack_digest import canonical_json_bytes, digest_pack, digest_question
from .pack_model import Pack, Question
from .pack_validation import load_pack
from .schema import SCHEMA_VERSION
from .storage import Storage
from .time_and_ids import TimeAndIds


class ApplicationService:
    """Runtime-independent application boundary; all returned values are JSON-compatible."""

    contract_version = "0.1"

    def __init__(
        self,
        user_data_path: str | Path,
        *,
        time_and_ids: TimeAndIds | None = None,
    ) -> None:
        self.storage = Storage(user_data_path)
        self.time_and_ids = time_and_ids or TimeAndIds()

    def system_health(self) -> dict[str, Any]:
        with self.storage.read() as connection:
            version = connection.execute(
                "SELECT value FROM schema_meta WHERE key = 'schema_version'"
            ).fetchone()["value"]
        return {
            "status": "ok",
            "contract_version": self.contract_version,
            "schema_version": version,
            "pack_format_versions": ["0.1"],
        }

    def learner_initialize(self, display_name: str) -> dict[str, Any]:
        require(isinstance(display_name, str) and bool(display_name.strip()), "INVALID_ARGUMENT", "display_name must be a non-empty string.")
        with self.storage.transaction() as connection:
            existing = connection.execute(
                "SELECT learner_id, display_name FROM learners ORDER BY created_at, learner_id LIMIT 1"
            ).fetchone()
            if existing is not None:
                return {
                    "learner_id": existing["learner_id"],
                    "display_name": existing["display_name"],
                    "created": False,
                }
            learner_id = self.time_and_ids.identifier("learner")
            connection.execute(
                "INSERT INTO learners(learner_id, display_name, created_at) VALUES (?, ?, ?)",
                (learner_id, display_name.strip(), self.time_and_ids.timestamp()),
            )
            return {"learner_id": learner_id, "display_name": display_name.strip(), "created": True}

    def pack_validate(self, source_path: str | Path) -> dict[str, Any]:
        pack = load_pack(source_path)
        return {
            "valid": True,
            "pack_id": pack.pack_id,
            "pack_version": pack.version,
            "pack_digest": digest_pack(pack),
            "objective_count": len(pack.objectives),
            "question_count": len(pack.questions),
            "diagnostics": [],
        }

    def pack_install(self, source_path: str | Path) -> dict[str, Any]:
        pack = load_pack(source_path)
        pack_digest = digest_pack(pack)
        with self.storage.read() as connection:
            existing = self._installed_pack_row(connection, pack.pack_id, pack.version)
        if existing is not None:
            return self._existing_install_result(existing, pack_digest)

        destination_key = hashlib.sha256(
            canonical_json_bytes([pack.pack_id, pack.version])
        ).hexdigest()
        destination = (self.storage.pack_store_path / destination_key).resolve(strict=False)
        destination.relative_to(self.storage.pack_store_path)
        created_destination = False
        if not destination.exists():
            temporary = Path(tempfile.mkdtemp(prefix="install-", dir=self.storage.pack_store_path))
            try:
                shutil.copyfile(pack.source_path / "pack.json", temporary / "pack.json")
                shutil.copyfile(pack.source_path / pack.lesson_name, temporary / pack.lesson_name)
                os.replace(temporary, destination)
                created_destination = True
            except FileExistsError:
                shutil.rmtree(temporary, ignore_errors=True)
            except BaseException:
                shutil.rmtree(temporary, ignore_errors=True)
                raise

        installed_pack = load_pack(destination)
        if (
            installed_pack.pack_id != pack.pack_id
            or installed_pack.version != pack.version
            or digest_pack(installed_pack) != pack_digest
        ):
            raise LearningError("PACK_VERSION_CONFLICT", "The controlled pack store contains different content for this pack version.")

        try:
            with self.storage.transaction() as connection:
                existing = self._installed_pack_row(connection, pack.pack_id, pack.version)
                if existing is not None:
                    return self._existing_install_result(existing, pack_digest)
                connection.execute(
                    """INSERT INTO installed_packs
                       (pack_id, pack_version, pack_digest, title, install_path, installed_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        pack.pack_id,
                        pack.version,
                        pack_digest,
                        pack.title,
                        str(destination),
                        self.time_and_ids.timestamp(),
                    ),
                )
        except BaseException:
            if created_destination:
                shutil.rmtree(destination, ignore_errors=True)
            raise
        return {
            "pack_id": pack.pack_id,
            "pack_version": pack.version,
            "pack_digest": pack_digest,
            "title": pack.title,
            "installed": True,
        }

    def study_start(self, learner_id: str, pack_id: str, pack_version: str) -> dict[str, Any]:
        self._require_text(learner_id, "learner_id")
        self._require_text(pack_id, "pack_id")
        self._require_text(pack_version, "pack_version")
        with self.storage.transaction() as connection:
            self._require_learner(connection, learner_id)
            pack_row = self._require_installed_pack(connection, pack_id, pack_version)
            pack = self._load_installed_pack(pack_row)
            active = connection.execute(
                "SELECT * FROM study_sessions WHERE learner_id = ? AND status = 'active'",
                (learner_id,),
            ).fetchone()
            if active is not None:
                if active["pack_id"] != pack_id or active["pack_version"] != pack_version:
                    raise LearningError("ACTIVE_SESSION_CONFLICT", "The learner already has an active session for another pack.")
                return self._session_start_result(connection, active, pack, resumed=True)
            session_id = self.time_and_ids.identifier("session")
            connection.execute(
                """INSERT INTO study_sessions
                   (session_id, learner_id, pack_id, pack_version, status, started_at, finished_at)
                   VALUES (?, ?, ?, ?, 'active', ?, NULL)""",
                (session_id, learner_id, pack_id, pack_version, self.time_and_ids.timestamp()),
            )
            session = connection.execute(
                "SELECT * FROM study_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
            return self._session_start_result(connection, session, pack, resumed=False)

    def study_next(self, session_id: str) -> dict[str, Any]:
        self._require_text(session_id, "session_id")
        with self.storage.transaction() as connection:
            session = self._require_active_session(connection, session_id)
            pack = self._load_installed_pack(
                self._require_installed_pack(connection, session["pack_id"], session["pack_version"])
            )
            outstanding = connection.execute(
                """SELECT p.* FROM presentations p
                   LEFT JOIN question_challenges q ON q.learner_id = ?
                     AND q.pack_id = ? AND q.pack_version = ? AND q.question_id = p.question_id
                   WHERE p.session_id = ? AND p.status = 'presented' AND q.challenge_id IS NULL
                   ORDER BY p.ordinal LIMIT 1""",
                (session["learner_id"], session["pack_id"], session["pack_version"], session_id),
            ).fetchone()
            if outstanding is not None:
                return self._presentation_result(outstanding, pack)

            presented_ids = {
                row["question_id"]
                for row in connection.execute(
                    "SELECT question_id FROM presentations WHERE session_id = ?", (session_id,)
                )
            }
            challenged_ids = self._challenged_ids(connection, session)
            candidates = sorted(
                (
                    question
                    for question in pack.questions
                    if question.question_id not in presented_ids and question.question_id not in challenged_ids
                ),
                key=lambda item: item.question_id,
            )
            if not candidates:
                raise LearningError("NO_ELIGIBLE_QUESTION", "No eligible question remains in this session.")
            question = candidates[0]
            ordinal = connection.execute(
                "SELECT coalesce(max(ordinal), 0) + 1 FROM presentations WHERE session_id = ?",
                (session_id,),
            ).fetchone()[0]
            presentation_id = self.time_and_ids.identifier("presentation")
            connection.execute(
                """INSERT INTO presentations
                   (presentation_id, session_id, ordinal, question_id, question_digest, status, presented_at)
                   VALUES (?, ?, ?, ?, ?, 'presented', ?)""",
                (
                    presentation_id,
                    session_id,
                    ordinal,
                    question.question_id,
                    digest_question(question),
                    self.time_and_ids.timestamp(),
                ),
            )
            presentation = connection.execute(
                "SELECT * FROM presentations WHERE presentation_id = ?", (presentation_id,)
            ).fetchone()
            return self._presentation_result(presentation, pack)

    def study_submit(
        self,
        session_id: str,
        presentation_id: str,
        selected_option_ids: list[str],
        confidence: int,
    ) -> dict[str, Any]:
        self._require_text(session_id, "session_id")
        self._require_text(presentation_id, "presentation_id")
        if not isinstance(confidence, int) or isinstance(confidence, bool) or not 1 <= confidence <= 5:
            raise LearningError("INVALID_CONFIDENCE", "confidence must be an integer from 1 through 5.")
        with self.storage.transaction() as connection:
            session = self._require_active_session(connection, session_id)
            presentation = connection.execute(
                "SELECT * FROM presentations WHERE presentation_id = ? AND session_id = ?",
                (presentation_id, session_id),
            ).fetchone()
            if presentation is None:
                raise LearningError("PRESENTATION_NOT_FOUND", "The presentation does not belong to this session.")
            pack_row = self._require_installed_pack(connection, session["pack_id"], session["pack_version"])
            pack = self._load_installed_pack(pack_row, verify_digest=False)
            question = self._question_or_error(pack, presentation["question_id"])
            if digest_question(question) != presentation["question_digest"]:
                raise LearningError("QUESTION_DIGEST_MISMATCH", "The presented question changed before submission.")
            if digest_pack(pack) != pack_row["pack_digest"]:
                raise LearningError("PACK_DIGEST_MISMATCH", "The installed pack changed after installation.")
            canonical_selection = self._validate_selection(question, selected_option_ids)
            selection_json = json.dumps(canonical_selection, separators=(",", ":"))

            existing = connection.execute(
                "SELECT * FROM attempts WHERE presentation_id = ?", (presentation_id,)
            ).fetchone()
            if existing is not None:
                if existing["selected_option_ids_json"] != selection_json or existing["confidence"] != confidence:
                    raise LearningError("ATTEMPT_CONFLICT", "This presentation already has a different immutable attempt.")
                return self._attempt_result(connection, existing, session, question, pack)
            if presentation["status"] != "presented":
                raise LearningError("PRESENTATION_NOT_SUBMITTABLE", "The presentation is not awaiting an answer.")

            is_correct = set(canonical_selection) == set(question.correct_option_ids)
            latest_attempt_time = connection.execute("SELECT max(submitted_at) FROM attempts").fetchone()[0]
            submitted_at = self.time_and_ids.timestamp(after=latest_attempt_time)
            attempt_id = self.time_and_ids.identifier("attempt")
            connection.execute(
                """INSERT INTO attempts
                   (attempt_id, presentation_id, selected_option_ids_json, is_correct, confidence, submitted_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (attempt_id, presentation_id, selection_json, int(is_correct), confidence, submitted_at),
            )
            connection.execute(
                "UPDATE presentations SET status = 'answered' WHERE presentation_id = ?",
                (presentation_id,),
            )
            connection.execute(
                """INSERT INTO objective_progress
                   (learner_id, pack_id, pack_version, objective_id, attempts_count, correct_count, updated_at)
                   VALUES (?, ?, ?, ?, 1, ?, ?)
                   ON CONFLICT(learner_id, pack_id, pack_version, objective_id) DO UPDATE SET
                     attempts_count = attempts_count + 1,
                     correct_count = correct_count + excluded.correct_count,
                     updated_at = excluded.updated_at""",
                (
                    session["learner_id"],
                    session["pack_id"],
                    session["pack_version"],
                    question.objective_id,
                    int(is_correct),
                    submitted_at,
                ),
            )
            attempt = connection.execute(
                "SELECT * FROM attempts WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
            return self._attempt_result(connection, attempt, session, question, pack)

    def study_status(self, learner_id: str) -> dict[str, Any]:
        self._require_text(learner_id, "learner_id")
        with self.storage.read() as connection:
            self._require_learner(connection, learner_id)
            installed_packs = [
                {
                    "pack_id": row["pack_id"],
                    "pack_version": row["pack_version"],
                    "title": row["title"],
                }
                for row in connection.execute(
                    "SELECT * FROM installed_packs ORDER BY pack_id, pack_version"
                )
            ]
            session = connection.execute(
                "SELECT * FROM study_sessions WHERE learner_id = ? AND status = 'active'",
                (learner_id,),
            ).fetchone()
            if session is None:
                return {"active_session": None, "objective_progress": [], "installed_packs": installed_packs}
            pack = self._load_installed_pack(
                self._require_installed_pack(connection, session["pack_id"], session["pack_version"])
            )
            challenged = self._challenged_ids(connection, session)
            answered = {
                row["question_id"]
                for row in connection.execute(
                    "SELECT question_id FROM presentations WHERE session_id = ? AND status = 'answered'",
                    (session["session_id"],),
                )
            }
            outstanding = connection.execute(
                "SELECT presentation_id FROM presentations WHERE session_id = ? AND status = 'presented' ORDER BY ordinal LIMIT 1",
                (session["session_id"],),
            ).fetchone()
            progress_rows = {
                row["objective_id"]: row
                for row in connection.execute(
                    """SELECT * FROM objective_progress
                       WHERE learner_id = ? AND pack_id = ? AND pack_version = ?""",
                    (learner_id, session["pack_id"], session["pack_version"]),
                )
            }
            progress = []
            for objective in pack.objectives:
                row = progress_rows.get(objective.objective_id)
                attempts = row["attempts_count"] if row is not None else 0
                correct = row["correct_count"] if row is not None else 0
                progress.append(
                    {
                        "objective_id": objective.objective_id,
                        "attempts_count": attempts,
                        "correct_count": correct,
                        "correct_ratio": correct / attempts if attempts else None,
                    }
                )
            eligible_ids = {question.question_id for question in pack.questions} - challenged
            return {
                "active_session": {
                    "session_id": session["session_id"],
                    "pack_id": session["pack_id"],
                    "pack_version": session["pack_version"],
                    "answered_count": len(answered & eligible_ids),
                    "remaining_count": len(eligible_ids - answered),
                    "challenged_count": len(challenged),
                    "outstanding_presentation_id": outstanding["presentation_id"] if outstanding else None,
                },
                "objective_progress": progress,
                "installed_packs": installed_packs,
            }

    def study_finish(self, session_id: str) -> dict[str, Any]:
        self._require_text(session_id, "session_id")
        with self.storage.transaction() as connection:
            session = connection.execute(
                "SELECT * FROM study_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
            if session is None:
                raise LearningError("SESSION_NOT_FOUND", "The session does not exist.")
            if session["status"] == "completed":
                return self._finished_summary(connection, session)
            pack = self._load_installed_pack(
                self._require_installed_pack(connection, session["pack_id"], session["pack_version"])
            )
            challenged = self._challenged_ids(connection, session)
            answered = {
                row["question_id"]
                for row in connection.execute(
                    "SELECT question_id FROM presentations WHERE session_id = ? AND status = 'answered'",
                    (session_id,),
                )
            }
            required_ids = {question.question_id for question in pack.questions} - challenged
            outstanding = connection.execute(
                "SELECT 1 FROM presentations WHERE session_id = ? AND status = 'presented' LIMIT 1",
                (session_id,),
            ).fetchone()
            if not required_ids <= answered or outstanding is not None:
                raise LearningError("SESSION_NOT_FINISHABLE", "Eligible questions remain unanswered.")
            connection.execute(
                "UPDATE study_sessions SET status = 'completed', finished_at = ? WHERE session_id = ?",
                (self.time_and_ids.timestamp(), session_id),
            )
            completed = connection.execute(
                "SELECT * FROM study_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
            return self._finished_summary(connection, completed)

    def question_challenge(self, session_id: str, presentation_id: str, reason: str) -> dict[str, Any]:
        self._require_text(session_id, "session_id")
        self._require_text(presentation_id, "presentation_id")
        self._require_text(reason, "reason")
        with self.storage.transaction() as connection:
            session = self._require_active_session(connection, session_id)
            presentation = connection.execute(
                "SELECT * FROM presentations WHERE presentation_id = ? AND session_id = ?",
                (presentation_id, session_id),
            ).fetchone()
            if presentation is None:
                raise LearningError("PRESENTATION_NOT_FOUND", "The presentation does not belong to this session.")
            existing = connection.execute(
                """SELECT * FROM question_challenges
                   WHERE learner_id = ? AND pack_id = ? AND pack_version = ? AND question_id = ?""",
                (session["learner_id"], session["pack_id"], session["pack_version"], presentation["question_id"]),
            ).fetchone()
            if existing is not None:
                return {
                    "challenge_id": existing["challenge_id"],
                    "question_id": existing["question_id"],
                    "quarantined": True,
                    "created": False,
                }
            challenge_id = self.time_and_ids.identifier("challenge")
            connection.execute(
                """INSERT INTO question_challenges
                   (challenge_id, learner_id, pack_id, pack_version, question_id, presentation_id, reason, challenged_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    challenge_id,
                    session["learner_id"],
                    session["pack_id"],
                    session["pack_version"],
                    presentation["question_id"],
                    presentation_id,
                    reason.strip(),
                    self.time_and_ids.timestamp(),
                ),
            )
            if presentation["status"] == "presented":
                connection.execute(
                    "UPDATE presentations SET status = 'challenged' WHERE presentation_id = ?",
                    (presentation_id,),
                )
            return {
                "challenge_id": challenge_id,
                "question_id": presentation["question_id"],
                "quarantined": True,
                "created": True,
            }

    @staticmethod
    def _require_text(value: Any, name: str) -> None:
        require(isinstance(value, str) and bool(value.strip()), "INVALID_ARGUMENT", f"{name} must be a non-empty string.")

    @staticmethod
    def _installed_pack_row(connection: sqlite3.Connection, pack_id: str, pack_version: str) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT * FROM installed_packs WHERE pack_id = ? AND pack_version = ?",
            (pack_id, pack_version),
        ).fetchone()

    def _require_installed_pack(self, connection: sqlite3.Connection, pack_id: str, pack_version: str) -> sqlite3.Row:
        row = self._installed_pack_row(connection, pack_id, pack_version)
        if row is None:
            raise LearningError("PACK_NOT_INSTALLED", "The requested pack version is not installed.")
        return row

    @staticmethod
    def _require_learner(connection: sqlite3.Connection, learner_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM learners WHERE learner_id = ?", (learner_id,)).fetchone()
        if row is None:
            raise LearningError("LEARNER_NOT_FOUND", "The learner does not exist.")
        return row

    @staticmethod
    def _require_active_session(connection: sqlite3.Connection, session_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM study_sessions WHERE session_id = ?", (session_id,)).fetchone()
        if row is None:
            raise LearningError("SESSION_NOT_FOUND", "The session does not exist.")
        if row["status"] != "active":
            raise LearningError("SESSION_NOT_ACTIVE", "The session is not active.")
        return row

    def _load_installed_pack(self, row: sqlite3.Row, *, verify_digest: bool = True) -> Pack:
        path = Path(row["install_path"]).resolve(strict=False)
        try:
            path.relative_to(self.storage.pack_store_path)
        except ValueError as exc:
            raise LearningError("PACK_PATH_INVALID", "The installed pack path is outside the controlled store.") from exc
        pack = load_pack(path)
        if pack.pack_id != row["pack_id"] or pack.version != row["pack_version"]:
            raise LearningError("PACK_IDENTITY_MISMATCH", "The installed pack identity changed.")
        if verify_digest and digest_pack(pack) != row["pack_digest"]:
            raise LearningError("PACK_DIGEST_MISMATCH", "The installed pack changed after installation.")
        return pack

    @staticmethod
    def _existing_install_result(existing: sqlite3.Row, proposed_digest: str) -> dict[str, Any]:
        if existing["pack_digest"] != proposed_digest:
            raise LearningError("PACK_VERSION_CONFLICT", "This pack ID and version are already installed with different content.")
        return {
            "pack_id": existing["pack_id"],
            "pack_version": existing["pack_version"],
            "pack_digest": existing["pack_digest"],
            "title": existing["title"],
            "installed": False,
        }

    @staticmethod
    def _question_or_error(pack: Pack, question_id: str) -> Question:
        try:
            return pack.question(question_id)
        except StopIteration as exc:
            raise LearningError("QUESTION_NOT_FOUND", "The presented question is no longer in the pack.") from exc

    @staticmethod
    def _validate_selection(question: Question, selected: Any) -> list[str]:
        if not isinstance(selected, list) or any(not isinstance(item, str) or not item for item in selected):
            raise LearningError("INVALID_SELECTION", "selected_option_ids must be an array of non-empty strings.")
        if len(set(selected)) != len(selected):
            raise LearningError("INVALID_SELECTION", "selected_option_ids must not contain duplicates.")
        known = {option.option_id for option in question.options}
        if not set(selected) <= known:
            raise LearningError("INVALID_SELECTION", "selected_option_ids contains an unknown option ID.")
        if question.question_type == "single_response" and len(selected) != 1:
            raise LearningError("INVALID_SELECTION", "A single-response submission must select exactly one option.")
        if question.question_type == "multiple_response" and not selected:
            raise LearningError("INVALID_SELECTION", "A multiple-response submission must select at least one option.")
        return sorted(selected)

    @staticmethod
    def _challenged_ids(connection: sqlite3.Connection, session: sqlite3.Row) -> set[str]:
        return {
            row["question_id"]
            for row in connection.execute(
                """SELECT question_id FROM question_challenges
                   WHERE learner_id = ? AND pack_id = ? AND pack_version = ?""",
                (session["learner_id"], session["pack_id"], session["pack_version"]),
            )
        }

    def _session_start_result(self, connection: sqlite3.Connection, session: sqlite3.Row, pack: Pack, *, resumed: bool) -> dict[str, Any]:
        challenged = self._challenged_ids(connection, session)
        answered_count = connection.execute(
            "SELECT count(*) FROM presentations WHERE session_id = ? AND status = 'answered'",
            (session["session_id"],),
        ).fetchone()[0]
        return {
            "session_id": session["session_id"],
            "status": session["status"],
            "resumed": resumed,
            "pack": {"pack_id": pack.pack_id, "version": pack.version, "title": pack.title},
            "lesson_markdown": pack.lesson_markdown,
            "answered_count": answered_count,
            "eligible_count": len(pack.questions) - len(challenged),
        }

    @staticmethod
    def _presentation_result(presentation: sqlite3.Row, pack: Pack) -> dict[str, Any]:
        question = pack.question(presentation["question_id"])
        objective = pack.objective(question.objective_id)
        return {
            "presentation_id": presentation["presentation_id"],
            "ordinal": presentation["ordinal"],
            "question": {
                "question_id": question.question_id,
                "type": question.question_type,
                "prompt": question.prompt,
                "options": [{"id": item.option_id, "text": item.text} for item in question.options],
                "objective": {"id": objective.objective_id, "title": objective.title},
            },
        }

    def _attempt_result(
        self,
        connection: sqlite3.Connection,
        attempt: sqlite3.Row,
        session: sqlite3.Row,
        question: Question,
        pack: Pack,
    ) -> dict[str, Any]:
        question_objectives = {item.question_id: item.objective_id for item in pack.questions}
        historical = connection.execute(
            """SELECT a.is_correct, p.question_id FROM attempts a
               JOIN presentations p ON p.presentation_id = a.presentation_id
               JOIN study_sessions s ON s.session_id = p.session_id
               WHERE s.learner_id = ? AND s.pack_id = ? AND s.pack_version = ?
                 AND a.submitted_at <= ?""",
            (
                session["learner_id"],
                session["pack_id"],
                session["pack_version"],
                attempt["submitted_at"],
            ),
        ).fetchall()
        objective_attempts = [
            row for row in historical if question_objectives.get(row["question_id"]) == question.objective_id
        ]
        return {
            "attempt_id": attempt["attempt_id"],
            "is_correct": bool(attempt["is_correct"]),
            "confidence": attempt["confidence"],
            "correct_option_ids": list(question.correct_option_ids),
            "explanation": question.explanation,
            "objective_progress": {
                "objective_id": question.objective_id,
                "attempts_count": len(objective_attempts),
                "correct_count": sum(row["is_correct"] for row in objective_attempts),
            },
        }

    @staticmethod
    def _finished_summary(connection: sqlite3.Connection, session: sqlite3.Row) -> dict[str, Any]:
        counts = connection.execute(
            """SELECT count(*) AS answered_count, coalesce(sum(a.is_correct), 0) AS correct_count
               FROM attempts a JOIN presentations p ON p.presentation_id = a.presentation_id
               WHERE p.session_id = ?""",
            (session["session_id"],),
        ).fetchone()
        return {
            "session_id": session["session_id"],
            "status": "completed",
            "answered_count": counts["answered_count"],
            "correct_count": counts["correct_count"],
        }
