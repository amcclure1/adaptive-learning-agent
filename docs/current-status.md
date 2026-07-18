# Current Status

Status: pre-alpha / runtime-independent core and Hermes adapter 0.1 implemented
Updated: 2026-07-18

## Completed

- Created the initial 11-document design package and preserved it under `docs/`.
- Established the local Git repository and open-source governance baseline.
- Created the public GitHub repository at `https://github.com/amcclure1/adaptive-learning-agent` and configured `main` to track `origin/main`.
- Defined normative product principles and durable project context.
- Implemented the Python 3.12 runtime-independent core with no runtime dependencies.
- Reserved documented boundaries for skills, packs, schemas, tests, and ignored local user data.
- Recorded accepted architectural direction in ADRs.
- Completed the final MVP design review and accepted the version-0.1 vertical slice.
- Accepted the Hermes plugin/skill boundary and JSON-plus-Markdown pack serialization in ADRs 0007 and 0008.
- Implemented strict pack validation, canonical digests, controlled installation, schema version 1, all ten core tools, deterministic scoring, confidence, restart, progress, and challenge quarantine.
- Added the synthetic `fixture-basics` pack and passing automated coverage for AT-01 through AT-12 plus the required additional cases.
- Verified installed-package tests on CPython 3.12.13, 3.13.14, and 3.14.6 and added the matching minimal GitHub Actions matrix.
- Measured 87% core statement coverage; all AT-01 through AT-12 behaviors have direct tests.
- Installed pinned Hermes v0.18.2 in an isolated uv tool environment and created the isolated `adaptive-learning-dev` profile with strict profile-local terminal home.
- Implemented the project-local ten-tool Hermes adapter and minimal qualified workflow skill.
- Completed real Codex-backed Hermes health, fixture, deterministic feedback, full process restart/fresh-conversation resume, quarantine, finish, and immutable-attempt acceptance checks.

## Existing design documents

- `vision.md`: product outcome, authority model, users, pilots, and non-goals.
- `mvp-requirements.md`: normative proposed MVP requirements and acceptance conditions.
- `architecture.md`: proposed component boundaries, workflows, algorithms, and security model.
- `evidence-policy.md`: proposed evidence modes, source classes, currency, and review gates.
- `pack-format.md`: proposed portable pack format version 1.0.
- `hermes-integration.md`: accepted and implemented thin-adapter integration boundary.
- `decisions/0001-lightweight-local-first.md`: accepted umbrella architecture decision.
- `repository-tree.md`: original proposed repository layout.
- `sqlite-schema.md`: proposed operational schema version 1.
- `tool-contract.md`: proposed runtime-neutral JSON tool contract.
- `test-plan.md`: proposed MVP validation and acceptance plan.
- `mvp-vertical-slice.md`: accepted first implementation scope, rules, schema, tools, and twelve acceptance tests.
- `handoffs/final-mvp-design-review.md`: final design-review decisions, deferrals, blockers, and implementation prompt.
- `handoffs/core-implementation-0.1.md`: implemented modules, tests, manual exercise, deviations, and remaining integration work.
- `handoffs/core-implementation-review.md`: exact core range, compatibility matrix, coverage, deviations, and audit observations.
- `hermes-compatibility-0.18.2.md`: tagged documentation/source findings and locally verified runtime behavior.
- `handoffs/hermes-integration-0.1.md`: installation, profile, plugin, skill, provider, acceptance, known issues, and cleanup.

## Under review

- Post-0.1 mastery, scheduling, and adaptive question-selection algorithms.
- Broader YAML pack format 1.0, archives, signing, and canonicalization.
- Post-0.1 schema normalization, migrations, generic audit/idempotency, backup, and restore.
- Broader authoring, review, administration, and runtime-adapter tool contracts.
- Global/package distribution of the currently project-local Hermes plugin and skill; v0.18.2 CLI development behavior is verified.
- Evidence policy for the two pilot packs, including independent-review expectations.
- Pilot-pack content licensing and source-use rules.

## Known unresolved decisions

- Permanent security-reporting contact and disclosure channel.
- Whether the package name and provisional project name remain final.
- Whether YAML should be added in a later pack format and which safe parser it would use.
- Supported Hermes versions beyond the verified v0.18.2 CLI target and Desktop/gateway installation paths.
- Whether an MCP adapter belongs after the in-process Hermes plugin.
- Pack signing and reviewer identity beyond local attestations.
- Final licensing policy for community and pilot pack content.
- Which broader proposed algorithms and schemas should become accepted after the vertical slice produces evidence.

## Next recommended task

Review the Hermes integration handoff and compatibility record. Next work should remain within explicitly accepted scope; do not begin subject building, content review, pilot packs, mastery, or scheduling without a new decision/task.

## Implementation authorization

The runtime-independent core portion of `docs/mvp-vertical-slice.md` has been implemented under explicit authorization. Focused core fixes and acceptance-test corrections may proceed within that accepted boundary.

The separately authorized Hermes v0.18.2 plugin and skill task is complete for the project-local CLI development target. No deferred feature, pilot pack, evidence workflow, YAML/archive support, mastery/scheduler, generic audit/idempotency system, backup framework, server, UI, global plugin install, or release publication is authorized.
