# ADR 0010: Whole Learning Architecture with Progressive Realization

Status: Proposed
Date: 2026-07-19

## Context

Building only the content requested in the moment can hide missing prerequisites, incomplete outcome coverage, and future integration problems. Requiring all content up front would make pilots too large and slow. The project needs both whole-plan coherence and incremental delivery.

## Proposed decision

Define a versioned, human-approved learning architecture for the complete stated outcome, then define independently versioned realization plans that select the portion to build now. Realizations reference one architecture version and visibly record selected, bridged, omitted, and deferred objectives.

Classify dependencies as blocking prerequisite, bridge prerequisite, recommended context, or independent objective. When a learner requests partial scope, map it into the whole architecture, report consequences, and recommend the smallest coherent realization. Refuse or revise scope only when it cannot satisfy the stated outcome.

Architecture revisions produce impact reports but do not silently migrate installed packs or learner progress.

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

## Acceptance prerequisites

- Review the four dependency categories and their validation expectations.
- Decide the authoritative serialization and repository location for architecture, realization, and impact artifacts.
- Define stable objective-version semantics and how pack objectives map to them.
- Define the human approval scope for architecture and realization changes.
