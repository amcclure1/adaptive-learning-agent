# Pack Format 0.2

Status: Accepted design; implementation not authorized
Updated: 2026-07-18
Governing decision: [ADR 0009](decisions/0009-sourced-pack-format-0.2.md)
Normative rights policy: [Subject-Pack Rights Policy](rights-policy.md)

## Compatibility and scope

Sourced packs use explicit `format_version: "0.2"`. The loader dispatches by exact version. Format 0.1 remains strict and unchanged, including its files, fields, canonical digest, installed data, and response semantics.

Format 0.2 remains an unpacked UTF-8 JSON-plus-Markdown directory parsed with Python standard-library components. All JSON objects are closed: unknown or missing required fields fail validation. It adds only multiple lessons, language/tags, pool/errata metadata, question origin/official identity, sources/citations, component rights, and human approval.

## Directory layout

```text
amateur-extra-e1a/
├── pack.json
├── lessons/
│   ├── 01-band-edges.md
│   └── 02-special-operations.md
└── NOTICE.md
```

`NOTICE.md` is optional and may summarize provenance and rights for humans. Machine validation relies on `pack.json`. No separate `sources.json`, `questions.json`, or citation file is required for the pilot.

Only the root `pack.json`, declared regular Markdown lesson files, and optional root `NOTICE.md` are allowed. Paths use normalized relative POSIX syntax. Absolute paths, traversal, links/reparse points, duplicate targets, undeclared entries, and case-colliding names fail validation. Packs contain no executable content or assets.

## Manifest model

The following is an abbreviated structural illustration, not a valid or installable pack. It deliberately contains no real question wording, choices, answer key, lesson, or explanation.

```json
{
  "format_version": "0.2",
  "pack_id": "us-amateur-extra-e1a",
  "version": "0.2.0",
  "title": "US Amateur Extra: E1A Pilot",
  "language": "en-US",
  "tags": ["amateur-radio", "element-4", "e1a"],
  "assessment_pool": {
    "id": "ncvec-extra-2024-2028",
    "title": "2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus",
    "publisher": "NCVEC Question Pool Committee",
    "effective_from": "2024-07-01",
    "effective_through": "2028-06-30",
    "source_id": "ncvec-pool-fourth-errata",
    "errata_revision": "fourth-errata-2026-02-04",
    "errata_source_id": "ncvec-release-page",
    "withdrawn_official_question_ids": ["E2A13", "E4D05", "E6D07", "E9E10"]
  },
  "rights": [
    {
      "id": "rights-ncvec-pool",
      "scope": "official_question_pool_content",
      "status": "public_domain",
      "basis_source_id": "ncvec-release-page",
      "covered_material": ["wording", "choices", "answer_keys", "identifiers"]
    },
    {
      "id": "rights-original-prose",
      "scope": "original_lessons_and_explanations",
      "status": "licensed",
      "license_expression": "CC-BY-4.0",
      "copyright_holder": "Adaptive Learning Agent contributors"
    },
    {
      "id": "rights-external-references",
      "scope": "external_official_sources",
      "status": "reference_only"
    }
  ],
  "sources": [
    {
      "id": "ncvec-pool-fourth-errata",
      "type": "official_question_pool",
      "title": "2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus",
      "publisher": "NCVEC Question Pool Committee",
      "url": "https://ncvec.org/downloads/example.pdf",
      "retrieved_on": "2026-07-18",
      "effective_from": "2024-07-01",
      "effective_through": "2028-06-30",
      "revision": "fourth-errata-2026-02-04",
      "locator": "E1A",
      "snapshot_retained": true,
      "content_sha256": "<64 lowercase hexadecimal characters>",
      "rights_id": "rights-ncvec-pool"
    },
    {
      "id": "fcc-97-301",
      "type": "regulation",
      "title": "47 CFR 97.301 — Authorized frequency bands",
      "publisher": "Federal Communications Commission",
      "url": "https://www.ecfr.gov/current/title-47/part-97/section-97.301",
      "retrieved_on": "2026-07-18",
      "snapshot_retained": false,
      "rights_id": "rights-external-references"
    },
    {
      "id": "ncvec-release-page",
      "type": "official_errata",
      "title": "2024-2028 Extra Class Question Pool Release",
      "publisher": "NCVEC Question Pool Committee",
      "url": "https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release",
      "retrieved_on": "2026-07-18",
      "revision": "fourth-errata-2026-02-04",
      "snapshot_retained": false,
      "rights_id": "rights-external-references"
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
      "path": "lessons/01-band-edges.md",
      "objective_ids": ["obj-band-edges"],
      "rights_id": "rights-original-prose",
      "citations": [{"source_id": "fcc-97-301", "locator": "§ 97.301(b)"}]
    }
  ],
  "questions": [
    {
      "id": "E1A01",
      "origin": "official_pool",
      "official_question_id": "E1A01",
      "pool_id": "ncvec-extra-2024-2028",
      "source_question_ref": {
        "source_id": "ncvec-pool-fourth-errata",
        "locator": "E1A01"
      },
      "objective_id": "obj-band-edges",
      "tags": ["band-edge", "occupied-bandwidth"],
      "prompt": "<official wording omitted>",
      "options": [{"id": "A", "text": "<official option omitted>"}],
      "correct_option_ids": ["<official key omitted>"],
      "question_rights_id": "rights-ncvec-pool",
      "explanation": "<original explanation omitted>",
      "explanation_rights_id": "rights-original-prose",
      "explanation_citations": [
        {"source_id": "fcc-97-301", "locator": "§ 97.301(b)"}
      ]
    }
  ],
  "approval": {
    "status": "approved",
    "reviewed_by": "<human reviewer designation>",
    "reviewed_at": "<RFC 3339 UTC timestamp>",
    "review_scope": [
      "official_wording",
      "option_ordering",
      "answer_keys",
      "official_ids",
      "lessons",
      "explanations",
      "citations",
      "rights_metadata",
      "pool_and_errata_metadata"
    ],
    "notes": "<optional review notes>"
  }
}
```

The example URL, digest, timestamps, omitted content, and incomplete choices make this illustration invalid by design.

## Common fields

- `format_version` is exactly `0.2`.
- `pack_id`, `version`, `title`, `objectives`, and existing multiple-choice/multiple-response scoring fields retain format-0.1 semantics.
- `language` is required and uses a conservative syntactic BCP 47-shaped ASCII validation; the pilot uses `en-US`.
- `tags` is optional. Values are unique normalized lowercase topic labels and never affect scoring or selection.
- `lessons`, `assessment_pool`, `sources`, `rights`, `questions`, and `approval` are required non-empty records/arrays as applicable.

## Ordered lessons

`lessons` is a non-empty ordered array. Each lesson has a stable ID, title, confined Markdown path, one or more valid objective IDs, a rights reference for its original prose, and citations. Every objective must be taught by at least one lesson.

Declared array order is presentation order. Reordering lessons changes canonical manifest bytes, digest, and deterministic presentation order. Markdown is normalized using the existing newline/Unicode rules; changing lesson content changes the pack digest.

## Source records and snapshots

Each source record has:

- required stable `id`, `title`, `publisher`, `type`, absolute HTTPS `url`, `retrieved_on`, `snapshot_retained`, and `rights_id`;
- optional `effective_from`, `effective_through`, `revision`, and `locator` where applicable;
- conditional `content_sha256`.

Allowed pilot source types are `official_question_pool`, `official_errata`, `regulation`, and `official_guidance`. Dates use ISO `YYYY-MM-DD`. A present effective range must be valid. Pool and errata sources require revision identity appropriate to their record.

If `snapshot_retained` is `true`, `content_sha256` is required and is exactly 64 lowercase hexadecimal characters representing the retained bytes the author used. If false, `content_sha256` is absent. The pilot need not distribute retained source files.

Validation and study never fetch URLs. Remote availability or changes cannot influence validation, installation, digesting, scoring, or study. The canonical pack digest covers the complete source record, including any declared `content_sha256`, but never dereferences or digests live content. Freshness checks belong to a later editorial workflow.

## Citations

A citation is exactly `{source_id, locator}`. Both strings are non-empty; `source_id` must resolve. A locator must be a trimmed, single-line, printable string within a bounded length and must identify a human-auditable question, section, paragraph, page, or equivalent location. URLs belong in sources, not locators. Control characters, multiline text, empty/whitespace-only values, and embedded content fail validation.

Complete citation records remain available in deterministic tool results. Citation records are provenance, not executable instructions or an evidence graph.

## Assessment pool and errata

The assessment-pool record requires `id`, `title`, `publisher`, valid inclusive `effective_from`/`effective_through`, `source_id`, non-empty declared `errata_revision`, `errata_source_id`, and unique `withdrawn_official_question_ids`. It supports optional unique `superseded_official_question_ids` using the same validation rule; the E1A pilot omits that field because its selected IDs are active.

Both source references must resolve to appropriate source types. Validation rejects an official question ID declared withdrawn or superseded, duplicate official IDs, missing pool metadata for official-pool questions, invalid date ranges, or missing errata revision. Errata knowledge is data in the pack. The engine does not query the internet or decide whether a declared revision is newest.

A corrected official wording/key requires updated source/errata metadata as applicable, a different pack digest, and a new pack version or renewed approval. Installed content and historical attempts are never silently rewritten.

## Question origin

`origin` is required and exactly `official_pool` or `generated`.

An `official_pool` question requires:

- `official_question_id` and, for this pilot, identical engine `id`;
- `pool_id` resolving to the assessment pool;
- `source_question_ref` resolving to the official pool source and locating that exact official ID;
- exact official prompt, option identifiers/order/text, and official answer key;
- component rights for official pool content;
- an original explanation with its separate rights record and one or more supporting citations/source references.

A `generated` question forbids `official_question_id`, official-pool source-question references, and any claim that it appeared in an official exam or pool. It uses original-content rights. Generated questions are reserved by the format but absent from the E1A pilot.

## Rights

Rights validation follows [rights-policy.md](rights-policy.md). The format supports `public_domain`, `licensed`, and `reference_only` statuses. It does not use public domain as a license or let Apache-2.0 stand in for educational-prose rights.

Every rights record requires stable `id`, `scope`, and `status`. `public_domain` additionally requires `basis_source_id` and non-empty `covered_material` and forbids a license expression. `licensed` requires `license_expression` and `copyright_holder`. `reference_only` carries no license expression or public-domain covered-material claim. All basis/component references must resolve and record shapes remain closed.

The E1A pilot requires separate rights records for NCVEC official pool material, CC-BY-4.0 original lessons/explanations, and reference-only external official sources. Missing or unresolved rights, dangling component references, and original prose marked public domain fail validation. Logos, seals, screenshots, branding assets, and unofficial third-party study text are prohibited.

## Human approval

Every released pack version has exactly one `approval` record. Required fields are:

- `status`, exactly `approved` for an installable pack;
- non-empty `reviewed_by` human designation;
- `reviewed_at`, an RFC 3339 UTC timestamp;
- non-empty unique `review_scope`;
- optional non-empty `notes`.

The format recognizes review-scope labels used by the pilot: `official_wording`, `option_ordering`, `answer_keys`, `official_ids`, `lessons`, `explanations`, `citations`, `rights_metadata`, and `pool_and_errata_metadata`. The E1A release policy requires all nine. General engine validation verifies only structure, allowed labels, and approved status; it does not authenticate the reviewer, verify review quality, or provide a signature.

All approval metadata is digest-covered. Any content modification changes the pack digest and editorially requires a new pack version or renewed approval record. The engine can enforce version/digest conflicts and approval structure but cannot prove that the named human repeated the review.

## Rights notice

Optional `NOTICE.md` is for human readability and cannot override `pack.json`. When present it is normalized and included in the pack digest so its provenance/rights summary cannot change unnoticed. A missing or inconsistent machine rights record remains invalid regardless of the notice.

## Canonical digest

Retain format-0.1 Unicode/newline normalization principles but use a distinct format-0.2 domain marker. SHA-256 covers:

1. canonical `pack.json`, including ordered arrays, source records/digests, rights, errata, and approval;
2. normalized declared lesson bytes in declared lesson order, each framed with its normalized path;
3. normalized root `NOTICE.md` bytes when present.

Undeclared files are rejected. No remote bytes participate. Thus changes to source metadata, declared snapshot digests, rights, approval, lesson content/order, or notice change the pack digest deterministically.

## Runtime-neutral tool capabilities

Tool contract version remains `0.1`; no new operation family or request argument is introduced. Future `system.health` output adds optional capability data such as:

```json
{
  "capabilities": {
    "supported_pack_formats": ["0.1", "0.2"],
    "sourced_content": true,
    "multiple_lessons": true,
    "official_question_identity": true,
    "post_answer_citations": true
  }
}
```

`capabilities` is an additive optional health field; its listed members are required when that object is present. Existing required health fields remain. New provenance fields are additive/optional, and format-0.1 responses remain semantically unchanged. `pack.validate`/`pack.install` may add source, pool, rights, approval, language, and origin summaries. `study.start` may add ordered lesson records. `study.next` may add origin and official ID but never keys, explanations, or answer-revealing citations. `study.submit` may add explanation citations and source summaries after deterministic scoring.

Complete provenance belongs in core tool results. A Hermes skill chooses concise display: always identify an official question by official ID, show a short source label after feedback, offer full source/regulation detail on request, and never describe a project-authored explanation as official NCVEC commentary.

## Engine impact

| Area | Future required change | Classification |
|---|---|---|
| Pack model/parser | Exact version dispatch and closed format-0.2 records for the accepted fields. | Pack parsing/validation |
| Validation | Cross-reference, path, source/digest, citation, pool/errata, origin, rights, and approval rules. | Pack parsing/validation |
| Digest/install copy | Format-0.2 domain, ordered lessons, optional notice, no remote reads. | Pack parsing/validation |
| SQLite | Existing pack identity/version/digest/path and session pinning suffice. | No change required |
| Scoring/state | Existing selection, scoring, attempts, confidence, sessions, retries, quarantine, and progress suffice. | No change required |
| Contract | Add optional capabilities/provenance under contract 0.1; no new tools or inputs. | Tool contract |
| Hermes | Present deterministic provenance concisely and accurately. | Hermes skill presentation |

## Required future validation cases

1. Missing approval record fails.
2. Empty approval scope fails.
3. A withdrawn official question ID fails.
4. A generated question containing an official ID fails.
5. An official-pool question missing its official ID fails.
6. An official-pool question missing its pool/source reference fails.
7. Duplicate official IDs fail.
8. A citation referencing a missing source fails.
9. An invalid citation locator shape fails.
10. Missing rights metadata fails.
11. Original prose scoped as public domain fails.
12. Invalid pool effective dates fail.
13. Lesson path traversal fails.
14. Changing source metadata changes the digest.
15. Changing lesson content changes the digest.
16. Reordering lessons changes the digest and presentation order.
17. Validation and study succeed without external network access.
18. Format-0.1 fixture bytes, digest, validation, installation, study, and responses remain unchanged.
19. Hermes presentation never calls an original explanation official NCVEC commentary.
