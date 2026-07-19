"""Strict parsing and validation for unpacked format-0.1 packs."""

from __future__ import annotations

import json
import re
import stat
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import LearningError
from .pack_digest import normalize_lesson, normalize_value
from .pack_model import Citation, Lesson, Objective, Option, Pack, Question, Source

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


def _load_v01(source_path: str | Path) -> Pack:
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


V02_TOP_REQUIRED = {
    "format_version", "pack_id", "version", "title", "language", "assessment_pool",
    "rights", "sources", "objectives", "lessons", "questions", "approval",
}
V02_TOP_OPTIONAL = {"tags"}
POOL_REQUIRED = {
    "id", "title", "publisher", "effective_from", "effective_through", "source_id",
    "errata_revision", "errata_source_id", "withdrawn_official_question_ids",
}
POOL_OPTIONAL = {"superseded_official_question_ids"}
SOURCE_REQUIRED = {"id", "type", "title", "publisher", "url", "retrieved_on", "snapshot_retained", "rights_id"}
SOURCE_OPTIONAL = {"effective_from", "effective_through", "revision", "locator", "content_sha256"}
LESSON_FIELDS = {"id", "title", "path", "objective_ids", "rights_id", "citations"}
CITATION_FIELDS = {"source_id", "locator"}
APPROVAL_REQUIRED = {"status", "reviewed_by", "reviewed_at", "review_scope"}
APPROVAL_OPTIONAL = {"notes"}
OFFICIAL_FIELDS = QUESTION_FIELDS | {
    "origin", "official_question_id", "pool_id", "source_question_ref", "tags",
    "question_rights_id", "explanation_rights_id", "explanation_citations",
}
GENERATED_FIELDS = QUESTION_FIELDS | {
    "origin", "tags", "question_rights_id", "explanation_rights_id", "explanation_citations",
}
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
LANGUAGE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
TAG = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SOURCE_TYPES = {"official_question_pool", "official_errata", "regulation", "official_guidance"}
HTTPS_URL = re.compile(r"^https://[^\s/]+(?:/[^\s]*)?$")
REVIEW_SCOPES = {
    "official_wording", "option_ordering", "answer_keys", "official_ids", "lessons",
    "explanations", "citations", "rights_metadata", "pool_and_errata_metadata",
}


def _strict_record(value: Any, label: str, required: set[str], optional: set[str] = frozenset()) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"{label} must be an object.")
    unknown = set(value) - required - optional
    missing = required - set(value)
    if unknown:
        _fail(f"{label} has unknown fields: {', '.join(sorted(unknown))}.")
    if missing:
        _fail(f"{label} is missing fields: {', '.join(sorted(missing))}.")
    return value


def _identifier(value: Any, label: str) -> str:
    text = _text(value, label)
    if not IDENTIFIER.fullmatch(text):
        _fail(f"{label} must use the portable identifier grammar.")
    return text


def _date(value: Any, label: str) -> str:
    text = _text(value, label)
    try:
        date.fromisoformat(text)
    except ValueError:
        _fail(f"{label} must be an ISO 8601 calendar date.")
    return text


def _string_list(value: Any, label: str, *, nonempty: bool = False) -> tuple[str, ...]:
    values = _list(value, label)
    if nonempty and not values:
        _fail(f"{label} must not be empty.")
    result = tuple(_text(item, f"{label}[{index}]") for index, item in enumerate(values))
    if len(set(result)) != len(result):
        _fail(f"{label} must not contain duplicates.")
    return result


def _citation(value: Any, label: str) -> Citation:
    record = _strict_record(value, label, CITATION_FIELDS)
    locator = _text(record["locator"], f"{label}.locator")
    if len(locator) > 300 or any(ord(char) < 32 for char in locator) or "://" in locator:
        _fail(f"{label}.locator must be a concise, non-URL source locator.")
    return Citation(_identifier(record["source_id"], f"{label}.source_id"), locator)


def _citations(value: Any, label: str, *, nonempty: bool = True) -> tuple[Citation, ...]:
    values = _list(value, label)
    if nonempty and not values:
        _fail(f"{label} must not be empty.")
    return tuple(_citation(item, f"{label}[{index}]") for index, item in enumerate(values))


def _safe_pack_file(source: Path, value: Any, label: str) -> tuple[str, Path]:
    name = _text(value, label)
    if "\\" in name:
        _fail(f"{label} must be a POSIX relative path.")
    relative = PurePosixPath(name)
    if relative.is_absolute() or not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        _fail(f"{label} must remain inside the pack directory.")
    if relative.suffix.lower() != ".md":
        _fail(f"{label} must reference a Markdown file.")
    path = source.joinpath(*relative.parts)
    cursor = source
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and (cursor.is_symlink() or bool(cursor.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT) if hasattr(cursor.stat(), "st_file_attributes") else cursor.is_symlink()):
            _fail(f"{label} must not traverse links or reparse points.")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(source)
    except (OSError, RuntimeError, ValueError) as exc:
        raise LearningError("PACK_VALIDATION_FAILED", f"{label} does not name a readable pack file.") from exc
    if not resolved.is_file():
        _fail(f"{label} must reference a regular file.")
    return relative.as_posix(), resolved


def _parse_options(record: dict[str, Any], q_index: int, question_id: str) -> tuple[tuple[Option, ...], tuple[str, ...]]:
    option_values = _list(record["options"], f"questions[{q_index}].options")
    if len(option_values) < 2:
        _fail(f"Question {question_id} must have at least two options.")
    options: list[Option] = []
    option_ids: set[str] = set()
    for index, value in enumerate(option_values):
        item = _strict_record(value, f"questions[{q_index}].options[{index}]", OPTION_FIELDS)
        option_id = _identifier(item["id"], f"questions[{q_index}].options[{index}].id")
        if option_id in option_ids:
            _fail(f"Question {question_id} has duplicate option ID {option_id}.")
        option_ids.add(option_id)
        options.append(Option(option_id, _text(item["text"], f"questions[{q_index}].options[{index}].text")))
    correct = _string_list(record["correct_option_ids"], f"questions[{q_index}].correct_option_ids", nonempty=True)
    if not set(correct) <= option_ids:
        _fail(f"Question {question_id} has an unknown correct option ID.")
    question_type = _text(record["type"], f"questions[{q_index}].type")
    if question_type not in QUESTION_TYPES:
        _fail(f"Unknown question type: {question_type}.")
    if question_type == "single_response" and len(correct) != 1:
        _fail(f"Single-response question {question_id} must have exactly one correct option.")
    if question_type == "multiple_response" and (len(correct) < 2 or len(correct) >= len(options)):
        _fail(f"Multiple-response question {question_id} needs at least two correct options and one distractor.")
    return tuple(options), correct


def _load_v02(source: Path, normalized: dict[str, Any]) -> Pack:
    top = _strict_record(normalized, "pack", V02_TOP_REQUIRED, V02_TOP_OPTIONAL)
    pack_id = _identifier(top["pack_id"], "pack_id")
    version = _text(top["version"], "version")
    title = _text(top["title"], "title")
    language = _text(top["language"], "language")
    if not LANGUAGE.fullmatch(language):
        _fail("language must use the conservative BCP 47-shaped grammar.")
    tags = _string_list(top.get("tags", []), "tags")
    if any(not TAG.fullmatch(tag) for tag in tags):
        _fail("tags must be normalized lowercase topic labels.")

    pool = _strict_record(top["assessment_pool"], "assessment_pool", POOL_REQUIRED, POOL_OPTIONAL)
    pool_id = _identifier(pool["id"], "assessment_pool.id")
    for field in ("title", "publisher", "errata_revision"):
        _text(pool[field], f"assessment_pool.{field}")
    effective_from = _date(pool["effective_from"], "assessment_pool.effective_from")
    effective_through = _date(pool["effective_through"], "assessment_pool.effective_through")
    if effective_from > effective_through:
        _fail("assessment_pool effective dates are reversed.")
    pool_source_id = _identifier(pool["source_id"], "assessment_pool.source_id")
    errata_source_id = _identifier(pool["errata_source_id"], "assessment_pool.errata_source_id")
    withdrawn = set(_string_list(pool["withdrawn_official_question_ids"], "assessment_pool.withdrawn_official_question_ids"))
    superseded = set(_string_list(pool.get("superseded_official_question_ids", []), "assessment_pool.superseded_official_question_ids"))

    rights_values = _list(top["rights"], "rights")
    if not rights_values:
        _fail("rights must not be empty.")
    rights: list[dict[str, object]] = []
    rights_by_id: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(rights_values):
        if not isinstance(value, dict):
            _fail(f"rights[{index}] must be an object.")
        status = value.get("status")
        fields = {
            "public_domain": {"id", "scope", "status", "basis_source_id", "covered_material"},
            "licensed": {"id", "scope", "status", "license_expression", "copyright_holder"},
            "reference_only": {"id", "scope", "status"},
        }.get(status)
        if fields is None:
            _fail(f"rights[{index}].status is unsupported.")
        item = _strict_record(value, f"rights[{index}]", fields)
        rights_id = _identifier(item["id"], f"rights[{index}].id")
        if rights_id in rights_by_id:
            _fail(f"Duplicate rights ID: {rights_id}.")
        _text(item["scope"], f"rights[{index}].scope")
        if status == "public_domain":
            _identifier(item["basis_source_id"], f"rights[{index}].basis_source_id")
            _string_list(item["covered_material"], f"rights[{index}].covered_material", nonempty=True)
        elif status == "licensed":
            _text(item["license_expression"], f"rights[{index}].license_expression")
            _text(item["copyright_holder"], f"rights[{index}].copyright_holder")
        rights_by_id[rights_id] = item
        rights.append(item)

    source_values = _list(top["sources"], "sources")
    if not source_values:
        _fail("sources must not be empty.")
    sources: list[Source] = []
    source_ids: set[str] = set()
    for index, value in enumerate(source_values):
        item = _strict_record(value, f"sources[{index}]", SOURCE_REQUIRED, SOURCE_OPTIONAL)
        source_id = _identifier(item["id"], f"sources[{index}].id")
        if source_id in source_ids:
            _fail(f"Duplicate source ID: {source_id}.")
        source_ids.add(source_id)
        source_type = _identifier(item["type"], f"sources[{index}].type")
        if source_type not in SOURCE_TYPES:
            _fail(f"sources[{index}].type is unsupported.")
        url = _text(item["url"], f"sources[{index}].url")
        if not HTTPS_URL.fullmatch(url):
            _fail(f"sources[{index}].url must be an absolute HTTPS URL.")
        retrieved_on = _date(item["retrieved_on"], f"sources[{index}].retrieved_on")
        rights_id = _identifier(item["rights_id"], f"sources[{index}].rights_id")
        if rights_id not in rights_by_id:
            _fail(f"Source {source_id} references unknown rights.")
        if not isinstance(item["snapshot_retained"], bool):
            _fail(f"sources[{index}].snapshot_retained must be boolean.")
        digest = item.get("content_sha256")
        if item["snapshot_retained"]:
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                _fail(f"sources[{index}].content_sha256 is required for a retained snapshot and must be a lowercase SHA-256 digest.")
        elif digest is not None:
            _fail(f"sources[{index}].content_sha256 is forbidden when snapshot_retained is false.")
        for field in ("effective_from", "effective_through"):
            if field in item:
                _date(item[field], f"sources[{index}].{field}")
        if item.get("effective_from") and item.get("effective_through") and item["effective_from"] > item["effective_through"]:
            _fail(f"sources[{index}] effective dates are reversed.")
        if source_type in {"official_question_pool", "official_errata"} and "revision" not in item:
            _fail(f"sources[{index}].revision is required for pool and errata sources.")
        sources.append(Source(source_id, source_type, _text(item["title"], f"sources[{index}].title"), _text(item["publisher"], f"sources[{index}].publisher"), url, retrieved_on, rights_id, item.get("revision"), digest))

    if pool_source_id not in source_ids or errata_source_id not in source_ids:
        _fail("assessment_pool source references must resolve.")
    source_by_id = {item.source_id: item for item in sources}
    if source_by_id[pool_source_id].source_type != "official_question_pool":
        _fail("assessment_pool.source_id must identify an official question-pool source.")
    if source_by_id[errata_source_id].source_type != "official_errata":
        _fail("assessment_pool.errata_source_id must identify an official errata source.")
    for item in rights:
        if item["status"] == "public_domain" and item["basis_source_id"] not in source_ids:
            _fail(f"Rights {item['id']} has an unknown basis source.")

    objective_values = _list(top["objectives"], "objectives")
    if not objective_values:
        _fail("At least one objective is required.")
    objectives: list[Objective] = []
    objective_ids: set[str] = set()
    for index, value in enumerate(objective_values):
        item = _strict_record(value, f"objectives[{index}]", OBJECTIVE_FIELDS)
        objective_id = _identifier(item["id"], f"objectives[{index}].id")
        if objective_id in objective_ids:
            _fail(f"Duplicate objective ID: {objective_id}.")
        objective_ids.add(objective_id)
        objectives.append(Objective(objective_id, _text(item["title"], f"objectives[{index}].title")))

    lesson_values = _list(top["lessons"], "lessons")
    if not lesson_values:
        _fail("At least one lesson is required.")
    lessons: list[Lesson] = []
    lesson_ids: set[str] = set()
    lesson_paths: set[str] = set()
    taught: set[str] = set()
    for index, value in enumerate(lesson_values):
        item = _strict_record(value, f"lessons[{index}]", LESSON_FIELDS)
        lesson_id = _identifier(item["id"], f"lessons[{index}].id")
        if lesson_id in lesson_ids:
            _fail(f"Duplicate lesson ID: {lesson_id}.")
        lesson_ids.add(lesson_id)
        path_name, path = _safe_pack_file(source, item["path"], f"lessons[{index}].path")
        if path_name in lesson_paths:
            _fail(f"Duplicate lesson path: {path_name}.")
        lesson_paths.add(path_name)
        linked_objectives = _string_list(item["objective_ids"], f"lessons[{index}].objective_ids", nonempty=True)
        if not set(linked_objectives) <= objective_ids:
            _fail(f"Lesson {lesson_id} references an unknown objective.")
        taught.update(linked_objectives)
        rights_id = _identifier(item["rights_id"], f"lessons[{index}].rights_id")
        if rights_id not in rights_by_id or rights_by_id[rights_id]["status"] != "licensed":
            _fail(f"Lesson {lesson_id} must use licensed rights.")
        citations = _citations(item["citations"], f"lessons[{index}].citations")
        try:
            markdown = normalize_lesson(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            raise LearningError("PACK_VALIDATION_FAILED", "Lessons must be readable UTF-8 Markdown.") from exc
        lessons.append(Lesson(lesson_id, _text(item["title"], f"lessons[{index}].title"), path_name, linked_objectives, rights_id, citations, markdown))
    if taught != objective_ids:
        _fail("Every objective must be taught by at least one lesson.")

    questions: list[Question] = []
    question_ids: set[str] = set()
    for index, value in enumerate(_list(top["questions"], "questions")):
        origin = value.get("origin") if isinstance(value, dict) else None
        fields = OFFICIAL_FIELDS if origin == "official_pool" else GENERATED_FIELDS if origin == "generated" else set()
        if not fields:
            _fail(f"questions[{index}].origin must be official_pool or generated.")
        item = _strict_record(value, f"questions[{index}]", fields)
        question_id = _identifier(item["id"], f"questions[{index}].id")
        if question_id in question_ids:
            _fail(f"Duplicate question ID: {question_id}.")
        question_ids.add(question_id)
        if question_id in withdrawn or question_id in superseded:
            _fail(f"Question {question_id} is withdrawn or superseded by the declared pool.")
        objective_id = _identifier(item["objective_id"], f"questions[{index}].objective_id")
        if objective_id not in objective_ids:
            _fail(f"Question {question_id} references an unknown objective.")
        options, correct = _parse_options(item, index, question_id)
        question_rights_id = _identifier(item["question_rights_id"], f"questions[{index}].question_rights_id")
        explanation_rights_id = _identifier(item["explanation_rights_id"], f"questions[{index}].explanation_rights_id")
        if question_rights_id not in rights_by_id or explanation_rights_id not in rights_by_id:
            _fail(f"Question {question_id} references unknown rights.")
        if rights_by_id[explanation_rights_id]["status"] != "licensed":
            _fail(f"Question {question_id} explanation must use licensed rights.")
        question_tags = _string_list(item["tags"], f"questions[{index}].tags")
        if any(not TAG.fullmatch(tag) for tag in question_tags):
            _fail(f"Question {question_id} tags must be normalized lowercase topic labels.")
        explanation_citations = _citations(item["explanation_citations"], f"questions[{index}].explanation_citations")
        official_id = None
        assessment_id = None
        source_reference = None
        if origin == "official_pool":
            if rights_by_id[question_rights_id]["status"] != "public_domain":
                _fail(f"Official question {question_id} must use public-domain rights.")
            official_id = _identifier(item["official_question_id"], f"questions[{index}].official_question_id")
            if official_id != question_id:
                _fail(f"Official question ID {official_id} must equal engine ID {question_id}.")
            assessment_id = _identifier(item["pool_id"], f"questions[{index}].pool_id")
            if assessment_id != pool_id:
                _fail(f"Official question {question_id} references another assessment pool.")
            source_reference = _citation(item["source_question_ref"], f"questions[{index}].source_question_ref")
            if source_reference.source_id != pool_source_id or not source_reference.locator.startswith(official_id):
                _fail(f"Official question {question_id} has an invalid source reference.")
        elif rights_by_id[question_rights_id]["status"] != "licensed":
            _fail(f"Generated question {question_id} must use licensed original-content rights.")
        questions.append(Question(question_id, item["type"], objective_id, _text(item["prompt"], f"questions[{index}].prompt"), options, correct, _text(item["explanation"], f"questions[{index}].explanation"), origin, official_id, assessment_id, source_reference, question_tags, question_rights_id, explanation_rights_id, explanation_citations))
    if not questions:
        _fail("At least one question is required.")

    for citation in [citation for lesson in lessons for citation in lesson.citations] + [citation for question in questions for citation in question.explanation_citations]:
        if citation.source_id not in source_ids:
            _fail(f"Citation references unknown source {citation.source_id}.")

    approval = _strict_record(top["approval"], "approval", APPROVAL_REQUIRED, APPROVAL_OPTIONAL)
    if approval["status"] != "approved":
        _fail("approval.status must be approved before validation or installation.")
    _text(approval["reviewed_by"], "approval.reviewed_by")
    reviewed_at = _text(approval["reviewed_at"], "approval.reviewed_at")
    try:
        if not reviewed_at.endswith("Z"):
            raise ValueError
        datetime.fromisoformat(reviewed_at[:-1] + "+00:00")
    except ValueError:
        _fail("approval.reviewed_at must be an RFC 3339 UTC timestamp.")
    review_scope = _string_list(approval["review_scope"], "approval.review_scope", nonempty=True)
    if not set(review_scope) <= REVIEW_SCOPES:
        _fail("approval.review_scope contains an unsupported label.")
    if "notes" in approval:
        _text(approval["notes"], "approval.notes")

    notice_path = source / "NOTICE.md"
    notice_markdown = None
    if notice_path.exists():
        if notice_path.is_symlink() or not notice_path.is_file():
            _fail("NOTICE.md must be a regular file.")
        try:
            notice_markdown = normalize_lesson(notice_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            raise LearningError("PACK_VALIDATION_FAILED", "NOTICE.md must be readable UTF-8 Markdown.") from exc

    expected_files = {"pack.json", *lesson_paths}
    if notice_markdown is not None:
        expected_files.add("NOTICE.md")
    actual_files = {item.relative_to(source).as_posix() for item in source.rglob("*") if item.is_file()}
    if actual_files != expected_files:
        _fail("A format-0.2 pack may contain only pack.json, declared lessons, and optional NOTICE.md.")

    return Pack(source, "0.2", pack_id, version, title, lessons[0].path, lessons[0].markdown, tuple(objectives), tuple(questions), normalized, tuple(lessons), tuple(sources), pool, tuple(rights), approval, language, tags, notice_markdown)


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
    if not isinstance(normalized, dict):
        _fail("pack must be an object.")
    format_version = normalized.get("format_version")
    if format_version == "0.1":
        return _load_v01(source)
    if format_version == "0.2":
        return _load_v02(source, normalized)
    _fail("format_version must be exactly 0.1 or 0.2.")
