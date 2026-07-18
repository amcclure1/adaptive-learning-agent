"""Typed application errors suitable for the public JSON envelope."""

from __future__ import annotations

from typing import Any


class LearningError(Exception):
    """A deterministic, public-safe core error."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = details

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details is not None:
            result["details"] = self.details
        return result


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise LearningError(code, message)
