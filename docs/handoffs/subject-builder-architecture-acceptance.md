# Subject Builder Architecture Acceptance

Date: 2026-07-19
Status: accepted architecture direction; implementation not authorized

## Acceptance

The user explicitly accepted all current proposed ADRs. The following decisions are now `Accepted`:

- [ADR 0010 — Whole Learning Architecture with Progressive Realization](../decisions/0010-whole-learning-architecture-progressive-realization.md)
- [ADR 0011 — Assessment Authenticity and Official-Question Reuse](../decisions/0011-assessment-authenticity-official-question-reuse.md)
- [ADR 0012 — Capability Discovery with Controlled Activation](../decisions/0012-capability-discovery-controlled-activation.md)
- [ADR 0013 — Evidence-Backed Authored Questions and Layered Approval](../decisions/0013-evidence-backed-authored-questions-layered-approval.md)

Acceptance establishes architectural direction only. It does not authorize 0.2B or 0.3 implementation, content creation/import, capability setup, or runtime changes.

## Exact decisions accepted

1. Design and approve a whole learning architecture for the stated outcome, then realize coherent content progressively through independently versioned plans.
2. Guide learner scope through blocking, bridge, recommended, and independent dependency categories with visible consequences and the smallest coherent recommendation.
3. Produce versioned curriculum impact reports without silently migrating installed packs or learner progress.
4. Research assessment authenticity from permissible evidence; reuse official questions only with documented rights and exact provenance, and exclude dumps/recalled/leaked/unauthorized material.
5. Copy assessment grammar rather than protected assessment sentences, use confidence-based fallback, and label authored questions as original.
6. Make capability discovery a Subject Builder/runtime-orchestration concern with abstract roles, controlled least-privileged activation, explicit permission levels, and graceful fallback.
7. Keep optional capabilities outside the deterministic core and portable packs.
8. Author complex questions through an evidence chain with explicit constraints, keyed and distractor rationales, citations, human uniqueness review, and separate claim/question/pack approvals.
9. Preserve human activation authority and prohibit authoring-agent self-approval.

## Refinements applied

### Assessment blueprint and learning architecture

An assessment blueprint is an independent assessment-model artifact. One blueprint may support multiple learning architectures. One learning architecture may reference zero, one, or several blueprints. Non-certification learning does not require an external exam blueprint.

The learning architecture owns curriculum outcome coverage, domains, objectives, prerequisites, dependencies, teaching scope, and completion criteria. Blueprint references inform assessment intent, grammar, and coverage mappings but do not replace curriculum architecture.

### Appropriate architecture depth

A complete learning architecture is complete in outcome coverage, domains, objectives, prerequisites, dependencies, assessment intent, completion criteria, and visible gaps.

> Complete in coverage and dependency structure, not complete in authored content.

It does not require complete lesson prose, complete claim sets, complete questions, or detailed content for every deferred module.

### Prior learning and waivers

A realization plan visibly records each relevant prerequisite as:

- included normally;
- supplied through a bridge;
- satisfied by prior learning;
- satisfied by evidence;
- satisfied by a diagnostic assessment; or
- temporarily waived.

Prior-learning assertions and waivers remain visible. They may lower confidence, restrict downstream scope, or qualify completion claims. When a blocking prerequisite is asserted rather than demonstrated, the agent recommends verification. Conversation memory cannot establish satisfaction.

### Capability lifecycle

Capability records distinguish:

- discovered;
- recommended;
- approved;
- configured;
- healthy;
- unavailable; and
- revoked.

Discovery is not activation. Recommendation is not approval. Approval is not configuration, and approval/configuration is not proof of health.

### Discovery timing

Discovery occurs during initial subject/project planning, on entry to a new workflow stage, when required roles are unsatisfied, when a requested action needs a new capability, or when an existing capability becomes unavailable/revoked. It does not run continuously during ordinary study turns.

### Runtime independence

Capability discovery belongs to Subject Builder/runtime orchestration. The deterministic learning core does not discover MCP servers, connectors, provider APIs, skills, or local utilities. Packs contain no credentials or runtime configuration. Installed packs remain usable when optional capabilities are unavailable, and normal study never depends on live discovery.

## Implementation details still deferred

Acceptance does not select or lock:

- exact artifact serialization or repository location;
- pack-format version or fields;
- JSON schemas;
- database representation or migration;
- tool-contract operations or request/response changes;
- stable objective-version mapping details;
- waiver expiry, confidence calculation, or diagnostic thresholds;
- reviewer qualifications or identity/authentication;
- approval record shapes and edit-invalidation rules;
- capability provider behavior, exact lifecycle persistence, health expiry, or audit format;
- asset media types, file/dimension limits, SVG/derivative policy, or terminal rendering details;
- originality/similarity algorithms;
- concrete modules, dependencies, Hermes integration, or MCP/AWS setup.

These require milestone-specific design review and explicit implementation authorization.

## Documents aligned

- [Product principles](../product-principles.md)
- [Assessment research policy](../assessment-research-policy.md)
- [Subject Builder architecture](../subject-builder-architecture.md)
- [Curriculum planning](../curriculum-planning.md)
- [Capability discovery](../capability-discovery.md)
- [Current status](../current-status.md)
- [Roadmap](../roadmap.md)
- [Project context](../project-context.md)
- [README](../../README.md)
- [Next-phase design handoff](subject-builder-next-phase-design.md)

## Scope confirmation

This acceptance task changed documentation only. It added no implementation or test code, pack format or content, diagram/asset bytes, AWS content, MCP integration/setup, capability provider, JSON tool, database table/migration, Hermes behavior/configuration, credential, dependency, or learner-state change.
