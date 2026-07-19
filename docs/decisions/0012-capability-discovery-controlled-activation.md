# ADR 0012: Capability Discovery with Controlled Activation

Status: Accepted
Date: 2026-07-19

## Context

Research and authored learning can benefit from document search, MCP servers, connectors, PDF/image tools, code execution, and labs. Hard-coding those services into the core would violate local-first operation, while ignoring them would make the agent less capable. Automatic setup would create credential, privacy, cost, and side-effect risk.

## Decision

Make capability discovery a future Subject Builder phase. Discover by abstract role, then propose trustworthy providers. Discovery may be automatic; activation is controlled.

Classify proposed operations as Level 0 public read-only, Level 1 private read-only, Level 2 external mutation, or Level 3 sensitive/destructive/production/costly. Require explicit approval for private access, credential setup, mutation, and sensitive execution. Explain provider, purpose, authentication, data, effects, cost, least privilege, fallback, and removal before setup.

Keep external capabilities optional to the runtime-independent core and portable packs. Runtime/profile configuration and secrets remain outside packs and learner state.

Capability lifecycle records distinguish `discovered`, `recommended`, `approved`, `configured`, `healthy`, `unavailable`, and `revoked`. Discovery is not activation, approval is not configuration, and approval/configuration is not proof of health.

Run discovery during initial subject/project planning, when entering a new workflow stage, when required roles are unsatisfied, when the user requests an action requiring a new capability, or when an existing capability becomes unavailable. Do not run discovery continuously during ordinary study turns.

Discovery belongs to the Subject Builder or runtime-orchestration layer. The deterministic learning core does not discover MCP servers, connectors, or provider tools. Packs contain no credentials or runtime configuration. Installed packs and normal study remain usable when optional capabilities are unavailable and do not depend on live discovery.

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

## Deferred milestone details

Acceptance establishes the discovery, lifecycle, timing, permission, and runtime-independence direction. It does not choose provider behavior, exact record serialization, database representation, tool-contract changes, pack fields, or implementation modules. Milestone-specific reviews must still:

- define the runtime-neutral boundary between role requests and runtime-specific discovery;
- decide where non-secret lifecycle/permission records live and how they expire;
- define approval granularity and audit evidence for each permission level;
- define health, revocation, rediscovery, and failure-transition behavior;
- verify Hermes support and every AWS/provider capability against current official documentation during implementation.
