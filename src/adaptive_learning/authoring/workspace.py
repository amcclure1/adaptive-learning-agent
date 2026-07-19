"""Confined file-backed authoring workspace and atomic record mutations."""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from adaptive_learning.errors import LearningError

from .canonical import canonical_json_file_bytes, normalize_markdown
from .schemas import APPROVAL_TYPES, ID_RE, validate_record, validate_reference


WORKSPACE_CONTRACT_VERSION = "ala-authoring-0.3b.1"
DIRECTORIES = (
    "sources/drafts", "sources/revisions", "claims/drafts", "claims/revisions",
    "lessons/drafts", "lessons/revisions", "question-specs/drafts", "question-specs/revisions",
    "questions/drafts", "questions/revisions", "validations/current", "validations/reports",
    "approvals/sources", "approvals/claims", "approvals/lesson-content",
    "approvals/question-content", "approvals/answer-uniqueness", "approvals/pack-release",
    "approvals/revocations", "release/selections", "release/candidates", "release/evidence",
    "verifications/runs", "verifications/findings", "verifications/resolutions", "verifications/metrics",
    "self-audits/records",
)
TYPE_DIRS = {
    "source": "sources", "claim": "claims", "lesson": "lessons",
    "question_spec": "question-specs", "question": "questions",
}
APPROVAL_DIRS = {
    "source_approval": "sources", "claim_approval": "claims",
    "question_content_approval": "question-content",
    "answer_uniqueness_approval": "answer-uniqueness",
    "pack_release_approval": "pack-release",
}


def _safe_id(value: str, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise LearningError("AUTHORING_ID_INVALID", f"{label} must use the stable lowercase identifier grammar.")
    return value


def project_path(authoring_root: str | Path, project_id: str) -> Path:
    _safe_id(project_id, "project_id")
    root = Path(authoring_root).resolve()
    path = (root / project_id).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:  # pragma: no cover - ID grammar makes this defensive.
        raise LearningError("AUTHORING_PATH_INVALID", "The project path escapes the authoring root.") from exc
    return path


@contextmanager
def workspace_lock(workspace: Path) -> Iterator[None]:
    lock_path = workspace / ".authoring.lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise LearningError("WORKSPACE_CONFLICT", "The authoring workspace is already being mutated.", retryable=True) from exc
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def atomic_write(path: Path, content: bytes, *, expected_absent: bool = False) -> None:
    if expected_absent and path.exists():
        raise LearningError("WORKSPACE_CONFLICT", f"{path.name} already exists.")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if expected_absent and path.exists():
            raise LearningError("WORKSPACE_CONFLICT", f"{path.name} was created concurrently.")
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def initialize_workspace(
    authoring_root: str | Path,
    project_id: str,
    *,
    title: str,
    created_at: str,
    workspace_commit: str,
    pilot_scope: dict[str, Any],
    author: dict[str, str],
) -> dict[str, Any]:
    workspace = project_path(authoring_root, project_id)
    if workspace.exists():
        raise LearningError("WORKSPACE_CONFLICT", "The project workspace already exists.")
    workspace.parent.mkdir(parents=True, exist_ok=True)
    try:
        workspace.mkdir()
        for relative in DIRECTORIES:
            workspace.joinpath(*relative.split("/")).mkdir(parents=True)
        from .schemas import seal_record

        project = seal_record({
            "schema_version": "ala.authoring.project.v2",
            "artifact_id": project_id,
            "artifact_type": "project",
            "revision": 1,
            "status": "draft",
            "created_at": created_at,
            "modified_at": created_at,
            "author": author,
            "supersedes": None,
            "project_id": project_id,
            "title": title,
            "workspace_commit": workspace_commit,
            "pilot_scope": pilot_scope,
            "workspace_contract_version": WORKSPACE_CONTRACT_VERSION,
            "default_target_pack_format": "0.2",
            "allowed_target_pack_formats": ["0.2", "0.3"],
            "text_only_default": True,
            "artifact_indexes": {
                "sources": "sources",
                "claims": "claims",
                "lessons": "lessons",
                "question_specifications": "question-specs",
                "questions": "questions",
                "validations": "validations",
                "approvals": "approvals",
                "release": "release",
            },
            "private_material_policy": "prohibited",
            "canonical_digest": "0" * 64,
        })
        atomic_write(workspace / "project.json", canonical_json_file_bytes(project), expected_absent=True)
    except Exception:
        if workspace.exists():
            for item in sorted(workspace.rglob("*"), reverse=True):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    item.rmdir()
            workspace.rmdir()
        raise
    return {"project_id": project_id, "workspace": workspace.as_posix(), "project": project, "created_directories": list(DIRECTORIES)}


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LearningError("AUTHORING_RECORD_INVALID", f"{path.name} is not readable UTF-8 JSON.") from exc
    if not isinstance(value, dict):
        raise LearningError("AUTHORING_RECORD_INVALID", f"{path.name} must contain a JSON object.")
    return value


def project_record(workspace: Path) -> dict[str, Any]:
    record = read_json(workspace / "project.json")
    validate_record(record)
    return record


def draft_path(workspace: Path, artifact_type: str, artifact_id: str) -> Path:
    if artifact_type not in TYPE_DIRS:
        raise LearningError("AUTHORING_TYPE_INVALID", "Only authored-content records have editable drafts.")
    _safe_id(artifact_id, "artifact_id")
    base = workspace / TYPE_DIRS[artifact_type] / "drafts"
    if artifact_type == "lesson":
        return base / artifact_id / "lesson.json"
    return base / f"{artifact_id}.json"


def revision_path(workspace: Path, artifact_type: str, artifact_id: str, revision: int) -> Path:
    if artifact_type not in TYPE_DIRS or not isinstance(revision, int) or revision < 1:
        raise LearningError("AUTHORING_REVISION_INVALID", "The artifact type or revision is invalid.")
    _safe_id(artifact_id, "artifact_id")
    base = workspace / TYPE_DIRS[artifact_type] / "revisions" / artifact_id
    if artifact_type == "lesson":
        return base / str(revision) / "lesson.json"
    return base / f"{revision}.json"


def markdown_path_for_record(json_path: Path, record: dict[str, Any]) -> Path | None:
    if record.get("artifact_type") != "lesson":
        return None
    return json_path.parent / record["markdown_path"]


def read_record(path: Path) -> tuple[dict[str, Any], str | None]:
    record = read_json(path)
    markdown_path = markdown_path_for_record(path, record)
    markdown = None
    if markdown_path is not None:
        try:
            markdown = markdown_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise LearningError("AUTHORING_RECORD_INVALID", "Lesson Markdown is not readable UTF-8.") from exc
    validate_record(record, markdown=markdown)
    return record, markdown


def write_draft(workspace: Path, record: dict[str, Any], *, expected_prior_digest: str | None, markdown: str | None = None) -> dict[str, Any]:
    from .schemas import seal_record

    if record.get("status") != "draft":
        raise LearningError("AUTHORING_STATE_INVALID", "Editable records must have draft status.")
    path = draft_path(workspace, record.get("artifact_type"), record.get("artifact_id"))
    with workspace_lock(workspace):
        if path.exists():
            current, _ = read_record(path)
            if expected_prior_digest != current["canonical_digest"]:
                raise LearningError("WORKSPACE_CONFLICT", "The expected prior draft digest does not match.")
        elif expected_prior_digest is not None:
            raise LearningError("WORKSPACE_CONFLICT", "A new draft requires expected_prior_digest null.")
        sealed = seal_record(record, markdown=markdown)
        if sealed["artifact_type"] == "lesson":
            if markdown is None:
                raise LearningError("AUTHORING_SCHEMA_INVALID", "Lesson drafts require Markdown.")
            atomic_write(path.parent / sealed["markdown_path"], normalize_markdown(markdown).encode("utf-8"))
        atomic_write(path, canonical_json_file_bytes(sealed))
    return sealed


def freeze_revision(workspace: Path, artifact_type: str, artifact_id: str, *, expected_draft_digest: str, modified_at: str) -> dict[str, Any]:
    from .schemas import seal_record

    draft = draft_path(workspace, artifact_type, artifact_id)
    with workspace_lock(workspace):
        record, markdown = read_record(draft)
        if record["canonical_digest"] != expected_draft_digest:
            raise LearningError("WORKSPACE_CONFLICT", "The expected draft digest does not match.")
        previous_paths = sorted((workspace / TYPE_DIRS[artifact_type] / "revisions" / artifact_id).rglob("*.json")) if (workspace / TYPE_DIRS[artifact_type] / "revisions" / artifact_id).exists() else []
        revision = len(previous_paths) + 1
        frozen = dict(record)
        frozen.update({"revision": revision, "status": "active", "modified_at": modified_at})
        if revision > 1:
            previous, _ = read_record(previous_paths[-1])
            frozen["supersedes"] = reference(previous)
        else:
            frozen["supersedes"] = None
        frozen = seal_record(frozen, markdown=markdown)
        path = revision_path(workspace, artifact_type, artifact_id, revision)
        if artifact_type == "lesson":
            atomic_write(path.parent / frozen["markdown_path"], normalize_markdown(markdown or "").encode("utf-8"), expected_absent=True)
        atomic_write(path, canonical_json_file_bytes(frozen), expected_absent=True)
    return frozen


def reference(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": record["artifact_id"], "artifact_type": record["artifact_type"],
        "revision": record["revision"], "canonical_digest": record["canonical_digest"],
    }


def find_record(workspace: Path, target: dict[str, Any]) -> tuple[dict[str, Any], str | None, Path]:
    validate_reference(target)
    artifact_type = target["artifact_type"]
    artifact_id = target["artifact_id"]
    revision = target["revision"]
    if artifact_type == "project":
        path = workspace / "project.json"
    elif artifact_type in TYPE_DIRS:
        path = revision_path(workspace, artifact_type, artifact_id, revision)
        if not path.exists():
            candidate = draft_path(workspace, artifact_type, artifact_id)
            if candidate.exists():
                path = candidate
    elif artifact_type in {"approval", "review", "validation_report", "release_candidate", "release_evidence", "ai_verification_run", "verification_finding", "finding_resolution", "author_self_audit"}:
        matches = [item for item in workspace.rglob(f"{artifact_id}.json") if ".authoring.lock" not in item.parts]
        if len(matches) != 1:
            raise LearningError("REFERENCE_MISMATCH", "The referenced artifact is missing or ambiguous.")
        path = matches[0]
    else:
        raise LearningError("REFERENCE_MISMATCH", "The referenced artifact type is not stored in this workspace.")
    if not path.exists():
        raise LearningError("REFERENCE_MISMATCH", "The referenced artifact is missing.")
    record, markdown = read_record(path)
    if artifact_type in TYPE_DIRS and reference(record) != target:
        candidate = draft_path(workspace, artifact_type, artifact_id)
        if candidate.exists():
            draft_record, draft_markdown = read_record(candidate)
            if reference(draft_record) == target:
                record, markdown, path = draft_record, draft_markdown, candidate
    if reference(record) != target:
        raise LearningError("REFERENCE_MISMATCH", "The referenced artifact revision or digest does not match.")
    return record, markdown, path


def decision_path(workspace: Path, record: dict[str, Any]) -> Path:
    if record["artifact_type"] == "approval":
        folder = "revocations" if record["record_kind"] in {"revocation", "supersession"} else APPROVAL_DIRS[record["approval_type"]]
    else:
        folder = {
            "lesson_content_review": "lesson-content", "question_originality_review": "question-content",
            "question_spec_design_review": "question-content", "impact_review": "revocations",
            "material_need_review": "pack-release",
        }[record["review_type"]]
    return workspace / "approvals" / folder / f"{record['artifact_id']}.json"


def store_immutable(workspace: Path, record: dict[str, Any], *, markdown: str | None = None, path: Path | None = None) -> dict[str, Any]:
    validate_record(record, markdown=markdown)
    destination = path or decision_path(workspace, record)
    with workspace_lock(workspace):
        atomic_write(destination, canonical_json_file_bytes(record), expected_absent=True)
    return record


def all_stored_records(workspace: Path) -> list[tuple[dict[str, Any], str | None, Path]]:
    records: list[tuple[dict[str, Any], str | None, Path]] = []
    for path in sorted(workspace.rglob("*.json")):
        relative = path.relative_to(workspace).as_posix()
        if relative.startswith("release/selections/") or relative.endswith("/pack.json"):
            continue
        record = read_json(path)
        if record.get("artifact_type") not in {"project", "source", "claim", "lesson", "question_spec", "question", "review", "approval", "validation_report", "release_candidate", "release_evidence", "ai_verification_run", "verification_finding", "finding_resolution", "author_self_audit"}:
            continue
        markdown_path = markdown_path_for_record(path, record)
        markdown = markdown_path.read_text(encoding="utf-8") if markdown_path is not None and markdown_path.exists() else None
        records.append((record, markdown, path))
    return records
