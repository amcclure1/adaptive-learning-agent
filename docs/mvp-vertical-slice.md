# MVP Vertical Slice 0.1

Status: Accepted implementation scope
Design review: 2026-07-18

## Purpose

Version 0.1 is the smallest end-to-end proof that Adaptive Learning Agent's accepted architecture works. It is not the full MVP described by the original proposals. It proves that one runtime-independent Python core can load one portable subject pack, run a deterministic practice session, persist state in SQLite, quarantine a challenged question, survive process and conversation restarts, and be invoked through a thin Hermes adapter.

This document governs the first implementation task. When it conflicts with a broader proposed detail in `mvp-requirements.md`, `architecture.md`, `pack-format.md`, `sqlite-schema.md`, `tool-contract.md`, or `test-plan.md`, this narrower version-0.1 decision wins.

## Acceptance recommendation

Accept the following version-0.1 decisions:

- one manually authored, non-certification fixture pack;
- JSON plus Markdown in an unpacked directory;
- Python standard library only at runtime;
- one local learner profile;
- practice mode with immediate feedback;
- single-response and multiple-response exact scoring only;
- required confidence from 1 through 5;
- eight SQLite tables;
- deterministic stable-ID question selection;
- challenge rows as learner-local quarantine;
- ten runtime-neutral tools;
- Hermes v0.18.2 as the first compatibility-test target;
- no authoring, evidence-release workflow, archive, scheduler, generic idempotency store, audit framework, or backup/restore in 0.1.

## Vertical-slice contents

### Fixture subject

Create exactly one manually authored fixture pack during implementation. It is synthetic instructional content, not AWS, Amateur Radio, or exam-preparation material.

The fixture contains:

- one pack ID and version;
- two objectives;
- one Markdown lesson;
- five questions;
- three `single_response` questions;
- two `multiple_response` questions;
- at least two questions mapped to each objective;
- an explanation for every answer.

Each question maps to exactly one objective in 0.1. This avoids objective weighting and delta history while still proving that the core is subject-agnostic and objective-aware.

### User and mode

- One local learner profile is supported.
- Only practice mode exists.
- A session presents each eligible question at most once.
- Feedback is returned immediately after submission.
- Confidence is mandatory and stored with the attempt.
- No readiness claim, mastery claim, exam simulation, spaced repetition, or review scheduling is produced.

## Minimum pack format

### Serialization choice

Version 0.1 uses JSON plus Markdown.

Why:

- `json`, UTF-8 handling, and deterministic serialization are in the Python standard library.
- JSON has no aliases, tags, or implicit scalar typing, reducing the initial parser and security surface.
- The fixture is tiny enough that JSON's weaker hand-authoring ergonomics are acceptable.
- Removing the YAML parser keeps the first proof dependency-free at runtime.

Tradeoff: JSON is less pleasant for comments and long hand-authored content. Markdown carries the prose, and a later pack-format version may add YAML after a concrete authoring need and parser review. Version 0.1 must not accept both formats because dual serialization would double validation and compatibility cases.

This decision is recorded in ADR 0008 and clarifies the broader file-format language in ADRs 0001 and 0005.

### Unpacked layout

```text
fixture-basics/
├── pack.json
└── lesson.md
```

ZIP archives, deterministic archive bytes, signatures, registries, public distribution controls, static assets, claims files, source files, review files, and export are deferred.

### Minimum `pack.json`

```json
{
  "format_version": "0.1",
  "pack_id": "org.adaptive-learning.fixture-basics",
  "version": "0.1.0",
  "title": "Fixture Basics",
  "lesson": "lesson.md",
  "objectives": [
    {"id": "objective-one", "title": "Recognize the first concept"},
    {"id": "objective-two", "title": "Apply the second concept"}
  ],
  "questions": [
    {
      "id": "q-001",
      "type": "single_response",
      "objective_id": "objective-one",
      "prompt": "Which option demonstrates the first concept?",
      "options": [
        {"id": "a", "text": "Option A"},
        {"id": "b", "text": "Option B"}
      ],
      "correct_option_ids": ["a"],
      "explanation": "Option A is the reviewed fixture answer."
    }
  ]
}
```

The actual fixture adds four more questions while retaining this shape.

### Validation rules

`pack.validate` must reject a pack unless:

- `format_version` is exactly `0.1`;
- `pack_id`, `version`, `title`, and `lesson` are non-empty strings;
- `lesson` is a relative file name confined to the pack directory and names an existing UTF-8 Markdown file;
- objective and question IDs are unique non-empty strings;
- at least one objective and one question exist;
- every question references an existing objective;
- every question has at least two uniquely identified options;
- every correct option ID exists in that question;
- `single_response` has exactly one correct option;
- `multiple_response` has at least two correct options and at least one incorrect option;
- no unknown question type is present;
- no answer or explanation is empty.
- the directory contains only `pack.json` and the one referenced Markdown lesson.

Unknown top-level or record fields are errors in 0.1. This keeps drift visible.

### Pack digest

A digest is required to detect in-place pack changes across a session. It is not an archive or signing scheme.

1. Parse `pack.json`.
2. Normalize all strings to Unicode NFC.
3. Serialize JSON with sorted object keys, preserved array order, `ensure_ascii=false`, separators `,` and `:`, UTF-8, and no insignificant whitespace.
4. Normalize `lesson.md` to UTF-8 NFC with LF line endings and one terminal newline.
5. Compute SHA-256 over the `pack.json` canonical bytes prefixed by their eight-byte unsigned big-endian length, followed by the lesson bytes prefixed the same way.

`pack.install` copies the two validated files atomically into the local pack store and records the digest. A repeated install of the same `(pack_id, version, digest)` returns the existing receipt. The same `(pack_id, version)` with a different digest returns `PACK_VERSION_CONFLICT`.

## Minimal deterministic rules

### Single-response scoring

- Input is an array containing exactly one option ID.
- Duplicate or unknown option IDs are validation errors.
- Correct when the selected set exactly equals `correct_option_ids`.
- Result is binary: `is_correct` is `true` or `false`.
- No LLM, fuzzy match, partial credit, or confidence adjustment is used.

### Multiple-response scoring

- Input is a non-empty array of unique option IDs.
- An empty selection is invalid.
- One valid selected option is a valid submission and is scored normally; it is incorrect when it does not exactly match the complete answer set.
- Unknown or duplicate IDs are validation errors.
- Order does not affect scoring; the stored response is a canonical lexicographically sorted JSON array.
- Correct only when the selected set exactly equals `correct_option_ids`.
- Any missing correct option or selected distractor makes the response incorrect.
- No partial credit is calculated.

### Confidence

- `confidence` is required on every submission.
- It is an integer from 1 through 5.
- It is stored unchanged on the immutable attempt.
- It never changes correctness or selection in 0.1.

### Question selection

For the active session:

1. If a `presented` presentation exists without an attempt and its question is not challenged, return it unchanged.
2. Otherwise load pack questions whose IDs have not appeared in a non-challenged presentation in this session.
3. Exclude every question with a challenge row for this learner and pack version.
4. Sort remaining questions by `question_id` using Unicode code-point order.
5. Present the first question and commit the presentation before returning its prompt and options.

No randomness, due date, difficulty, mastery, or confidence affects 0.1 selection.

`question_digest` is SHA-256 over the canonical JSON bytes of the complete question record, using the same NFC, sorted-key, UTF-8, and compact-serialization rules as `pack.json`. If no eligible question remains, `study.next` returns `NO_ELIGIBLE_QUESTION` and does not mutate state.

### Objective progress

Each submitted question increments `attempts_count` for its one objective. A correct submission also increments `correct_count`. Status reports both counts and the display ratio `correct_count / attempts_count`; when attempts are zero, the ratio is `null`.

This is descriptive progress, not mastery or readiness.

### Challenge quarantine

- `question.challenge` identifies a question through a presentation, records one challenge row with a required human-supplied reason, and returns the quarantine receipt.
- A duplicate challenge returns the existing receipt without creating another row.
- If the presentation is unanswered, its status changes from `presented` to `challenged` in the same transaction.
- If it is already answered, the presentation and attempt remain unchanged.
- A challenge never rewrites or deletes an attempt and never changes objective progress.
- Any challenge row excludes that question from future selection for the learner and pack version.
- Challenge resolution and reactivation are deferred.

### Session resume

- At most one active session exists for the local learner.
- `study.start` returns the existing active session when asked to start the same installed pack.
- When no active session exists, `study.start` creates a new active session even if completed sessions exist for the same learner and pack version.
- `study.status` discovers the active session from SQLite and reports installed packs when no session is active.
- `study.next` returns an existing outstanding presentation before selecting another.
- A process restart has no special recovery file: the new process reopens SQLite and the installed pack path, checks the recorded digest, and continues.
- `study.finish` changes an active session to `completed`. Retrying it returns the completed summary.
- `study.finish` succeeds only when every non-quarantined question has an answered presentation and no presentation is outstanding; otherwise it returns `SESSION_NOT_FINISHABLE` without mutation.
- An unanswered presentation changed to `challenged` is resolved for finish eligibility because its question is quarantined; it does not need an attempt.

## Minimal SQLite schema

The first migration may contain only these eight tables. Foreign keys are enabled on every connection. All timestamps are RFC 3339 UTC strings generated by the core. IDs are application-generated opaque strings.

Required uniqueness includes the primary/unique keys stated below plus a partial unique index allowing at most one active `study_sessions` row per learner. `presentations` has unique `(session_id, ordinal)` and `(session_id, question_id)` constraints. `question_challenges` has a unique `(learner_id, pack_id, pack_version, question_id)` constraint.

Acceptance-test references correspond to the numbered tests below.

### `schema_meta`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `key` | text primary key | Finds `schema_version` after clean creation and restart (AT-01, AT-08). |
| `value` | non-null text | Stores the version value needed to open the database safely (AT-01, AT-08). |

### `learners`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `learner_id` | text primary key | Stable local identity across sessions/restarts (AT-03, AT-08, AT-09). |
| `display_name` | non-empty text | Confirms initialization returns the same human-readable learner (AT-03, AT-09). |
| `created_at` | non-null text | Distinguishes persisted initialization from conversational memory (AT-03, AT-08). |

### `installed_packs`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `pack_id` | composite primary key | Selects a subject without hard-coded subject logic (AT-02, AT-04). |
| `pack_version` | composite primary key | Pins the session to exact content (AT-04, AT-08). |
| `pack_digest` | 64-character text | Detects changed content before scoring/resume (AT-02, AT-08, AT-12). |
| `title` | non-empty text | Supplies installed-pack/session display context (AT-04, AT-09). |
| `install_path` | non-empty text | Reloads pack files after process restart (AT-08, AT-09). |
| `installed_at` | non-null text | Proves installation receipt persistence (AT-02, AT-08). |

### `study_sessions`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `session_id` | text primary key | Resumes the same practice session (AT-04, AT-08, AT-09). |
| `learner_id` | foreign key | Associates session with the persisted learner (AT-04, AT-09). |
| `pack_id` | composite foreign key | Loads the correct installed pack (AT-04, AT-09). |
| `pack_version` | composite foreign key | Prevents silent pack-version switching (AT-04, AT-08). |
| `status` | `active` or `completed` | Finds resumable work and makes finish retryable (AT-08, AT-09). |
| `started_at` | non-null text | Persists the session start fact (AT-04, AT-08). |
| `finished_at` | nullable text | Persists deterministic completion and retry result (AT-09). |

### `presentations`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `presentation_id` | text primary key | Binds submit/challenge to what was shown (AT-05, AT-06, AT-10). |
| `session_id` | foreign key | Orders and resumes questions within a session (AT-05, AT-09). |
| `ordinal` | positive integer, unique per session | Proves deterministic delivery order (AT-05, AT-09). |
| `question_id` | unique per session | Prevents repeated delivery and connects to pack/challenge state (AT-05, AT-11). |
| `question_digest` | 64-character text | Detects question mutation before scoring (AT-06, AT-12). |
| `status` | `presented`, `answered`, or `challenged` | Finds outstanding work and skips an unanswered challenge (AT-09, AT-10, AT-11). |
| `presented_at` | non-null text | Proves presentation was committed before return (AT-05, AT-08). |

### `attempts`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `attempt_id` | text primary key | Identifies the immutable scored fact (AT-06, AT-12). |
| `presentation_id` | unique foreign key | Guarantees at most one attempt per presentation and retry safety (AT-06, AT-12). |
| `selected_option_ids_json` | canonical non-null JSON text | Persists the exact normalized response for deterministic retry comparison (AT-06, AT-08, AT-12). |
| `is_correct` | integer 0 or 1 | Persists deterministic binary scoring (AT-06, AT-08). |
| `confidence` | integer 1 through 5 | Proves confidence survives restart (AT-07, AT-08). |
| `submitted_at` | non-null text | Establishes immutable attempt time (AT-06, AT-12). |

### `objective_progress`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `learner_id` | composite primary/foreign key | Separates progress by learner (AT-06, AT-09). |
| `pack_id` | composite primary/foreign key | Keeps progress subject-specific (AT-06, AT-09). |
| `pack_version` | composite primary/foreign key | Keeps progress version-specific (AT-06, AT-09). |
| `objective_id` | composite primary key | Reports progress for each of the two fixture objectives (AT-06, AT-09). |
| `attempts_count` | non-negative integer | Supplies simple descriptive coverage (AT-06, AT-09). |
| `correct_count` | integer from 0 through `attempts_count` | Supplies simple descriptive correctness (AT-06, AT-09). |
| `updated_at` | non-null text | Proves progress was transactionally persisted (AT-06, AT-08). |

### `question_challenges`

| Column | Constraint | Why / acceptance test |
|---|---|---|
| `challenge_id` | text primary key | Returns a stable quarantine receipt (AT-10). |
| `learner_id` | unique-key component/foreign key | Makes quarantine learner-local (AT-10, AT-11). |
| `pack_id` | unique-key component/foreign key | Scopes quarantine to a subject (AT-10, AT-11). |
| `pack_version` | unique-key component/foreign key | Avoids carrying a challenge silently into changed content (AT-10, AT-11). |
| `question_id` | unique-key component | Excludes the exact question from selection (AT-10, AT-11). |
| `presentation_id` | foreign key | Shows which delivered item caused the challenge (AT-10). |
| `reason` | non-empty text | Preserves the learner's quality report without agent invention (AT-10). |
| `challenged_at` | non-null text | Persists quarantine across restart (AT-10, AT-11). |

### Transaction boundaries

- `study.next`: insert a new presentation before returning it; retries return an existing outstanding row.
- `study.submit`: validate response, insert the attempt, mark presentation answered, and upsert objective progress in one transaction.
- `question.challenge`: insert the challenge and, when unanswered, mark the presentation challenged in one transaction.
- `study.finish`: mark session completed once; retries read the completed row.

### Deferred schema

Do not implement in 0.1:

- `authoring_projects`;
- `attempt_objectives` or detailed objective-delta history;
- `item_progress`, Leitner boxes, due dates, or scheduler state;
- generic `idempotency_results`;
- generic `audit_events`;
- event-sourced or rebuildable projection machinery;
- backup manifests, restore history, or advanced backup/restore operations;
- credential, chat transcript, memory, evidence-review, or source-content tables.

The eight-table schema is deliberately disposable until real migrations begin. A one-step schema version still proves clean creation and restart.

## Minimal tool contract 0.1

### Envelope

Requests:

```json
{"contract_version":"0.1","tool":"study.next","arguments":{"session_id":"session-1"}}
```

Success:

```json
{"ok":true,"result":{}}
```

Error:

```json
{"ok":false,"error":{"code":"SESSION_NOT_ACTIVE","message":"The session is not active.","retryable":false}}
```

No generic request ID or idempotency key is required in 0.1. Retry safety comes from unique constraints and operation-specific comparison rules.

### `system.health`

Request:

```json
{"contract_version":"0.1","tool":"system.health","arguments":{}}
```

Response:

```json
{"ok":true,"result":{"status":"ok","contract_version":"0.1","schema_version":"1","pack_format_versions":["0.1"]}}
```

### `learner.initialize`

Request:

```json
{"contract_version":"0.1","tool":"learner.initialize","arguments":{"display_name":"Alex"}}
```

Response:

```json
{"ok":true,"result":{"learner_id":"learner-1","display_name":"Alex","created":true}}
```

If a learner already exists, return it with `created:false`. Do not create or update another profile.

### `pack.validate`

Request:

```json
{"contract_version":"0.1","tool":"pack.validate","arguments":{"source_path":"C:/packs/fixture-basics"}}
```

Response:

```json
{"ok":true,"result":{"valid":true,"pack_id":"org.adaptive-learning.fixture-basics","pack_version":"0.1.0","pack_digest":"<sha256>","objective_count":2,"question_count":5,"diagnostics":[]}}
```

This tool is read-only.

### `pack.install`

Request:

```json
{"contract_version":"0.1","tool":"pack.install","arguments":{"source_path":"C:/packs/fixture-basics"}}
```

Response:

```json
{"ok":true,"result":{"pack_id":"org.adaptive-learning.fixture-basics","pack_version":"0.1.0","pack_digest":"<sha256>","title":"Fixture Basics","installed":true}}
```

An identical retry returns the receipt with `installed:false`. A version/digest mismatch fails.

### `study.start`

Request:

```json
{"contract_version":"0.1","tool":"study.start","arguments":{"learner_id":"learner-1","pack_id":"org.adaptive-learning.fixture-basics","pack_version":"0.1.0"}}
```

Response:

```json
{"ok":true,"result":{"session_id":"session-1","status":"active","resumed":false,"pack":{"pack_id":"org.adaptive-learning.fixture-basics","version":"0.1.0","title":"Fixture Basics"},"lesson_markdown":"# Fixture Basics\n...","answered_count":0,"eligible_count":5}}
```

Starting the same pack while its session is active returns that session with `resumed:true`.

### `study.next`

Request:

```json
{"contract_version":"0.1","tool":"study.next","arguments":{"session_id":"session-1"}}
```

Response:

```json
{"ok":true,"result":{"presentation_id":"presentation-1","ordinal":1,"question":{"question_id":"q-001","type":"single_response","prompt":"Which option demonstrates the first concept?","options":[{"id":"a","text":"Option A"},{"id":"b","text":"Option B"}],"objective":{"id":"objective-one","title":"Recognize the first concept"}}}}
```

The response contains no correct option IDs or explanation. A retry returns the same outstanding presentation.

### `study.submit`

Request:

```json
{"contract_version":"0.1","tool":"study.submit","arguments":{"session_id":"session-1","presentation_id":"presentation-1","selected_option_ids":["a"],"confidence":4}}
```

Response:

```json
{"ok":true,"result":{"attempt_id":"attempt-1","is_correct":true,"confidence":4,"correct_option_ids":["a"],"explanation":"Option A is the reviewed fixture answer.","objective_progress":{"objective_id":"objective-one","attempts_count":1,"correct_count":1}}}
```

An exact retry returns the original result. A different response or confidence for the same presentation returns `ATTEMPT_CONFLICT`.

### `study.status`

Request:

```json
{"contract_version":"0.1","tool":"study.status","arguments":{"learner_id":"learner-1"}}
```

Response:

```json
{"ok":true,"result":{"active_session":{"session_id":"session-1","pack_id":"org.adaptive-learning.fixture-basics","pack_version":"0.1.0","answered_count":1,"remaining_count":4,"outstanding_presentation_id":null},"objective_progress":[{"objective_id":"objective-one","attempts_count":1,"correct_count":1,"correct_ratio":1.0}],"installed_packs":[{"pack_id":"org.adaptive-learning.fixture-basics","pack_version":"0.1.0","title":"Fixture Basics"}]}}
```

No attempt response, confidence history, answer key, database path, or challenge reason is included in the context summary.

### `study.finish`

Request:

```json
{"contract_version":"0.1","tool":"study.finish","arguments":{"session_id":"session-1"}}
```

Response:

```json
{"ok":true,"result":{"session_id":"session-1","status":"completed","answered_count":5,"correct_count":4}}
```

Retrying a completed session returns the same persisted summary.

### `question.challenge`

Request:

```json
{"contract_version":"0.1","tool":"question.challenge","arguments":{"session_id":"session-1","presentation_id":"presentation-1","reason":"The wording is ambiguous."}}
```

Response:

```json
{"ok":true,"result":{"challenge_id":"challenge-1","question_id":"q-001","quarantined":true,"created":true}}
```

Retrying returns the same row with `created:false`.

## Mutation retry matrix

| Tool | Retry rule without generic idempotency storage |
|---|---|
| `learner.initialize` | Singleton learner row; return existing. |
| `pack.install` | Unique `(pack_id, version)`; same digest returns existing, changed digest conflicts. |
| `study.start` | Return active session for same learner/pack; conflicting active pack fails. |
| `study.next` | Return outstanding non-challenged presentation before inserting. |
| `study.submit` | Unique attempt per presentation; identical canonical payload returns existing, changed payload conflicts. |
| `study.finish` | Completed row returns its stored summary. |
| `question.challenge` | Unique learner/pack-version/question row; return existing. |

This covers concrete lost-response and repeated-tool-call failures without a generic subsystem.

## Hermes boundary

The responsibility split in ADR 0007 is accepted for 0.1:

- The Hermes plugin registers the ten tool schemas and invokes the deterministic application service.
- Hermes-safe registered names may use underscores, such as `ala_study_next`, while mapping exactly to the dotted runtime-neutral operation.
- The plugin validates adapter-level arguments and passes structured results; it does not tutor, choose pedagogy, score, query SQLite directly outside the service, or perform free-form reasoning.
- The Hermes skill supplies conversational workflow and pedagogy: introduce the lesson, ask when the learner is ready, call the next tool, request confidence, present feedback, and offer challenge language.
- Skills do not read/write SQLite or parse pack files directly.
- Hermes owns models, providers, authentication, Codex OAuth, and credential refresh.
- Adaptive Learning Agent does not access or store `~/.hermes/auth.json`, `~/.codex/auth.json`, access tokens, or refresh tokens.

Use Hermes v0.18.2 as the first compatibility-test target because it is the latest tagged release verified in the repository's official-documentation review. This is a test target, not a claim of compatibility. Installation, plugin discovery, enablement, reload/restart, tool registration, and skill loading must be demonstrated on an actual v0.18.2 installation before compatibility is documented.

## Fresh-conversation and restart context

### Bootstrap calls

A fresh Hermes conversation does not rely on prior chat or Hermes memory for learning state:

1. Call `system.health`.
2. Call `learner.initialize`; it returns the existing local learner.
3. Call `study.status` for that learner.
4. If an active session exists, call `study.next`; it returns the outstanding presentation or selects the next eligible question.
5. If no active session exists, use `installed_packs` from status and call `study.start` after learner confirmation.

### Minimal context packet

Load only:

- learner ID and display name;
- active session ID and status, if any;
- pack ID, version, title, and recorded digest status;
- answered, remaining, and challenged counts;
- per-objective attempt/correct counts;
- the one outstanding question's presentation ID, prompt, options, type, and objective label when resuming;
- the last tool result only when it is needed to continue immediate feedback.

Do not load:

- full attempt history or raw prior responses;
- confidence history beyond aggregate-free storage;
- answer keys or explanations for unpresented questions;
- the entire pack or lesson on every turn;
- SQLite paths, SQL rows, digests unrelated to the active pack, logs, or audit history;
- Hermes memory as a substitute for any persisted value;
- provider configuration or OAuth credentials.

Full attempts and confidence remain only in SQLite. Questions, answers, explanations, objectives, and lesson content remain only in installed pack files. The fresh-session packet is a transient rendering of tool results and is never authoritative.

## Acceptance tests

### AT-01: Clean install

Given an empty temporary user-data directory, start the core without Hermes. It creates one SQLite database containing schema version `1` and only the eight approved tables. `system.health` returns `ok`. No network or runtime dependency is required.

### AT-02: Fixture pack validation

Validate the manually authored unpacked fixture. Assert format `0.1`, two objectives, one readable lesson, five questions with the required 3/2 type split, valid cross-references, and a stable digest. Mutate a correct option to an unknown ID and assert deterministic rejection. Install the valid fixture and verify the recorded receipt.

### AT-03: Learner initialization

Initialize learner `Alex`. Assert one row is created. Repeat after closing/reopening the service and assert the same learner ID returns with no second row.

### AT-04: Session start

Start practice for the installed fixture. Assert one active session pins learner, pack ID, version, and returns the lesson. Repeat and assert the same session is resumed rather than duplicated.

### AT-05: Question delivery without answer leakage

Call `study.next`. Assert the presentation row exists before the result is observed. Assert the result contains prompt/options/objective but no `correct_option_ids`, explanation, or hidden answer field. Repeat and assert the same presentation returns.

### AT-06: Deterministic submission

Submit one single-response and one multiple-response item. Assert exact-set correct answers produce `is_correct:true`; a missing selection or extra distractor produces `false`; option order does not affect multiple-response correctness. Assert no model or network call is made and objective counts update in the same transaction.

### AT-07: Confidence persistence

Submit confidence values 1 and 5 on separate questions. Read attempts through the repository/test boundary and assert the exact integers are stored and do not affect correctness.

### AT-08: Process restart

Close all database connections and discard every in-memory service object. Start a new process/service instance using the same user-data path. Assert learner, installed pack, active session, presentations, attempts, confidence, progress, and challenges remain available and the pack digest is rechecked.

### AT-09: Session resume

After restart, use only `learner.initialize`, `study.status`, and `study.next`. Assert the same active session is found, aggregate counts match SQLite, and an outstanding presentation is returned unchanged. No prior conversation text is supplied.

### AT-10: Question challenge

Challenge a delivered question with a non-empty reason. Assert one challenge row is committed. If unanswered, assert its presentation becomes `challenged`. Retry and assert the same challenge returns without duplication.

### AT-11: Quarantined question exclusion

Continue the active session and then start a new session after completion. Assert the challenged question is never selected for that learner and pack version while the other four questions remain eligible in a new session.

### AT-12: Attempt immutability

Retry a prior `study.submit` with the same canonical selections and confidence; assert the original attempt ID/result returns and the row count is unchanged. Retry with a different response or confidence; assert `ATTEMPT_CONFLICT`. Challenge the answered question and assert its attempt and objective counts remain unchanged. Direct update/delete methods for attempts are absent.

### Compatibility checks outside the core 12

- Register the ten tools in a Hermes v0.18.2 test installation, execute health/start/next/submit through the plugin, and confirm results match direct core calls. Record any installation or restart differences before claiming support.
- Inspect the core, schema, and pack validation for subject-specific constants. Pack identity/objectives/questions must be data-driven so a later second pack requires content, not a core branch.

## Explicit deferrals

- Conversational subject building and all authoring tools.
- AWS SAP-C02 and US Amateur Extra functional packs.
- Evidence-required release validation, sources, claims, reviews, and challenges as editorial adjudication.
- Numeric, short-answer, free-text, or model-assisted scoring.
- Partial credit.
- Mastery, readiness, calibration, FSRS, Leitner, due dates, and review scheduling.
- Multiple learners, learner editing, authentication, or hosting.
- Pack ZIP import/export, canonical archive bytes, signatures, registries, and marketplace behavior.
- Generic idempotency storage and generic audit events.
- Event sourcing, projection rebuilds, and objective-delta history.
- Advanced backup, restore, repair, and migration frameworks beyond schema version 1 creation.
- MCP, web/API server, UI, background jobs, and cloud deployment.
- Challenge resolution, reviewer workflow, or content reactivation.

## Definition of done

The runtime-independent core is complete when AT-01 through AT-12 pass without Hermes or an LLM, a clean process restart resumes state using only SQLite and pack files, and no deferred feature has been added. Full version-0.1 runtime compatibility additionally requires the separately scoped Hermes v0.18.2 plugin check; that adapter work is not part of the core implementation task.
