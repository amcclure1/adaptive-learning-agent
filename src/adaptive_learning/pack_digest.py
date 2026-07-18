"""Canonical pack and question digests."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any

from .pack_model import Pack, Question


def normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {normalize_value(key): normalize_value(item) for key, item in value.items()}
    return value


def canonical_json_bytes(value: Any) -> bytes:
    normalized = normalize_value(value)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def normalize_lesson(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return normalized.rstrip("\n") + "\n"


def digest_pack(pack: Pack) -> str:
    record_bytes = canonical_json_bytes(pack.normalized_record)
    lesson_bytes = normalize_lesson(pack.lesson_markdown).encode("utf-8")
    payload = (
        len(record_bytes).to_bytes(8, "big")
        + record_bytes
        + len(lesson_bytes).to_bytes(8, "big")
        + lesson_bytes
    )
    return hashlib.sha256(payload).hexdigest()


def digest_question(question: Question) -> str:
    return hashlib.sha256(canonical_json_bytes(question.as_record())).hexdigest()
