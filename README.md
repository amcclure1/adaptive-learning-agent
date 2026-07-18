# Adaptive Learning Agent

Adaptive Learning Agent is a lightweight, local-first, agent-native learning system. Its runtime-independent Python core owns deterministic practice scoring, learner state, question selection, pack validation, and challenge quarantine. A thin project-local adapter and workflow skill are now verified with Hermes v0.18.2.

## Status

**Pre-alpha — runtime-independent core and Hermes adapter version 0.1 implemented.**

The repository contains a working core, an eight-table SQLite schema, a strict JSON-plus-Markdown fixture pack, ten JSON-compatible operations, a Hermes v0.18.2 project plugin, one fixture workflow skill, and automated core/adapter tests. Conversational authoring, evidence workflows, scheduling, and pilot subject packs have not been implemented.

> Adaptive Learning Agent is not ready for certification preparation or Amateur Radio examination preparation. The included fixture is synthetic test content, not a production learning pack.

## Run the core tests

Python 3.12 or newer is required. The learning core has no third-party runtime dependencies.

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

The public Python boundary is `ApplicationService` plus `ToolContract`. Tool requests and responses use JSON-compatible dictionaries; local learner state is written only to the caller-selected user-data directory. The suite is exercised in CI on Python 3.12, 3.13, and 3.14.

## Run the isolated Hermes profile

The verified development setup uses pinned Hermes v0.18.2 and the isolated `adaptive-learning-dev` profile. From this trusted repository root:

```powershell
$env:HERMES_ENABLE_PROJECT_PLUGINS='1'
& "$env:USERPROFILE\.local\bin\hermes.exe" -p adaptive-learning-dev --skills adaptive-learning:adaptive-learning
Remove-Item Env:HERMES_ENABLE_PROJECT_PLUGINS
```

Project plugins execute repository code. Never set the discovery environment variable globally or use this command from an untrusted checkout. See [the compatibility record](docs/hermes-compatibility-0.18.2.md) for setup, trust boundaries, exact paths, known tagged-release differences, and cleanup.

## Goals

- Make the agent harness the primary user experience.
- Keep deterministic learning behavior in testable Python code.
- Store operational learner data locally in SQLite.
- Define portable, versioned subject packs using YAML, JSON, and Markdown.
- Let users create and review subjects conversationally.
- Support evidence-sensitive packs with provenance and human review gates.
- Keep installation and operation practical for an individual user.
- Remain open source and runtime-independent from the beginning.

## Non-goals for the MVP

- A web frontend or separate API server.
- PostgreSQL, Redis, Celery, a vector database, or Kubernetes.
- Required Docker or cloud deployment.
- Hosted multi-user identity and authorization.
- A public pack marketplace.
- Autonomous content activation or publishing.
- A multi-agent swarm.
- Dependence on Lumen, OpenTutor, or another complete learning platform.

## Proposed architecture

```text
Hermes or another agent runtime
            |
            v
       thin adapter
            |
            v
runtime-neutral JSON tool contract
            |
            v
deterministic Python learning core
       |                    |
       v                    v
local SQLite state     portable subject packs
                       (JSON/Markdown in 0.1)
```

Conversation and agent memory may shape presentation, but they are not authoritative learner state. Packs define reviewed content and evidence. Python owns state transitions and scoring. SQLite records operational learner facts.

## Initial use cases

- AWS Certified Solutions Architect – Professional (SAP-C02).
- United States Amateur Radio Extra class.

Both pilots are expected to use evidence-sensitive policies. The project will not present generated questions as real or recalled examination questions.

## Repository organization

- `docs/`: vision, requirements, architecture proposals, decisions, status, and handoffs.
- `src/adaptive_learning/`: runtime-independent pack, SQLite, learning, and tool-contract code.
- `.hermes/plugins/adaptive-learning/`: thin project-local Hermes v0.18.2 adapter.
- `skills/adaptive-learning/`: minimal deterministic fixture workflow guidance.
- `packs/fixture-basics/`: synthetic functional pack used by the core acceptance tests.
- `packs/`: additional template and pilot-pack workspaces; no functional pilot content exists yet.
- `schemas/`: planned standalone machine-readable contracts; schema version 1 currently lives in the core.
- `tests/`: standard-library pack, storage, contract, vertical-slice, and direct adapter tests.
- `user-data/`: ignored local operational state boundary.

Start with [product principles](docs/product-principles.md), [current status](docs/current-status.md), and [project context](docs/project-context.md). The original design package is indexed in [the initial handoff](docs/handoffs/initial-design-package.md).

## Contributing

Contributions are welcome for the accepted core scope and for review of requirements, architecture, pack policy, governance, and documentation. Deferred features still require explicit design acceptance. See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before proposing changes.

## License

Original engine, adapter, schema, and skill code is intended to be licensed under the [Apache License 2.0](LICENSE). Subject-pack content may require its own compatible license and provenance metadata.
