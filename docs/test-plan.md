# Proposed MVP Test Plan

Status: proposed for review  
Design baseline: 2026-07-18

## Accepted version 0.1 release gate

AT-01 through AT-12 in [`mvp-vertical-slice.md`](mvp-vertical-slice.md) are the complete core release gate for the first implementation. All twelve must pass without Hermes, an LLM, a network, or non-standard-library runtime dependencies. A separate compatibility check must exercise health, start, next, and submit through a real Hermes v0.18.2 plugin installation before support is claimed.

The broader mastery, scheduling, archive, authoring, evidence, migration, backup, generic idempotency, and performance suites below are deferred. They are test-design inventory, not version-0.1 implementation requirements.

## Deferred broader MVP test inventory

## Test principles

- Deterministic tests inject clock, UUID factory, and selection seed.
- Core tests run without Hermes, a model, network access, or a persistent user database.
- Every bug in scoring, scheduling, archive safety, migrations, or idempotency receives a regression test.
- Pilot packs are tested with the same public validators as third-party packs.
- No test requires or reads real OAuth credentials.

## 1. Domain unit tests

### Scoring

- Single choice exact match and wrong/malformed option IDs.
- Multiple choice exact mode, explicit partial mode, negative/clamped partial cases, and duplicate selections.
- Numeric absolute/relative boundaries using `Decimal`, unit aliases, wrong units, locale separators, NaN/infinity, and excessive precision.
- Short-answer Unicode NFC, casefolding, whitespace, punctuation policy, accepted aliases, confusable characters, and empty input.
- Stored fixed-point values and `is_correct` invariant.
- Golden vectors produce byte-identical JSON on Windows, macOS, and Linux.

### Mastery and scheduling

- Formula examples at 0, partial, and perfect score for every objective weight.
- Objective weights sum validation and round-half-up behavior.
- Evidence-count and readiness thresholds prevent one-item readiness.
- Every box/confidence/score transition and due-date interval.
- Daylight-saving boundaries prove calculations use UTC durations.
- Algorithm version recorded and historical results unchanged by a new default.

### Selection

- Due before not-due; lower mastery, fewer exposures, older last-seen, and stable ID tie-breaks.
- Outstanding presentation is reused.
- The just-answered box-0 item is deprioritized in-session when alternatives exist.
- Same state/seed selects the same sequence; different permitted seeds affect only exact ties.
- Retired, expired, unavailable, and objective-filtered items are excluded.

### Evidence

- Every authority class/mode combination.
- Missing locator, missing source, disallowed class, superseded source, stale review, expired pack/source/question, and review-by warnings.
- Content/evidence edit invalidates a review digest.
- Independent-review label rule and explicit statement that it is not identity proof.
- Agent-authored draft cannot satisfy human review.

## 2. Pack-format tests

### Valid fixtures

- Minimal pack for every question type.
- Hierarchical objectives, Markdown claim markers, assets, and optional unknown fields.
- Both pilot pack skeletons with required evidence and reviews.

### Invalid fixtures

- Unknown format major, duplicate IDs, cycles, dangling references, wrong weight totals, invalid dates/versions, inactive accepted questions, and malformed YAML.
- Missing evidence/reviews under each validation profile.
- Review digest mismatch and canonical digest mismatch.
- Raw HTML, remote embedded content, unsupported assets, and answer types that require model grading.

### Hostile fixtures

- ZIP slip (`../`), absolute paths, Windows drive/UNC paths, mixed separators, case collisions, Unicode normalization collisions, symlinks, device entries, duplicate ZIP names, and nested archives.
- Compression bomb ratio, excessive file count/size/path length, YAML alias bomb/depth/node limits, invalid UTF-8, and oversized scalars.
- Markdown script/iframe/data URL and SVG scripts/external references.
- Ensure rejection happens before any file escapes staging or enters the install store.

### Reproducibility

- Two exports from identical input are byte-identical and have the same archive and pack digest.
- Input mtime, platform permissions, directory enumeration order, and CRLF/LF do not affect output.
- Any canonical content change changes the digest; noncanonical excluded files do not enter export.
- Validate -> export -> install -> export round-trip is identical.

## 3. SQLite tests

- Schema creates on every supported Python/SQLite combination; foreign keys are active.
- `PRAGMA integrity_check` and `foreign_key_check` pass after all fixtures.
- One submission produces exactly one attempt and consistent objective/item projections.
- Failure injected at each write rolls back the entire submit transaction.
- Same idempotency key/request replays original response; same key/different request conflicts.
- Concurrent local writers respect busy timeout and never duplicate an attempt.
- Pack cannot be deleted while referenced; marking unavailable preserves history.
- Projection rebuild from attempts matches stored progress exactly.
- Online backup during reads restores cleanly; staged corrupt restore never replaces live data.
- Migration success, already-applied migration, interrupted migration, backup creation, and unsupported downgrade.
- Logs and database contain no provider credentials or Hermes memory.

## 4. JSON contract tests

- Every request/result validates against contract schemas and rejects unknown request fields.
- Every mutating tool requires an idempotency key; reads reject it or ignore only as explicitly specified.
- Stable error type/code/details for each documented failure.
- Backup and restore require explicit destinations; restore rejects missing human confirmation, digest mismatch, active transactions, and incompatible schema.
- `ala_study_next` never exposes answer, rationale, tolerance secrets, or review data.
- `ala_study_submit` rejects caller-supplied scores/answers and returns pack-derived fields.
- Canonical response is identical through direct service and JSON CLI.
- Paths are constrained by the relevant operation and never interpolated into shell commands.
- Fuzz malformed JSON, deep objects, oversized strings, invalid Unicode, and wrong scalar types.

## 5. Authoring lifecycle tests

- Create draft; add manifest, objectives, sources, Markdown, claims, and each question type.
- Each edit is atomic and returns ordered current diagnostics.
- Optimistic digest conflict prevents overwriting another edit.
- Author cannot set release status through generic apply.
- Human review requires explicit confirmation, current target digest, and all required checks.
- Editing question or evidence invalidates acceptance.
- Release validation blocks incomplete review/evidence and succeeds after corrections.
- Export writes only canonical pack content and never authoring metadata, chat, database, or secrets.
- No call publishes, pushes Git, or accesses a marketplace.

## 6. Hermes adapter tests

Use a fake public plugin registration context; do not import private Hermes internals.

- Expected namespaced tools, toolset, schemas, and handlers register once.
- Each handler maps arguments/envelopes without changing values.
- Direct, CLI, and plugin paths pass the same golden conformance corpus.
- Typed core errors remain structured rather than becoming fabricated success prose.
- Provider interruption after commit can resume and retrieve the stored result with the same idempotency key.
- Plugin never reads Hermes memory or `~/.hermes/auth.json` / `~/.codex/auth.json`.
- Learner, authoring, and review mode gates are honored.
- Skill instructs Hermes to call submit, preserve idempotency keys, and never self-approve reviews.

Manual compatibility matrix before release:

- latest supported tagged Hermes on Linux/macOS/Windows where available;
- CLI startup, plugin discovery, explicit enablement, restart behavior, tool call, structured error, and skill loading;
- OpenAI Codex provider, one API-key provider, and a local compatible provider, using test accounts/configuration owned by the tester;
- no assertion about a provider credential beyond confirming the adapter does not access it.

## 7. End-to-end acceptance journeys

### Learner journey

1. Install a validated fixture pack.
2. Create a learner and start a 10-question session.
3. Answer all deterministic question types with known confidence values.
4. Interrupt/restart between presentation and submission and after submission.
5. Verify exact scores, schedule, objective progress, session summary, and idempotent retry.
6. Export a learner-data backup separately and confirm pack export has no learner data.

### Author journey

1. Conversationally create an evidence-required draft.
2. Add an authoritative source, objective, content, and generated question.
3. Observe release failure before review.
4. Record a human `changes_requested`, edit, then record `accepted` against the new digest.
5. Export, install, study, and reproduce the archive digest.
6. Confirm no publication or remote upload occurred.

### AWS SAP-C02 pilot

- Manifest scope and domain weights validate.
- Each active question cites allowed official AWS material with a precise locator.
- Volatile product behavior has review-by metadata.
- Every question has a current accepted review and originality check.
- A deliberately stale AWS source blocks or warns exactly as pack policy declares.

### US Amateur Extra pilot

- Exact question-pool effective period and FCC rules retrieval date validate.
- Regulatory answers cite the applicable 47 CFR locator.
- Each active question has current review and rights/originality metadata.
- A fixture outside the declared pool/effective period fails release validation.

## 8. Non-functional tests

- Cold local core command target under 500 ms excluding Hermes/model startup on a typical laptop.
- Submit transaction target under 100 ms for a database with 100,000 attempts.
- Pack validation target under 2 seconds for 1,000 questions and no network checks.
- Database and pack operations produce actionable errors when disk is full, read-only, locked, missing, or corrupt.
- Screen-reader-friendly plain-text results and no reliance on color alone in CLI diagnostics.
- Paths with spaces and non-ASCII characters on all supported systems.
- Dependency audit confirms no server framework, task queue, database client, vector library, or model SDK is pulled directly by this project.

Performance figures are proposed budgets and must be measured on documented hardware before becoming release gates.

## 9. Release gates

The MVP release is ready for review only when:

- all deterministic unit/integration tests pass;
- hostile-pack corpus causes safe, expected rejection;
- schema migration, backup, restore, and projection rebuild pass;
- direct/CLI/Hermes contract conformance is exact;
- both pilot packs pass release validation and end-to-end journeys;
- the Hermes version matrix and previously unverified install/discovery behavior are documented from actual tests;
- no package installation, configuration mutation, network publication, or autonomous review occurs during normal tests unless the test explicitly owns an isolated fixture environment.
