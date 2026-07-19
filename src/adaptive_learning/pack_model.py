"""Immutable, runtime-neutral subject-pack records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Option:
    option_id: str
    text: str


@dataclass(frozen=True, slots=True)
class Objective:
    objective_id: str
    title: str


@dataclass(frozen=True, slots=True)
class Citation:
    source_id: str
    locator: str


@dataclass(frozen=True, slots=True)
class Source:
    source_id: str
    source_type: str
    title: str
    publisher: str
    url: str
    retrieved_on: str
    rights_id: str
    revision: str | None = None
    content_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class Asset:
    asset_id: str
    media_type: str
    path: str
    title: str
    caption: str
    alt_text: str
    terminal_fallback: str
    source_id: str
    rights_id: str
    accessibility_rights_id: str
    content_sha256: str
    width: int
    height: int
    official_figure_id: str
    language: str
    content: bytes
    derivation: dict[str, object] | None = None


@dataclass(frozen=True, slots=True)
class Lesson:
    lesson_id: str
    title: str
    path: str
    objective_ids: tuple[str, ...]
    rights_id: str
    citations: tuple[Citation, ...]
    markdown: str
    asset_ids: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class Question:
    question_id: str
    question_type: str
    objective_id: str
    prompt: str
    options: tuple[Option, ...]
    correct_option_ids: tuple[str, ...]
    explanation: str
    origin: str | None = None
    official_question_id: str | None = None
    assessment_pool_id: str | None = None
    source_question_reference: Citation | None = None
    tags: tuple[str, ...] = ()
    question_rights_id: str | None = None
    explanation_rights_id: str | None = None
    explanation_citations: tuple[Citation, ...] = ()
    asset_ids: tuple[str, ...] | None = None

    def as_record(self) -> dict[str, object]:
        record: dict[str, object] = {
            "id": self.question_id,
            "type": self.question_type,
            "objective_id": self.objective_id,
            "prompt": self.prompt,
            "options": [
                {"id": option.option_id, "text": option.text}
                for option in self.options
            ],
            "correct_option_ids": list(self.correct_option_ids),
            "explanation": self.explanation,
        }
        if self.origin is not None:
            record.update(
                {
                    "origin": self.origin,
                    "tags": list(self.tags),
                    "question_rights_id": self.question_rights_id,
                    "explanation_rights_id": self.explanation_rights_id,
                    "explanation_citations": [
                        {"source_id": item.source_id, "locator": item.locator}
                        for item in self.explanation_citations
                    ],
                }
            )
            if self.origin == "official_pool":
                record.update(
                    {
                        "official_question_id": self.official_question_id,
                        "pool_id": self.assessment_pool_id,
                        "source_question_ref": {
                            "source_id": self.source_question_reference.source_id,
                            "locator": self.source_question_reference.locator,
                        },
                    }
                )
        if self.asset_ids is not None:
            record["asset_ids"] = list(self.asset_ids)
        return record


@dataclass(frozen=True, slots=True)
class Pack:
    source_path: Path
    format_version: str
    pack_id: str
    version: str
    title: str
    lesson_name: str
    lesson_markdown: str
    objectives: tuple[Objective, ...]
    questions: tuple[Question, ...]
    normalized_record: dict[str, object]
    lessons: tuple[Lesson, ...] = ()
    sources: tuple[Source, ...] = ()
    assessment_pool: dict[str, object] | None = None
    rights: tuple[dict[str, object], ...] = ()
    approval: dict[str, object] | None = None
    language: str | None = None
    tags: tuple[str, ...] = ()
    notice_markdown: str | None = None
    assets: tuple[Asset, ...] = ()

    def objective(self, objective_id: str) -> Objective:
        return next(item for item in self.objectives if item.objective_id == objective_id)

    def question(self, question_id: str) -> Question:
        return next(item for item in self.questions if item.question_id == question_id)

    @property
    def declared_files(self) -> tuple[str, ...]:
        if self.format_version == "0.1":
            return ("pack.json", self.lesson_name)
        files = (
            "pack.json",
            *(lesson.path for lesson in self.lessons),
            *(asset.path for asset in self.assets),
        )
        return (*files, "NOTICE.md") if self.notice_markdown is not None else files

    def source(self, source_id: str) -> Source:
        return next(item for item in self.sources if item.source_id == source_id)

    def asset(self, asset_id: str) -> Asset:
        return next(item for item in self.assets if item.asset_id == asset_id)
