# ADR 0004: SQLite for Operational Learner State

Status: Accepted
Date: 2026-07-18

## Context

The MVP needs transactional attempts, progress, sessions, idempotency, and backup on one local machine. It does not need hosted concurrency or a database service.

## Decision

Use SQLite as the only operational learner-state database for the MVP. Use explicit transactions, foreign keys, forward migrations, integrity checks, and SQLite-safe backup/restore. Subject-pack content remains file-based rather than being made canonical in SQLite.

## Consequences

- The Python standard library supplies the database driver.
- Installation requires no database server or credentials.
- Local concurrency and filesystem behavior must be tested.
- A hosted multi-user service would require a new decision and migration plan.

## Alternatives considered

- JSON or YAML learner-state files: rejected because transactional multi-entity updates and constraints would be fragile.
- PostgreSQL: rejected because a database service is unnecessary for the local MVP.
- Redis or an event queue: rejected because request-driven local workflows do not require them.
