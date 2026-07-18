# Pack Format 0.2 Proposal

Status: Proposed; not implemented or accepted
Updated: 2026-07-18
Related decision: [ADR 0009](decisions/0009-sourced-pack-format-0.2.md)

## Decision summary

Use explicit format `0.2`, not optional format-0.1 fields. Format 0.1 has strict unknown-field validation and exactly one lesson, so its semantics cannot safely grow in place. A future loader must dispatch on the exact version and preserve format-0.1 behavior byte-for-byte.

Continue using unpacked UTF-8 JSON plus Markdown and Python standard-library parsing. Do not add YAML, archives, assets, executable content, remote fetching, or another dependency for this milestone.

## Proposed directory shape

```text
pack-root/
├── pack.json
└── lessons/
    ├── 01-band-edges-and-emissions.md
    └── 02-special-operations-and-power.md
```

Only regular files named by the manifest are allowed. Paths are relative, normalized POSIX-style paths; traversal, absolute paths, links/reparse points, duplicate targets, undeclared entries, and case-colliding names fail validation. Lesson Markdown contains no executable directives.

## Proposed manifest shape

This example is structural and intentionally omits real question wording, choices, answers, lessons, and explanations.

```json
{
  "format_version": "0.2",
  "pack_id": "us-amateur-extra-e1a",
  "version": "0.2.0",
  "title": "US Amateur Extra: E1A Pilot",
  "language": "en-US",
  "tags": ["amateur-radio", "element-4", "e1a"],
  "assessment_pool": {
    "name": "2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus",
    "publisher": "NCVEC Question Pool Committee",
    "effective_from": "2024-07-01",
    "effective_through": "2028-06-30",
    "source_id": "ncvec-pool-current",
    "errata_checked_through": "2026-02-04",
    "errata_source_id": "ncvec-release-errata",
    "withdrawn_official_question_ids": ["E2A13", "E4D05", "E6D07", "E9E10"]
  },
  "rights": [
    {
      "scope": "official_question_pool_material",
      "status": "public_domain_statement",
      "statement_source_id": "ncvec-release-errata",
      "notice": "NCVEC states that it releases the pool into the public domain."
    },
    {
      "scope": "original_lessons_and_explanations",
      "status": "licensed",
      "license_expression": "Apache-2.0",
      "notice": "Subject to project review before publication."
    }
  ],
  "sources": [
    {
      "id": "ncvec-pool-current",
      "kind": "official_question_pool",
      "title": "2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus",
      "publisher": "NCVEC Question Pool Committee",
      "url": "https://ncvec.org/downloads/...pdf",
      "retrieved_on": "2026-07-18"
    },
    {
      "id": "fcc-97-301",
      "kind": "regulation",
      "title": "47 CFR 97.301 — Authorized frequency bands",
      "publisher": "Federal Communications Commission",
      "url": "https://www.ecfr.gov/current/title-47/part-97/section-97.301",
      "retrieved_on": "2026-07-18"
    }
  ],
  "objectives": [
    {"id": "obj-band-edges", "title": "Band-edge and emission compliance"},
    {"id": "obj-special-operations", "title": "Special operations and LF/MF power rules"}
  ],
  "lessons": [
    {
      "id": "lesson-band-edges",
      "title": "Band edges and occupied signals",
      "path": "lessons/01-band-edges-and-emissions.md",
      "objective_ids": ["obj-band-edges"],
      "citations": [{"source_id": "fcc-97-301", "locator": "§ 97.301(b)"}]
    }
  ],
  "questions": [
    {
      "id": "E1A01",
      "official_question_id": "E1A01",
      "origin": "official_pool",
      "objective_id": "obj-band-edges",
      "tags": ["band-edge", "occupied-bandwidth"],
      "question_source": {"source_id": "ncvec-pool-current", "locator": "E1A01"},
      "prompt": "<official wording omitted from this design>",
      "options": [{"id": "A", "text": "<omitted>"}],
      "correct_option_ids": ["D"],
      "explanation": "<original reviewed explanation omitted from this design>",
      "explanation_citations": [
        {"source_id": "fcc-97-301", "locator": "§ 97.301(b)"}
      ]
    }
  ]
}
```

The abbreviated URL and incomplete choice set make this example intentionally invalid as a pack. It is not content to install.

## Field rules

All objects remain closed: missing required fields or unknown fields fail. Identifiers use the existing conservative identifier grammar; arrays preserve author-declared order unless a rule explicitly treats them as sets.

### Top level

- `format_version` must equal `0.2`.
- Existing `pack_id`, `version`, `title`, `objectives`, and scored multiple-choice/multiple-response question semantics remain.
- `language` is a required BCP 47-shaped ASCII tag validated syntactically offline; no locale library is required. The pilot uses `en-US`.
- `tags` is optional, unique, normalized lowercase labels. Tags are descriptive only and do not affect selection or scoring.
- `lessons`, `assessment_pool`, `sources`, and `rights` are required for a sourced pilot pack.

### Lessons

`lessons` is a non-empty ordered array. Each record has `id`, `title`, `path`, one or more valid `objective_ids`, and a possibly empty `citations` array. Every objective must be taught by at least one lesson. Markdown is returned verbatim after the existing normalization rules; citations are structured separately so the skill can display them consistently.

### Sources and citations

A source has stable pack-local `id`, closed `kind` enumeration, `title`, `publisher`, absolute HTTPS `url`, and ISO date `retrieved_on`. Proposed kinds are `official_question_pool`, `regulation`, `official_errata`, and `official_guidance`. The loader does not fetch URLs or decide whether a publisher is authoritative.

A citation is only `{source_id, locator}`. `locator` is human-auditable text such as `E1A01` or `§ 97.313(k)`; it is not a claim graph. Every reference must resolve. Explanations require at least one citation in this evidence-sensitive pilot. A citation supports review and presentation but never makes agent memory authoritative.

### Official identity and origin

- `origin` is required and exactly `official_pool` or `generated`.
- `official_pool` requires `official_question_id` and `question_source`; the source kind must be `official_question_pool`, and its locator must equal the official identifier for this pilot.
- `generated` forbids `official_question_id`, must identify original-content rights, and must not be described as official or recalled exam content.
- `id` remains the engine-stable question identifier. For this pilot an official question's `id` must exactly equal `official_question_id`, preserving E1A identifiers without an alias layer.
- Prompt, ordered option IDs/text, and ordered answer-key IDs are digest-covered. Any change produces a different pack digest and requires a new pack version; the installer never silently mutates the existing `(pack_id, version)`.

The pilot contains no generated questions, but the origin discriminator is required now so official and generated content can never be conflated later.

### Pool and errata

`assessment_pool` makes the pool name, publisher, effective interval, current-pool source, errata check date/source, and known withdrawn IDs visible offline. Dates use ISO `YYYY-MM-DD` and are metadata, not network-backed currency guarantees.

Validation rejects:

- an official question ID listed in `withdrawn_official_question_ids`;
- duplicate official IDs;
- an errata check date outside the assessment pool's effective interval;
- a missing/mistyped pool or errata source reference;
- an official question locator that does not match its preserved ID.

Wording or key corrections in a consolidated official pool are replacements: the pack author updates the source and `errata_checked_through`, increments the pack version, and generates a new digest. The existing version remains immutable and separately installed. The core does not infer legal currency or rewrite old attempts.

### Rights

Rights are scoped records rather than one misleading pack-wide license. `status` is `public_domain_statement`, `licensed`, or `unresolved`. A public-domain statement requires the official source carrying that statement; it is not represented as an SPDX license. A licensed scope requires `license_expression`. An unresolved scope fails publication policy but may be allowed by a future draft validator; installable pilot packs require no unresolved scope.

The NCVEC statement appears to cover the official pool. It does not establish rights in separately written explanations, third-party study material, marks, seals, or copied website presentation. Original lessons/explanations therefore need their own project-approved notice.

## Canonical digest

Retain existing Unicode/newline normalization. The format-0.2 digest is SHA-256 over a domain-separated sequence containing canonical `pack.json` and every declared lesson's normalized bytes, sorted by normalized relative path. Source URLs and rights notices are inside the manifest and therefore covered. Undeclared files are rejected rather than ignored.

## Backward compatibility

- Format 0.1 continues to require exactly its current fields, `pack.json`, and one lesson; its parser, model behavior, and digest do not change.
- Format 0.2 uses a separate strict validator/model branch and a distinct digest domain marker.
- No automatic conversion or in-place migration occurs.
- Existing format-0.1 installed rows and sessions remain valid because the SQLite schema stores pack identity/version/digest and controlled path, not a serialized question schema.

## Engine impact

| Area | Required change | Classification |
|---|---|---|
| Pack model | Add versioned model records for lessons, sources/citations, assessment pool, rights, language, tags, origin, and official ID. | Pack parsing/validation |
| Loader/validator | Exact version dispatch, closed 0.2 fields, path/source/citation/origin/errata/rights cross-checks. Keep 0.1 branch unchanged. | Pack parsing/validation |
| Digest/install copy | Cover all declared lessons with a 0.2 domain marker; reject undeclared entries. | Pack parsing/validation |
| SQLite schema/tables | Existing installed pack identity/path/digest and session pinning suffice. | No change required |
| Scoring, attempts, sessions, quarantine, objective progress | Existing identifiers and answer-key semantics suffice. | No change required |
| `pack.validate` / `pack.install` results | Add format, language, pool, errata, origin counts, and rights/source summaries for 0.2 packs. | Tool contract |
| `study.start` result | Return the ordered lesson records for 0.2 while preserving the current 0.1 lesson result. | Tool contract |
| `study.next` result | Add question origin and official identifier, never answers/explanations. | Tool contract |
| `study.submit` result | Add reviewed explanation citations after scoring. | Tool contract |
| Hermes workflow skill | Present multiple lessons, label official/generated origin, show pool/source currency, and render citations without inventing authority. | Hermes skill presentation |
| New tools, request arguments, scoring types | Not needed. | No change required |

The exact additive output envelope and capability/version signaling remain a review decision. Hermes input schemas can remain the same because no operation or request argument is added.

## Validation acceptance cases

- The current format-0.1 fixture validates, installs, studies, and digests exactly as before.
- All E1A official IDs round-trip exactly; aliases, case changes, missing IDs, and duplicate IDs fail.
- A golden manifest comparison detects any official prompt, ordered-option, or answer-key change; a different version/digest is required for a reviewed replacement.
- Validation output exposes pool name/version, effective dates, errata date, source records, and scoped rights.
- Adding a selected ID to the withdrawn list makes the pack invalid; a reviewed corrected pack version can replace it without changing old attempts.
- Official and generated origin rules are mutually exclusive and visible in tool output.
- Repeated install/study operations over identical input retain deterministic digest, selection, scoring, retry, and progress behavior.
