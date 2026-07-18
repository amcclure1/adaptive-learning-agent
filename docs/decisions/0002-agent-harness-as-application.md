# ADR 0002: Agent Harness as the Application

Status: Accepted
Date: 2026-07-18

## Context

The project is intended to be agent-native. A conventional learning application with a chat assistant would create two competing interaction models and require a web or UI stack that the MVP does not need.

## Decision

The agent harness is the primary application and conversational interface. Learning operations are exposed as structured tools used in conversation. The MVP does not include a separate web frontend or API application.

The agent may decide how to present information, but deterministic tools remain authoritative for assessment and state.

## Consequences

- Normal workflows are designed first as conversations backed by tools.
- Tool contracts, errors, and resumability are product interfaces rather than internal details.
- Accessibility and inspectability must work in text-first surfaces.
- A future UI may be added only as another client of the same core boundaries.

## Alternatives considered

- A web learning application with an embedded chat assistant: rejected for the MVP because it adds a second application and deployment stack.
- A standalone CLI without an agent: retained only as a diagnostic/runtime-neutral boundary, not the primary experience.
