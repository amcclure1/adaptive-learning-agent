# ADR 0007: Hermes Plugin and Skill Boundary

Status: Accepted
Date: 2026-07-18

## Context

Hermes is the first conversational runtime, but neither learner state nor learning behavior may depend on a conversation, model, provider, or Hermes memory. Hermes extensions can expose both deterministic tools and conversational guidance, so their responsibilities must be explicit.

## Decision

Use a thin Hermes plugin to register the version-0.1 tool schemas and delegate each call to the runtime-independent application service. The plugin may translate Hermes-safe tool names and validate adapter-level arguments. It must not score answers, select questions, implement pedagogy, query SQLite outside the application service, inspect pack files independently, or perform free-form reasoning.

Use a Hermes skill only for conversational workflow and pedagogy: introducing a lesson, eliciting an answer and confidence, calling tools, presenting returned feedback, and offering the challenge workflow. The skill must not read or write SQLite, parse packs, infer persisted state, or override tool results.

Hermes owns model/provider configuration, Codex OAuth, credential storage, and refresh. Adaptive Learning Agent must not read, copy, log, or store Hermes or Codex credentials.

The runtime-neutral contract uses dotted operation names. A Hermes adapter may expose underscore aliases when required by Hermes and must maintain a one-to-one mapping.

## Consequences

- The core and its acceptance tests run without Hermes or an LLM.
- A future runtime can implement the same contract without changing learning rules or state.
- Conversation or memory loss cannot erase or rewrite authoritative learner state.
- Hermes compatibility remains an adapter test, not a property inferred from the core.
- Workflow prose can evolve without changing deterministic behavior.

## Alternatives considered

- Put learning behavior in a Hermes skill: rejected because skills are model-interpreted and runtime-specific.
- Put tutoring behavior in the plugin: rejected because it couples pedagogy to the adapter and invites nondeterministic business logic.
- Use Hermes memory as learner state: rejected because memory is non-authoritative and may be absent in a fresh conversation.
- Start with MCP: deferred because an in-process plugin is the smallest Hermes proof and the core contract already preserves a later adapter boundary.
