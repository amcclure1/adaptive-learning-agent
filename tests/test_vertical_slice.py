from __future__ import annotations

import ast
import json
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Any

from adaptive_learning.application_service import ApplicationService
from adaptive_learning.schema import APPROVED_TABLES
from adaptive_learning.tool_contract import ToolContract


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src" / "adaptive_learning"
FIXTURE_PACK = REPOSITORY_ROOT / "packs" / "fixture-basics"
PACK_ID = "org.adaptive-learning.fixture-basics"
PACK_VERSION = "0.1.0"
CORRECT = {
    "q-001": ["b"],
    "q-002": ["c"],
    "q-003": ["a", "b", "d"],
    "q-004": ["a"],
    "q-005": ["a", "b", "d"],
}


class CoreTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.user_data = Path(self.temporary.name) / "user-data"
        self.service = ApplicationService(self.user_data)
        self.tools = ToolContract(self.service)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        response = self.tools.invoke(tool, arguments)
        self.assertTrue(response["ok"], response)
        json.dumps(response)
        return response["result"]

    def error(self, tool: str, code: str, **arguments: Any) -> dict[str, Any]:
        response = self.tools.invoke(tool, arguments)
        self.assertFalse(response["ok"], response)
        self.assertEqual(response["error"]["code"], code)
        json.dumps(response)
        return response["error"]

    def initialize(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        installed = self.call("pack.install", source_path=str(FIXTURE_PACK))
        learner = self.call("learner.initialize", display_name="Alex")
        session = self.call(
            "study.start",
            learner_id=learner["learner_id"],
            pack_id=PACK_ID,
            pack_version=PACK_VERSION,
        )
        return installed, learner, session

    def next_and_submit(
        self,
        session_id: str,
        *,
        selections: list[str] | None = None,
        confidence: int = 3,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        presentation = self.call("study.next", session_id=session_id)
        question_id = presentation["question"]["question_id"]
        attempt = self.call(
            "study.submit",
            session_id=session_id,
            presentation_id=presentation["presentation_id"],
            selected_option_ids=selections if selections is not None else CORRECT[question_id],
            confidence=confidence,
        )
        return presentation, attempt


class VerticalSliceAcceptanceTests(CoreTestCase):
    def test_at_01_clean_install_and_health(self) -> None:
        health = self.call("system.health")
        self.assertEqual(health["schema_version"], "1")
        self.assertEqual(health["pack_format_versions"], ["0.1", "0.2"])
        self.assertEqual(health["capabilities"]["supported_pack_formats"], ["0.1", "0.2"])
        with self.service.storage.read() as connection:
            tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                )
            }
        self.assertEqual(tables, APPROVED_TABLES)

    def test_at_02_fixture_validate_install_and_conflict(self) -> None:
        validated = self.call("pack.validate", source_path=str(FIXTURE_PACK))
        self.assertEqual(validated["objective_count"], 2)
        self.assertEqual(validated["question_count"], 5)
        installed = self.call("pack.install", source_path=str(FIXTURE_PACK))
        repeated = self.call("pack.install", source_path=str(FIXTURE_PACK))
        self.assertTrue(installed["installed"])
        self.assertFalse(repeated["installed"])
        self.assertEqual(installed["pack_digest"], repeated["pack_digest"])

        changed = Path(self.temporary.name) / "changed-pack"
        shutil.copytree(FIXTURE_PACK, changed)
        manifest = changed / "pack.json"
        record = json.loads(manifest.read_text(encoding="utf-8"))
        record["title"] = "Changed in place"
        manifest.write_text(json.dumps(record), encoding="utf-8")
        self.error("pack.install", "PACK_VERSION_CONFLICT", source_path=str(changed))

        with self.service.storage.read() as connection:
            install_path = Path(
                connection.execute("SELECT install_path FROM installed_packs").fetchone()["install_path"]
            )
        self.assertTrue(install_path.is_relative_to(self.user_data / "packs"))
        self.assertNotEqual(install_path, FIXTURE_PACK)

    def test_at_03_learner_initialization_survives_restart(self) -> None:
        first = self.call("learner.initialize", display_name="Alex")
        restarted = ToolContract(ApplicationService(self.user_data))
        second_response = restarted.invoke("learner.initialize", {"display_name": "Different ignored name"})
        self.assertTrue(second_response["ok"])
        second = second_response["result"]
        self.assertEqual(first["learner_id"], second["learner_id"])
        self.assertEqual(second["display_name"], "Alex")
        self.assertFalse(second["created"])
        with self.service.storage.read() as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM learners").fetchone()[0], 1)

    def test_at_04_session_start_retry_and_new_after_completion(self) -> None:
        _, learner, session = self.initialize()
        repeated = self.call(
            "study.start",
            learner_id=learner["learner_id"],
            pack_id=PACK_ID,
            pack_version=PACK_VERSION,
        )
        self.assertEqual(repeated["session_id"], session["session_id"])
        self.assertTrue(repeated["resumed"])
        for _ in range(5):
            self.next_and_submit(session["session_id"])
        self.call("study.finish", session_id=session["session_id"])
        new_session = self.call(
            "study.start",
            learner_id=learner["learner_id"],
            pack_id=PACK_ID,
            pack_version=PACK_VERSION,
        )
        self.assertNotEqual(new_session["session_id"], session["session_id"])
        self.assertFalse(new_session["resumed"])

    def test_at_05_delivery_is_committed_without_answer_leakage(self) -> None:
        _, _, session = self.initialize()
        first = self.call("study.next", session_id=session["session_id"])
        serialized = json.dumps(first)
        self.assertNotIn("correct_option_ids", serialized)
        self.assertNotIn("explanation", serialized)
        with self.service.storage.read() as connection:
            row = connection.execute(
                "SELECT status FROM presentations WHERE presentation_id = ?",
                (first["presentation_id"],),
            ).fetchone()
        self.assertEqual(row["status"], "presented")
        repeated = self.call("study.next", session_id=session["session_id"])
        self.assertEqual(repeated, first)

    def test_at_06_exact_scoring_and_multiple_response_rules(self) -> None:
        _, _, session = self.initialize()
        _, single = self.next_and_submit(session["session_id"], selections=["b"])
        self.assertTrue(single["is_correct"])
        self.next_and_submit(session["session_id"], selections=["a"])
        multi_presentation = self.call("study.next", session_id=session["session_id"])
        one_option = self.call(
            "study.submit",
            session_id=session["session_id"],
            presentation_id=multi_presentation["presentation_id"],
            selected_option_ids=["a"],
            confidence=3,
        )
        self.assertFalse(one_option["is_correct"])

        with tempfile.TemporaryDirectory() as alternate_directory:
            alternate = ApplicationService(alternate_directory)
            tools = ToolContract(alternate)
            install = tools.invoke("pack.install", {"source_path": str(FIXTURE_PACK)})["result"]
            learner = tools.invoke("learner.initialize", {"display_name": "Alex"})["result"]
            other = tools.invoke(
                "study.start",
                {"learner_id": learner["learner_id"], "pack_id": install["pack_id"], "pack_version": install["pack_version"]},
            )["result"]
            for answer in (["b"], ["c"]):
                shown = tools.invoke("study.next", {"session_id": other["session_id"]})["result"]
                self.assertTrue(
                    tools.invoke(
                        "study.submit",
                        {
                            "session_id": other["session_id"],
                            "presentation_id": shown["presentation_id"],
                            "selected_option_ids": answer,
                            "confidence": 3,
                        },
                    )["ok"]
                )
            shown = tools.invoke("study.next", {"session_id": other["session_id"]})["result"]
            correct = tools.invoke(
                "study.submit",
                {
                    "session_id": other["session_id"],
                    "presentation_id": shown["presentation_id"],
                    "selected_option_ids": ["d", "a", "b"],
                    "confidence": 3,
                },
            )
            self.assertTrue(correct["result"]["is_correct"])
            shown = tools.invoke("study.next", {"session_id": other["session_id"]})["result"]
            tools.invoke(
                "study.submit",
                {
                    "session_id": other["session_id"],
                    "presentation_id": shown["presentation_id"],
                    "selected_option_ids": ["a"],
                    "confidence": 3,
                },
            )
            shown = tools.invoke("study.next", {"session_id": other["session_id"]})["result"]
            extra_distractor = tools.invoke(
                "study.submit",
                {
                    "session_id": other["session_id"],
                    "presentation_id": shown["presentation_id"],
                    "selected_option_ids": ["a", "b", "c", "d"],
                    "confidence": 3,
                },
            )
            self.assertFalse(extra_distractor["result"]["is_correct"])

        self.error(
            "study.submit",
            "ATTEMPT_CONFLICT",
            session_id=session["session_id"],
            presentation_id=multi_presentation["presentation_id"],
            selected_option_ids=["b"],
            confidence=3,
        )

    def test_additional_invalid_multiple_response_selections(self) -> None:
        _, _, session = self.initialize()
        self.next_and_submit(session["session_id"])
        self.next_and_submit(session["session_id"])
        presentation = self.call("study.next", session_id=session["session_id"])
        common = {"session_id": session["session_id"], "presentation_id": presentation["presentation_id"], "confidence": 3}
        self.error("study.submit", "INVALID_SELECTION", selected_option_ids=[], **common)
        self.error("study.submit", "INVALID_SELECTION", selected_option_ids=["a", "a"], **common)
        self.error("study.submit", "INVALID_SELECTION", selected_option_ids=["missing"], **common)

    def test_at_07_confidence_persists_and_does_not_change_scoring(self) -> None:
        _, _, session = self.initialize()
        _, low = self.next_and_submit(session["session_id"], confidence=1)
        _, high = self.next_and_submit(session["session_id"], confidence=5)
        self.assertTrue(low["is_correct"])
        self.assertTrue(high["is_correct"])
        with self.service.storage.read() as connection:
            values = [row["confidence"] for row in connection.execute("SELECT confidence FROM attempts ORDER BY submitted_at")]
        self.assertEqual(values, [1, 5])

    def test_at_08_process_restart_restores_and_rechecks_state(self) -> None:
        installed, learner, session = self.initialize()
        first, _ = self.next_and_submit(session["session_id"], confidence=5)
        second = self.call("study.next", session_id=session["session_id"])
        challenge = self.call(
            "question.challenge",
            session_id=session["session_id"],
            presentation_id=second["presentation_id"],
            reason="Ambiguous for this test.",
        )
        restarted_tools = ToolContract(ApplicationService(self.user_data))
        status = restarted_tools.invoke("study.status", {"learner_id": learner["learner_id"]})
        self.assertTrue(status["ok"])
        self.assertEqual(status["result"]["active_session"]["session_id"], session["session_id"])
        with self.service.storage.read() as connection:
            attempt = connection.execute(
                "SELECT confidence FROM attempts WHERE presentation_id = ?", (first["presentation_id"],)
            ).fetchone()
            persisted_challenge = connection.execute(
                "SELECT challenge_id FROM question_challenges WHERE challenge_id = ?", (challenge["challenge_id"],)
            ).fetchone()
        self.assertEqual(attempt["confidence"], 5)
        self.assertIsNotNone(persisted_challenge)
        self.assertEqual(installed["pack_digest"], self.call("pack.validate", source_path=str(FIXTURE_PACK))["pack_digest"])
        with self.service.storage.read() as connection:
            install_path = Path(connection.execute("SELECT install_path FROM installed_packs").fetchone()["install_path"])
        lesson = install_path / "lesson.md"
        lesson.write_text(lesson.read_text(encoding="utf-8") + "\nChanged after restart.\n", encoding="utf-8")
        changed_status = restarted_tools.invoke("study.status", {"learner_id": learner["learner_id"]})
        self.assertFalse(changed_status["ok"])
        self.assertEqual(changed_status["error"]["code"], "PACK_DIGEST_MISMATCH")

    def test_at_09_resume_uses_only_persisted_state(self) -> None:
        _, learner, session = self.initialize()
        outstanding = self.call("study.next", session_id=session["session_id"])
        restarted = ToolContract(ApplicationService(self.user_data))
        initialized = restarted.invoke("learner.initialize", {"display_name": "Alex"})
        status = restarted.invoke("study.status", {"learner_id": learner["learner_id"]})
        resumed = restarted.invoke("study.next", {"session_id": session["session_id"]})
        self.assertFalse(initialized["result"]["created"])
        self.assertEqual(status["result"]["active_session"]["outstanding_presentation_id"], outstanding["presentation_id"])
        self.assertEqual(resumed["result"], outstanding)

    def test_at_10_challenge_is_retry_safe(self) -> None:
        _, _, session = self.initialize()
        presentation = self.call("study.next", session_id=session["session_id"])
        first = self.call(
            "question.challenge",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            reason="The wording is ambiguous.",
        )
        repeated = self.call(
            "question.challenge",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            reason="A different retry reason is ignored.",
        )
        self.assertTrue(first["created"])
        self.assertFalse(repeated["created"])
        self.assertEqual(first["challenge_id"], repeated["challenge_id"])
        with self.service.storage.read() as connection:
            status = connection.execute(
                "SELECT status FROM presentations WHERE presentation_id = ?", (presentation["presentation_id"],)
            ).fetchone()["status"]
            count = connection.execute("SELECT count(*) FROM question_challenges").fetchone()[0]
        self.assertEqual(status, "challenged")
        self.assertEqual(count, 1)

    def test_at_11_quarantine_excludes_question_and_allows_finish(self) -> None:
        _, learner, session = self.initialize()
        challenged = self.call("study.next", session_id=session["session_id"])
        challenged_id = challenged["question"]["question_id"]
        self.call(
            "question.challenge",
            session_id=session["session_id"],
            presentation_id=challenged["presentation_id"],
            reason="Quarantine this fixture question.",
        )
        delivered = []
        for _ in range(4):
            presentation, _ = self.next_and_submit(session["session_id"])
            delivered.append(presentation["question"]["question_id"])
        self.assertNotIn(challenged_id, delivered)
        finished = self.call("study.finish", session_id=session["session_id"])
        self.assertEqual(finished["answered_count"], 4)

        new_session = self.call(
            "study.start",
            learner_id=learner["learner_id"],
            pack_id=PACK_ID,
            pack_version=PACK_VERSION,
        )
        next_ids = []
        for _ in range(4):
            presentation, _ = self.next_and_submit(new_session["session_id"])
            next_ids.append(presentation["question"]["question_id"])
        self.assertNotIn(challenged_id, next_ids)

    def test_at_12_attempt_is_immutable_and_retry_reconstructs_original_result(self) -> None:
        _, _, session = self.initialize()
        presentation, first = self.next_and_submit(session["session_id"], confidence=4)
        self.next_and_submit(session["session_id"])
        self.next_and_submit(session["session_id"])
        repeated = self.call(
            "study.submit",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            selected_option_ids=["b"],
            confidence=4,
        )
        self.assertEqual(repeated, first)
        self.error(
            "study.submit",
            "ATTEMPT_CONFLICT",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            selected_option_ids=["a"],
            confidence=4,
        )
        with self.service.storage.read() as connection:
            before_attempt = dict(connection.execute("SELECT * FROM attempts WHERE attempt_id = ?", (first["attempt_id"],)).fetchone())
            before_progress = [dict(row) for row in connection.execute("SELECT * FROM objective_progress ORDER BY objective_id")]
        self.call(
            "question.challenge",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            reason="Challenge after answering.",
        )
        with self.service.storage.read() as connection:
            after_attempt = dict(connection.execute("SELECT * FROM attempts WHERE attempt_id = ?", (first["attempt_id"],)).fetchone())
            after_progress = [dict(row) for row in connection.execute("SELECT * FROM objective_progress ORDER BY objective_id")]
            attempt_count = connection.execute("SELECT count(*) FROM attempts WHERE presentation_id = ?", (presentation["presentation_id"],)).fetchone()[0]
        self.assertEqual(before_attempt, after_attempt)
        self.assertEqual(before_progress, after_progress)
        self.assertEqual(attempt_count, 1)
        self.assertFalse(hasattr(self.service, "update_attempt"))
        self.assertFalse(hasattr(self.service, "delete_attempt"))


class AdditionalCoreRequirementsTests(CoreTestCase):
    def test_changed_question_digest_rejects_submission(self) -> None:
        _, _, session = self.initialize()
        presentation = self.call("study.next", session_id=session["session_id"])
        with self.service.storage.read() as connection:
            install_path = Path(connection.execute("SELECT install_path FROM installed_packs").fetchone()["install_path"])
        manifest = install_path / "pack.json"
        record = json.loads(manifest.read_text(encoding="utf-8"))
        record["questions"][0]["prompt"] = "Changed after presentation"
        manifest.write_text(json.dumps(record), encoding="utf-8")
        self.error(
            "study.submit",
            "QUESTION_DIGEST_MISMATCH",
            session_id=session["session_id"],
            presentation_id=presentation["presentation_id"],
            selected_option_ids=["b"],
            confidence=3,
        )

    def test_every_tool_success_response_is_json_serializable(self) -> None:
        responses = [self.tools.invoke("system.health", {})]
        responses.append(self.tools.invoke("pack.validate", {"source_path": str(FIXTURE_PACK)}))
        responses.append(self.tools.invoke("pack.install", {"source_path": str(FIXTURE_PACK)}))
        learner_response = self.tools.invoke("learner.initialize", {"display_name": "Alex"})
        responses.append(learner_response)
        learner = learner_response["result"]
        start_response = self.tools.invoke(
            "study.start",
            {"learner_id": learner["learner_id"], "pack_id": PACK_ID, "pack_version": PACK_VERSION},
        )
        responses.append(start_response)
        session_id = start_response["result"]["session_id"]
        first_next = self.tools.invoke("study.next", {"session_id": session_id})
        responses.append(first_next)
        presentation = first_next["result"]
        responses.append(
            self.tools.invoke(
                "study.submit",
                {
                    "session_id": session_id,
                    "presentation_id": presentation["presentation_id"],
                    "selected_option_ids": CORRECT[presentation["question"]["question_id"]],
                    "confidence": 3,
                },
            )
        )
        responses.append(self.tools.invoke("study.status", {"learner_id": learner["learner_id"]}))
        challenged = self.tools.invoke("study.next", {"session_id": session_id})["result"]
        responses.append(
            self.tools.invoke(
                "question.challenge",
                {"session_id": session_id, "presentation_id": challenged["presentation_id"], "reason": "Test reason"},
            )
        )
        for _ in range(3):
            shown = self.tools.invoke("study.next", {"session_id": session_id})["result"]
            self.tools.invoke(
                "study.submit",
                {
                    "session_id": session_id,
                    "presentation_id": shown["presentation_id"],
                    "selected_option_ids": CORRECT[shown["question"]["question_id"]],
                    "confidence": 3,
                },
            )
        responses.append(self.tools.invoke("study.finish", {"session_id": session_id}))
        self.assertEqual(len(responses), 10)
        for response in responses:
            self.assertTrue(response["ok"], response)
            json.dumps(response)

    def test_source_has_no_runtime_or_network_imports(self) -> None:
        forbidden_roots = {
            "anthropic",
            "boto3",
            "cohere",
            "google",
            "hermes",
            "http",
            "httpx",
            "mistralai",
            "openai",
            "requests",
            "smtplib",
            "socket",
            "urllib",
        }
        found: set[str] = set()
        for path in SOURCE_ROOT.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    found.update(alias.name for alias in node.names if alias.name.split(".")[0] in forbidden_roots)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.split(".")[0] in forbidden_roots:
                        found.add(node.module)
        self.assertEqual(found, set())
        project = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(project["project"]["dependencies"], [])

    def test_core_contains_no_fixture_or_pilot_subject_constants(self) -> None:
        source = "\n".join(path.read_text(encoding="utf-8").lower() for path in SOURCE_ROOT.glob("*.py"))
        for subject_term in ("fixture-basics", "org.adaptive-learning", "sap-c02", "amateur extra"):
            self.assertNotIn(subject_term, source)

    def test_tool_catalog_is_exact_and_request_envelope_is_strict(self) -> None:
        self.assertEqual(
            set(self.tools.tool_names),
            {
                "system.health",
                "learner.initialize",
                "pack.validate",
                "pack.install",
                "study.start",
                "study.next",
                "study.submit",
                "study.status",
                "study.finish",
                "question.challenge",
            },
        )
        response = self.tools.handle(
            {"contract_version": "0.1", "tool": "system.health", "arguments": {}}
        )
        self.assertTrue(response["ok"])
        json.dumps(response)

    def test_finish_rejects_an_unresolved_eligible_question(self) -> None:
        _, _, session = self.initialize()
        self.error("study.finish", "SESSION_NOT_FINISHABLE", session_id=session["session_id"])


if __name__ == "__main__":
    unittest.main()
