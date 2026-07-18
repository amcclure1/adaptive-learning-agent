# Current Status

Status: pre-alpha / version 0.1.0 runtime and architecture proof complete; version 0.2A design proposed
Updated: 2026-07-18

## Released baseline

Version 0.1.0 proves that a runtime-independent deterministic Python core, local SQLite state, strict portable pack input, a runtime-neutral JSON tool contract, and a thin Hermes adapter can work together without moving learning authority into the agent runtime.

- The deterministic version-0.1 core is complete.
- The installed-package suite passes 29/29 tests on CPython 3.12.13, 3.13.14, and 3.14.6.
- Hosted GitHub Actions passed all three Python matrix jobs.
- Core statement coverage measured 87%; every AT-01 through AT-12 behavior has a direct test.
- Hermes v0.18.2 Windows CLI/profile compatibility is verified through real health, study, scoring, restart/resume, challenge, finish, and immutable-attempt checks.
- The `fixture-basics` subject is synthetic test data, not a real learning pack and not examination preparation.

The release details and reproducible commands are in [releases/0.1.0.md](releases/0.1.0.md). No compatibility is claimed for Linux, macOS, Hermes Desktop, the gateway, or another Hermes version.

## Architecture boundary proven

- Python owns pack validation, deterministic selection and scoring, persistence, challenge quarantine, and progress counts.
- SQLite is authoritative for learner state; model conversation and agent memory are not.
- The Hermes plugin delegates exactly ten operations to the public core and does not own subject logic or storage.
- The JSON-compatible contract and Python core do not import Hermes, MCP, model-provider, or network clients.
- Format 0.1 is an unpacked directory with exactly `pack.json` and one Markdown lesson.

## Known single-user limitations

- One local learner and at most one active session are supported; multi-user hosting and concurrent-process guarantees are absent.
- The workflow is practice only: no mastery, scheduling, readiness prediction, or exam simulation.
- There is no real subject pack, conversational subject builder, evidence-review workflow, or pack-review administration.
- There is no application backup/restore workflow or encryption at rest; hostile same-account processes are outside the threat model.
- The project-local Hermes plugin is trusted-checkout development behavior. Discovery requires a process-local gate and launch from the repository root.
- Pack-directory/database installation is not fully atomic across competing processes, and validation of an unexpected existing database may create expected tables before failing closed.

## Proposed next milestone: 0.2A design

The version-0.2A proposal selects official question group E1A within Amateur Extra subelement E1 for a small, sourced pilot: 11 official questions, two objectives, two lessons, and no generated questions. It proposes explicit pack format `0.2`, source/citation and rights metadata, current-pool/errata metadata, and multiple lessons. See [amateur-extra-pilot-0.2.md](amateur-extra-pilot-0.2.md) and [pack-format-0.2-proposal.md](pack-format-0.2-proposal.md).

This proposal is not accepted implementation scope. No Amateur Extra question text, lesson, explanation, pack, scoring change, or database change has been added.

## Deferred

- Subject building and real AWS or Amateur Extra packs.
- Evidence collection/review workflows and reviewer attestations.
- Scheduling, mastery, adaptive algorithms, readiness, and exam simulation.
- YAML, archives, assets, signing, marketplaces, and public distribution workflows.
- Global/package Hermes distribution, Desktop/gateway support, MCP, and broader runtime/version/platform compatibility.
- Multi-user identity, servers, cloud deployment, backup/restore, and stronger local-process isolation.

## Unresolved decisions

- Review and acceptance of Proposed ADR 0009 and the exact format-0.2 schema.
- Final component-level licensing notice for original pilot lessons and explanations, and legal review of the NCVEC public-domain statement's intended reuse scope.
- Whether installation should reject a pack whose pool currency date cannot be checked online; 0.2A currently proposes deterministic offline validation only.
- How a future authoring/review workflow records human approval without building a general evidence subsystem.
- Permanent security-reporting contact, final package/project name, and supported Hermes targets beyond the verified baseline.

## Implementation authorization

Version 0.1 focused fixes may proceed within the accepted ADR and vertical-slice boundaries. Version 0.2A is design-only and awaits review. Subject content, pack-format 0.2 parsing, tool-output changes, and Hermes presentation changes are not authorized by these documents.
