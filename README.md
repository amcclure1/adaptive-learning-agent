# Adaptive Learning Agent

Adaptive Learning Agent is a proposed lightweight, local-first, agent-native learning system. The agent harness is the conversational application; deterministic Python tools will own scoring, learner state, question selection, review scheduling, and pack validation. Hermes is the first planned runtime, while the learning core and subject-pack format remain runtime-independent.

## Status

**Pre-alpha — design and repository-establishment phase.**

This repository contains planning, architecture, governance, and package-boundary files only. The learning engine, Hermes adapter, skills, schemas, and pilot subject packs have not been implemented.

> Adaptive Learning Agent is not ready for learning, certification preparation, or Amateur Radio examination preparation. It currently provides no functional assessment capability, and its proposed algorithms and pack policies remain under review.

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
                       (YAML/JSON/Markdown)
```

Conversation and agent memory may shape presentation, but they are not authoritative learner state. Packs define reviewed content and evidence. Python owns state transitions and scoring. SQLite records operational learner facts.

## Initial use cases

- AWS Certified Solutions Architect – Professional (SAP-C02).
- United States Amateur Radio Extra class.

Both pilots are expected to use evidence-sensitive policies. The project will not present generated questions as real or recalled examination questions.

## Repository organization

- `docs/`: vision, requirements, architecture proposals, decisions, status, and handoffs.
- `src/adaptive_learning/`: reserved minimal Python package boundary.
- `skills/`: planned runtime guidance for learning, subject authoring, and review.
- `packs/`: template and pilot-pack workspaces; no functional pilot content exists yet.
- `schemas/`: planned machine-readable contracts.
- `tests/`: planned deterministic and integration tests.
- `user-data/`: ignored local operational state boundary.

Start with [product principles](docs/product-principles.md), [current status](docs/current-status.md), and [project context](docs/project-context.md). The original design package is indexed in [the initial handoff](docs/handoffs/initial-design-package.md).

## Contributing

Contributions are currently welcome for review of requirements, architecture, pack policy, governance, and documentation. Implementation work is not yet authorized. See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before proposing changes.

## License

Original engine, adapter, schema, and skill code is intended to be licensed under the [Apache License 2.0](LICENSE). Subject-pack content may require its own compatible license and provenance metadata.
