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
class Question:
    question_id: str
    question_type: str
    objective_id: str
    prompt: str
    options: tuple[Option, ...]
    correct_option_ids: tuple[str, ...]
    explanation: str

    def as_record(self) -> dict[str, object]:
        return {
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

    def objective(self, objective_id: str) -> Objective:
        return next(item for item in self.objectives if item.objective_id == objective_id)

    def question(self, question_id: str) -> Question:
        return next(item for item in self.questions if item.question_id == question_id)
