# Final MVP Design Review Handoff

Date: 2026-07-18
Outcome: Version 0.1 accepted for a separately invoked implementation task

## Acceptance recommendations

Accept [`mvp-vertical-slice.md`](../mvp-vertical-slice.md) as the only implementation scope for version 0.1. It proves the architectural risks with one synthetic fixture pack, one learner, practice mode, exact deterministic scoring, confidence storage, SQLite persistence, learner-local challenge quarantine, process/conversation restart, and a thin Hermes adapter.

Accept the following concrete decisions:

- JSON plus Markdown in an unpacked directory; no YAML parser or archive in 0.1.
- Python 3.12 standard library only at runtime.
- Five fixture questions across two objectives and one lesson; three single-response and two multiple-response.
- Binary exact-set scoring, stable question-ID selection, and descriptive attempt/correct counts only.
- Eight SQLite tables, each column justified by AT-01 through AT-12.
- Ten runtime-neutral JSON tools with operation-specific retry safety.
- Challenges quarantine content without mutating attempts or progress.
- SQLite and installed pack files are authoritative; agent memory is never authoritative.
- A Hermes plugin exposes deterministic tools; a Hermes skill supplies conversational workflow only.
- Hermes v0.18.2 is the first compatibility-test target, not an unverified support claim.

## Deliberate deferrals

- Conversational pack authoring and publishing.
- AWS SAP-C02 and US Amateur Extra content.
- Evidence sources, claims, reviews, currency gates, and editorial challenge resolution.
- YAML, ZIP import/export, assets, signing, registries, and marketplace behavior.
- Numeric, short-answer, free-text, partial-credit, or model-assisted scoring.
- Mastery, readiness, FSRS, Leitner, due dates, scheduling, calibration, or adaptive difficulty.
- Multiple learners, authentication, hosting, server/API, UI, background workers, MCP, or cloud deployment.
- Generic idempotency and audit stores, event sourcing, objective deltas, projection rebuilding, and advanced backup/restore.
- Challenge resolution/reactivation and pack-version migration.

## Documents changed

- Added `docs/mvp-vertical-slice.md`.
- Focused `docs/mvp-requirements.md`, `docs/architecture.md`, `docs/evidence-policy.md`, `docs/pack-format.md`, `docs/sqlite-schema.md`, `docs/tool-contract.md`, `docs/hermes-integration.md`, and `docs/test-plan.md` on the accepted 0.1 overlay while preserving broader proposals as deferred material.
- Updated `docs/current-status.md` with the design decision and narrowly conditional implementation authorization.
- Added this handoff.

## ADRs

- [ADR 0007](../decisions/0007-hermes-plugin-skill-boundary.md): accepted Hermes plugin and skill responsibility boundary.
- [ADR 0008](../decisions/0008-json-markdown-pack-serialization.md): accepted JSON plus Markdown for version 0.1.

ADRs 0001 through 0006 remain accepted. ADR 0008 narrows the serialization allowed by ADRs 0001 and 0005 for the first slice; it does not reverse their portable file-pack decision.

## Blockers and unverified items

There is no design blocker to direct-core implementation.

Hermes compatibility is not yet verified. The official-documentation review identified v0.18.2 as the first target, but actual local project installation, plugin discovery/enablement, tool registration, skill loading, and CLI/Desktop restart behavior must be tested against that release. If the target installation is unavailable, core completion may be reported but version-0.1 completion and Hermes compatibility must not be claimed.

The permanent security-reporting address, final project/package naming, future pack licensing, and future YAML parser remain unresolved but do not block the synthetic vertical slice.

## Exact prompt for the first implementation task

```text
Read AGENTS.md and every required context document in its precedence order. Then implement only the accepted version-0.1 scope in docs/mvp-vertical-slice.md, ADR 0007, and ADR 0008.

Use Python 3.12 and the standard library only at runtime. Create exactly one synthetic unpacked fixture pack with pack.json, one Markdown lesson, two objectives, and five questions in the required 3-single/2-multiple split. Implement only the eight approved SQLite tables, their constraints and transaction boundaries, the deterministic runtime-independent core, and the ten version-0.1 JSON tools. Keep attempts immutable, make challenge quarantine learner- and pack-version-local, and implement the documented operation-specific retry behavior without a generic idempotency or audit subsystem.

Write AT-01 through AT-12 first and make them pass without Hermes, an LLM, a network, or agent memory. Then add only the thin Hermes plugin and minimal conversational workflow skill described by ADR 0007. Exercise system health, study start, next, and submit through a real Hermes v0.18.2 installation and compare them with direct core calls. If that Hermes installation or a documented API is unavailable, stop at the adapter boundary, mark the exact behavior unverified, and do not claim compatibility.

Do not implement YAML, archives, signing, authoring, evidence workflows, AWS SAP-C02 or US Amateur Extra packs, additional scoring types, partial credit, mastery, readiness, scheduling, multiple learners, generic idempotency/audit, event sourcing, backup/restore, MCP, an API server, a web UI, background jobs, or cloud deployment. Do not modify Hermes provider configuration or access/store Hermes or Codex OAuth credentials. Do not publish a pack or release.

Preserve runtime independence: SQLite and installed pack files are authoritative, and the core must import no Hermes code. Update docs/current-status.md and create a focused implementation handoff with tests run, compatibility evidence, deviations, and remaining blockers. Commit and push the focused implementation only after reviewing the diff for deferred scope.
```

## Implementation statement

This review contains documentation and decisions only. It does not create implementation modules, database migrations, schemas, fixture packs, functional skills, install packages, or modify Hermes configuration.
