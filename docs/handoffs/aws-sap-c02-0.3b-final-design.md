# AWS SAP-C02 0.3B Final Design Handoff

Status: final design complete; Proposed ADR acceptance and separate implementation/content authorization required
Design date: 2026-07-18
Pilot: `aws-sap-c02-org-04-pilot`

## Outcome

0.3A is accepted and closed. The exact proposed 0.3B implementation boundary is designed without creating sources, claims, lessons, learner-ready questions, packs, tools, schemas, SQLite migrations, Hermes changes, MCP configuration, AWS access/resources, releases, or tags.

## Accepted 0.3A baseline

The repository user explicitly accepted:

1. AWS Certified Solutions Architect - Professional, `SAP-C02`, as the current target.
2. The official-source/exam identity baseline as of 2026-07-18.
3. Assessment blueprint `0.3A.1` with overall medium confidence.
4. Fail-closed analysis-only use of official exam-guide/sample-question expression unless separate rights are established.
5. Original assessment grammar without protected/recalled expression.
6. The complete 22-objective high-level learning architecture.
7. Progressive realization as the governing model.
8. Domain 1 task 1.4 / `SAP-ORG-04` as the pilot.
9. Public AWS documentation and ordinary public retrieval for the pilot.
10. Deferral of MCP configuration and AWS-account access.

The controlling record is [the 0.3A acceptance handoff](aws-sap-c02-0.3a-acceptance.md).

## Fixed pilot boundary

- Domain 1 task 1.4 only: design a multi-account AWS environment.
- Primary objective `SAP-ORG-04`, with bounded `SAP-FND-01`, `SAP-FND-02`, and `SAP-ORG-02` bridges.
- Two original cited lessons.
- Approximately 24–30 approved atomic claims.
- Exactly five original scenario questions: three single-response and two select-two multiple-response.
- No diagram by default. Existing static-PNG support is available only after a separate material-need and source/rights/accessibility/non-leakage review.
- No AWS account, lab, private documentation, authenticated Skill Builder material, MCP installation, or complete Domain 1/SAP-C02 claim.

## Proposed authored-content architecture

The canonical authoring system is a separate, Git-versioned, file-backed workspace. It owns source records, atomic claims, two lesson drafts, five design specifications, five question drafts, validation reports, immutable human approvals, and a release-evidence manifest. SQLite remains operational learner-state storage and gains no authoring tables.

The lifecycle is:

```text
source candidate
→ approved source
→ claim draft
→ approved claim
→ question design specification
→ question draft
→ deterministic checks
→ human question and uniqueness review
→ pack approval
→ activation
```

Lifecycle, validation, review, and release state are separate axes. Passing validation never changes human review state. Stale/invalidated dependencies block downstream content while preserving historical decisions.

See [authored-content model](../aws/sap-c02-0.3b-authored-content-model.md) and [authoring workspace](../aws/sap-c02-0.3b-authoring-workspace.md).

## Source and claim boundary

Source records include stable identity, publisher/title/URL, retrieval/revision dates, category, authority, rights/reuse, optional snapshot digest, freshness policy, and review state.

Claims are concise and atomic, with category, precise source locators, applicability, service/architecture scope, Region/account/configuration/time sensitivity, retrieval/review dates, explicit freshness horizon, reviewer, approval, and supersession/invalidation state. Derived architectural recommendations reference their approved factual-premise claims and decision criterion.

## Question and uniqueness boundary

Question design specifications remain separate from learner-ready records. A final question later contains original stem/options/key, selection rule, explanation, one rationale per distractor, requirement-option matrix, claim IDs, blueprint/objective mapping, originality review, question-content approval, and separate answer-uniqueness approval.

The uniqueness reviewer must confirm explicit requirements, full key coverage, documented distractor failure, no hidden assumption, one stated prioritizer yielding one unique answer/set, current sensitive claims, and independent expression. Deterministic diagnostics can expose conflicts but cannot approve uniqueness.

The five specifications are finalized without stems/options/keys in [the accepted pilot specification](../aws/sap-c02-0.3b-pilot-proposal.md). They deliberately cover different judgments: organizational boundaries; workforce/permission assignment versus SCP guardrails; central audit evidence; central security/configuration visibility and delegated administration; and shared-resource ownership.

## Layered approval

Five independent human approvals are required:

1. source approval;
2. claim approval;
3. question-content approval;
4. answer-uniqueness approval;
5. pack-release approval.

Each targets exact artifact bytes/digests and records reviewer role/qualification, decision, scope, findings, dependencies, and time. A single qualified human may fill several roles if recorded separately, but an author cannot approve the same artifact and a human who materially writes a question cannot approve its uniqueness. Changes invalidate approvals according to the impact matrix in [the approval model](../aws/sap-c02-0.3b-approval-model.md).

## Pack-format and compilation decision

The proposed decision is:

- do not extend fixed format 0.3;
- do not introduce format 0.4 for the first manual pilot;
- keep draft/review records in the authoring workspace;
- compile the approved learner-facing projection into existing format 0.2 by default;
- use unchanged format 0.3 only if a separately approved supported PNG is demonstrably necessary.

Installed packs contain the reviewed lessons/questions, response behavior, learner-facing explanations, citations/source summaries, rights/notices, and existing pack approval record. Full claim records, requirement matrices, internal distractor/originality/uniqueness findings, private notes, and most reviewer identities remain authoring-side. A release-evidence manifest outside the pack binds exact approved workspace records to the compiled pack digest.

Concise learner-safe wrong-option teaching should ship post-answer when representable in the existing explanation. If structured per-option learner output or installed claim-chain verification becomes required, propose explicit format 0.4 rather than overloading format 0.2/0.3.

## Tool boundary

The smallest proposed future operations cover source registration/review, claim create/validate/review/impact, question-spec validation/drafting/content review/uniqueness review, and pack compile/validate/release review. They are authoring operations, separate from the ten learner-study operations. They accept workspace-relative IDs/paths and controlled records; they expose no shell, unrestricted filesystem/network access, install, publish, or tag operation.

## Deterministic versus human validation

Structural validators check required fields, allowed vocabularies, IDs/digests, citation/source/claim/approval references, freshness arithmetic, applicability conflicts in controlled fields, complete distractor rationales/matrices, option/key/selection counts, prohibited sources, originality-review presence, compilation eligibility, projection exclusions, and reproducible output.

Humans decide authority/rights, factual truth, claim atomicity/applicability, architecture quality, originality, distractor plausibility/fairness, completeness of requirements, answer uniqueness, editorial quality, and release suitability. See [validation plan](../aws/sap-c02-0.3b-validation-plan.md).

## Human-review plan

Required competencies cover source/rights review, AWS factual accuracy, multi-account architectural judgment, originality, distractor design, uniqueness, and pack release. All checklist entries remain pending because no content exists. See [human-review plan](../aws/sap-c02-0.3b-human-review-plan.md).

## Proposed ADRs

- [ADR 0017: Authored-Content Workspace and Released-Pack Projection](../decisions/0017-authored-content-workspace-release-projection.md)
- [ADR 0018: Claim-Centered Evidence for Authored Content](../decisions/0018-claim-centered-authored-content-evidence.md)
- [ADR 0019: Layered Authored-Content Approval and Invalidation](../decisions/0019-layered-authored-content-approval.md)
- [ADR 0020: Compile Authored Content to Existing Pack Formats for 0.3B](../decisions/0020-compile-authored-content-to-existing-pack-formats.md)

All four are `Proposed`. This handoff records the final design but does not silently accept them or authorize implementation.

## Unresolved decisions before implementation

1. Accept, revise, or reject ADRs 0017–0020.
2. Fix exact JSON schemas, canonicalization, ID/version rules, and expected-prior-digest/atomic-write behavior.
3. Fix the release-evidence manifest and compiler version/input/output contract.
4. Name reviewers and record qualification/conflict/privacy rules.
5. Decide whether concise per-option learner teaching fits the existing explanation field; otherwise propose format 0.4.
6. Define the exact material-need test if a later author requests a static diagram.

These are bounded implementation details. The ownership, approval layers, no-SQLite decision, author/study separation, default format-0.2 compilation path, and pilot counts are fixed as the Proposed design.

## Documents created

- [0.3A acceptance](aws-sap-c02-0.3a-acceptance.md)
- [Authored-content model](../aws/sap-c02-0.3b-authored-content-model.md)
- [Approval model](../aws/sap-c02-0.3b-approval-model.md)
- [Authoring workspace](../aws/sap-c02-0.3b-authoring-workspace.md)
- [Validation plan](../aws/sap-c02-0.3b-validation-plan.md)
- [Human-review plan](../aws/sap-c02-0.3b-human-review-plan.md)
- Proposed ADRs 0017–0020
- This handoff

## Explicitly not performed

- no source/claim/question/lesson authoring;
- no final learner-ready stems, options, keys, rationales, or pack;
- no authoring workspace/compiler/tool/schema implementation;
- no production core, pack parser, Hermes plugin, SQLite, scoring, or learner-state change;
- no MCP setup, AWS credential/account/private source/lab/resource;
- no release or tag.

## Recommended next action

Run a documentation-only ADR review to accept or revise ADRs 0017–0020 and the remaining schema/manifest decisions. Only after that review should a separately authorized manual 0.3B content task create file-backed source and claim records. It must stop before compilation/activation unless that exact later task is also authorized.
