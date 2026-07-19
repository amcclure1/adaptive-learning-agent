# Amateur Extra 0.2A Final Design Handoff

Date: 2026-07-18
Status: implementation-ready design; implementation not authorized

## Accepted decisions

- ADR 0009 is `Accepted`; all of its review questions are resolved.
- Format 0.1 remains unchanged. Sourced packs use exact `format_version: "0.2"`.
- Format 0.2 is strict, unpacked, directory-based UTF-8 JSON plus Markdown and adds only the accepted sourced-content fields.
- SQLite and deterministic scoring/state behavior remain unchanged.
- Tool contract version remains `0.1`; sourced-content support is advertised through additive optional capabilities and provenance fields.
- Rights are component-level under [rights-policy.md](../rights-policy.md).
- One structurally valid human approval record with `status: "approved"` is required per installable released pack version.
- Errata and withdrawals are declared pack metadata, not hard-coded or network-fetched engine knowledge.

## Final format shape

```text
amateur-extra-e1a/
├── pack.json
├── lessons/
│   ├── 01-band-edges.md
│   └── 02-special-operations.md
└── NOTICE.md
```

`NOTICE.md` is optional, human-facing, and digest-covered; `pack.json` remains machine-authoritative. The manifest contains pack identity/version, language/tags, one assessment-pool record, component rights, sources, objectives, ordered lessons, questions, and one approval record. No separate question/source/citation files are required for this pilot.

The format-0.2 digest uses a distinct domain and covers canonical `pack.json`, normalized lesson paths/content in declared order, and optional normalized `NOTICE.md`. It never covers or fetches live remote content.

## Final rights policy

- Official NCVEC pool wording, choices, answer keys, and identifiers: `public_domain`, scoped only to material covered by the cited NCVEC release statement. Public domain is not a license.
- Original project lessons and explanations: `licensed`, `CC-BY-4.0`, copyright `Adaptive Learning Agent contributors` unless a contributor uses a more precise designation.
- Project code and schemas: Apache License 2.0 outside pack-content rights.
- External official sources: `reference_only`; redistribute metadata, URLs, locators, titles, publisher details, dates/revisions, and optional digests only unless separately authorized.
- Pilot prohibition: logos, seals, screenshots, branding assets, substantial external-source copies, and unofficial third-party study text.

This is project policy, not legal advice or formal legal review.

## Source snapshot and digest policy

Source records require stable ID, title, publisher, type, HTTPS URL, retrieval date, retained-snapshot declaration, and rights reference; they support effective dates, revision/errata identity, locator, and `content_sha256`.

`content_sha256` is required when the author retained and used a local source snapshot and absent when no snapshot was retained. The pilot need not redistribute complete snapshots. Validation and study never fetch URLs, test freshness, or depend on source availability. The pack digest covers declared source metadata/hash only. Freshness is a later editorial responsibility.

## Approval policy

Every released pack version has one record containing `status`, `reviewed_by`, UTC `reviewed_at`, non-empty `review_scope`, and optional notes. Installable status requires `approved`. The E1A scope covers official wording, option ordering, answer keys, official IDs, lessons, explanations, citations, rights, and pool/errata metadata.

The engine validates structure, allowed scope, and status only. It does not authenticate the reviewer or sign the pack. A digest-covered content change requires a new pack version or renewed approval; machine validation cannot prove that the named human actually repeated the review.

## Errata and origin policy

The pool record carries pool ID/title/publisher, effective dates, pool/errata sources, declared errata revision, withdrawn IDs, and optional future superseded IDs. Validation rejects invalid date ranges, missing required pool/errata data, duplicate official IDs, and included withdrawn/superseded official IDs. It does not decide whether the revision is current.

`official_pool` requires the preserved official ID, pool/source and source-question references, exact wording, exact option ordering, exact key, official-content rights, and cited original explanation. `generated` forbids an official ID or any official-exam/pool claim. The E1A pilot has zero generated questions.

## Tool and presentation policy

Future `system.health` capability data reports supported pack formats, sourced content, multiple lessons, official identity, and post-answer citations. Existing required fields and format-0.1 semantics stay unchanged.

`study.next` may add origin and official ID but cannot reveal keys, explanations, or answer-revealing citations. `study.submit` may add complete explanation citations/source summaries after scoring. Deterministic tools own complete provenance. Hermes always names official questions by ID, gives a concise source label after feedback, offers expanded sources on request, and never calls project prose official NCVEC commentary.

## Questions still unresolved

No design question from ADR 0009 remains unresolved. Future release execution must still supply:

- the named human reviewer and completed approval;
- actual retained-snapshot choices and hashes;
- a current NCVEC/FCC/errata recheck;
- authored and reviewed E1A content;
- optional formal legal review if project maintainers want it.

## Exact future implementation scope

Only a separately authorized implementation task may:

1. add a strict format-0.2 model/loader branch while preserving format 0.1;
2. validate paths, sources/snapshots, citations, pool/errata, origins, component rights, and approval;
3. compute/copy the accepted format-0.2 digest/layout;
4. add optional contract-0.1 capabilities/provenance without new operations or inputs;
5. update Hermes presentation for ordered lessons, official IDs, and post-answer citations;
6. add the 19 required validation/compatibility cases plus E1A-specific acceptance tests;
7. in a separately explicit content scope, add the reviewed 11-question/two-lesson E1A pack.

The parser/tool/presentation implementation and real-content authoring may be split into separate reviews to keep provenance review independent from engine code.

## Exact implementation non-goals

- No changes to SQLite, scoring types/rules, attempts, confidence, sessions, retries, quarantine, objective progress, mastery, scheduling, readiness, or exam simulation.
- No YAML, archives, assets, executable content, network fetcher, freshness service, RAG, embeddings, vector database, evidence graph, signing, marketplace, authoring agent, or autonomous approval/publication.
- No full Extra pool, diagrams, generated E1A questions, brain dumps, recalled questions, unofficial explanations, or third-party study text.
- No new tool family, operation, or request argument and no format-0.1 semantic change.

## Documents changed by design finalization

- `docs/decisions/0009-sourced-pack-format-0.2.md`
- `docs/rights-policy.md`
- `docs/pack-format-0.2-proposal.md`
- `docs/amateur-extra-pilot-0.2.md`
- `docs/test-plan.md`
- `docs/handoffs/amateur-extra-0.2-design.md`
- `docs/handoffs/amateur-extra-0.2-final-design.md`
- `docs/current-status.md`
- `docs/roadmap.md`
- `docs/project-context.md`

## Scope confirmation

This task changed documentation only. It added no implementation code, test code, real Amateur Extra wording/choices/keys, lesson/explanation content, pack data, database change, tool behavior, or Hermes behavior.
