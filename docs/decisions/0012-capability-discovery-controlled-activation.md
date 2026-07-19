# ADR 0012: Capability Discovery with Controlled Activation

Status: Proposed
Date: 2026-07-19

## Context

Research and authored learning can benefit from document search, MCP servers, connectors, PDF/image tools, code execution, and labs. Hard-coding those services into the core would violate local-first operation, while ignoring them would make the agent less capable. Automatic setup would create credential, privacy, cost, and side-effect risk.

## Proposed decision

Make capability discovery a future Subject Builder phase. Discover by abstract role, then propose trustworthy providers. Discovery may be automatic; activation is controlled.

Classify proposed operations as Level 0 public read-only, Level 1 private read-only, Level 2 external mutation, or Level 3 sensitive/destructive/production/costly. Require explicit approval for private access, credential setup, mutation, and sensitive execution. Explain provider, purpose, authentication, data, effects, cost, least privilege, fallback, and removal before setup.

Keep external capabilities optional to the runtime-independent core and portable packs. Runtime/profile configuration and secrets remain outside packs and learner state.

## Consequences

- The agent can seek better research and lab tools without making them platform dependencies.
- Users retain control over credentials, private data, changes, and costs.
- Runtime adapters need a future capability-discovery boundary and health model.
- Provider behavior and compatibility must be verified during each setup implementation.
- Workflows need graceful fallbacks when capabilities are declined or unavailable.

## Alternatives considered

- Bundle a mandatory MCP stack: rejected because it expands installation and couples the core to external services.
- Let the agent install capabilities automatically: rejected because discovery is not authorization.
- Forbid external capabilities: rejected because optional tools can materially improve authoritative research and hands-on learning.
- Store capability configuration in packs: rejected because packs must remain portable and credential-free.

## Acceptance prerequisites

- Define the runtime-neutral boundary between role requests and runtime-specific discovery.
- Decide where non-secret availability/permission records live and how they expire.
- Define approval granularity and audit evidence for each permission level.
- Verify Hermes support and any AWS capability only against current official documentation during implementation.
