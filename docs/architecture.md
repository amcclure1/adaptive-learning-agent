# Architecture

Status: proposed for review  
Design baseline: 2026-07-18

## System shape

```text
Learner
   |
   v
Hermes conversation
   |
   v
Thin Hermes plugin  ---- same JSON contract ----> CLI / future runtime adapter
   |                                             
   v
Application services: study, authoring, packs, reporting
   |                    |                  |
   v                    v                  v
Deterministic engine  Pack validator    Evidence policy
   |                    |                  |
   +--------------------+------------------+
                        |
                repositories + transactions
                   |                    |
                   v                    v
              SQLite state       YAML/Markdown packs
```

The dependency arrow always points inward: `adapters -> application -> domain`. Infrastructure implements domain interfaces. `domain` and `pack_format` MUST NOT import Hermes, a model SDK, or plugin code.

## Components

### Domain

Pure Python types and functions for answers, scoring, objective evidence, mastery updates, scheduling, selection, evidence rules, and validation diagnostics. Domain functions receive time and random seed as arguments; they do not read the clock, filesystem, environment, or database directly.

### Application services

Use cases coordinate domain functions and transaction boundaries:

- learner profile management;
- study start/next/submit/status;
- draft authoring and review;
- pack validate/install/export/list;
- backup and integrity reporting.

Each mutating use case accepts an idempotency key and produces a JSON-serializable result.

### Pack subsystem

Reads a directory or safe archive, parses YAML and Markdown, normalizes paths and line endings, validates cross-references, evaluates evidence/review gates, and computes a canonical SHA-256 digest. It never executes pack content. Installed pack files remain immutable and are read by exact version and digest.

YAML requires a small parser dependency because the Python standard library does not provide one. All other proposed MVP primitives—SQLite, JSON, hashing, ZIP handling, timestamps, decimal parsing, UUIDs, and filesystem operations—are available in the standard library.

### Persistence

SQLite stores learner profiles, sessions, presentations, attempts, progress projections, installed-pack receipts, idempotency results, and audit events. Pack content stays on disk. Attempt facts are append-only; derived progress can be rebuilt from attempts if the projection algorithm changes.

Recommended connection settings are `PRAGMA foreign_keys=ON`, a bounded busy timeout, WAL mode for normal local use, and explicit transactions. Backup uses the SQLite backup API. WAL is an implementation choice to verify on network-synchronized folders; the default data directory should be local rather than inside a cloud-sync folder.

### Runtime-neutral tool service

The service exposes the contract in `docs/tool-contract.md` as in-process Python calls and newline-delimited or one-shot JSON through a CLI. It returns typed errors and never prints conversational prose on the JSON channel. This boundary is the conformance target for every adapter.

### Hermes adapter

A minimal Hermes plugin registers tool schemas and handlers, maps calls to the tool service, and returns its structured JSON. It contains no scoring, SQL, scheduling, pack validation, or evidence judgment. Hermes is responsible for conversation and may render explanations; the plugin is responsible for faithfully passing tool results.

Official Hermes documentation recommends plugins for user or project custom tools and describes `ctx.register_tool()` as the registration surface. General plugins are opt-in. See [Hermes Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md) and [Build a Hermes Plugin](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/build-a-hermes-plugin.md).

### Hermes skill

The integration may also ship a small skill that teaches conversational workflows and requires the Adaptive Learning toolset. It is guidance only: it does not contain answer keys or state. Hermes skills are on-demand documents under `~/.hermes/skills/`, use progressive disclosure, and can be created or changed by the agent, so the skill cannot be a trust boundary. See the official [Hermes Skills System](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).

## Data ownership

| Data | Canonical owner | Not authoritative |
|---|---|---|
| Scores and due dates | Python domain rules + recorded rule version | Agent narrative |
| Attempts and progress | SQLite | Hermes session/memory |
| Pack content and answer keys | Installed pack files by digest | SQLite caches, model recall |
| Evidence acceptability | Pack policy + validator + human review | URL presence alone |
| Conversation wording | Hermes | Scoring or persisted facts |
| OAuth/provider credentials | Hermes-managed credential store | This project |

The project MUST NOT read, copy, log, export, or refresh provider credentials.

## Deterministic scoring and scheduling v1

All stored fractions use integer millionths from 0 to 1,000,000.

### Item scoring

- `single_choice`: 1,000,000 for exact option ID match; otherwise 0.
- `multiple_choice`: exact mode by default. Optional declared partial mode computes `(correct selected - incorrect selected) / correct options`, clamped to `[0,1]`; the pack must opt in and the rule version is recorded.
- `numeric`: 1,000,000 when the Decimal-parsed response is inside the declared inclusive absolute or relative tolerance; otherwise 0. Units are declared and normalized from an explicit alias map.
- `short_answer`: normalize Unicode, case, surrounding whitespace, and declared punctuation rules, then require an exact match to one of the reviewed accepted forms. No semantic model judgment.

`is_correct` is true only when the fixed-point score equals 1,000,000. Confidence is learner-reported on an integer 1-5 scale and does not change correctness.

### Objective mastery projection

Each question's objective weights sum to 1,000,000. For each affected objective:

```text
alpha = max(100000, 300000 - 50000 * min(prior_evidence_count, 4))
effective_alpha = round_half_up(alpha * objective_weight / 1000000)
new_mastery = old_mastery + round_half_up(effective_alpha * (score - old_mastery) / 1000000)
```

An unseen objective starts at 0 with zero coverage. The algorithm version is stored on every attempt. Readiness requires both a pack-defined mastery threshold and a pack-defined minimum evidence count; a high score from one question is not sufficient.

### Item scheduling

The v1 Leitner intervals are 0, 1, 3, 7, 14, and 30 days for boxes 0-5.

- Perfect score with confidence 4-5: advance two boxes, maximum 5.
- Perfect score with confidence 1-3: advance one box.
- Partial score: move down one box, minimum 0.
- Zero score: reset to box 0.
- Due time is `answered_at + interval[new_box]`; box 0 is immediately due but selection deprioritizes the just-answered item within the same session.

Next-item selection sorts eligible items by: overdue status, lowest objective mastery, fewest exposures, oldest last-seen time, stable question ID. A seeded hash of `(session_id, ordinal, question_id)` may break an otherwise exact tie. This policy is deliberately simple and replaceable through versioned algorithms.

## Core workflows

### Study

1. Start pins learner, pack ID/version/digest, algorithm versions, locale, and seed.
2. Next selects a question and commits a presentation row before returning prompt-safe content.
3. Submit verifies the outstanding presentation and question hash, scores, records the immutable attempt, updates projections, and commits once.
4. The adapter returns the authoritative result and reviewed rationale to Hermes.
5. Hermes explains conversationally without changing the result.

### Authoring

1. Create a draft directory with a generated pack ID and declared evidence mode.
2. Add source and objective records, then Markdown notes and deterministic questions.
3. Validate after every mutation; preserve diagnostics with file and logical path.
4. Compute the question digest and request explicit human review.
5. Accepted review binds to that digest; any content change invalidates it.
6. Release validation applies evidence and review policy.
7. Export creates a deterministic archive. No operation publishes or uploads it.

### Install

1. Copy an archive or directory into a temporary staging area.
2. Reject unsafe archive entries and resource-limit violations before extraction.
3. Parse and validate all canonical files without executing content.
4. Compute the digest and reject version/digest conflicts.
5. Atomically move the validated directory into the local pack store and record an install receipt.

## Failure and recovery

- Every error uses a stable type, code, human message, retryability flag, and structured details.
- A model/provider failure cannot roll back a committed attempt; resuming the session reads SQLite.
- A database failure returns no apparent success. Transaction boundaries make partial scoring impossible.
- If a pack is unavailable, historical state remains visible by IDs and digests; scoring new answers is blocked.
- Progress projections are rebuildable from immutable attempts and installed historical pack versions.
- Import, restore, migration, and pack install always stage and validate before replacing live state.

## Security boundaries

- Packs are data, never code.
- Archive paths are normalized and constrained beneath a staging root; symlinks and device files are rejected.
- Size, file-count, compression-ratio, and YAML alias/depth limits protect local resources.
- Markdown HTML is treated as text in the MVP.
- Answer keys are not returned by `study.next`.
- Tool handlers validate every argument even if Hermes supplied a schema.
- Authoring and administrative tools are separate from learner-mode tools so a prompt cannot silently approve its own question.
- Logs use IDs and result codes; raw responses and pack answer keys are redacted by default.

## Deferred extension points

- Another conversational runtime adapter.
- A local stdio MCP adapter. Hermes officially supports local stdio and remote HTTP MCP servers, but an MCP process adds no MVP value over the in-process plugin and JSON CLI. See [Hermes MCP](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md).
- Additional scheduling algorithms through explicit version migrations.
- Signed packs and maintainer trust roots.
- Optional non-authoritative semantic feedback on essays.
