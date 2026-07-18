from __future__ import annotations

import ast
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_FILE = REPOSITORY_ROOT / ".hermes" / "plugins" / "adaptive-learning" / "__init__.py"
FIXTURE = REPOSITORY_ROOT / "packs" / "fixture-basics"


def load_plugin():
    spec = importlib.util.spec_from_file_location("ala_hermes_plugin_test", PLUGIN_FILE)
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load the project-local Hermes plugin")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeContext:
    def __init__(self) -> None:
        self.tools: dict[str, dict[str, Any]] = {}

    def register_tool(self, **registration: Any) -> None:
        self.tools[registration["name"]] = registration


class HermesPluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.previous_home = os.environ.get("HERMES_HOME")
        os.environ["HERMES_HOME"] = self.temporary.name
        self.plugin = load_plugin()
        self.context = FakeContext()
        self.plugin.register(self.context)

    def tearDown(self) -> None:
        if self.previous_home is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = self.previous_home
        self.temporary.cleanup()

    def call(self, name: str, **arguments: Any) -> dict[str, Any]:
        raw = self.context.tools[name]["handler"](arguments)
        result = json.loads(raw)
        self.assertIsInstance(result, dict)
        return result

    def test_registers_exact_schemas_and_operation_mappings(self) -> None:
        self.assertEqual(set(self.context.tools), set(self.plugin.TOOL_OPERATIONS))
        self.assertEqual(len(self.context.tools), 10)
        expected_operations = {
            "ala_system_health": "system.health",
            "ala_learner_initialize": "learner.initialize",
            "ala_pack_validate": "pack.validate",
            "ala_pack_install": "pack.install",
            "ala_study_start": "study.start",
            "ala_study_next": "study.next",
            "ala_study_submit": "study.submit",
            "ala_study_status": "study.status",
            "ala_study_finish": "study.finish",
            "ala_question_challenge": "question.challenge",
        }
        self.assertEqual(self.plugin.TOOL_OPERATIONS, expected_operations)
        for name, registration in self.context.tools.items():
            self.assertEqual(registration["toolset"], "adaptive_learning")
            self.assertEqual(registration["schema"]["name"], name)
            self.assertFalse(registration["schema"]["parameters"]["additionalProperties"])

    def test_every_handler_runs_the_fixture_flow_and_returns_json(self) -> None:
        self.assertTrue(self.call("ala_system_health")["ok"])
        learner = self.call("ala_learner_initialize", display_name="Plugin Test")["result"]
        self.assertTrue(self.call("ala_pack_validate", source_path=str(FIXTURE))["ok"])
        installed = self.call("ala_pack_install", source_path=str(FIXTURE))["result"]
        started = self.call(
            "ala_study_start",
            learner_id=learner["learner_id"],
            pack_id=installed["pack_id"],
            pack_version=installed["pack_version"],
        )["result"]
        session_id = started["session_id"]
        self.assertTrue(self.call("ala_study_status", learner_id=learner["learner_id"])["ok"])

        first = self.call("ala_study_next", session_id=session_id)["result"]
        self.assertNotIn("correct_option_ids", first)
        self.assertNotIn("explanation", first)
        self.assertNotIn("correct_option_ids", first["question"])
        self.assertNotIn("explanation", first["question"])
        self.assertTrue(
            self.call(
                "ala_study_submit",
                session_id=session_id,
                presentation_id=first["presentation_id"],
                selected_option_ids=[first["question"]["options"][0]["id"]],
                confidence=3,
            )["ok"]
        )

        challenged = self.call("ala_study_next", session_id=session_id)["result"]
        self.assertTrue(
            self.call(
                "ala_question_challenge",
                session_id=session_id,
                presentation_id=challenged["presentation_id"],
                reason="The wording is ambiguous in this test.",
            )["ok"]
        )

        while True:
            next_result = self.call("ala_study_next", session_id=session_id)
            if not next_result["ok"]:
                self.assertEqual(next_result["error"]["code"], "NO_ELIGIBLE_QUESTION")
                break
            presentation = next_result["result"]
            self.assertTrue(
                self.call(
                    "ala_study_submit",
                    session_id=session_id,
                    presentation_id=presentation["presentation_id"],
                    selected_option_ids=[presentation["question"]["options"][0]["id"]],
                    confidence=2,
                )["ok"]
            )
        self.assertEqual(self.call("ala_study_finish", session_id=session_id)["result"]["status"], "completed")

    def test_adapter_errors_are_structured_and_safe(self) -> None:
        wrong = self.call("ala_system_health", unexpected=True)
        self.assertEqual(wrong["error"]["code"], "ADAPTER_INVALID_ARGUMENTS")

        class FailingContract:
            def invoke(self, operation: str, arguments: dict[str, Any]) -> dict[str, Any]:
                raise RuntimeError("private detail")

        raw = self.plugin._serialize_operation(FailingContract(), "system.health", set(), {})
        failure = json.loads(raw)
        self.assertEqual(failure["error"]["code"], "ADAPTER_INTERNAL_ERROR")
        self.assertNotIn("private detail", raw)

    def test_adapter_does_not_import_storage_internals(self) -> None:
        tree = ast.parse(PLUGIN_FILE.read_text(encoding="utf-8"))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        self.assertFalse(any(name.endswith(".storage") or name == "sqlite3" for name in imported))


if __name__ == "__main__":
    unittest.main()
