# Current Status

Status: pre-alpha / runtime-independent core 0.1 implemented
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

## Existing design documents

- `vision.md`: product outcome, authority model, users, pilots, and non-goals.
- `mvp-requirements.md`: normative proposed MVP requirements and acceptance conditions.
- `architecture.md`: proposed component boundaries, workflows, algorithms, and security model.
- `evidence-policy.md`: proposed evidence modes, source classes, currency, and review gates.
- `pack-format.md`: proposed portable pack format version 1.0.
- `hermes-integration.md`: verified Hermes baseline and proposed thin-adapter integration.
- `decisions/0001-lightweight-local-first.md`: accepted umbrella architecture decision.
- `repository-tree.md`: original proposed repository layout.
- `sqlite-schema.md`: proposed operational schema version 1.
- `tool-contract.md`: proposed runtime-neutral JSON tool contract.
- `test-plan.md`: proposed MVP validation and acceptance plan.
- `mvp-vertical-slice.md`: accepted first implementation scope, rules, schema, tools, and twelve acceptance tests.
- `handoffs/final-mvp-design-review.md`: final design-review decisions, deferrals, blockers, and implementation prompt.
- `handoffs/core-implementation-0.1.md`: implemented modules, tests, manual exercise, deviations, and remaining integration work.

## Under review

- Post-0.1 mastery, scheduling, and adaptive question-selection algorithms.
- Broader YAML pack format 1.0, archives, signing, and canonicalization.
- Post-0.1 schema normalization, migrations, generic audit/idempotency, backup, and restore.
- Broader authoring, review, administration, and runtime-adapter tool contracts.
- Hermes v0.18.2 plugin packaging, discovery, enablement, restart, and skill distribution, which require an actual compatibility test.
- Evidence policy for the two pilot packs, including independent-review expectations.
- Pilot-pack content licensing and source-use rules.

## Known unresolved decisions

- Permanent security-reporting contact and disclosure channel.
- Whether the package name and provisional project name remain final.
- Whether YAML should be added in a later pack format and which safe parser it would use.
- Exact supported Hermes version range and tested installation paths.
- Whether an MCP adapter belongs after the in-process Hermes plugin.
- Pack signing and reviewer identity beyond local attestations.
- Final licensing policy for community and pilot pack content.
- Which broader proposed algorithms and schemas should become accepted after the vertical slice produces evidence.

## Next recommended task

Review the core implementation handoff and diff. After acceptance, scope the thin Hermes v0.18.2 plugin and workflow skill as a separate task; do not duplicate core behavior in that adapter.

## Implementation authorization

The runtime-independent core portion of `docs/mvp-vertical-slice.md` has been implemented under explicit authorization. Focused core fixes and acceptance-test corrections may proceed within that accepted boundary.

Hermes plugin and skill implementation was explicitly excluded from the core task and has not started. It requires a separately invoked implementation task and real v0.18.2 compatibility testing. No deferred feature, pilot pack, evidence workflow, YAML/archive support, mastery/scheduler, generic audit/idempotency system, backup framework, server, UI, or release publication is authorized.
