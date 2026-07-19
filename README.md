# Adaptive Learning Agent

Adaptive Learning Agent is a lightweight, local-first, agent-native learning system. Its runtime-independent Python core owns deterministic practice scoring, learner state, question selection, pack validation, and challenge quarantine. A thin project-local adapter and workflow skill are verified with Hermes v0.18.2.

## Status

**Pre-alpha — version 0.2.0-alpha.1 is published; the unreleased 0.2B format-0.3 asset candidate has final acceptance PASS.**

The deterministic version-0.1 core is complete. The installed-package suite passes on Python 3.12, 3.13, and 3.14, and the Hermes v0.18.2 CLI/profile integration is verified on Windows. The included `fixture-basics` subject is synthetic acceptance-test data, not a real learning pack and not preparation for any certification or examination.

The core supports strict formats 0.1, 0.2, and 0.3. Format 0.3 adds bounded local PNG assets, exact-byte validation/digesting, reviewed accessibility fallbacks, and logical installed-asset references without changing SQLite schema 1 or scoring. Anthony McClure approved the E7B10–E7B12/Figure E7-1 candidate after reviewing its source mapping, fidelity, redistribution disposition, accessibility text, mappings, content, rights, and activation. It is valid, installable, and final-acceptance PASS; no release or tag has been created. See [the review package](docs/reviews/amateur-extra-e7b-asset-content-review.md), [current status](docs/current-status.md), and [roadmap](docs/roadmap.md).

## Install from the tagged source

Python 3.12 or newer and Git are required. Hermes v0.18.2 is additionally required for the verified conversational workflow.

```powershell
git clone --branch v0.2.0-alpha.1 https://github.com/amcclure1/adaptive-learning-agent.git
Set-Location adaptive-learning-agent
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install .
```

Detailed core validation and Hermes study instructions are in [the release record](docs/releases/0.2.0-alpha.1.md#installation-and-use).

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
                       (JSON/Markdown plus bounded PNG in 0.3)
```

Conversation and agent memory may shape presentation, but they are never authoritative learner state. Packs define reviewed content and evidence. Python owns state transitions and scoring. SQLite records operational learner facts.

## Current limitations

- One local learner and at most one active session; no hosted or concurrent multi-user operation.
- Practice workflow only; no mastery, scheduling, readiness prediction, or exam simulation.
- The approved real E1A content covers only one question group and is not complete examination preparation.
- No application backup/restore, encryption at rest, or protection from hostile same-account processes.
- Project-local Hermes plugin discovery is trusted-checkout development behavior and requires a process-local environment gate.
- Only the Windows Hermes v0.18.2 CLI/profile path has been verified.

## Goals and non-goals

The project aims to make an agent harness the primary experience while keeping deterministic learning behavior in testable Python, operational state in local SQLite, and portable subject content in versioned files. It does not require a web frontend, API server, PostgreSQL, Redis, Celery, a vector database, Docker, cloud deployment, hosted identity, a marketplace, autonomous publishing, or a multi-agent swarm.

The first real pilot is the released United States Amateur Radio Extra E1A slice. Proposed next phases separately cover an official static-asset Amateur Extra pilot (0.2B) and assessment/curriculum research followed by a manually reviewed AWS SAP-C02 slice (0.3A–B). Generated questions will be original, evidence-backed, human-reviewed, and never presented as official, real, or recalled examination questions. See [the roadmap](docs/roadmap.md) and [future Subject Builder architecture](docs/subject-builder-architecture.md).

## Repository organization

- `docs/`: product principles, accepted decisions, status, proposals, releases, and handoffs.
- `src/adaptive_learning/`: runtime-independent pack, SQLite, learning, and tool-contract code.
- `.hermes/plugins/adaptive-learning/`: thin project-local Hermes v0.18.2 adapter.
- `skills/adaptive-learning/`: minimal deterministic fixture workflow guidance.
- `packs/fixture-basics/`: synthetic functional pack used by acceptance tests.
- `packs/amateur-extra-e1a/`: approved sourced E1A pilot with two lessons and eleven official questions.
- `packs/amateur-extra-e7b/`: pending-review format-0.3 candidate with three official questions and exact Figure E7-1 bytes; not installable.
- `schemas/`: reserved standalone machine-readable contracts; schema version 1 currently lives in the core.
- `tests/`: standard-library pack, storage, contract, vertical-slice, and direct adapter tests.
- `user-data/`: ignored local operational state boundary.

Start with [product principles](docs/product-principles.md), [current status](docs/current-status.md), and [project context](docs/project-context.md). The original design package is indexed in [the initial handoff](docs/handoffs/initial-design-package.md).

Accepted next-phase architecture direction is indexed by [assessment policy](docs/assessment-research-policy.md), [curriculum planning](docs/curriculum-planning.md), [capability discovery](docs/capability-discovery.md), and the [Subject Builder architecture](docs/subject-builder-architecture.md). The 0.2B E7B asset pilot is implemented and human-approved; final runtime/CI acceptance remains in progress. Later Subject Builder milestones remain separately gated.

## Contributing

Contributions are welcome within accepted scope and for review of proposals. Deferred features require explicit design acceptance. See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before proposing changes.

## License

Original engine, adapter, schema, and skill code is licensed under the [Apache License 2.0](LICENSE). Subject-pack content may require separate compatible rights and provenance metadata.
