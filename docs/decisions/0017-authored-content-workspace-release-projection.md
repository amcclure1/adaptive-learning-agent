# ADR 0017: Authored-Content Workspace and Released-Pack Projection

Status: Accepted
Date: 2026-07-18

## Context

The SAP-C02 0.3B pilot needs draft sources, atomic claims, question design specifications, learner-ready drafts, layered reviews, invalidation history, and compilation evidence. Installed learner packs need reviewed lessons, questions, explanations, citations, rights, and release approval, but should not expose draft material, private reviewer notes, rejected alternatives, or authoring workflow state.

Putting every authoring record in a pack would enlarge the portable learner format around editorial concerns. Making SQLite canonical would conflict with file-backed portable content and use an operational learner-state database for authoring governance.

## Decision

Use a separate, Git-versioned, file-backed authored-content workspace as the canonical owner of 0.3B draft and review records. Compile an approved release projection into an existing supported pack format only after every required approval is current.

The workspace layout is fixed under `authoring/<project-id>/` with `project.json`, `sources/`, `claims/`, `lessons/`, `question-specs/`, `questions/`, `validations/`, `approvals/`, and `release/`. Draft and immutable-revision ownership, record identities, canonicalization, and paths are defined in [the authoring-workspace contract](../aws/sap-c02-0.3b-authoring-workspace.md) and [the schema contract](../aws/sap-c02-0.3b-schemas.md).

The workspace contains source records, claims, design specifications, question drafts, lessons, immutable approval/review records, generated validation reports, and release evidence. It contains no learner data, credentials, runtime configuration, browser state, temporary downloads, licensed source copies, private AWS data, private notes intended to stay outside Git, or executable content.

The installed pack contains only learner-facing reviewed content and the provenance/rights/pack-approval fields required by the selected existing pack format. Authoring histories, rejected drafts, full claim records, detailed review findings, originality notes, and non-release reviewer identities remain outside the installed pack.

SQLite remains learner-state storage and gains no authoring tables.

## Release projection

Compilation is deterministic and fail-closed. It selects exact approved artifact versions, checks their digests and approval dependencies, creates a candidate pack directory, and emits a release-evidence manifest binding the workspace inputs to the compiled pack digest. Compilation never creates approval and never activates content.

The release-evidence manifest remains an authoring/release artifact beside the pack rather than a learner-state record. It makes the claim and review chain inspectable without requiring installed packs to contain the full editorial workspace.

## Consequences

- Git and ordinary file review remain the authoritative authoring workflow.
- Drafts and private review notes cannot accidentally become learner-facing pack data when the compiler uses a strict projection allowlist.
- Pack review can bind exact compiled bytes to exact approved inputs.
- The compiler and workspace validators become future implementation work.
- A hosted collaborative authoring service remains unnecessary.

## Alternatives considered

- Put all authoring records in packs: rejected because drafts and governance history are not learner-facing portable content.
- Make SQLite canonical: rejected because authoring artifacts are versioned content/review records, not operational learner state.
- Keep only free-form Markdown notes: rejected because deterministic cross-reference, approval, freshness, and compilation checks require structured records.

## Fixed implementation contract

- Structured records use strict UTF-8 JSON and stable IDs independent of filenames where practical; lessons bind strict JSON records to normalized Markdown bytes.
- Draft writes require an expected prior digest and atomic replacement. Immutable revisions, approvals, and release evidence are append-only; silent merge or retargeting is forbidden.
- Reviewer contact details, credentials, private notes, source copies, and temporary retrieval state remain outside Git. Public records retain only the bounded identity, role, qualification summary, conflict declaration, scope, and findings required by review policy.
- Validation reports are generated and replaceable until selected for release, but release evidence binds the exact report ID, source commit, and digest used.
- The two-phase release-evidence shape avoids a digest cycle: the compiler emits candidate evidence; a later approved finalization emits a new final manifest binding the pack-release approval without changing the historical candidate manifest.

These decisions authorize a later implementation task to build the bounded file workspace and deterministic compiler. They do not authorize content authoring, compilation of a real pilot pack, installation, publication, or runtime changes.
