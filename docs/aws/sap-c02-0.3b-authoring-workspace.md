# SAP-C02 0.3B Authoring Workspace and Compilation Boundary

Status: accepted contract; generic workspace infrastructure implemented; no AWS workspace or content created

## Decision

The canonical authoring system is a separate Git-versioned, file-backed workspace. SQLite remains learner-state only. Approved learner-facing content compiles into existing pack format 0.2 by default. Unchanged format 0.3 is eligible only when an independently approved static PNG is materially required. The first pilot does not create format 0.4.

This implements the documentation decisions in [ADR 0017](../decisions/0017-authored-content-workspace-release-projection.md) and [ADR 0020](../decisions/0020-compile-authored-content-to-existing-pack-formats.md). The generic standard-library infrastructure is implemented; this does not authorize AWS content creation, installation, activation, publication, tagging, or release.

## Fixed layout

```text
authoring/aws-sap-c02-org-04/
  project.json
  sources/
    drafts/
    revisions/<source-id>/<revision>.json
  claims/
    drafts/
    revisions/<claim-id>/<revision>.json
  lessons/
    drafts/<lesson-id>/lesson.json
    drafts/<lesson-id>/lesson.md
    revisions/<lesson-id>/<revision>/lesson.json
    revisions/<lesson-id>/<revision>/lesson.md
  question-specs/
    drafts/
    revisions/<specification-id>/<revision>.json
  questions/
    drafts/
    revisions/<question-id>/<revision>.json
  validations/
    current/
    reports/
  self-audits/
    records/
  verifications/
    runs/
    findings/
    resolutions/
    metrics/
  approvals/
    sources/
    claims/
    lesson-content/
    question-content/
    answer-uniqueness/
    pack-release/
    revocations/
  release/
    selections/
    candidates/
    evidence/
```

Verification records are authoring evidence outside installed packs and SQLite. Runs and findings bind exact target digests. Findings and resolutions are immutable; a resolution does not erase the finding, and only a completed fresh reverification establishes current eligibility.

Repository-relative paths and lower-case directory names are normative. Artifact identity comes from record fields, not filenames. Implementations must reject a path whose contained ID disagrees with its record.

## Ownership and mutability

| Record class | Owner/location | Mutability |
| --- | --- | --- |
| Project configuration and active draft records | `project.json` and each `drafts/` directory | Editable with expected-prior-digest checking; edits invalidate approvals over the prior digest |
| Released authoring revisions | Each `revisions/<id>/<revision>` location | Immutable and append-only |
| Validation reports | `validations/current/` and `validations/reports/` | Generated; current reports may be replaced, while a report selected by release evidence remains bound by ID, commit, and digest |
| Author self-audits | `self-audits/records/` | Immutable exact-digest procedural evidence; never an approval |
| Human approvals and review decisions | `approvals/` | Immutable append-only records; revocation/supersession is a new record |
| Release selections | `release/selections/` | Explicit compiler inputs; immutable once compiled |
| Candidate packs | `release/candidates/` | Generated compiled learner-facing output; immutable per candidate digest |
| Release evidence | `release/evidence/` | Generated immutable candidate/final manifests |
| Installed/released pack | Existing pack area, only in a separately authorized task | Not owned by the authoring workspace and never written automatically |

The common record, canonicalization, and revision rules are normative in [the schema contract](sap-c02-0.3b-schemas.md).

## Prohibited contents

The workspace must not contain credentials, session tokens, browser state, temporary downloads, caches, licensed source copies, copied exam-question text used for style comparison, or private notes intended to remain outside Git. Sensitive reviewer contact data is neither required nor permitted. Source records may retain an authorized snapshot digest without retaining the snapshot bytes.

## Installed-pack boundary

The installed pack receives only approved learner-facing content supported by the target format:

- approved lesson Markdown;
- approved final stems, ordered options, keyed option IDs, response rules, and learner-facing explanations;
- learner-safe citations and source summaries;
- rights, attribution, notices, objectives, and existing pack-approval projection.

The installed pack excludes full claims, internal locators beyond learner-safe citation needs, question specifications, requirement-option matrices, internal distractor rationales, originality and uniqueness findings, conflict declarations, private reviewer notes, draft history, and most qualification details. Exact release traceability remains in [release evidence](sap-c02-0.3b-release-evidence.md).

## Compiler boundary

Compilation is a deterministic projection described in [the compiler contract](sap-c02-0.3b-compiler-contract.md). It verifies exact revisions, digests, dependencies, validations, and approvals; rejects stale or prohibited input; and emits a candidate and evidence. It never grants approval or performs installation, activation, publication, Git mutation, tagging, release, source retrieval, or workspace rewriting.

## Concurrency and recovery

Every draft mutation supplies the expected prior digest and uses atomic file replacement. Revision, approval, evidence, and candidate creation uses create-if-absent semantics. Conflicts fail closed. Git is the history and recovery layer, but a commit itself grants no validation or approval state.

## Implemented module boundary

`adaptive_learning.authoring.workspace` implements the fixed directories, safe project IDs, confined record locations, create-if-absent immutable records, expected-prior-digest draft writes, same-directory temporary files, `os.replace` atomic replacement, and a fail-closed per-workspace mutation lock. `adaptive_learning.authoring.canonical` and `adaptive_learning.authoring.schemas` implement the accepted canonical bytes, portable paths, record digests, and closed schemas. No new dependency is required.

Initialization creates only `project.json` and the fixed empty directories. New projects use project schema v2 and accept an explicit timestamp, author, clean initialization commit, intended claim range, and generic design references; project schema v1 remains readable. Initialization performs no retrieval and creates no source, claim, lesson, question, approval, validation, candidate, pack, learner state, or runtime configuration.
