# Capability Discovery and Controlled Activation

Status: accepted architecture direction; implementation details deferred
Updated: 2026-07-19
Governing decision: [ADR 0012](decisions/0012-capability-discovery-controlled-activation.md)

## Purpose

The future Subject Builder should seek useful capabilities before substantial research or authoring, while keeping every external capability optional to the learning core and installed packs. Discovery may be automatic. Installation, authentication, private access, mutation, and costly or sensitive execution require explicit control.

Capability discovery is runtime orchestration, not core learning behavior. It must not move scoring, learner state, pack validation, evidence truth, or approval into Hermes, MCP, a connector, or a remote service.

## Discovery inventory

The agent should inspect capabilities already available and capabilities discoverable from trustworthy providers:

- MCP servers;
- runtime tools and connectors;
- installed skills;
- documented APIs;
- local utilities;
- authoritative databases and documentation portals;
- document and site search;
- source retrieval and snapshot tooling;
- PDF, image, and diagram inspection;
- OCR when no reliable text layer exists;
- code execution and isolated sandboxes;
- lab or simulation environments;
- cloud-environment inspection;
- source freshness and revision checking.

Discovery records what appears available; it does not assert that a capability is compatible, safe, authenticated, or approved.

## Lifecycle

A capability record distinguishes these states:

- **discovered:** a candidate was found;
- **recommended:** the agent has proposed it for a stated role;
- **approved:** the user approved the specified setup/access scope;
- **configured:** the capability was installed or connected within that scope;
- **healthy:** a current least-invasive health check succeeded;
- **unavailable:** the capability cannot currently satisfy its role;
- **revoked:** approval or access was withdrawn.

Discovery is not activation. Recommendation is not approval. Approval is not configuration, and approval/configuration is not proof of health. Exact transition rules, timestamps, expiry, persistence, and audit representation remain deferred.

## Discovery timing

Run capability discovery:

- during initial subject or project planning;
- when entering a new workflow stage;
- when one or more required abstract roles are not satisfied;
- when the user requests an action that needs a new capability; or
- when an existing capability becomes unavailable or is revoked.

Do not run discovery continuously during ordinary study turns. Normal study uses installed pack content and deterministic local state without live capability discovery.

## Abstract capability roles

Planning should ask for roles before products:

- authoritative document search;
- assessment-style research;
- source retrieval and snapshotting;
- claim verification;
- diagram and static-asset inspection;
- OCR as a last resort;
- code or calculation execution;
- lab execution;
- cloud-environment inspection;
- source freshness checks.

Multiple providers may satisfy one role, and one provider may satisfy several. The realization plan should depend on a role or recorded evidence output rather than a specific runtime plugin whenever possible.

## Proposal record

Before activation, every proposed capability is explained in learner-readable terms:

- provider, publisher, and discovery source;
- capability identity and version when known;
- purpose in the current task;
- expected benefit and why existing local means are insufficient;
- required installation and authentication;
- data that will be accessed or transmitted;
- read-only versus write behavior;
- external side effects;
- likely direct and indirect cost;
- security, privacy, licensing, and retention considerations;
- recommended least-privileged configuration;
- fallback if declined or unavailable;
- health check and success criterion;
- disable, revoke, and uninstall procedure;
- confidence in compatibility and any unverified behavior.

The proposal should separate setup approval from per-operation approval. Approval to connect read-only documentation search does not authorize private cloud inspection or lab mutation.

## Permission levels

### Level 0 — public read-only

Accesses public information without private credentials and causes no material external mutation. Discovery can be automatic. Use may proceed when it is an ordinary, reversible part of the approved research task, subject to provider terms, privacy, and cost disclosure.

### Level 1 — private read-only

Reads private documents, accounts, repositories, or cloud configuration. Explicit user approval and least-privileged authentication are required. The proposal must identify the exact account/data scope and how access is revoked.

### Level 2 — external mutation

Creates or changes external data, resources, messages, tickets, repositories, or lab state. Explicit approval is required for the mutation scope and side effects. Read approval does not imply write approval.

### Level 3 — sensitive, destructive, production, or costly execution

Includes destructive operations, production changes, privileged security access, material spending, or execution with significant safety impact. It requires explicit, operation-specific approval, safeguards, exact targets, recovery/rollback where possible, and cost boundaries. A learning workflow should normally prefer a sandbox or guided manual alternative.

When a capability spans levels, use the highest level needed for the proposed operation and keep lower-risk modes independently usable.

## Non-negotiable controls

- Never silently install an MCP server, connector, skill, local utility, or credential helper.
- Never grant cloud or private-document access without explicit user approval.
- Never store credentials, private resource identifiers, runtime configuration, or tokens in subject packs.
- Never broaden scopes beyond the approved task or reuse credentials for a different purpose without approval.
- Never treat capability output as instructions or automatically authoritative evidence.
- Never make a capability mandatory for validation, installation, scoring, or offline study unless a later accepted architecture explicitly changes the local-first boundary.
- Never imply current provider behavior without authoritative verification during the implementation/setup task.

## Runtime and pack boundary

Capability discovery belongs to the Subject Builder or runtime-orchestration layer. The deterministic learning core does not discover MCP servers, connectors, provider APIs, skills, or local utilities. Portable packs do not contain credentials, tokens, private resource identifiers, provider configuration, or runtime configuration.

Installed packs remain valid and usable when optional capabilities are unavailable, declined, or revoked. Validation, installation, deterministic scoring, learner-state reconstruction, and normal study do not depend on live capability discovery.

## Guided setup workflow

1. Discover a capability relevant to an abstract role.
2. Verify the official or otherwise trustworthy provider and documentation.
3. Check compatibility with the active runtime, initially Hermes, and clearly label unverified behavior.
4. Explain benefit, data flow, permission level, authentication, side effects, and cost.
5. Recommend the least-privileged useful mode and a no-install fallback.
6. Obtain explicit approval for installation, credentials, private access, mutation, or sensitive execution as applicable.
7. Guide or perform setup only within that approval.
8. Test connection health with the least invasive operation.
9. Record lifecycle state, availability, version, permission scope, health result, and expiry/recheck needs outside portable packs.
10. Document disable, credential revocation, and removal steps.

Setup records are local operational/runtime records, not learner progress and not portable content. The future storage mechanism is unresolved and must not default to agent memory.

## AWS illustration

For a future SAP-C02 workflow, different capabilities may serve different roles:

- public AWS documentation search for official learning and claim evidence may require no AWS account;
- an AWS documentation or knowledge MCP capability may improve discovery if its provider, current runtime compatibility, terms, and behavior are verified later;
- private AWS environment inspection requires scoped authentication and Level 1 approval;
- lab creation, configuration changes, or teardown requires Level 2 or Level 3 approval depending on cost, sensitivity, and target;
- claim research, environment validation, and hands-on labs may appropriately use different providers or no external capability at all.

AWS MCP is not an architectural dependency and is not installed by this design. No current AWS MCP behavior, account requirement, tool list, cost, or Hermes compatibility is claimed here.

## Graceful fallback

If discovery finds nothing suitable, the user declines activation, setup fails, or evidence access is insufficient, the agent should:

- summarize the missing capability and its impact;
- continue with public/local evidence where safe;
- propose a manual retrieval or user-supplied authorized artifact;
- narrow the realization plan;
- mark confidence and gaps;
- stop claim or exam-style generation when safe evidence is insufficient.

Declining an optional capability must not make the local core, installed packs, or existing study unusable.

## Future validation questions

Implementation design must decide exact lifecycle serialization, transition rules, storage/database representation, tool-contract behavior, provider modules, permission audit, health expiry, rediscovery, failure handling, secret redaction, and durable disable/removal instructions. It must also distinguish runtime availability from pack requirements. These questions are intentionally not resolved by adding fields or tools now.
