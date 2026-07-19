# Current Status

Status: pre-alpha / version 0.1.0 released; version 0.2A E1A pilot independently approved and acceptance-verified
Updated: 2026-07-19

## Released baseline

Version 0.1.0 proved the runtime-independent deterministic Python core, local SQLite state, strict portable pack input, runtime-neutral JSON tool contract, and thin Hermes adapter. The synthetic `fixture-basics` pack remains test data, not examination preparation. See [the 0.1.0 release record](releases/0.1.0.md).

## Version 0.2A outcome

Accepted ADR 0009 is implemented in a subject-neutral format-0.2 parser, immutable records, digest/install path, and additive contract-0.1 provenance. Format 0.1, SQLite schema 1, scoring, sessions, retries, progress, and quarantine remain unchanged.

The approved `amateur-extra-e1a` pack contains exactly two objectives, two ordered original lessons, E1A01–E1A11, zero generated questions, and no assets. Its approved digest is `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`. Anthony McClure completed all nine human-review scopes and gave an overall PASS at `2026-07-19T01:12:29.8952607Z`, including explicit acceptance of preserving the official E1A06 locator while citing the current operative rule in project prose.

Verification completed:

- Fresh authoritative NCVEC and eCFR snapshots matched the declared hashes and current revision identities.
- All eleven official records matched the fresh NCVEC DOCX exactly by ID, prompt, ordered option labels/text, answer key, and printed locator.
- The approved golden fixture detects omissions, extras, duplicate IDs, punctuation/Unicode changes, option reorder/text changes, key changes, and locator changes.
- The 45-test standard-library suite passed on CPython 3.12.13, 3.13.14, and 3.14.6; measured statement coverage was 87% (1,064 statements, 141 missed).
- Hosted GitHub Actions passed all three Python jobs for implementation commit `2c3d364df410a9408e9c4f558d23904749de5207`.
- Real pinned Hermes v0.18.2 acceptance passed validation/install, ordered lessons, answer-safe question display, confidence scoring, post-answer explanation/source display, independent restart reconstruction, challenge quarantine, and immutable retry rejection.

See [the independent-review handoff](handoffs/amateur-extra-0.2-independent-review.md) and [release-readiness handoff](handoffs/amateur-extra-0.2-release-readiness.md). This is release-readiness evidence, not a release or tag.

## Architecture boundary proven

- Python owns pack validation, deterministic selection and scoring, persistence, challenge quarantine, and progress counts.
- SQLite is authoritative for learner state; model conversation and agent memory are not.
- The Hermes plugin delegates exactly ten operations to the public core and owns no subject logic or storage.
- The JSON-compatible contract and Python core import no Hermes, MCP, model-provider, or network clients.
- Format 0.2 added sourced content without changing SQLite schema 1 or embedding Amateur Extra constants in the core or adapter.

## Known limitations

- One local learner and at most one active session are supported; multi-user hosting and concurrent-process guarantees are absent.
- The workflow is practice only: no mastery, scheduling, readiness prediction, or exam simulation.
- E1A is one question group, not a complete Amateur Extra course or examination-preparation claim.
- There is no conversational subject builder, evidence-review administration, application backup/restore, or encryption at rest.
- Project-local Hermes discovery is trusted-checkout development behavior and requires a process-local gate.
- Compatibility is verified only for Hermes v0.18.2 Windows CLI/profile, not Linux, macOS, Desktop, gateway, or other Hermes versions.
- Formal legal review has not been claimed; the accepted rights policy is project policy, not legal advice.

## Deferred

Subject building, AWS content, expansion beyond E1A, scheduling, mastery, readiness, exam simulation, YAML, archives, export ergonomics, signing, marketplaces, broader Hermes distribution, hosted identity, servers, cloud deployment, and stronger local-process isolation remain deferred.
