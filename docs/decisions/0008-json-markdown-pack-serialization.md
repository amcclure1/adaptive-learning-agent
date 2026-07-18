# ADR 0008: JSON and Markdown Pack Serialization for Version 0.1

Status: Accepted
Date: 2026-07-18

## Context

ADRs 0001 and 0005 permit portable file-based packs containing YAML, JSON, and Markdown but leave the first serialization unresolved. Supporting more than one representation would expand validation and compatibility work before the runtime-independent vertical slice is proven.

## Decision

Version 0.1 packs are unpacked directories containing exactly one `pack.json` file and one referenced UTF-8 Markdown lesson. Structured objectives and questions live in JSON; instructional prose lives in Markdown. The accepted fields, validation rules, and digest procedure are defined in `docs/mvp-vertical-slice.md`.

Use Python's standard-library JSON parser. Unknown fields are validation errors. Version 0.1 does not accept YAML, archives, signatures, static assets, or multiple serialization forms.

A later format may add YAML only through an explicit format-version and ADR decision that addresses parser choice, safe loading, canonicalization, and compatibility. This decision narrows, rather than reverses, ADRs 0001 and 0005.

## Consequences

- The first runtime has no pack-parser dependency.
- Parsing behavior and canonical JSON bytes are straightforward to test.
- The initial validation and security surface is small.
- Hand-authored structured content is less ergonomic than YAML and cannot contain comments.
- Existing broader YAML format proposals remain future design material, not version-0.1 contracts.

## Alternatives considered

- YAML plus Markdown: deferred because it requires choosing and securing an additional parser before a concrete authoring need exists.
- Accept JSON and YAML: rejected because two equivalent inputs double early validation and compatibility cases.
- Put prose in JSON: rejected because Markdown is easier to review and preserves the portable-content boundary.
- ZIP archives: deferred until export or sharing creates a concrete archive requirement.
