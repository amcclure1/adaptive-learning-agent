"""Deterministic format-0.3 test-pack builders."""

from __future__ import annotations

import hashlib
import json
import struct
import zlib
from pathlib import Path

from adaptive_learning.pack_validation import V03_REVIEW_SCOPES


def _chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def png_bytes(width: int = 2, height: int = 2, *, marker: bytes = b"") -> bytes:
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    rows = b"".join(b"\x00" + b"\x00\x00\x00" * width for _ in range(height))
    chunks = [_chunk(b"IHDR", ihdr)]
    if marker:
        chunks.append(_chunk(b"tEXt", b"marker\x00" + marker))
    chunks.extend((_chunk(b"IDAT", zlib.compress(rows)), _chunk(b"IEND", b"")))
    return b"\x89PNG\r\n\x1a\n" + b"".join(chunks)


def approved_scopes() -> list[str]:
    return sorted(V03_REVIEW_SCOPES)


def manifest(asset_content: bytes) -> dict[str, object]:
    questions = []
    for number, correct in ((1, "B"), (2, "D"), (3, "C")):
        question_id = f"Q{number}"
        questions.append(
            {
                "id": question_id,
                "type": "single_response",
                "objective_id": "obj-figure",
                "prompt": f"Using Figure T-1, answer test item {number}.",
                "options": [
                    {"id": "A", "text": f"Distractor A{number}"},
                    {"id": "B", "text": f"Key phrase B{number}"},
                    {"id": "C", "text": f"Key phrase C{number}"},
                    {"id": "D", "text": f"Key phrase D{number}"},
                ],
                "correct_option_ids": [correct],
                "explanation": f"Project explanation {number}.",
                "origin": "official_pool",
                "official_question_id": question_id,
                "pool_id": "test-pool",
                "source_question_ref": {"source_id": "pool", "locator": f"{question_id}; Figure T-1"},
                "tags": ["figure-reading"],
                "question_rights_id": "rights-official",
                "explanation_rights_id": "rights-original",
                "explanation_citations": [{"source_id": "pool", "locator": f"{question_id}; Figure T-1"}],
                "asset_ids": ["asset-t1"],
            }
        )
    return {
        "format_version": "0.3",
        "pack_id": "format-03-test",
        "version": "0.3.0",
        "title": "Format 0.3 Test Pack",
        "language": "en-US",
        "tags": ["test"],
        "assessment_pool": {
            "id": "test-pool",
            "title": "Test Pool",
            "publisher": "Test Publisher",
            "effective_from": "2026-01-01",
            "effective_through": "2028-12-31",
            "source_id": "pool",
            "errata_revision": "test-revision",
            "errata_source_id": "errata",
            "withdrawn_official_question_ids": [],
        },
        "rights": [
            {
                "id": "rights-official",
                "scope": "Official test material",
                "status": "public_domain",
                "basis_source_id": "pool",
                "covered_material": ["questions", "figure"],
            },
            {
                "id": "rights-original",
                "scope": "Original prose",
                "status": "licensed",
                "license_expression": "CC-BY-4.0",
                "copyright_holder": "Adaptive Learning Agent contributors",
            },
            {"id": "rights-reference", "scope": "Reference metadata", "status": "reference_only"},
        ],
        "sources": [
            {
                "id": "pool",
                "type": "official_question_pool",
                "title": "Test Pool Source",
                "publisher": "Test Publisher",
                "url": "https://example.invalid/pool",
                "retrieved_on": "2026-07-18",
                "snapshot_retained": True,
                "rights_id": "rights-reference",
                "revision": "test-revision",
                "content_sha256": "1" * 64,
            },
            {
                "id": "errata",
                "type": "official_errata",
                "title": "Test Errata",
                "publisher": "Test Publisher",
                "url": "https://example.invalid/errata",
                "retrieved_on": "2026-07-18",
                "snapshot_retained": True,
                "rights_id": "rights-reference",
                "revision": "test-revision",
                "content_sha256": "2" * 64,
            },
        ],
        "objectives": [{"id": "obj-figure", "title": "Read a bounded test figure"}],
        "lessons": [
            {
                "id": "lesson-figure",
                "title": "Figure reading",
                "path": "lessons/figure.md",
                "objective_ids": ["obj-figure"],
                "rights_id": "rights-original",
                "citations": [{"source_id": "pool", "locator": "Figure T-1"}],
                "asset_ids": [],
            }
        ],
        "assets": [
            {
                "id": "asset-t1",
                "media_type": "image/png",
                "path": "assets/figure-t1.png",
                "title": "Official Figure T-1",
                "caption": "Official test Figure T-1.",
                "alt_text": "A neutral drawing with labels X and Y connected by one line.",
                "terminal_fallback": "Orientation: left to right.\nConnection: X joins Y by one line.",
                "source_id": "pool",
                "rights_id": "rights-official",
                "accessibility_rights_id": "rights-original",
                "content_sha256": hashlib.sha256(asset_content).hexdigest(),
                "width": 2,
                "height": 2,
                "official_figure_id": "T-1",
                "language": "en-US",
            }
        ],
        "questions": questions,
        "approval": {
            "status": "approved",
            "reviewed_by": "Test Reviewer",
            "reviewed_at": "2026-07-18T12:00:00Z",
            "review_scope": approved_scopes(),
            "notes": "Synthetic test approval only.",
        },
    }


def write_pack(root: Path, *, approval: str = "approved", content: bytes | None = None) -> dict[str, object]:
    content = content if content is not None else png_bytes()
    data = manifest(content)
    if approval == "pending":
        data["approval"] = {
            "status": "pending",
            "reviewed_by": None,
            "reviewed_at": None,
            "review_scope": [],
            "notes": "Awaiting explicit human review.",
        }
    (root / "lessons").mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(exist_ok=True)
    (root / "lessons" / "figure.md").write_text("# Figure reading\n\nSynthetic lesson.\n", encoding="utf-8")
    (root / "assets" / "figure-t1.png").write_bytes(content)
    write_manifest(root, data)
    return data


def write_manifest(root: Path, data: dict[str, object]) -> None:
    (root / "pack.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
