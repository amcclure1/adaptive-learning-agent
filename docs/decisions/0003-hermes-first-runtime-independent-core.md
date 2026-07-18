# ADR 0003: Hermes First, Runtime-Independent Core

Status: Accepted
Date: 2026-07-18

## Context

Hermes provides the first intended conversational runtime, tool surface, and provider integration. Coupling learning behavior or pack content to Hermes would make testing harder and prevent future runtimes from reusing the system.

## Decision

Hermes is the first supported runtime. Runtime adapters depend on a runtime-neutral Python core and JSON-compatible tool contract. The learning core and subject-pack format must not import, configure, or require Hermes.

Hermes-specific skills contain workflow guidance only. Hermes memory and provider credentials are outside the authoritative learning-state boundary.

## Consequences

- A thin Hermes adapter must translate without duplicating business rules.
- Core tests can run without Hermes or a model.
- Another runtime can implement the same contract.
- Hermes packaging and compatibility require adapter-specific tests.

## Alternatives considered

- Implement learning behavior directly in Hermes skills and memory: rejected because it is not deterministic or runtime-independent.
- Use MCP as the mandatory core boundary: deferred because it adds a process/protocol layer before multiple runtimes demonstrate a need.
