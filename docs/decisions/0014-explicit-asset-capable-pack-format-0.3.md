# ADR 0014: Explicit Asset-Capable Pack Format 0.3

Status: Proposed  
Date: 2026-07-19

## Context

Strict format 0.2 rejects unknown fields and undeclared files and explicitly excludes assets. An official figure changes pack digest inputs, requires old loaders to understand mandatory pre-answer presentation, and must not be silently ignored. The 0.2B pilot needs one shared static figure without changing formats 0.1 or 0.2.

## Proposed decision

Introduce exact `format_version: "0.3"` for sourced packs with static local assets. Retain strict unpacked JSON/Markdown, deterministic version dispatch, source/pool/rights/approval semantics, offline operation, and the existing learning rules. Add only top-level asset records and ordered lesson/question asset references as specified in [the format proposal](../asset-pack-format-proposal.md).

Support only exact local PNG bytes in 0.3. Keep runtime-neutral tool contract version 0.1 and its ten operations, with additive format-0.3 capabilities and response descriptors. Keep SQLite schema 1.

Formats 0.1 and 0.2, their fields, declared inventories, digests, installed content, requests, responses, and study semantics remain unchanged.

## Rationale

Optional 0.2 fields would be rejected by a conforming loader and might be ignored by a permissive one even though the figure is required to answer. A distinct digest domain prevents ambiguity over whether asset bytes are covered. Explicit dispatch makes compatibility failure safe and testable.

## Consequences

- Asset-aware loaders can require presentation and integrity semantics.
- Existing packs need no migration or re-release.
- A third strict parsing/digest branch and compatibility tests are required.
- General multimedia, YAML, archives, and remote content remain deferred.
- Implementation and content import still require separate authorization and approval.

## Alternatives considered

- Extend format 0.2: rejected because it violates strict closed validation and permits unsafe old-loader behavior.
- Put the figure beside a 0.2 pack without declaring it: rejected because it is undeclared, unhashed, and non-portable.
- Encode the figure in Markdown/base64 or `pack.json`: rejected because it obscures inventory, expands JSON, and weakens media validation.
- Add a remote URL: rejected because study must remain offline and deterministic.

## Acceptance before changing status

Acceptance requires agreement on the closed asset record, PNG-only limits, raw-byte/pack digest procedure, reference semantics, approval scopes, logical runtime reference, no SQLite migration, and preservation tests for formats 0.1 and 0.2.

