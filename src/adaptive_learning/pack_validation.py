"""Strict parsing and validation for unpacked format-0.1 packs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import LearningError
from .pack_digest import normalize_lesson, normalize_value
from .pack_model import Objective, Option, Pack, Question

TOP_FIELDS = {"format_version", "pack_id", "version", "title", "lesson", "objectives", "questions"}
OBJECTIVE_FIELDS = {"id", "title"}
QUESTION_FIELDS = {"id", "type", "objective_id", "prompt", "options", "correct_option_ids", "explanation"}
OPTION_FIELDS = {"id", "text"}
QUESTION_TYPES = {"single_response", "multiple_response"}


def _fail(message: str) -> None:
    raise LearningError("PACK_VALIDATION_FAILED", message)


def _record(value: Any, label: str, fields: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"{label} must be an object.")
    unknown = set(value) - fields
    missing = fields - set(value)
    if unknown:
        _fail(f"{label} has unknown fields: {', '.join(sorted(unknown))}.")
    if missing:
        _fail(f"{label} is missing fields: {', '.join(sorted(missing))}.")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be a non-empty string.")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(f"{label} must be an array.")
    return value


def _resolve_source(source_path: str | Path) -> Path:
    try:
        path = Path(source_path).expanduser().resolve(strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        raise LearningError("PACK_PATH_INVALID", "The pack source path is invalid.") from exc
    if not path.is_dir():
        raise LearningError("PACK_PATH_INVALID", "The pack source path must be a directory.")
    return path


def load_pack(source_path: str | Path) -> Pack:
    source = _resolve_source(source_path)
    manifest_path = source / "pack.json"
    if not manifest_path.is_file():
        _fail("pack.json is required.")
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LearningError("PACK_VALIDATION_FAILED", "pack.json must be valid UTF-8 JSON.") from exc
    normalized = normalize_value(raw)
    top = _record(normalized, "pack", TOP_FIELDS)

    format_version = _text(top["format_version"], "format_version")
    if format_version != "0.1":
        _fail("format_version must be exactly 0.1.")
    pack_id = _text(top["pack_id"], "pack_id")
    version = _text(top["version"], "version")
    title = _text(top["title"], "title")
    lesson_name = _text(top["lesson"], "lesson")

    lesson_relative = Path(lesson_name)
    if lesson_relative.is_absolute() or len(lesson_relative.parts) != 1 or lesson_relative.suffix.lower() != ".md":
        _fail("lesson must be one relative Markdown file name.")
    lesson_path = (source / lesson_relative).resolve(strict=False)
    try:
        lesson_path.relative_to(source)
    except ValueError:
        _fail("lesson must remain inside the pack directory.")
    if not lesson_path.is_file():
        _fail("The referenced lesson file does not exist.")
    try:
        lesson_markdown = normalize_lesson(lesson_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        raise LearningError("PACK_VALIDATION_FAILED", "The lesson must be readable UTF-8 Markdown.") from exc

    actual_entries = {item.name for item in source.iterdir()}
    expected_entries = {"pack.json", lesson_relative.name}
    if actual_entries != expected_entries:
        _fail("A format-0.1 pack may contain only pack.json and its lesson file.")

    objective_values = _list(top["objectives"], "objectives")
    if not objective_values:
        _fail("At least one objective is required.")
    objectives: list[Objective] = []
    objective_ids: set[str] = set()
    for index, value in enumerate(objective_values):
        record = _record(value, f"objectives[{index}]", OBJECTIVE_FIELDS)
        objective_id = _text(record["id"], f"objectives[{index}].id")
        if objective_id in objective_ids:
            _fail(f"Duplicate objective ID: {objective_id}.")
        objective_ids.add(objective_id)
        objectives.append(Objective(objective_id, _text(record["title"], f"objectives[{index}].title")))

    question_values = _list(top["questions"], "questions")
    if not question_values:
        _fail("At least one question is required.")
    questions: list[Question] = []
    question_ids: set[str] = set()
    for q_index, value in enumerate(question_values):
        record = _record(value, f"questions[{q_index}]", QUESTION_FIELDS)
        question_id = _text(record["id"], f"questions[{q_index}].id")
        if question_id in question_ids:
            _fail(f"Duplicate question ID: {question_id}.")
        question_ids.add(question_id)
        question_type = _text(record["type"], f"questions[{q_index}].type")
        if question_type not in QUESTION_TYPES:
            _fail(f"Unknown question type: {question_type}.")
        objective_id = _text(record["objective_id"], f"questions[{q_index}].objective_id")
        if objective_id not in objective_ids:
            _fail(f"Question {question_id} references an unknown objective.")

        option_values = _list(record["options"], f"questions[{q_index}].options")
        if len(option_values) < 2:
            _fail(f"Question {question_id} must have at least two options.")
        options: list[Option] = []
        option_ids: set[str] = set()
        for o_index, option_value in enumerate(option_values):
            option_record = _record(option_value, f"questions[{q_index}].options[{o_index}]", OPTION_FIELDS)
            option_id = _text(option_record["id"], f"questions[{q_index}].options[{o_index}].id")
            if option_id in option_ids:
                _fail(f"Question {question_id} has duplicate option ID {option_id}.")
            option_ids.add(option_id)
            options.append(Option(option_id, _text(option_record["text"], f"questions[{q_index}].options[{o_index}].text")))

        correct_values = _list(record["correct_option_ids"], f"questions[{q_index}].correct_option_ids")
        if not correct_values or any(not isinstance(item, str) or not item for item in correct_values):
            _fail(f"Question {question_id} must have non-empty correct option IDs.")
        if len(set(correct_values)) != len(correct_values):
            _fail(f"Question {question_id} has duplicate correct option IDs.")
        if not set(correct_values) <= option_ids:
            _fail(f"Question {question_id} has an unknown correct option ID.")
        if question_type == "single_response" and len(correct_values) != 1:
            _fail(f"Single-response question {question_id} must have exactly one correct option.")
        if question_type == "multiple_response":
            if len(correct_values) < 2 or len(correct_values) >= len(option_ids):
                _fail(f"Multiple-response question {question_id} needs at least two correct options and one distractor.")

        questions.append(
            Question(
                question_id=question_id,
                question_type=question_type,
                objective_id=objective_id,
                prompt=_text(record["prompt"], f"questions[{q_index}].prompt"),
                options=tuple(options),
                correct_option_ids=tuple(correct_values),
                explanation=_text(record["explanation"], f"questions[{q_index}].explanation"),
            )
        )

    return Pack(
        source_path=source,
        format_version=format_version,
        pack_id=pack_id,
        version=version,
        title=title,
        lesson_name=lesson_name,
        lesson_markdown=lesson_markdown,
        objectives=tuple(objectives),
        questions=tuple(questions),
        normalized_record=normalized,
    )
