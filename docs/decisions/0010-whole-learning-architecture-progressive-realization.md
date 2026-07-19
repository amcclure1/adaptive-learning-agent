# ADR 0010: Whole Learning Architecture with Progressive Realization

Status: Accepted
Date: 2026-07-19

## Context

Building only the content requested in the moment can hide missing prerequisites, incomplete outcome coverage, and future integration problems. Requiring all content up front would make pilots too large and slow. The project needs both whole-plan coherence and incremental delivery.

## Decision

Define a versioned, human-approved learning architecture for the complete stated outcome, then define independently versioned realization plans that select the portion to build now. Realizations reference one architecture version and visibly record selected, bridged, omitted, and deferred objectives.

Classify dependencies as blocking prerequisite, bridge prerequisite, recommended context, or independent objective. When a learner requests partial scope, map it into the whole architecture, report consequences, and recommend the smallest coherent realization. Refuse or revise scope only when it cannot satisfy the stated outcome.

Architecture revisions produce impact reports but do not silently migrate installed packs or learner progress.

An assessment blueprint is an independent assessment-model artifact. One blueprint may support multiple learning architectures, and one learning architecture may reference zero, one, or several blueprints. Non-certification learning does not require an external exam blueprint. The learning architecture—not the blueprint—owns curriculum coverage, prerequisites, dependencies, and completion criteria.

A complete learning architecture is complete in outcome coverage, domains, objectives, prerequisites, dependencies, assessment intent, completion criteria, and visible gaps. It does not require complete lesson prose, claim sets, questions, or detailed content for every deferred module. It is **complete in coverage and dependency structure, not complete in authored content**.

A realization plan records how each relevant prerequisite is handled: included normally, supplied through a bridge, satisfied by prior learning, satisfied by evidence, satisfied by a diagnostic assessment, or temporarily waived. Prior-learning assertions and waivers remain visible and may reduce confidence or narrow completion claims. When a blocking prerequisite is asserted rather than demonstrated, the planner recommends verification.

## Consequences

- Small pilots remain possible without being mistaken for complete curricula.
- Learner choice is preserved while prerequisites and downstream gaps stay visible.
- Architecture and realization versions add authoring and review artifacts.
- Stable objective identity and change-impact rules become necessary before implementation.
- Current packs and SQLite remain unchanged until a later accepted serialization and integration design.

## Alternatives considered

- Build only requested modules with no whole plan: rejected because gaps and dependency conflicts emerge too late.
- Author the entire curriculum before any pilot: rejected because it prevents evidence-driven progressive delivery.
- Let the model infer prerequisites during each conversation: rejected because results would be inconsistent and non-authoritative.
- Treat every prerequisite as blocking: rejected because concise bridges and optional context are important for learner control.

## Deferred milestone details

Acceptance establishes the direction above but does not choose exact serialization, JSON schema, database representation, pack-format version, tool contract, or implementation modules. Milestone-specific reviews must still:

- define validation expectations for dependency and prerequisite-disposition categories;
- decide the authoritative serialization and repository location for architecture, blueprint references, realization, and impact artifacts;
- define stable objective-version semantics and how pack objectives map to them;
- define human approval scope for architecture and realization changes;
- define waiver expiry, confidence effects, and diagnostic-evidence requirements.
