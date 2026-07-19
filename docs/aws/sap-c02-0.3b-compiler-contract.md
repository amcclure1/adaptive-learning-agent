# SAP-C02 0.3B Deterministic Compiler Contract

Status: Accepted contract; generic format-0.2 candidate compiler and bounded operations implemented

Compiler contract: `ala-authoring-compiler-v1`

Pilot: `aws-sap-c02-org-04-pilot`

## Authority boundary

The compiler is a deterministic release-projection tool, not an author, reviewer, installer, or publisher. It accepts one explicitly identified workspace project, verifies exact revisions/digests and current human decisions, produces a candidate learner pack and release evidence, and stops.

It never:

- retrieve a URL or use unrestricted network access;
- invoke a model or infer missing content;
- change a draft, approval, validation, or source record;
- grant or infer human approval;
- install or activate a pack;
- commit, push, tag, release, publish, or modify Git configuration;
- read credentials, browser state, private notes, AWS data, or files outside the allowed workspace and explicit output root.

## Versioning

`compiler_version` is a semantic implementation version plus immutable build identity. Any change to canonicalization, validation eligibility, field projection, ordering, pack serialization, exclusion rules, or evidence shape increments the compiler version. A compiler-version change triggers impact analysis and a new pack-release approval even when content inputs are unchanged.

The compiler declares the exact authoring contract versions and target pack formats it supports. Unknown schema or target-format versions fail closed.

## Compile request

The implemented compiler accepts one closed selection and a confined operation request equivalent to:

```json
{
  "operation": "authoring.release.compile_candidate",
  "project_id": "aws-sap-c02-org-04-pilot",
  "workspace_root": "authoring/aws-sap-c02-org-04",
  "workspace_commit": "<40-character Git commit>",
  "project_revision": 1,
  "project_digest": "<canonical project digest>",
  "selection_manifest": "release/selections/<selection-id>.json",
  "target_pack_format": "0.2",
  "candidate_output": "release/candidates/<pack-version>",
  "compilation_timestamp": "2030-01-01T00:00:00Z",
  "expected_absent_or_digest": null
}
```

Every path is workspace-relative POSIX form and resolves inside the allowed workspace or configured release-output root. The operation does not accept arbitrary absolute paths, shell strings, globbing, or open-ended URLs. `compilation_timestamp` is an explicit canonical input; the compiler never reads the wall clock for digest-covered output.

The selection manifest binds exact project, blueprint, architecture, realization, source, claim, lesson, question-specification, final-question, review, approval, and validation-report references. It contains no implicit “latest” selector.

## Required compile inputs

The compiler requires:

1. one exact `project.json` revision;
2. accepted assessment blueprint identity/version/digest;
3. accepted learning architecture identity/version/digest;
4. accepted realization-plan identity/version/digest;
5. every selected source revision and current source approval;
6. every selected claim revision and current claim approval;
7. exactly two lesson revisions with current immutable lesson-content reviews;
8. exactly five question specifications and five final questions;
9. exactly three single-response and two multiple-response questions;
10. current originality review, question-content approval, and answer-uniqueness approval for each final question;
11. current deterministic validation reports over the selected exact digests;
12. current rights, freshness, scope, and non-claim decisions;
13. target format `0.2`, unless the format-0.3 material-need gate below passes.

All dependency graphs must resolve, be acyclic, and use exact revision/digest references. A record's convenience review state never substitutes for its immutable decision record.

## Eligibility checks

Compilation rejects:

- unknown, missing, duplicate, draft-only, stale, superseded, invalidated, rejected, or revoked selected artifacts;
- a digest, revision, workspace commit, schema, validator, or approval mismatch;
- expired freshness or unresolved warning disposition;
- prohibited, excluded, unresolved-rights, recalled, leaked, commercial-bank, or suspicious source dependencies;
- author/approver or question-author/uniqueness-reviewer conflicts;
- unsupported claim assertions or derived recommendations without approved premises;
- incomplete requirement matrices, rationales, citation projections, or review graphs;
- a question-count, lesson-count, response-mix, key-count, or selection-count mismatch;
- an unapproved diagram or any target other than exact format 0.2/0.3;
- any file or field not on the learner-facing projection allowlist;
- any private note, internal finding, credential, source copy, temporary download, browser state, runtime configuration, or learner data in selected inputs/output inventory.

Passing these checks proves compilation eligibility only. It grants no human approval.

## Deterministic output

For identical compiler version, canonical request, exact input bytes, and explicit compilation timestamp, the compiler emits byte-identical:

- candidate pack directory bytes and inventory;
- target-format pack digest;
- compiler diagnostics;
- candidate release-evidence manifest.

Filesystem enumeration order, current time, absolute path, locale, machine name, operating system, environment variables, network state, and Git working-tree metadata do not participate. Arrays use explicit schema order; files use manifest order. Output files are written to a new temporary directory under the approved output root, revalidated, and atomically renamed. Existing output fails unless `expected_absent_or_digest` exactly authorizes replacement of an unapproved generated candidate. An approved or release-bound candidate is immutable.

## Compilation phases

### 1. Resolve

Load the exact project and selection manifest at the declared source commit. Resolve each reference by ID/type/revision/digest and reject uncommitted or out-of-workspace inputs.

### 2. Validate eligibility

Run or verify the accepted deterministic rule set, decision graph, freshness, counts, conflicts, and target-format gate. The compiler may consume a selected prior report only when its validator/rule version, source commit, checked digests, and output digest match.

### 3. Project learner-facing content

Use a strict allowlist. Internal records are never copied wholesale.

### 4. Serialize and validate candidate

Create exact format-0.2 or unchanged format-0.3 bytes, calculate the existing target-format digest, and run the existing public pack validator in candidate-review mode appropriate to the pending pack-approval record. Compilation does not modify pack parsers or formats.

### 5. Emit candidate evidence

Emit an immutable candidate evidence manifest with `phase: "candidate"`, the exact compiler inputs, diagnostics/report digests, candidate pack inventory/digest, and a null release-review approval. This is the target of pack-release review together with the release-candidate artifact digest.

### 6. Human pack-release review

Outside the compiler, a qualified human reviews the exact candidate, candidate evidence digest, prior approvals, rights/notices, scope, validation, and non-claims. The immutable pack-release approval targets the exact `release_candidate` artifact digest and candidate-evidence digest. It cannot target “latest.”

### 7. Finalize approved projection

A separate deterministic `authoring.release.finalize_evidence` operation verifies the pack-release approval and creates:

- the final existing-format pack approval projection;
- the final target-format pack digest;
- a new immutable release-evidence manifest with `phase: "final"` binding the candidate manifest, pack-release approval, and final pack digest.

This phase does not edit the candidate evidence or approval. It does not install, activate, publish, commit, tag, or release. Any learner-facing input change requires a new candidate and approval.

The current generic implementation completes the external-evidence portion of this phase and deliberately leaves the pending candidate bytes unchanged. Creating a separate installable format-0.2 projection containing the human pack approval remains a later explicitly authorized release-projection task; final evidence alone is not an installable pack and performs no release action.

## Format-0.2 projection

Format 0.2 is the default and fixed path for the text-only pilot:

| Authoring artifact | Existing format-0.2 projection |
|---|---|
| Project/realization identity | Pack ID/version/title/tags and bounded scope wording |
| Approved objectives | Existing ordered objective records |
| Approved lesson records + Markdown | Exactly two lesson records and exact normalized Markdown files |
| Approved final-question stem/options/key | Existing generated-question fields with ordered options and key |
| Question type/selection count | Existing `single_response` or `multiple_response` semantics; explicit select count in learner wording where required |
| Learner explanation | Existing post-answer `explanation`; may include concise learner-safe alternative discussion |
| Learner-safe citations | Existing explanation/lesson citations and source locators |
| Approved source summaries | Existing source records with allowed metadata only |
| Rights decisions | Existing component rights records and `NOTICE.md` |
| Pack-release approval | Existing format-0.2 digest-covered approval record after human release review |

Original authored questions use the existing generated/original origin semantics and must never claim to be official, real, recalled, or copied exam questions.

Authoring-only material omitted from the installed pack includes full claim records, internal locators not needed for learner-safe citations, requirement-option matrices, full option rationales, distractor taxonomies, originality and uniqueness findings, conflict declarations, private reviewer notes, source copies, validator workpapers, and most reviewer qualification details.

## Learner wrong-option teaching

For 0.3B, the existing learner-facing explanation may contain concise prose explaining why major alternatives fail when that prose is approved, learner-safe, supported by approved claims, and clear without structured per-option fields. Internal option rationales are not copied verbatim or exposed as review evidence.

If adequate teaching requires structured per-option output, the implementation must stop and propose explicit format 0.4. It must not overload tags, citations, option text, arbitrary existing fields, or expose internal reviewer rationales.

## Multiple-response behavior

Every multiple-response question states the selection count. `required_selection_count` equals keyed-option count, all keyed selections are required, duplicate selections are rejected, and scoring remains exact set equality with no partial credit. This contract changes no scoring or runtime behavior.

## Material-need gate for format 0.3

Text-only is mandatory by default for `SAP-ORG-04`. Unchanged format 0.3 is eligible only if an immutable material-need review and all existing asset approvals establish:

1. the objective depends on visual interpretation;
2. text-only presentation would materially reduce assessment validity or realism;
3. the diagram is not decorative or merely convenient;
4. an authoritative source and redistribution basis are available;
5. exact identity and fidelity can be reviewed;
6. caption, alt text, fallback, mappings, and cross-question non-leakage can be approved;
7. one local PNG satisfies unchanged format-0.3 limits and security rules;
8. no new media type, remote dependency, transformation pipeline, or runtime-specific requirement is introduced.

Failure of any condition selects format 0.2 or returns the design for revision. It does not justify format 0.4 automatically.

## Implemented authoring operations

The initial Python facade is `adaptive_learning.authoring.operations.AuthoringOperations`. It remains separate from the learner CLI and ten learner-study operations. Its closed methods are:

| Python operation | Boundary |
|---|---|
| `initialize_project` | Create deterministic starter metadata and only the fixed empty workspace directories |
| `validate_project` | Return or persist an authority-free deterministic validation report |
| `add_or_update_draft` | Write a type-directed draft with expected-prior-digest protection |
| `freeze_draft` | Create the next immutable revision and supersedes reference |
| `calculate_artifact_digest` | Calculate a domain-separated JSON/Markdown digest without mutation |
| `create_decision` | Create an immutable approval, review, revocation, or supersession record after target/conflict checks |
| `analyze_impact` | Report affected decision types and historical decision IDs without mutation |
| `store_selection` | Store one closed explicit compiler selection; no implicit latest references |
| `validate_release_candidate` | Recompute and compare candidate pack digest without installation |
| `compile_approved_project` | Produce a pending format-0.2 candidate and candidate evidence |
| `generate_release_evidence` | Bind an explicit pack-release approval into a new final evidence record |

The finer-grained accepted names below remain the design mapping for a later conversational Subject Builder adapter; no adapter or MCP registration is part of this implementation.

| Operation | Mutation | Required input | Output / boundary |
|---|---:|---|---|
| `authoring.project.initialize` | Yes | Project ID, accepted scope references, workspace-relative destination, expected absence | Draft `project.json` and fixed empty directories; no content |
| `authoring.source.register` | Yes | Project ID, closed source metadata, expected absence/prior digest | Draft source record; no network retrieval |
| `authoring.source.validate` | No | Exact source reference and rule version | Generated validation report only |
| `authoring.source.record_review` | Yes | Human confirmation, immutable approval payload, exact target/dependencies | New source approval; never edits source |
| `authoring.claim.create_draft` | Yes | Exact approved source references, placeholder/draft statement fields, expected absence/prior digest | Draft claim record |
| `authoring.claim.validate` | No | Exact claim reference and rule version | Generated validation report |
| `authoring.claim.record_review` | Yes | Human confirmation and exact approval payload | New claim approval |
| `authoring.impact.analyze` | No | Changed artifact reference/digest pair and workspace commit | Generated dependency/invalidation report; no state change |
| `authoring.lesson.validate` | No | Exact lesson JSON/Markdown reference | Generated report over combined lesson digest |
| `authoring.question_spec.validate` | No | Exact specification reference | Generated report; rejects final wording/options/keys |
| `authoring.question.create_draft` | Yes | Exact approved spec/claim refs and closed draft fields | Draft question; no approval |
| `authoring.question.validate` | No | Exact question reference | Generated structural/traceability report |
| `authoring.question.record_content_review` | Yes | Human confirmation, exact question/claim/report digests | New question-content approval |
| `authoring.question.record_uniqueness_review` | Yes | Independent human confirmation, exact question/matrix/content-approval digests | New uniqueness approval |
| `authoring.workspace.validate` | No | Project revision/digest, workspace commit, rule version | Generated full-workspace report |
| `authoring.release.compile_candidate` | Yes | Closed compile request above | New candidate pack and candidate evidence; no approval/install |
| `authoring.release.record_pack_review` | Yes | Human confirmation, candidate/evidence/dependency digests | New pack-release approval |
| `authoring.release.finalize_evidence` | Yes | Candidate, candidate evidence, current pack approval, explicit timestamp | Final pack projection and final evidence; no install/publish |

All mutations use atomic replacement or append-only creation, expected-prior-digest checks, workspace-relative confined paths, and structured errors. Operations expose no shell, unrestricted filesystem, unrestricted network, package installation, AWS access, Git mutation, publication, or release capability. They remain separate from the exact ten learner-study operations and are not registered in the learner Hermes plugin.

## Implemented selection and candidate behavior

The closed `ala.authoring.selection.v1` record binds the exact project and design documents; ordered source, claim, lesson, question-specification, question, approval/review, and validation references; explicit format-0.2 source/lesson/question projection mappings; pack identity/objectives/rights/notice metadata; compiler timestamp; workspace commit field; and the per-option-teaching escalation flag. It accepts no implicit `latest` reference.

The compiler uses the existing format-0.2 implementation's pre-existing internal `skip_approval` review hook. It does not change public parser behavior: public format-0.2 loading still requires `approval.status: approved`. Candidate output instead contains `approval.status: pending`, is structurally reviewed and digested, and is intentionally not installable. Final evidence can bind a later pack-release approval, but no installation, activation, or publication action is exposed.

## Compiler results and errors

Success returns compiler version, project/source commit, target format, selected artifact IDs/digests, candidate output path relative to the workspace, candidate pack digest, evidence ID/digest, diagnostics summary, and `human_approval_granted: false`.

Failures are structured and non-mutating, including `WORKSPACE_CONFLICT`, `SCHEMA_UNSUPPORTED`, `REFERENCE_MISMATCH`, `STALE_DEPENDENCY`, `APPROVAL_MISSING`, `APPROVAL_INVALIDATED`, `REVIEWER_CONFLICT`, `VALIDATION_FAILED`, `PROHIBITED_SOURCE`, `COUNT_MISMATCH`, `TARGET_FORMAT_INELIGIBLE`, `PROJECTION_VIOLATION`, `OUTPUT_CONFLICT`, and `REPRODUCIBILITY_FAILURE`.
