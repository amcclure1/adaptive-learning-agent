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
    if pack.format_version == "0.1":
        lesson_bytes = normalize_lesson(pack.lesson_markdown).encode("utf-8")
        payload = _frame(record_bytes) + _frame(lesson_bytes)
    else:
        payload = _frame(b"adaptive-learning-pack-format-0.2") + _frame(record_bytes)
        for lesson in pack.lessons:
            payload += _frame(lesson.path.encode("utf-8"))
            payload += _frame(normalize_lesson(lesson.markdown).encode("utf-8"))
        if pack.notice_markdown is not None:
            payload += _frame(b"NOTICE.md")
            payload += _frame(normalize_lesson(pack.notice_markdown).encode("utf-8"))
    return hashlib.sha256(payload).hexdigest()


def _frame(value: bytes) -> bytes:
    return len(value).to_bytes(8, "big") + value


def digest_question(question: Question) -> str:
    return hashlib.sha256(canonical_json_bytes(question.as_record())).hexdigest()
