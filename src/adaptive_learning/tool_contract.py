"""Versioned JSON-compatible dispatch for the ten runtime-neutral tools."""

from __future__ import annotations

from typing import Any, Callable

from .application_service import ApplicationService
from .errors import LearningError


class ToolContract:
    contract_version = "0.1"

    def __init__(self, service: ApplicationService) -> None:
        self.service = service
        self._tools: dict[str, tuple[set[str], Callable[..., dict[str, Any]]]] = {
            "system.health": (set(), service.system_health),
            "learner.initialize": ({"display_name"}, service.learner_initialize),
            "pack.validate": ({"source_path"}, service.pack_validate),
            "pack.install": ({"source_path"}, service.pack_install),
            "study.start": ({"learner_id", "pack_id", "pack_version"}, service.study_start),
            "study.next": ({"session_id"}, service.study_next),
            "study.submit": (
                {"session_id", "presentation_id", "selected_option_ids", "confidence"},
                service.study_submit,
            ),
            "study.status": ({"learner_id"}, service.study_status),
            "study.finish": ({"session_id"}, service.study_finish),
            "question.challenge": ({"session_id", "presentation_id", "reason"}, service.question_challenge),
        }

    @property
    def tool_names(self) -> tuple[str, ...]:
        return tuple(self._tools)

    def handle(self, request: Any) -> dict[str, Any]:
        try:
            if not isinstance(request, dict) or set(request) != {"contract_version", "tool", "arguments"}:
                raise LearningError("INVALID_REQUEST", "The request envelope has invalid fields.")
            if request["contract_version"] != self.contract_version:
                raise LearningError("CONTRACT_VERSION_UNSUPPORTED", "contract_version must be exactly 0.1.")
            return self.invoke(request["tool"], request["arguments"])
        except LearningError as error:
            return {"ok": False, "error": error.as_dict()}

    def invoke(self, tool: Any, arguments: Any) -> dict[str, Any]:
        try:
            if not isinstance(tool, str) or tool not in self._tools:
                raise LearningError("TOOL_NOT_FOUND", "The requested tool is not part of contract 0.1.")
            if not isinstance(arguments, dict):
                raise LearningError("INVALID_ARGUMENTS", "arguments must be an object.")
            expected, operation = self._tools[tool]
            if set(arguments) != expected:
                argument_list = ", ".join(sorted(expected)) if expected else "(none)"
                raise LearningError(
                    "INVALID_ARGUMENTS",
                    f"{tool} requires exactly these arguments: {argument_list}.",
                )
            return {"ok": True, "result": operation(**arguments)}
        except LearningError as error:
            return {"ok": False, "error": error.as_dict()}
        except Exception:
            error = LearningError("INTERNAL_ERROR", "The core could not complete the operation.")
            return {"ok": False, "error": error.as_dict()}
