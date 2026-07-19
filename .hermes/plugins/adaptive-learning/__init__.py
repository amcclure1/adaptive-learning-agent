"""Hermes v0.18.2 adapter for the runtime-independent learning core."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


_PLUGIN_DIR = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _PLUGIN_DIR.parents[2]
_SOURCE_ROOT = _REPOSITORY_ROOT / "src"
if str(_SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SOURCE_ROOT))

from adaptive_learning.application_service import ApplicationService  # noqa: E402
from adaptive_learning.tool_contract import ToolContract  # noqa: E402


TOOL_OPERATIONS = {
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

_STRING = {"type": "string", "minLength": 1}


def _schema(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
    }


TOOL_SCHEMAS = {
    "ala_system_health": _schema(
        "ala_system_health",
        "Check the deterministic learning core, contract, schema, and supported pack format.",
        {},
        [],
    ),
    "ala_learner_initialize": _schema(
        "ala_learner_initialize",
        "Create the one local learner or retrieve the persisted learner.",
        {"display_name": _STRING},
        ["display_name"],
    ),
    "ala_pack_validate": _schema(
        "ala_pack_validate",
        "Validate an unpacked subject pack through the core without installing it.",
        {"source_path": _STRING},
        ["source_path"],
    ),
    "ala_pack_install": _schema(
        "ala_pack_install",
        "Validate and install an unpacked subject pack into the controlled pack store.",
        {"source_path": _STRING},
        ["source_path"],
    ),
    "ala_study_start": _schema(
        "ala_study_start",
        "Start or resume the learner's active deterministic study session and return its lesson.",
        {"learner_id": _STRING, "pack_id": _STRING, "pack_version": _STRING},
        ["learner_id", "pack_id", "pack_version"],
    ),
    "ala_study_next": _schema(
        "ala_study_next",
        "Persist and return the next eligible question without its answer or explanation.",
        {"session_id": _STRING},
        ["session_id"],
    ),
    "ala_study_submit": _schema(
        "ala_study_submit",
        "Submit selected option IDs and confidence for deterministic scoring and feedback.",
        {
            "session_id": _STRING,
            "presentation_id": _STRING,
            "selected_option_ids": {"type": "array", "items": _STRING},
            "confidence": {"type": "integer", "minimum": 1, "maximum": 5},
        },
        ["session_id", "presentation_id", "selected_option_ids", "confidence"],
    ),
    "ala_study_status": _schema(
        "ala_study_status",
        "Read persisted installed packs, active session state, and descriptive objective progress.",
        {"learner_id": _STRING},
        ["learner_id"],
    ),
    "ala_study_finish": _schema(
        "ala_study_finish",
        "Complete a session only when no eligible question remains unanswered.",
        {"session_id": _STRING},
        ["session_id"],
    ),
    "ala_question_challenge": _schema(
        "ala_question_challenge",
        "Persist a learner's reason for challenging a presented question and quarantine it.",
        {"session_id": _STRING, "presentation_id": _STRING, "reason": _STRING},
        ["session_id", "presentation_id", "reason"],
    ),
}


def _controlled_user_data_path() -> Path:
    """Return a fixed profile-local path that is never supplied by the model."""

    raw_home = os.environ.get("HERMES_HOME")
    if not raw_home:
        raise RuntimeError("HERMES_HOME is required for the adaptive-learning plugin")
    profile_home = Path(raw_home).expanduser().resolve(strict=False)
    user_data = (profile_home / "adaptive-learning" / "user-data").resolve(strict=False)
    user_data.relative_to(profile_home)
    return user_data


def _invalid_arguments(operation: str, expected: set[str]) -> str:
    names = ", ".join(sorted(expected)) if expected else "(none)"
    return json.dumps(
        {
            "ok": False,
            "error": {
                "code": "ADAPTER_INVALID_ARGUMENTS",
                "message": f"{operation} requires exactly these arguments: {names}.",
            },
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _serialize_operation(contract: ToolContract, operation: str, expected: set[str], params: Any) -> str:
    """Validate the adapter boundary and serialize one core operation safely."""

    if not isinstance(params, dict) or set(params) != expected:
        return _invalid_arguments(operation, expected)
    try:
        result = contract.invoke(operation, params)
        return json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return json.dumps(
            {
                "ok": False,
                "error": {
                    "code": "ADAPTER_INTERNAL_ERROR",
                    "message": "The Hermes adapter could not complete the operation.",
                },
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )


def _handler(contract: ToolContract, operation: str, expected: set[str]):
    def handle(params: Any, **_: Any) -> str:
        return _serialize_operation(contract, operation, expected, params)

    return handle


def register(ctx: Any) -> None:
    """Register exactly the ten version-0.1 runtime-neutral operations."""

    contract = ToolContract(ApplicationService(_controlled_user_data_path()))
    for tool_name, operation in TOOL_OPERATIONS.items():
        schema = TOOL_SCHEMAS[tool_name]
        expected = set(schema["parameters"]["required"])
        ctx.register_tool(
            name=tool_name,
            toolset="adaptive_learning",
            schema=schema,
            handler=_handler(contract, operation, expected),
            description=schema["description"],
        )
    ctx.register_skill(
        "adaptive-learning",
        _REPOSITORY_ROOT / "skills" / "adaptive-learning" / "SKILL.md",
        "Study installed packs through deterministic Adaptive Learning Agent tools with concise sourced provenance.",
    )
