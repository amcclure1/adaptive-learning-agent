# AWS SAP-C02 0.3B Final Design Handoff

Status: design and implementation contract accepted; content and implementation require separate authorization
Design date: 2026-07-18

## Outcome

The documentation-only 0.3B design gate is complete. ADRs 0017–0020 are Accepted, and the workspace, record schemas, canonical digests, approval/invalidation behavior, validation reports, deterministic compiler, release evidence, format projection, reviewer rules, and diagram gate are sufficiently fixed for later implementation.

No AWS source record, claim, lesson, question, option, key, rationale, pack, authoring tool, production-core change, SQLite change, Hermes/MCP change, credential/account/resource action, release, or tag was created.

## Accepted baseline and pilot boundary

The accepted 0.3A baseline remains authoritative. The pilot is Domain 1 task 1.4 / `SAP-ORG-04`, design a multi-account AWS environment, with:

- exactly two future original lessons;
- approximately 24–30 future approved atomic claims;
- exactly five future original scenario questions: three single-response and two select-two multiple-response;
- public authoritative AWS evidence and explicit reuse classifications;
- text-only delivery by default;
- no official, recalled, dumped, or copied exam-question expression.

The five accepted question specifications remain design records only. They contain no learner-ready stems, options, keys, or explanations and grant no content or uniqueness approval.

## Authoring ownership

The canonical workspace is `authoring/aws-sap-c02-org-04/`, with explicit directories for sources, claims, lessons, question specifications, questions, validations, approvals, and release artifacts. Drafts are editable with expected-prior-digest checks. Frozen revisions, approvals, candidates, and evidence are append-only. SQLite remains learner-state only.

Credentials, browser state, temporary downloads, licensed source copies, copied question text, and non-public private notes are prohibited from the Git workspace. See [the workspace contract](../aws/sap-c02-0.3b-authoring-workspace.md).

## Record and digest contract

Stable artifact IDs are independent of filenames. Records bind artifact type, schema version, revision, status, UTC timestamps, author/provenance where appropriate, supersession, and canonical digest. Cross-references bind ID, type, revision, and digest.

Canonical JSON uses UTF-8 without BOM, NFC normalization, LF, sorted object keys, preserved semantic array order, no insignificant whitespace, portable POSIX paths, canonical UTC timestamps, and artifact-type domain separation. Lesson digests bind normalized Markdown and its lesson record. Exact closed schemas and illustrative placeholders are in [the schema contract](../aws/sap-c02-0.3b-schemas.md).

## Evidence and approval

Claims are atomic, precisely located, applicability-bounded, sensitivity/freshness classified, and source-bound. Derived recommendations cite approved premise claims and an explicit decision criterion. Lessons may introduce no material assertion outside approved claims.

Five independent human approval authorities exist: source, claim, question content, answer uniqueness, and pack release. Lesson-content and originality decisions are immutable review records and release prerequisites. Passing validation grants none of these.

Every decision targets exact bytes and dependencies. Historical decisions remain immutable; revocation and supersession are new records. Artifact authors cannot approve their artifact, and a person who materially authors or rewrites a question cannot approve answer uniqueness. See [the approval model](../aws/sap-c02-0.3b-approval-model.md).

## Question and learner-teaching boundary

A future final-question record contains original stem, ordered stable option IDs/text, keyed option IDs, question type, explicit selection count, learner explanation, one internal rationale per option, requirement-option matrix, claim/objective/blueprint references, citation projection, review states, and exact digest.

For multiple response, keyed count equals required selection count, all keyed selections are required, and existing exact-set/no-partial-credit scoring remains unchanged.

The existing learner explanation may include concise learner-safe prose about why major alternatives fail. Internal rationales do not ship. If adequate teaching needs structured per-option output, work stops and proposes explicit format 0.4; no existing field may be overloaded.

## Validation and invalidation

Deterministic validation checks closed schemas, identities/digests/references, source and claim eligibility, freshness arithmetic, required mappings/rationales, response counts, prohibited sources, reviewer conflicts, approval currency, projection exclusions, and reproducibility. It does not decide factual truth, authority, quality, originality, or uniqueness.

Generated reports record validator version, execution timestamp, workspace commit, checked artifact digests, structured findings/severity/blocking status, and output digest, with no human-approval implication. Release evidence binds the exact report used.

The exact invalidation matrix is fail-closed: material source/rights changes invalidate source authority; claim statement/locator/applicability/freshness changes invalidate claim approval; lesson mapping/prose changes invalidate lesson review; question stem/options/key/explanation/rationale changes invalidate content review; requirement/prioritizer/key/option/rationale changes invalidate uniqueness; and every compiled learner-facing byte or dependency change invalidates pack release.

## Compiler and release evidence

The compiler accepts one explicit project and closed selection. It rejects stale, invalidated, unapproved, prohibited, mismatched, or unsupported inputs; projects only approved learner-facing fields; emits byte-identical output for identical canonical inputs; and never installs, activates, publishes, commits, tags, or releases.

Format 0.2 is the default. Existing format 0.3 is allowed only when an independently reviewed static PNG passes the complete material-need, authority/rights, accessibility, non-leakage, and representation gate. No format 0.4 is created for this pilot.

A candidate manifest binds all inputs, approvals, validations, compiler version, source commit, and candidate pack. A later pack-release approval targets that exact candidate/evidence. A separate deterministic final manifest binds the unchanged candidate and approval, avoiding a digest cycle. Evidence remains outside the installed pack. See [the compiler](../aws/sap-c02-0.3b-compiler-contract.md) and [release-evidence](../aws/sap-c02-0.3b-release-evidence.md) contracts.

## Authoring operation boundary

Accepted future operation names cover project initialization, source registration/validation/review, claim draft/validation/review, impact analysis, lesson and question-spec validation, question drafting/validation/content/uniqueness review, full-workspace validation, candidate compilation, pack review, and evidence finalization.

They use closed requests and workspace-relative IDs/paths, expose no shell or unrestricted filesystem/network, and perform no install, publication, Git tag, or release. They are separate from the ten learner-study operations and are not registered in the learner Hermes plugin by default.

## Accepted ADRs

- [ADR 0017: Authored-Content Workspace and Released-Pack Projection](../decisions/0017-authored-content-workspace-release-projection.md)
- [ADR 0018: Claim-Centered Evidence for Authored Content](../decisions/0018-claim-centered-authored-content-evidence.md)
- [ADR 0019: Layered Authored-Content Approval and Invalidation](../decisions/0019-layered-authored-content-approval.md)
- [ADR 0020: Compile Authored Content to Existing Pack Formats for 0.3B](../decisions/0020-compile-authored-content-to-existing-pack-formats.md)

## Implementation details still open

The accepted contracts intentionally leave only implementation choices: Python module/CLI layout, schema-validation technique, atomic-write/locking mechanics, compiler build-identity plumbing, reviewer assignment, authorized retrieval workflow, and separately authorized candidate/release versioning. None permits weakening the accepted boundary.

## Completion and next gate

[The design-acceptance record](aws-sap-c02-0.3b-design-acceptance.md) closes this documentation gate. A later explicit task may implement contract machinery without content, and a separate explicit task may author/review pilot content. Compilation, install, activation, and release remain independent authorization gates.
