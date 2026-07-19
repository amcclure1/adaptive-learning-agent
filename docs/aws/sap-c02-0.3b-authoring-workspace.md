# SAP-C02 0.3B Authoring Workspace and Compilation Boundary

Status: final design proposal; no workspace or compiler implemented
Design date: 2026-07-18

## Decision summary

Use a separate file-backed authoring workspace as the canonical owner of sources, claims, drafts, reviews, and release evidence. Do not put authoring state in SQLite. Do not extend pack format 0.3 or introduce format 0.4 for the first manual pilot. After all approvals, compile a learner-facing projection into existing format 0.2 by default, or existing format 0.3 only if a separately reviewed supported-PNG need is demonstrated.

This is proposed architecture under [ADR 0017](../decisions/0017-authored-content-workspace-release-projection.md) and [ADR 0020](../decisions/0020-compile-authored-content-to-existing-pack-formats.md), not implemented behavior.

## Proposed repository ownership

The exact serialization remains an implementation task, but the ownership boundary is fixed:

| Artifact | Canonical owner | Ships in installed pack? | Notes |
|---|---|---:|---|
| Source register | Authoring workspace files | Projection only | Pack gets allowed source summaries/citations; full review/freshness history stays authoring-side |
| Claim workspace | Authoring workspace files | No full records | Release-evidence manifest binds approved claim IDs/digests; learner pack gets supporting citations/explanations |
| Question design specifications | Authoring workspace files | No | They are planning records, not learner content |
| Question drafts and requirement matrices | Authoring workspace files | Only final learner projection | Rejected/options-review history stays out |
| Approval records | Authoring workspace/release-evidence files | Pack-release approval only, as existing format requires | Source/claim/question/uniqueness identities/findings remain authoring-side unless explicitly public |
| Assessment blueprint | `docs/aws/` design artifact, referenced by workspace | No | Accepted version is an authoring input |
| Learning architecture/dependency model | `docs/aws/` design artifacts, referenced by workspace | Objective projection only | Whole architecture remains separate from one pack realization |
| Realization plan | Authoring workspace or accepted design file | No full plan | Pack scope/objectives reflect selected realization; omissions/gaps remain authoring/release records |
| Lessons | Authoring workspace Markdown | Yes, approved compiled bytes | Exactly two for the pilot |
| Compiled released pack | Pack directory under existing conventions | Yes | Immutable learner-facing projection after approval |
| Release-evidence manifest | Release review/handoff area | No | Binds workspace inputs, compiler version, output digest, and approvals |

## Illustrative layout

This layout is informative, not a created directory or schema commitment:

```text
authoring/aws-sap-c02-org-04/
├── workspace.json
├── sources/
│   └── sources.json
├── claims/
│   ├── AWS-ORG-CLAIM-001.json
│   └── ...
├── lessons/
│   ├── lesson-01.md
│   └── lesson-02.md
├── question-specs/
│   ├── QSPEC-01.json
│   └── ... QSPEC-05.json
├── questions/
│   ├── Q-01.json
│   └── ... Q-05.json
├── reviews/
│   ├── sources/
│   ├── claims/
│   ├── question-content/
│   ├── uniqueness/
│   └── pack-release/
├── validation/
└── releases/
    └── release-evidence.json
```

JSON is preferred for structured records because the repository already has strict standard-library JSON practice. Markdown remains appropriate for lessons and human-facing review summaries. YAML is not introduced without a separate parser/canonicalization decision.

## Pack-format evaluation

### Extend format 0.3

Rejected for this pilot. Format 0.3 is a fixed asset-capable learner-pack contract. Adding claims and layered editorial review fields would break its strict closed semantics and conflate asset delivery with authoring workflow.

### Introduce format 0.4

Deferred. A new format is justified only if installed packs must themselves carry claim IDs, layered approvals, full distractor rationales, claim freshness horizons, or offline authoring-chain verification. The first pilot can retain that trace in release evidence while delivering learner-facing content through an existing format.

### Authoring workspace plus compilation

Recommended. The text-only pilot compiles to format 0.2. Existing format 0.3 is available only for a demonstrably necessary approved static PNG and is not extended. The compiler uses an explicit field allowlist; unapproved drafts, internal notes, and authoring-only records are errors if encountered in the release projection.

## What belongs in the installed pack

The compiled pack should contain:

- exact pilot identity/version and `original/generated` question origin semantics;
- selected objectives and exactly two approved lessons;
- exactly five approved final questions, ordered options, keys, response behavior, and learner-facing explanations;
- citations/source summaries and precise locators needed to support learner-facing material;
- rights records and notices;
- the existing human pack approval record;
- static PNG asset/accessibility data only if the separately reviewed format-0.3 path is used.

It should not contain:

- rejected or superseded drafts;
- full atomic claim records and derivation workpapers;
- requirement-option matrices or internal distractor taxonomies as editorial data;
- private reviewer notes, conflict disclosures, or source/claim/question/uniqueness reviewer identities;
- originality comparison notes or protected source expression;
- capability configuration, credentials, AWS data, learner data, or runtime state.

### Approved claims

Full claim records stay authoring-side. The pack ships the material learner-facing citations and explanations derived from them. The release-evidence manifest records exact claim IDs/digests and proves which approved claims compiled into each question/lesson.

### Distractor rationales

Full per-option reviewer rationales and requirement matrices stay authoring-side. Concise, learner-safe reasons why incorrect options fail should be included post-answer when the existing explanation field can express them clearly. If per-option structured learner output becomes a requirement that existing formats cannot preserve, propose format 0.4 rather than overloading a field.

### Review identities

Only the reviewer identity already required by the compiled pack's pack-approval record ships. Other reviewer identities and qualifications remain in release evidence; private contact details never ship. Public attribution requires explicit reviewer consent.

### Freshness data

Pack source records retain retrieval/effective/revision metadata and optional snapshot digests supported by the selected format. Claim-specific horizons, recheck schedules, stale history, and review findings remain authoring-side. Release evidence records the final freshness checks.

## Compilation contract

The future compiler accepts only:

1. one accepted blueprint version;
2. one accepted architecture/realization version;
3. exact approved source and claim versions;
4. exactly two approved lessons;
5. exactly five questions with current content and uniqueness approvals;
6. current rights and freshness decisions;
7. an explicit target format (`0.2` by default; `0.3` only with approved asset need).

It produces:

- a candidate pack directory;
- deterministic compiled-pack digest using the existing target-format algorithm;
- a release-evidence manifest binding all input IDs/versions/digests, validator versions, compiler version, output digest, exclusions, and approval IDs;
- diagnostics.

It does not approve, install, activate, publish, fetch sources, or modify the workspace. Recompilation after any input change produces a new candidate digest and invalidates prior pack-release approval.

## Smallest future authoring operations

These operations are proposed only; manual file editing remains possible.

| Group | Operation | Boundary |
|---|---|---|
| Source | `source.register`, `source.validate`, `source.review` | Workspace-relative records; public URLs as data; no unrestricted network/filesystem access |
| Claim | `claim.create`, `claim.validate`, `claim.review`, `claim.impact` | Explicit source/claim IDs; model may draft, human supplies review decision |
| Question design | `question_spec.validate`, `question.create` | Exact blueprint/objective/spec IDs; no approval side effect |
| Question review | `question.validate`, `question.review_content`, `question.review_uniqueness`, `question.impact` | Separate human decisions; deterministic checks advisory only |
| Release | `pack.compile`, `pack.validate_candidate`, `pack.review_release` | Allowlisted workspace inputs and explicit output directory; no install/publish/tag |

Authoring operations are a separate module/CLI or tool surface from the ten learner-study operations. They must not be registered in the learner Hermes plugin by default. Inputs use IDs and workspace-relative paths, not arbitrary absolute paths, shell commands, or open-ended URLs. Public retrieval remains an explicitly controlled research capability outside deterministic compilation.

## Persistence and concurrency

Files and Git satisfy the single-author/manual pilot. A future implementation should use atomic file replacement, canonical serialization, per-record digests, conflict detection against expected prior digest, and no silent merge. SQLite tables are not justified because no runtime learner-state behavior requires these records. Multi-user hosted authoring would require measured need and a new decision.
