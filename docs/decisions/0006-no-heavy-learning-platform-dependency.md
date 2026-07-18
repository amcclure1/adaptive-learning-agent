# ADR 0006: No Heavy Learning-Platform Dependency for the MVP

Status: Accepted
Date: 2026-07-18

## Context

Complete learning platforms can provide broad content, course, web, user, and deployment features. The MVP needs a narrow local kernel and would inherit substantial assumptions and infrastructure by adopting a full platform.

## Decision

Do not depend on Lumen, OpenTutor, or another complete learning platform for the MVP. Prefer focused standard-library components and small libraries for concrete gaps. Study external projects only for patterns or narrowly reusable components with compatible licensing.

## Consequences

- The project owns a smaller, purpose-built domain model.
- Dependency and deployment footprints remain constrained.
- Some features available in mature platforms must be designed or deferred.
- Adding a major platform later requires demonstrated need and a new ADR.

## Alternatives considered

- Adopt a complete platform and disable unused features: rejected because unused architecture still creates maintenance and coupling.
- Copy large subsystems from other projects: rejected due to fit, licensing, and long-term maintenance risk.
- Add focused libraries only when needed: accepted as the incremental path.
