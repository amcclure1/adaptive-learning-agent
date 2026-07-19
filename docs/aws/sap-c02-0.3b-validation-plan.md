# SAP-C02 0.3B Deterministic Validation Plan

Status: accepted contract; generic deterministic validator implemented; AWS content review remains pending
Design date: 2026-07-18

## Principle

Deterministic validation proves record shape, reference integrity, rule consistency, freshness arithmetic, compilation eligibility, and some explicit contradictions. It cannot approve source authority/rights, factual truth, architectural quality, originality, distractor plausibility, or answer uniqueness.

Generated reports use `ala.validation-report/1` and the exact fields in [the schema contract](sap-c02-0.3b-schemas.md): validator name/version, execution UTC timestamp, source workspace commit, project revision/digest, checked artifact IDs/revisions/digests, deterministic findings with severity and blocking state, result, and output digest. Every report declares `human_approval_implication: "none"`. Passing reports expire when an input digest or relevant rule changes.

## Severity

- **Error:** blocks review or compilation.
- **Warning:** requires recorded human disposition before release.
- **Information:** trace/audit result with no gate effect.

No warning is silently converted to pass by a model.

## Required checks

| Check | Deterministic behavior | Human judgment still required |
|---|---|---|
| Missing citations | Every material factual claim has at least one approved source/locator; every question fact maps to a claim or explicit scenario assumption | Whether the source actually supports the proposition and is authoritative |
| Unapproved claims | Reject lesson/question/release dependencies whose claim approval is absent, mismatched, invalidated, rejected, or authored/approved by the same prohibited identity | Whether the human reviewer is qualified and the claim is true |
| Stale claims | Compare review/retrieval dates and explicit horizons; block expired or unresolved `stale` claims | Whether revalidation evidence is sufficient or a horizon should change |
| Broken source references | IDs unique/resolvable; URL/date/digest/locator syntax; cited source version matches approval | Whether a locator is substantively precise and relevant |
| Contradictory applicability | Detect explicit conflicts in controlled fields: mutually exclusive Region/partition, organization mode, required/forbidden feature, account role, or time interval | Semantic conflicts expressed only in prose; which interpretation controls |
| Missing distractor rationales | Exactly one rationale record per non-key option; category, failed requirement, claim links, and explanation present | Whether the distractor is plausible, fair, and actually fails |
| Missing requirement-to-answer traceability | Every material requirement has a matrix row; every option has a cell; key rows all marked satisfied; every distractor has at least one explicit fail | Whether all material requirements were identified and matrix judgments are correct |
| Selection-count mismatch | Single response has one key; multiple response has explicit `select_n`, at least five options, at least two keys, and key cardinality equals `n` | Whether the chosen set is uniquely best |
| Unsupported service assertions | Every named real-service behavior in stem/options/rationales maps to approved claims; scenario assumptions cannot masquerade as AWS facts | Truth, completeness, and architectural interpretation |
| Unapproved question/uniqueness | Require separate current content and uniqueness approvals over exact question digest | Quality and uniqueness themselves |
| Compilation from draft content | Compiler allowlist accepts only current approved lesson/question/source/claim versions; reject draft/rejected/stale/invalidated records | Final editorial/release decision |
| Prohibited source categories | Reject excluded/prohibited/unsafe sources and any dependency on them; flag unresolved-rights sources as non-reusable | Borderline provenance/rights decisions |
| Missing originality review | Require a human originality decision over exact question digest with no unresolved concern | Whether expression is independently authored and not overly similar |

## Additional structural checks

### Sources

- required field presence and controlled vocabularies;
- stable ID uniqueness and no silent ID reuse;
- HTTPS URL syntax and approved-domain policy where configured;
- retrieval/revision date precision and valid chronology;
- SHA-256 syntax and retained-snapshot rule;
- authority tier compatible with intended use;
- rights classification compatible with copying/analysis behavior;
- excluded-source indicators never enter content fields.

### Claims

- concise statement is nonempty and not a compound list according to explicit record structure (advisory lint only for prose atomicity);
- citation source approvals resolve and predate claim approval;
- locators present for material factual claims;
- derived recommendations have supporting factual claim IDs, no dependency cycles, and a stated decision criterion/applicability;
- scenario assumptions are explicitly marked and referenced by only their question/design unless intentionally scoped;
- Region/account/configuration/time-sensitive categories have corresponding conditions/horizon;
- supersession links are acyclic and prior IDs exist.

### Question design specifications

- exactly five accepted specification IDs and versions;
- exactly three single-response and two multiple-response specifications;
- multiple-response specs declare `select_two` for this pilot;
- target objective is `SAP-ORG-04`; supporting bridge IDs are allowed and visible;
- each contains every required design field and no final stem/options/key;
- set-level coverage assertions are satisfied: organization structure, permissions/guardrails/workforce identity, audit, security/configuration/delegation, and resource sharing.

### Question drafts

- exactly four options for single response; five or more for multiple response;
- labels unique, order explicit, option text nonempty;
- no answer key or key-revealing citations in pre-answer fields;
- key labels resolve and are not duplicated;
- every option/rationale uses current approved claim IDs;
- each distractor has taxonomy category and explicit failed requirement;
- blueprint/objective/design-spec versions resolve;
- question content, uniqueness, and originality reviews target the exact current digest;
- no prohibited claims such as `official AWS exam question`, `actual`, or `recalled`.

### Approval integrity

- authors and prohibited approving identities are distinct;
- approval ID/type/artifact/digest/decision/time/scope fields complete;
- prerequisite approval graph resolves and is acyclic;
- later invalidation or stale events block dependent approvals;
- no pack approval predates a prerequisite approval or compiled digest;
- approval status on content equals derived current decision state.

### Compilation

- pilot counts are exact: two lessons, five questions, 3/2 response mix;
- only approved artifacts selected;
- target pack format is `0.2` unless an approved format-0.3 asset-need record exists;
- authoring-only fields/files cannot enter the pack inventory;
- compiled source/citation/rights/approval projection satisfies the target format;
- release-evidence manifest contains every input digest and the output pack digest;
- compiling the same inputs/compiler version is reproducible;
- compiler never fetches network content, installs, activates, tags, or publishes.

## Contradiction and uniqueness diagnostics

The validator can report:

- more than one option marked as satisfying every recorded requirement;
- a keyed option marked failing any requirement;
- a distractor with no failed requirement;
- two requirements with contradictory controlled conditions;
- key/selection-count mismatch;
- a rationale that relies on an unlinked claim;
- a prioritizer absent from the stem but used in the rationale.

These findings block. Their absence does not prove uniqueness because the matrix itself and the completeness of requirements are human judgments.

## Originality checks

Deterministic lint may detect copied phrases against project-controlled content or prohibited labels, but the project will not retain unsafe question banks or official sample expression for automated comparison. No numeric similarity threshold can approve originality. The human reviewer uses provenance, the abstract blueprint, and independent-construction history; credible similarity concern causes replacement rather than cosmetic paraphrase.

## Failure output

Each finding should identify artifact ID/version/digest, rule ID/version, severity, field/path, related source/claim/approval IDs, explanation, and a bounded recommended resolution. Validators never rewrite content or change approval state automatically.

Reports in `validations/current/` may be regenerated and replaced with expected-prior-digest checking. [Release evidence](sap-c02-0.3b-release-evidence.md) binds the exact report ID, validator version, source workspace commit, and digest selected for compilation. Replacing a current report never changes historical release evidence.

## Validation order

1. workspace and record syntax;
2. source references and approval state;
3. claim structure, evidence, applicability, freshness, and approval;
4. design-spec completeness and set coverage;
5. question structure, claims, matrices, rationales, originality record, and approvals;
6. lesson-content review records;
7. compilation eligibility and target-format validation;
8. release-evidence integrity;
9. pack-release approval eligibility.

Human review occurs after relevant deterministic checks and may return content for revision even when every check passes.

## Implemented validator

`adaptive_learning.authoring.validation.validate_workspace` enforces closed records and digests, exact references, prohibited/unresolved sources, source/claim authority, claim freshness and derivation premises, lesson claim eligibility and content review, question-specification review, question rationales/matrices/counts, originality/content/uniqueness decisions, reviewer conflicts, declared generic scope counts, and validation-report authority boundaries. Dates, execution time, and workspace commit are explicit inputs; the validator performs no retrieval and never grants approval.

The implementation is deliberately subject-neutral. Pilot-specific factual truth, objective semantics, assessment coverage, AWS architecture judgment, originality, distractor quality, and answer uniqueness remain human review duties. The synthetic tests exercise structural rules without embedding AWS facts or learner-ready pilot content.
