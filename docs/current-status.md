# Current Status

Status: pre-alpha / version 0.2.0-alpha.1 sourced-content pilot published as a pre-release
Updated: 2026-07-19

## Released baseline

Version 0.1.0 proved the runtime-independent deterministic Python core, local SQLite state, strict portable pack input, runtime-neutral JSON tool contract, and thin Hermes adapter. The synthetic `fixture-basics` pack remains test data, not examination preparation. See [the 0.1.0 release record](releases/0.1.0.md).

## Version 0.2.0-alpha.1 release

Accepted ADR 0009 is implemented in a subject-neutral format-0.2 parser, immutable records, digest/install path, and additive contract-0.1 provenance. Format 0.1, SQLite schema 1, scoring, sessions, retries, progress, and quarantine remain unchanged.

The approved `amateur-extra-e1a` pack contains exactly two objectives, two ordered original lessons, E1A01–E1A11, zero generated questions, and no assets. Its approved digest is `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`. Anthony McClure completed all nine human-review scopes and gave an overall PASS at `2026-07-19T01:12:29.8952607Z`, including explicit acceptance of preserving the official E1A06 locator while citing the current operative rule in project prose.

Verification completed:

- Fresh authoritative NCVEC and eCFR snapshots matched the declared hashes and current revision identities.
- All eleven official records matched the fresh NCVEC DOCX exactly by ID, prompt, ordered option labels/text, answer key, and printed locator.
- The approved golden fixture detects omissions, extras, duplicate IDs, punctuation/Unicode changes, option reorder/text changes, key changes, and locator changes.
- The 45-test standard-library suite passed on CPython 3.12.13, 3.13.14, and 3.14.6; measured statement coverage was 87% (1,064 statements, 141 missed).
- Hosted GitHub Actions passed all three Python jobs for implementation commit `2c3d364df410a9408e9c4f558d23904749de5207`.
- Real pinned Hermes v0.18.2 acceptance passed validation/install, ordered lessons, answer-safe question display, confidence scoring, post-answer explanation/source display, independent restart reconstruction, challenge quarantine, and immutable retry rejection.

See [the independent-review handoff](handoffs/amateur-extra-0.2-independent-review.md) and [release-readiness handoff](handoffs/amateur-extra-0.2-release-readiness.md).

The approved pilot is published as the `v0.2.0-alpha.1` annotated tag and GitHub pre-release. See [the release record](releases/0.2.0-alpha.1.md). The Python distribution version is the PEP 440 equivalent `0.2.0a1`.

## Architecture boundary proven

- Python owns pack validation, deterministic selection and scoring, persistence, challenge quarantine, and progress counts.
- SQLite is authoritative for learner state; model conversation and agent memory are not.
- The Hermes plugin delegates exactly ten operations to the public core and owns no subject logic or storage.
- The JSON-compatible contract and Python core import no Hermes, MCP, model-provider, or network clients.
- Format 0.2 added sourced content without changing SQLite schema 1 or embedding Amateur Extra constants in the core or adapter.

## Next-phase design checkpoint

Documentation now proposes two separate future lines:

- **0.2B** is a bounded official Amateur Extra static-asset pilot. E7B is the research-first candidate, with E7D and E9B as fallbacks, but no question/figure has been imported and no format change is accepted.
- **0.3A–C** progresses from assessment/curriculum research, to a manually reviewed five-question SAP-C02 slice, to agent-assisted construction with mandatory human gates.

Proposed ADRs 0010–0013 cover whole learning architecture with progressive realization, assessment authenticity and official-question reuse, capability discovery with controlled activation, and evidence-backed authored questions with layered approval. They are **Proposed**, not Accepted. They do not authorize implementation.

The target Subject Builder flow now distinguishes learning architecture from realization plans, guides partial learner scope through dependency categories, researches assessment grammar automatically, seeks optional capabilities by role, and degrades gracefully when evidence or access is insufficient. External capabilities remain optional to the core and packs.

See [Subject Builder architecture](subject-builder-architecture.md), [assessment policy](assessment-research-policy.md), [curriculum planning](curriculum-planning.md), [capability discovery](capability-discovery.md), [asset pilot plan](amateur-extra-asset-pilot-plan.md), and [SAP-C02 plan](aws-sap-c02-pilot-plan.md).

## Known limitations

- One local learner and at most one active session are supported; multi-user hosting and concurrent-process guarantees are absent.
- The workflow is practice only: no mastery, scheduling, readiness prediction, or exam simulation.
- E1A is one question group, not a complete Amateur Extra course or examination-preparation claim.
- There is no conversational subject builder, evidence-review administration, application backup/restore, or encryption at rest.
- Project-local Hermes discovery is trusted-checkout development behavior and requires a process-local gate.
- Compatibility is verified only for Hermes v0.18.2 Windows CLI/profile, not Linux, macOS, Desktop, gateway, or other Hermes versions.
- Formal legal review has not been claimed; the accepted rights policy is project policy, not legal advice.

## Deferred

Implementation of asset support, subject building, assessment/curriculum artifacts, capability discovery, AWS content, expansion beyond E1A, scheduling, mastery, readiness, exam simulation, YAML, archives, export ergonomics, signing, marketplaces, broader Hermes distribution, hosted identity, servers, cloud deployment, and stronger local-process isolation remains deferred. No MCP server, connector, AWS access, diagram content, new pack field/tool, database change, or Hermes workflow change was added by the next-phase design.
