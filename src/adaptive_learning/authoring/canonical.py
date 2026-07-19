"""Canonical authored-content bytes and domain-separated digests."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import PurePosixPath
from typing import Any

from adaptive_learning.errors import LearningError


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, bool) or value is None or isinstance(value, int):
        return value
    if isinstance(value, float):
        raise LearningError("AUTHORING_CANONICALIZATION_FAILED", "Floating-point JSON numbers are not supported.")
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise LearningError("AUTHORING_CANONICALIZATION_FAILED", "JSON object keys must be strings.")
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized:
                raise LearningError("AUTHORING_CANONICALIZATION_FAILED", "Unicode normalization produced a duplicate object key.")
            normalized[normalized_key] = _normalize(item)
        return normalized
    raise LearningError("AUTHORING_CANONICALIZATION_FAILED", f"Unsupported JSON value type: {type(value).__name__}.")


def canonical_json_bytes(value: Any) -> bytes:
    """Return strict UTF-8 canonical JSON without a trailing newline."""

    return json.dumps(
        _normalize(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_json_file_bytes(value: Any) -> bytes:
    """Return canonical JSON with the repository's one-trailing-LF file policy."""

    return canonical_json_bytes(value) + b"\n"


def normalize_markdown(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return normalized.rstrip("\n") + "\n"


def portable_relative_path(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    if normalized != value or "\\" in value or ":" in value:
        raise LearningError("AUTHORING_PATH_INVALID", "Paths must be NFC-normalized POSIX relative paths.")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise LearningError("AUTHORING_PATH_INVALID", "Paths must remain inside the authoring workspace.")
    return path.as_posix()


def _frame(value: bytes | str) -> bytes:
    encoded = value.encode("utf-8") if isinstance(value, str) else value
    return len(encoded).to_bytes(8, "big") + encoded


def artifact_digest(record: dict[str, Any], *, markdown_path: str | None = None, markdown: str | None = None) -> str:
    """Digest a record according to the accepted 0.3B authoring contract."""

    artifact_type = record.get("artifact_type")
    schema_version = record.get("schema_version")
    if not isinstance(artifact_type, str) or not isinstance(schema_version, str):
        raise LearningError("AUTHORING_SCHEMA_INVALID", "artifact_type and schema_version are required before digesting.")
    digest_record = dict(record)
    digest_record.pop("canonical_digest", None)
    if artifact_type == "validation_report":
        digest_record.pop("output_digest", None)
    payload = _frame("adaptive-learning-authoring") + _frame(artifact_type) + _frame(schema_version)
    payload += _frame(canonical_json_bytes(digest_record))
    if artifact_type == "lesson":
        if markdown_path is None or markdown is None:
            raise LearningError("AUTHORING_SCHEMA_INVALID", "Lesson digests require the Markdown path and content.")
        payload += _frame(portable_relative_path(markdown_path))
        payload += _frame(normalize_markdown(markdown).encode("utf-8"))
    return hashlib.sha256(payload).hexdigest()


def markdown_digest(markdown: str) -> str:
    return hashlib.sha256(normalize_markdown(markdown).encode("utf-8")).hexdigest()


def digest_file_set(files: dict[str, bytes]) -> str:
    payload = _frame(b"ala-authored-content\0compiler_output\0v1")
    for path in sorted(files, key=lambda item: item.encode("utf-8")):
        payload += _frame(portable_relative_path(path)) + _frame(files[path])
    return hashlib.sha256(payload).hexdigest()
