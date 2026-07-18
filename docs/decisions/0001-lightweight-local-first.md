# ADR 0001: Lightweight, Local-First Architecture

Status: Accepted  
Date: 2026-07-18

## Context

Adaptive Learning Agent needs durable, deterministic assessment inside an agent conversation. Hermes is the first conversational runtime, but subject packs and learner logic must remain portable. The MVP is for one local installation, must support conversational pack creation and evidence review, and must avoid service infrastructure.

The main choices were:

1. Put learning logic and state in Hermes prompts, skills, and memory.
2. Build a standalone web/API service with a server database.
3. Build a local Python core with SQLite and files, then attach a thin Hermes adapter.
4. Make an MCP server the primary core boundary.

## Decision

Choose option 3.

- Python domain and application services own deterministic scoring, scheduling, validation, evidence gates, and transactions.
- SQLite owns operational learner state.
- Versioned YAML and Markdown packs own portable subject content.
- A runtime-neutral JSON contract is the stable adapter boundary.
- A thin Hermes plugin is the first conversational adapter, optionally supported by a workflow skill.
- MCP is deferred to an optional adapter if multiple runtimes later need tool discovery.
- Agent memory is explicitly non-authoritative.

## Rationale

Prompts and memory are mutable, probabilistic, and difficult to migrate or audit. They are appropriate for conversation style but not scores or durable progress.

A web service and distributed data stack add deployment, authentication, failure, privacy, and maintenance work without helping the single-machine MVP.

SQLite supplies transactions, constraints, backups, and mature local tooling in the Python standard library. YAML/Markdown packs remain readable, diffable, and shareable without coupling content to a database or runtime. A narrow adapter preserves Hermes' strong conversational experience while letting core tests run without Hermes or a model.

Hermes officially documents Python plugins as the extension route for custom local tools and MCP as a route to external tool servers. The plugin choice is therefore the smaller first integration. See [Hermes Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md) and [Hermes MCP](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md).

## Consequences

Positive:

- fully local learner state and simple backup;
- deterministic, replayable assessment;
- runtime-independent core and pack format;
- small dependency and operational footprint;
- ordinary Git workflows for pack sharing and review;
- evidence gates can be validated without a model.

Costs:

- adapters must translate the common contract;
- SQLite is not intended for concurrent hosted multi-user workloads;
- pack migrations and canonicalization require careful versioning;
- local reviewer identity is an attestation rather than cryptographic proof;
- model conversation may be unavailable even while local core operations remain usable.

## Alternatives considered

### Hermes memory as learner state

Rejected because memory is agent-controlled, may be summarized or missing, and is not a transactional or authoritative record.

### Hermes skill as the learning engine

Rejected because a skill is instructional text. It can guide tool use but cannot guarantee scoring or state transitions.

### Separate API server

Rejected for MVP because it creates a service lifecycle and security boundary on a single machine without a user need.

### PostgreSQL, Redis, Celery, or vector database

Rejected because MVP data is relational and modest, tasks are request-driven, and semantic retrieval is not needed for authoritative scoring.

### MCP as the primary core

Rejected for MVP because it adds a process/protocol layer between a local Python plugin and local Python logic. The JSON boundary preserves this option later.

### LLM grading as authoritative scoring

Rejected because results can vary with model, prompt, provider, and time and cannot satisfy the reproducibility requirement.

## Revisit triggers

Reconsider parts of this decision only if:

- multiple simultaneous remote users become an explicit goal;
- more than one runtime needs live tool discovery enough to justify MCP;
- SQLite write concurrency or dataset size is measured as a real constraint;
- signed review identities and distribution trust become requirements;
- a server feature is accepted through a new ADR with migration and privacy plans.
