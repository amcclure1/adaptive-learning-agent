# SAP-C02 0.3B Authored-Content Model

Status: accepted contract; generic lifecycle infrastructure implemented; no AWS content records created

This document defines lifecycle semantics. Exact record fields, controlled vocabularies, identity/revision rules, and canonical digests are normative in [the 0.3B schema contract](sap-c02-0.3b-schemas.md). ADRs 0017–0020 are Accepted; acceptance does not authorize content creation or implementation.
Design date: 2026-07-18
Pilot: `aws-sap-c02-org-04-pilot`

## Fixed scope

This model applies only to the accepted Domain 1 task 1.4 / `SAP-ORG-04` pilot: two original lessons, approximately 24–30 source-bound claims, and exactly five original scenario questions (three single-response and two multiple-response). It uses public AWS documentation and normal public retrieval only. It creates no AWS account, lab, private-source dependency, authenticated Skill Builder access, MCP setup, final content, pack, or runtime behavior.

## Lifecycle

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

Generation, retrieval, validation, compilation, and model critique never imply approval. Every transition requiring human authority is represented by a separate review record over exact artifact bytes.

## State model

Avoid one overloaded status field. Each record uses independent axes where applicable:

- **lifecycle:** whether the artifact is current (`candidate`, `draft`, `active`, `stale`, `superseded`, `invalidated`, `rejected`);
- **validation:** `not_run`, `passed`, or `failed`, with a report ID and validator/rule version;
- **review:** `pending`, `in_review`, `changes_requested`, `approved`, `rejected`, or `invalidated`;
- **release:** for compiled candidates only: `not_compiled`, `compiled`, `blocked`, `release_approved`, `activated`, or `superseded`.

An artifact may be structurally valid and still have `review: pending`. A historically approved artifact may later have `lifecycle: stale` and dependent release state `blocked`; approval history is never rewritten.

| Artifact | Initial state | Human-gated state | Terminal/current-loss states |
|---|---|---|---|
| Source | lifecycle `candidate`; review `pending` | review `approved`; lifecycle `active` | `rejected`, `stale`, `superseded`, `invalidated` |
| Claim | lifecycle `draft`; validation `not_run` | review `approved`; lifecycle `active` | `changes_requested`, `rejected`, `stale`, `superseded`, `invalidated` |
| Question design specification | lifecycle `draft`; validation `not_run` | review `approved_for_drafting` recorded as a design decision | `changes_requested`, `superseded`, `invalidated` |
| Question draft | lifecycle `draft`; validation `not_run`; content/uniqueness reviews `pending` | both question-content and uniqueness approvals current | `changes_requested`, `rejected`, `superseded`, `invalidated` |
| Lesson draft | lifecycle `draft`; validation `not_run`; content review `pending` | immutable lesson-content review current | `changes_requested`, `superseded`, `invalidated` |
| Release candidate | release `not_compiled` or `compiled` | pack-release approval over exact compiled digest | `blocked`, `superseded`; `activated` only after approval |

`approved_for_drafting` does not approve a future question. It only permits the design specification to be realized as a new draft.

## Minimum source record

Sources remain file-backed. The minimum structured record is:

| Field | Requirement |
|---|---|
| `source_id` | Stable workspace ID; never silently reused |
| `title` | Exact source title at retrieval |
| `publisher` | Provider/issuing organization |
| `url` | Canonical public URL; HTTPS unless an explicit exception is reviewed |
| `retrieved_at` | Exact date/time or date with declared precision |
| `published_or_updated_at` | Date and precision when available; explicit `null` plus note when absent |
| `source_category` | Exam guide, user guide, service FAQ, architecture guidance, announcement, rights policy, or another controlled value |
| `authority_tier` | Tier 1 official, Tier 2 licensed/open, Tier 3 descriptive, or excluded |
| `rights_reuse` | Reusable verbatim, reusable with attribution, analysis-only, style-evidence-only, prohibited/unsafe, unresolved, or reference-only |
| `snapshot_sha256` | Optional; required when a retained snapshot was used; absence is explicit |
| `freshness_policy` | Trigger/horizon and what must be rechecked |
| `review_status` | Separate approval state and approval-record ID |

Recommended additional fields are intended use, precise source-version/revision identity, snapshot-retention location/status, conflict notes, and superseded source ID. A source with prohibited/unsafe classification cannot become an approved factual source.

## Minimum claim record

Each claim is concise and atomic enough that a reviewer can approve, invalidate, or supersede it without approving unrelated assertions.

| Field | Requirement |
|---|---|
| `claim_id` | Stable pilot-scoped ID |
| `statement` | Concise atomic statement; conditions included or linked explicitly |
| `category` | One or more controlled categories below; one primary category |
| `citations` | Approved source IDs plus precise locators and the exact proposition supported |
| `applicability` | Required conditions, exclusions, and decision context |
| `scope` | Service(s), architecture pattern, organization/account boundary, and objective IDs |
| `region_sensitivity` | `none`, `possible`, or `explicit`, with Regions/partitions when material |
| `account_configuration_sensitivity` | Required organization mode, delegated administrator, permissions, enabled feature, quota, or other state |
| `time_sensitivity` | `stable`, `review_on_change`, or explicit short horizon |
| `retrieved_at` / `reviewed_at` | Evidence retrieval and human review dates |
| `freshness_horizon` | Exact date or rule; never an implied default for release |
| `reviewer` | Human reviewer identity/role reference |
| `review_status` | Pending/approved/etc. plus immutable approval ID |
| `supersession` | Prior/new claim IDs and reason, or explicit null |
| `invalidation` | State, trigger, affected dependency report, and resolution |

Claim categories:

1. authoritative documented fact;
2. service limitation;
3. derived architectural recommendation;
4. scenario assumption;
5. cost or operational tradeoff;
6. time-sensitive fact;
7. Region-sensitive fact;
8. account/configuration-dependent fact.

A claim may have sensitivity tags in addition to its primary category. A derived architectural recommendation must reference its supporting approved factual claim IDs, state the prioritizing criterion, and explain why the recommendation applies. It cannot cite only general guidance.

Scenario assumptions live with a question design/draft unless deliberately reusable. They must be explicit to the learner and cannot silently override real AWS behavior.

## Question design specification

A design specification is authoring-only and contains no final stem, final options, key, or learner-ready explanation. Minimum fields:

- stable specification ID and version;
- target objective and supporting prerequisites;
- intended cognitive operation;
- assessment-blueprint ID/version/features;
- response format and explicit selection count;
- scenario theme;
- material requirements and constraints;
- compared services or patterns;
- expected keyed-answer characteristics, not final key text;
- planned distractor categories;
- evidence/claim requirements;
- intended difficulty;
- ambiguity, similarity, freshness, and review risks.

Specification finalization permits drafting only and is not an authority-bearing content approval. A material design change after a question exists triggers impact review for that question.

## Final question record

The future learner-ready question record must support:

| Field | Requirement |
|---|---|
| `question_id`, version, digest | Stable identity and immutable review target |
| `design_spec_id` | Exact source specification/version |
| `objective_ids` | One primary objective plus explicit supporting objectives |
| `stem` | Original learner-ready scenario and command |
| `options` | Stable labels and ordered original option text |
| `keyed_answer` | Exact label or set; never exposed before submission |
| `selection_rule` | Single response or explicit `select_n` matching the key count |
| `explanation` | Learner-facing post-answer explanation |
| `option_rationales` | One internal record per option, including keyed options, with category, requirement links, claims, and factual rationale |
| `requirement_matrix` | Every material requirement mapped to the key and every option's satisfy/fail/not-applicable result |
| `claim_ids` | Only current approved claims; scenario assumptions distinguished |
| `blueprint_refs` | Blueprint ID/version and matched features |
| `originality_review` | Immutable human review ID, method, decision, and concerns |
| `content_approval` | Human question-content approval ID |
| `uniqueness_approval` | Separate human answer-uniqueness approval ID |
| `review_status` | Derived release eligibility; never self-declared by the draft |

The workspace record may contain full rationales and review evidence. The compiled pack projection contains only the learner-facing subset supported by the chosen existing format; the external release-evidence manifest preserves the full chain.

## Answer-uniqueness evidence

Every question draft must have a requirement-option matrix showing:

1. all material requirements and assumptions appear in the stem;
2. every keyed option satisfies every material requirement;
3. every distractor fails for a documented scenario-specific reason;
4. no unstated assumption is needed;
5. the prioritizer makes one answer or exact answer set uniquely best;
6. selection count and key count agree;
7. all material claims remain approved/current;
8. independent-expression/originality review has no unresolved concern.

Deterministic tooling may find empty cells, multiple all-satisfying options, mismatched counts, stale claim references, and unsupported assertions. Only a qualified human can decide whether the requirements are complete and the architecture is uniquely best.

## Change and invalidation behavior

Records are append/supersede rather than silently overwritten after approval. An editable draft may change only with expected-prior-digest checking; the edit invalidates approvals targeting its former digest. Immutable revisions receive a new revision number and `supersedes` reference. Changes compute an impact set using IDs and digests. Historical decisions remain readable but become ineligible when prerequisites are stale or invalid. See [the approval model](sap-c02-0.3b-approval-model.md) for the exact layer consequences.
