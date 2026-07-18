# ADR 0005: File-Based Portable Subject Packs

Status: Accepted
Date: 2026-07-18

## Context

Subject content must be inspectable, versionable, exportable, shareable, and independent of the learner database and runtime. Evidence-sensitive packs need structured provenance alongside readable explanatory content.

## Decision

Define subject packs as versioned directories or safe archives of YAML, JSON, Markdown, and approved static assets. Packs contain structured objectives, deterministic questions, sources, claims, and reviews but no learner data, credentials, runtime configuration, or executable code.

The exact format version, schemas, canonicalization, and archive limits remain proposed until reviewed.

## Consequences

- Packs work naturally with Git and ordinary editors.
- Validators must handle cross-references, canonical digests, archive safety, and compatibility.
- Pack content licensing and provenance remain the pack maintainer's responsibility.
- Operational state and portable content have separate backup/export lifecycles.

## Alternatives considered

- Store canonical content in SQLite: rejected because it reduces portability and reviewability.
- Runtime-specific prompts or skills as packs: rejected because they couple content to an agent and cannot enforce deterministic scoring.
- Executable pack plugins: rejected for the MVP due to security and portability risks.
