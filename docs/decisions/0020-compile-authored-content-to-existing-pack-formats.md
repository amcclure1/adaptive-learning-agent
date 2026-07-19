# ADR 0020: Compile Authored Content to Existing Pack Formats for 0.3B

Status: Proposed
Date: 2026-07-18

## Context

Format 0.2 already supports sourced text content, multiple lessons, original/generated questions, citations, component rights, and one human pack approval. Format 0.3 adds static PNG assets while preserving those semantics. Neither format represents the full source/claim/question/uniqueness authoring lifecycle. Both are strict closed formats, and format 0.3 is fixed by ADRs 0014–0016.

The 0.3B pilot is text-first and does not need diagrams unless an already-supported static asset is demonstrably necessary.

## Proposed decision

Do not extend format 0.3 and do not introduce format 0.4 for the first manual 0.3B pilot.

Keep all draft, claim, detailed rationale, originality, uniqueness, and layered-review records in the separate authoring workspace. After all approvals, deterministically compile the learner-facing release projection into:

- format 0.2 by default for the text-only pilot; or
- existing format 0.3 only if a separately reviewed need for a supported PNG asset is demonstrated before content compilation.

The compiled pack includes objectives, two approved lessons, five approved original questions, response/selection semantics, learner-facing explanations, appropriate post-answer distractor teaching where useful, citations/source summaries, component rights, notices, and the existing pack-level human approval record.

Full approved claims, internal requirement-option matrices, complete distractor-review records, originality comparison notes, uniqueness-review findings, and source/claim/question reviewer identities do not ship in the installed pack. A release-evidence manifest outside the pack binds those authoring records and approvals to the compiled pack digest. Pack source records retain allowed retrieval/effective dates and optional snapshot digests; claim freshness horizons remain editorial workspace data.

## Rationale

The first pilot should prove the manual evidence and review chain before expanding the learner pack contract. Existing formats can deliver the resulting text content and citations. A new format would be justified only if learner-facing or offline audit requirements cannot be met by the compiled projection plus release evidence.

## Consequences

- No pack parser, core, SQLite, Hermes, or contract change is required for the proposed 0.3B content exercise.
- Format 0.3 remains asset-specific and unchanged.
- Installed packs avoid private/editorial workflow data.
- Full claim/approval traceability depends on retaining the release-evidence bundle with the source repository/release records.

## Revisit triggers

Propose explicit format 0.4 if a later accepted requirement needs installed packs themselves to carry claim IDs, layered approval attestations, full distractor rationales, freshness horizons, or offline authoring-chain verification, or if compilation cannot preserve required learner-facing behavior in formats 0.2/0.3.

## Open points before acceptance

- Exact release-evidence manifest and compiler input/output contracts.
- Whether concise per-option rationales fit the existing learner-facing explanation without a format change.
- Exact static-asset necessity test if a future 0.3B author requests a diagram.
