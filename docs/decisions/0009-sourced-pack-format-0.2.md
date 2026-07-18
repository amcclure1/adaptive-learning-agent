# ADR 0009: Explicit Format 0.2 for Sourced Packs

Status: Proposed
Date: 2026-07-18

## Context

Accepted format 0.1 deliberately permits exactly one Markdown lesson and has no representation for authoritative sources, official question identity, origin, pool currency, errata, language, or component rights. A real Amateur Extra pilot needs those semantics. Adding them as ignorable optional 0.1 fields would conflict with 0.1's strict unknown-field rejection and would let old loaders misinterpret sourced content.

## Proposed decision

Introduce explicit `format_version: "0.2"` while retaining JSON plus Markdown, strict validation, unpacked directories, and standard-library parsing. A future loader would dispatch by exact format version and continue accepting format 0.1 unchanged.

Format 0.2 would add multiple ordered lessons; language; assessment-pool identity/effective dates; source records and structured citation references; official/generated question origin; preserved official identifiers; errata metadata; scoped rights records; and optional tags. It would not add YAML, archives, executable content, assets, RAG, embeddings, evidence graphs, signing, new scoring types, mastery, scheduling, or authoring agents.

The canonical digest would cover the manifest and every referenced lesson in normalized path order. Official content modifications would require a new pack version/digest; they would never silently replace an installed pack. Withdrawn official identifiers would fail validation.

## Consequences

- Old format-0.1 fixture bytes and behavior can remain unchanged.
- Sourced content becomes inspectable offline and distinguishable from generated content.
- The parser, pack model, digest procedure, selected tool outputs, and Hermes presentation need narrow changes.
- SQLite and deterministic learning behavior need no change.
- Two explicit loader branches are more work than one, but avoid ambiguous compatibility and migration behavior.

## Alternatives

- Optional 0.1 fields: rejected because strict 0.1 loaders reject them and older semantics cannot safely consume multiple lessons or provenance.
- A general evidence subsystem: rejected because source records and citations meet the pilot need.
- YAML or archives in 0.2: deferred; neither is needed to prove sourced content.

## Review questions

- Is the proposed component-level rights representation sufficiently clear without implying that public-domain status is a license?
- Should a source record preserve a retrieved-content digest in 0.2 or defer byte snapshots until export/reproducibility work?
- Should 0.2 tool responses be additive under contract 0.1 or explicitly identify a contract-minor capability?
