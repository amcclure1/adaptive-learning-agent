# Adaptive Learning Agent

Adaptive Learning Agent is a lightweight, local-first, agent-native learning system. Its runtime-independent Python core owns deterministic practice scoring, learner state, question selection, pack validation, and challenge quarantine. A thin project-local adapter and workflow skill are verified with Hermes v0.18.2.

## Status

**Pre-alpha — version 0.1.0 is a runtime and architecture proof.**

The deterministic version-0.1 core is complete. The installed-package suite passes on Python 3.12, 3.13, and 3.14, and the Hermes v0.18.2 CLI/profile integration is verified on Windows. The included `fixture-basics` subject is synthetic acceptance-test data, not a real learning pack and not preparation for any certification or examination.

Subject building, real certification packs, evidence workflows, scheduling, mastery, and exam simulation remain deferred. Version 0.2A is a design proposal for a small sourced Amateur Extra pilot; it does not yet authorize implementation. See [the 0.1.0 release record](docs/releases/0.1.0.md), [current status](docs/current-status.md), and [roadmap](docs/roadmap.md).

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

Project plugins execute repository code. Never set the discovery environment variable globally or use this command from an untrusted checkout. See [the compatibility record](docs/hermes-compatibility-0.18.2.md) for setup, trust boundaries, exact paths, known tagged-release differences, and cleanup. Compatibility is not claimed for Linux, macOS, Hermes Desktop, the gateway, or Hermes versions other than v0.18.2.

## Proven architecture

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

Conversation and agent memory may shape presentation, but they are never authoritative learner state. Packs define reviewed content and evidence. Python owns state transitions and scoring. SQLite records operational learner facts.

## Version-0.1 limitations

- One local learner and at most one active session; no hosted or concurrent multi-user operation.
- Practice workflow only; no mastery, scheduling, readiness prediction, or exam simulation.
- Synthetic fixture content only; no real subject pack or evidence-review workflow.
- No application backup/restore, encryption at rest, or protection from hostile same-account processes.
- Project-local Hermes plugin discovery is trusted-checkout development behavior and requires a process-local environment gate.
- Only the Windows Hermes v0.18.2 CLI/profile path has been verified.

## Goals and non-goals

The project aims to make an agent harness the primary experience while keeping deterministic learning behavior in testable Python, operational state in local SQLite, and portable subject content in versioned files. It does not require a web frontend, API server, PostgreSQL, Redis, Celery, a vector database, Docker, cloud deployment, hosted identity, a marketplace, autonomous publishing, or a multi-agent swarm.

The first intended real pilots are AWS Certified Solutions Architect – Professional (SAP-C02) and United States Amateur Radio Extra class. Both are evidence-sensitive. The project will not present generated questions as official, real, or recalled examination questions.

## Repository organization

- `docs/`: product principles, accepted decisions, status, proposals, releases, and handoffs.
- `src/adaptive_learning/`: runtime-independent pack, SQLite, learning, and tool-contract code.
- `.hermes/plugins/adaptive-learning/`: thin project-local Hermes v0.18.2 adapter.
- `skills/adaptive-learning/`: minimal deterministic fixture workflow guidance.
- `packs/fixture-basics/`: synthetic functional pack used by acceptance tests.
- `schemas/`: reserved standalone machine-readable contracts; schema version 1 currently lives in the core.
- `tests/`: standard-library pack, storage, contract, vertical-slice, and direct adapter tests.
- `user-data/`: ignored local operational state boundary.

Start with [product principles](docs/product-principles.md), [current status](docs/current-status.md), and [project context](docs/project-context.md). The original design package is indexed in [the initial handoff](docs/handoffs/initial-design-package.md).

## Contributing

Contributions are welcome within accepted scope and for review of proposals. Deferred features require explicit design acceptance. See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before proposing changes.

## License

Original engine, adapter, schema, and skill code is licensed under the [Apache License 2.0](LICENSE). Subject-pack content may require separate compatible rights and provenance metadata.
