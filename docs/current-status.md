# Current Status

Status: pre-alpha / vertical-slice design accepted
Updated: 2026-07-18

## Completed

- Created the initial 11-document design package and preserved it under `docs/`.
- Established the local Git repository and open-source governance baseline.
- Created the public GitHub repository at `https://github.com/amcclure1/adaptive-learning-agent` and configured `main` to track `origin/main`.
- Defined normative product principles and durable project context.
- Added a minimal Python 3.12 package boundary with no application behavior and no runtime dependencies.
- Reserved documented boundaries for skills, packs, schemas, tests, and ignored local user data.
- Recorded accepted architectural direction in ADRs.
- Completed the final MVP design review and accepted the version-0.1 vertical slice.
- Accepted the Hermes plugin/skill boundary and JSON-plus-Markdown pack serialization in ADRs 0007 and 0008.

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

Run the first implementation task using only the exact prompt in `docs/handoffs/final-mvp-design-review.md`. Begin with AT-01 through AT-12 and do not pull deferred features into the slice.

## Implementation authorization

The exact version-0.1 scope in `docs/mvp-vertical-slice.md` is design-approved for implementation **only when the user explicitly invokes the first implementation task**. That authorization permits the synthetic fixture, eight-table schema/migration, deterministic core, ten-tool contract, thin Hermes plugin, minimal workflow skill, and tests needed for AT-01 through AT-12 and the Hermes compatibility check.

It does not authorize any deferred feature, pilot pack, evidence workflow, YAML/archive support, mastery/scheduler, generic audit/idempotency system, backup framework, server, UI, or release publication. This design-review task created no application code, migrations, schemas, fixture packs, or functional skills.
