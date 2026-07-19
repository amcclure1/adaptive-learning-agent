# ADR 0009: Explicit Format 0.2 for Sourced Packs

Status: Accepted
Date: 2026-07-18

## Context

Accepted format 0.1 permits exactly one Markdown lesson and has no representation for authoritative sources, official question identity, origin, pool currency, errata, language, component rights, or human approval. A real Amateur Extra pilot needs those semantics. Adding them as optional format-0.1 fields would conflict with strict unknown-field rejection and could let an older loader misinterpret sourced content.

## Decision

Introduce explicit `format_version: "0.2"` for sourced packs. Format 0.2 retains UTF-8 JSON plus Markdown, strict closed-object validation, unpacked directories, standard-library parsing, and deterministic canonical digests. The loader dispatches by exact format version. Format 0.1 and its digest, files, validation, responses, and behavior remain unchanged.

Format 0.2 may add only:

- multiple ordered lessons;
- language and optional tags;
- assessment-pool identity, effective dates, and declared errata metadata;
- question origin and official question identifiers;
- source and citation records;
- component-level rights records;
- one human approval record per released pack version.

It does not add YAML, archives, assets, executable content, network retrieval, RAG, embeddings, evidence graphs, signing, new scoring types, mastery, scheduling, authoring agents, or marketplace behavior.

SQLite, deterministic scoring, attempts, confidence, sessions, retries, challenge quarantine, and objective progress remain unchanged.

### Rights

Rights are component-scoped, not pack-wide. Official NCVEC pool material uses rights status `public_domain` and cites NCVEC's release statement; public-domain status is not a license. Original project lessons and explanations use `CC-BY-4.0`. Project code and schemas remain under Apache License 2.0 and are outside pack-content rights. External official sources use `reference_only`; packs redistribute only metadata, links, locators, titles, publisher details, and optional digests unless separate authorization exists. The normative project policy is [rights-policy.md](../rights-policy.md).

### Sources and snapshots

Source records carry stable identity, title, publisher, type, URL, retrieval date, applicable effective dates, revision or errata identity, optional locator information, and optional `content_sha256`. The digest is required when an author retained and used a local source snapshot and may be absent for a live reference with no retained copy. Snapshots need not be distributed in the pilot.

Validation and study never fetch external URLs. Remote availability cannot affect installation, digesting, scoring, or study. The pack digest covers source metadata and a declared `content_sha256`, not live remote bytes. Freshness checking is a later editorial workflow.

### Approval

Every released format-0.2 pack version contains one human approval record with `status`, `reviewed_by`, `reviewed_at`, non-empty `review_scope`, and optional `notes`. An installable pack requires `status: "approved"`. The engine validates structure and status only; it neither authenticates the reviewer nor supplies signatures. Any digest-covered content change requires a new pack version or renewed approval.

### Errata and question identity

Errata knowledge is pack metadata, never hard-coded engine logic. An assessment-pool record includes pool ID, title, publisher, effective start/end, declared errata revision, withdrawn official IDs, and optionally future replaced/superseded IDs. The validator rejects invalid date ranges, missing required pool/errata metadata, duplicate official IDs, and any included official ID declared withdrawn. It does not query or decide whether the declared revision is current.

`official_pool` questions require a preserved official ID, pool/source reference, source-question reference, exact official wording, exact option order, exact answer key, and explanation citations/source references. `generated` questions forbid an official ID and any claim of appearing in an official examination or pool. The E1A pilot includes no generated questions.

### Contract and presentation

The runtime-neutral tool contract remains version `0.1`; there is no separate 0.2 tool family. Future `system.health` output adds capabilities for supported pack formats, sourced content, multiple lessons, official identity, and post-answer citations. Existing required fields remain unchanged and new provenance fields are optional/additive. Format-0.1 response semantics remain unchanged.

`study.next` may expose origin and official ID but never the answer key, explanation, or answer-revealing citations. `study.submit` may expose explanation citations and source summaries after scoring. Complete provenance lives in deterministic tool results; a Hermes skill may present a concise label by default and expand it on request, but must never call project-authored prose official NCVEC commentary.

### Digest and layout

Format 0.2 is an unpacked directory containing `pack.json`, declared Markdown lessons, and optional `NOTICE.md`. Machine validation relies only on `pack.json`; no separate source, question, or citation file is required for this pilot. The canonical digest covers the canonical manifest, each declared lesson in declared lesson order, and optional `NOTICE.md`, with domain separation. Changing or reordering lessons therefore changes both digest and presentation order. Official content modifications require a new pack version/digest and never silently replace installed content.

## Consequences

- Format 0.1 fixtures and behavior remain compatible without migration.
- Sourced content, official identity, human approval, and component rights become inspectable offline.
- Pack parsing/model/digest code and additive tool results will need narrow future implementation changes.
- SQLite and deterministic learning behavior need no change.
- The engine can verify declared structure and internal consistency but not source freshness, legal status, reviewer identity, or truth of an authorship claim.

## Alternatives considered

- Optional format-0.1 fields: rejected because strict 0.1 loaders reject them and old semantics cannot safely consume multiple lessons or provenance.
- General evidence subsystem: rejected because source records and citations meet the pilot requirement.
- YAML, archives, or assets in 0.2: rejected for this milestone because none is needed for sourced text content.
- Pack-wide license: rejected because official pool material, original prose, project code, and references have different rights bases.
- Mandatory embedded snapshots: rejected because deterministic reference metadata and optional retained-snapshot digests meet the pilot need without redistributing source documents.
- New contract 0.2: rejected because operation semantics and request shapes remain compatible; explicit additive capabilities are sufficient.
- Cryptographic reviewer identity: deferred because a local human attestation is sufficient for this single-user pilot.

## Resolved review questions

- Component rights use explicit `public_domain`, `licensed`, and `reference_only` semantics; public domain is not represented as a license.
- `content_sha256` is optional generally and required exactly when a retained local snapshot was used.
- Tool changes are additive under runtime-neutral contract `0.1`, advertised by `system.health` capabilities.
