# Current Status

Status: pre-alpha / design phase
Updated: 2026-07-18

## Completed

- Created the initial 11-document design package and preserved it under `docs/`.
- Established the local Git repository and open-source governance baseline.
- Created the public GitHub repository at `https://github.com/amcclure1/adaptive-learning-agent` and configured `main` to track `origin/main`.
- Defined normative product principles and durable project context.
- Added a minimal Python 3.12 package boundary with no application behavior and no runtime dependencies.
- Reserved documented boundaries for skills, packs, schemas, tests, and ignored local user data.
- Recorded accepted architectural direction in ADRs.

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

## Under review

- Exact scoring, mastery, scheduling, and question-selection algorithms.
- Pack format 1.0 details and canonicalization rules.
- SQLite schema normalization, migration strategy, and default data paths.
- JSON tool names, mode separation, idempotency, backup, and restore behavior.
- Hermes plugin packaging, discovery, enablement, restart, and skill distribution.
- Evidence policy for the two pilot packs, including independent-review expectations.
- Pilot-pack content licensing and source-use rules.

## Known unresolved decisions

- Permanent security-reporting contact and disclosure channel.
- Whether the package name and provisional project name remain final.
- Which YAML parser, if any, to add when pack parsing implementation is authorized.
- Exact supported Hermes version range and tested installation paths.
- Whether an MCP adapter belongs after the in-process Hermes plugin.
- Pack signing and reviewer identity beyond local attestations.
- Final licensing policy for community and pilot pack content.
- Which proposed algorithms and schemas should become accepted contracts before implementation.

## Next recommended task

Conduct a human design review of the initial package in this order: product principles and vision; MVP requirements; accepted ADRs; architecture boundaries; pack/evidence policy; SQLite/tool contracts; Hermes integration; test plan. Record accepted or revised decisions without implementing the engine.

## Implementation authorization

**Implementation has not been authorized.** Do not add learning-engine behavior, functional skills, pack schemas, pilot questions, database migrations, or runtime integration code until an explicit reviewed update to this file authorizes a scoped implementation task.
