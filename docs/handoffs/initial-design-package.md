# Initial Design Package Handoff

Status: review package
Prepared: 2026-07-18

## Project summary

Adaptive Learning Agent is a proposed lightweight, local-first, agent-native learning system. Hermes is the first conversational runtime, while a runtime-independent Python core will eventually own deterministic scoring, scheduling, state mutation, evidence enforcement, and pack operations. SQLite stores operational learner data, and portable YAML/JSON/Markdown subject packs carry reviewed content without learner state. The repository is currently design-only.

## Classification key

- **Accepted direction:** explicitly established by product principles or an Accepted ADR.
- **Codex recommendation:** a detailed design proposal that still requires review.
- **Assumption:** context used to make a proposal, not an accepted fact.
- **Unresolved:** a decision or verification gap that must not be silently closed.
- **Verified external fact:** checked against official documentation as of the stated date.

## Index of the 11 original documents

| Original document | Purpose | Classification |
|---|---|---|
| [`docs/vision.md`](../vision.md) | Product outcome, users, authority hierarchy, pilots, and exclusions | Accepted direction with proposed success criteria |
| [`docs/mvp-requirements.md`](../mvp-requirements.md) | Normative proposed MVP requirements | Codex recommendation under review |
| [`docs/architecture.md`](../architecture.md) | Component boundaries, workflows, proposed algorithms, and security | Accepted boundaries plus proposed details |
| [`docs/evidence-policy.md`](../evidence-policy.md) | Source authority, traceability, currency, and human review gates | Codex recommendation under review |
| [`docs/pack-format.md`](../pack-format.md) | Proposed pack format 1.0 and canonicalization | Codex recommendation under review |
| [`docs/hermes-integration.md`](../hermes-integration.md) | Official Hermes findings and proposed adapter | Verified facts plus recommendations |
| [`docs/decisions/0001-lightweight-local-first.md`](../decisions/0001-lightweight-local-first.md) | Umbrella local-first architecture decision | Accepted direction |
| [`docs/repository-tree.md`](../repository-tree.md) | Original proposed implementation-era tree | Codex recommendation; superseded in part by established tree |
| [`docs/sqlite-schema.md`](../sqlite-schema.md) | Proposed SQLite schema and transaction invariants | Codex recommendation under review |
| [`docs/tool-contract.md`](../tool-contract.md) | Proposed runtime-neutral JSON tools | Codex recommendation under review |
| [`docs/test-plan.md`](../test-plan.md) | Proposed unit, integration, safety, adapter, and end-to-end tests | Codex recommendation under review |

All 11 remain preserved in their original repository locations. No disagreements were merged away.

## Proposed architecture

**Accepted direction:** the agent harness is the application; deterministic behavior belongs in a runtime-independent Python core; adapters depend inward; SQLite owns local operational state; packs own portable content; agent memory is non-authoritative.

**Codex recommendation:** organize the future code into domain, application, pack-format, persistence, contract, CLI, and thin runtime-adapter layers. Expose one runtime-neutral JSON contract through in-process calls and a diagnostic CLI. Use an in-process Hermes plugin first and defer MCP to an optional adapter.

**Codex recommendation:** use fixed-point integer scores, versioned algorithms, immutable attempt facts, projection rebuilds, and explicit idempotency. The exact formulas in `architecture.md` remain proposed.

## Proposed repository structure

The established repository separates governance and design (`docs/`), a behavior-free Python boundary (`src/adaptive_learning/`), planned skills (`skills/`), pack workspaces (`packs/`), future machine-readable schemas (`schemas/`), tests (`tests/`), and ignored local state (`user-data/`). The broader implementation tree in `repository-tree.md` remains a proposal and must not be created wholesale before implementation authorization.

## Proposed SQLite entities and relationships

The schema proposal contains:

- `learners` with local profile metadata;
- `installed_packs` keyed by pack ID/version/digest;
- `authoring_projects` for local draft workflow metadata;
- `study_sessions` pinned to learner, pack, and rule versions;
- `presentations` committed before answer submission;
- append-only `attempts` and `attempt_objectives`;
- derived `objective_progress` and `item_progress` projections;
- `idempotency_results` for mutation retries;
- `audit_events` for inspectable state changes;
- `schema_meta` for forward migration control.

**Codex recommendation:** one submission transaction inserts the attempt, records objective deltas, updates projections, marks the presentation answered, saves the idempotent response, and appends an audit event. Pack content itself remains in files.

## Proposed tool contracts

The `ala.tools.v1` proposal uses a common JSON request/success/error envelope, stable typed errors, explicit idempotency keys for mutations, and answer-key redaction before submission. Proposed tool groups cover system/learner operations, SQLite-safe backup/restore, pack validation/install/export, draft authoring and human review, and study start/next/submit/status/finish.

**Unresolved:** tool granularity, naming, author/reviewer mode enforcement, path policy, error taxonomy, and the complete JSON Schema are not accepted contracts.

## Proposed Hermes integration

**Codex recommendation:** use a thin, opt-in Hermes plugin to register namespaced tools and return the core's structured results. An optional skill teaches conversational workflow but is never authoritative. Hermes owns model providers and OAuth; the project does not read or store Hermes credentials. A CLI uses the same contract for tests and future adapters.

MCP is deferred because a local subprocess/protocol layer adds little value for the first in-process adapter. It remains a future runtime adapter option.

## Proposed MVP dependencies

The repository currently has no runtime dependencies. Python 3.12 or newer is required by project metadata. The standard library is proposed for SQLite, JSON, hashing, ZIP handling, timestamps, decimal arithmetic, UUIDs, and filesystem operations.

**Unresolved:** Python has no standard YAML parser. The original design recommends one small safe YAML parser, with PyYAML named as an example. No parser has been selected or installed.

## Explicit assumptions

- One local installation can contain multiple learner profiles without becoming a hosted multi-user system.
- Pack size and learner history fit comfortably in local files and SQLite for the MVP.
- Deterministic question types are sufficient for authoritative MVP scoring.
- Human review is an explicit local attestation; cryptographic reviewer identity is deferred.
- The user already has or will separately install/configure Hermes and a model provider.
- Pilot content can be authored lawfully using original questions and permissible source references.

## Unresolved decisions

- Acceptance or revision of proposed scoring, mastery, scheduling, and selection algorithms.
- Final pack schema, canonicalization, archive limits, compatibility, and signing.
- Final SQLite DDL, migrations, backup format, data directory, and concurrency settings.
- Final tool schemas and enforcement of human confirmation.
- Hermes plugin packaging across installer, PyPI, Desktop, CLI, and profiles.
- Pack and pilot content licenses; authoritative-source snapshot policy.
- Security contact and disclosure workflow.
- Remote repository owner and URL.

## Potential conflicts with product principles

- The original `hermes-integration.md` suggests Python 3.11 to align with the inspected Hermes installer; this establishment task requires Python 3.12 or newer. Project metadata now follows 3.12, and Hermes compatibility must be tested rather than assumed.
- The original repository-tree proposal includes implementation modules and scripts. Creating them now would conflict with the explicit implementation gate, so only documented boundaries were established.
- A broad Hermes installer may install Node.js, ripgrep, ffmpeg, or browser components. The project's lightweight principle constrains this project's direct footprint, not all Hermes-managed transitive tooling.
- Proposed URL checking and source retrieval could introduce network access. Local validation must remain useful offline, and remote checks must stay explicit.
- A future MCP adapter could be useful, but making MCP the core boundary would add infrastructure without demonstrated MVP need.

## Optional recommendations, not requirements

- Use a Leitner-style v1 scheduler and fixed-point mastery projection as described in `architecture.md`.
- Use a single deterministic ZIP pack format and exact archive limits proposed in `pack-format.md`.
- Use WAL mode for normal local SQLite operation after testing cloud-synchronized and network paths.
- Package an optional Hermes workflow skill alongside the plugin.
- Add signed packs and stronger reviewer identity after the MVP.

## Verified Hermes facts

The following were verified on 2026-07-18 against official NousResearch documentation and are external facts, not project requirements:

- Hermes documents CLI installation on Linux, macOS, WSL2, native Windows, and Termux, with managed dependencies and an optional `--skip-browser` path: [Installation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md).
- Hermes skills are on-demand documents using progressive disclosure and primarily live under the Hermes home directory: [Skills System](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).
- Hermes supports local stdio and remote HTTP MCP servers with tool discovery/filtering: [MCP](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md).
- Hermes documents plugins and `ctx.register_tool()` for custom tools; general plugins are opt-in: [Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md) and [Build a Hermes Plugin](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/build-a-hermes-plugin.md).
- `hermes model` configures providers/authentication, while `/model` switches among configured choices in-session: [AI Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md).
- Hermes documents a device-code OpenAI Codex provider, a Hermes auth store, and optional import of Codex CLI credentials: [AI Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md).
- The latest tagged release visible during the design review was [v0.18.2](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2).

## Unverified Hermes items

- Exact editable/local package installation commands for every Hermes distribution method.
- Plugin entry-point discovery precedence in the target release.
- Whether package installation can bundle a skill without copying it into profile state.
- Exact restart/reload behavior in Hermes Desktop versus CLI.
- A tested Hermes version support range for this future adapter.

Documentation on Hermes `main` may be ahead of the latest tagged release; implementation must verify behavior against the selected target release.

## Recommended review order

1. `product-principles.md`, then `vision.md`.
2. `mvp-requirements.md`.
3. Accepted ADRs under `decisions/`.
4. `architecture.md`.
5. `evidence-policy.md` and `pack-format.md` together.
6. `sqlite-schema.md` and `tool-contract.md` together.
7. `hermes-integration.md`.
8. `test-plan.md`.
9. `repository-tree.md` as a historical implementation proposal.
