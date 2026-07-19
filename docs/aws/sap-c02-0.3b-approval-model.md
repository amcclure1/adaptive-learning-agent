# SAP-C02 0.3B Approval and Invalidation Model

Status: accepted implementation contract; no approval records created

## Governing rule

Approval is an explicit human decision over an exact artifact revision, canonical digest, and required dependency digests. Generation, retrieval, deterministic validation, compilation, model critique, or Git history never implies approval. Agent memory is non-authoritative.

The record schema is fixed in [the schema contract](sap-c02-0.3b-schemas.md). An original approval record is immutable. Revocation or supersession creates a new record that refers to it; current status is derived from the append-only chain. Changed bytes are never silently retargeted.

## Authority-bearing approvals

| Approval type | Exact target | Human judgment |
| --- | --- | --- |
| `source_approval` | Source revision/digest and intended use | Identity, authority, access, rights/reuse, freshness policy, prohibited-source disposition |
| `claim_approval` | Atomic claim revision/digest and exact source dependencies | Truth, locator fit, applicability, sensitivities, freshness, derived reasoning |
| `question_content_approval` | Stem, ordered options, key, explanation, internal rationales, mappings, claims, and originality result | Accuracy, objective fit, clarity, originality, realism, difficulty, distractor quality |
| `answer_uniqueness_approval` | Exact question plus requirement-option matrix and content approval | Every stated requirement is tested, all keyed answers are necessary, distractors fail explicitly, no hidden assumption changes the answer |
| `pack_release_approval` | Exact candidate pack and candidate evidence manifest | Completeness, compilation fidelity, earlier approvals, rights/notices, validation, exclusions, release suitability |

Lesson content and question-originality review use immutable review records with the same exact-target and conflict discipline. They are pack-release prerequisites but do not create additional authority-bearing approval types.

## Required approval fields

Every authority-bearing decision contains:

- approval ID and approval type;
- target artifact ID, type, revision, and canonical digest;
- exact dependency digests;
- decision;
- reviewer stable identity and public display name where appropriate;
- reviewer role and concise qualification summary;
- conflict-of-interest declaration;
- scope, findings, and conditions;
- UTC timestamp;
- record kind and the superseded/revoked record ID when applicable.

Allowed decisions are `approved`, `changes_requested`, `rejected`, and, only for an explicit revocation record, `revoked`. Conditions cannot defer a blocking issue while recording `approved`.

## Reviewer independence and competency

Required competencies are source and rights, AWS factual accuracy, multi-account architecture, question originality, distractor quality, answer uniqueness, and final release suitability. One qualified person may fill multiple roles when each decision is recorded separately, subject to both hard conflicts:

- an artifact author cannot approve that artifact;
- a person who materially authors or rewrites a question cannot approve its answer uniqueness.

Final release review confirms every required earlier approval and review. Public records need only a stable reviewer identity, role, qualification summary, and conflict declaration; contact details and sensitive personnel information are prohibited.

## Exact invalidation matrix

Historical records remain preserved. `Invalidates` means the former approval is ineligible for future compilation; the replacement artifact requires a new review. When materiality is listed, an immutable impact-review record must justify a no-invalidation result while the approved target bytes remain unchanged.

| Change | Source | Claim | Lesson/content | Question content | Answer uniqueness | Pack release |
| --- | --- | --- | --- | --- | --- | --- |
| Source identity, publisher, canonical URL, category, authority, rights, use, prohibited disposition, or materially relevant publication/retrieval data | Invalidates when material | Invalidates dependent claims if evidence identity/applicability/freshness changes | Invalidates through dependencies | Invalidates through dependencies | Invalidates through dependencies | Invalidates if any selected dependency or learner-facing byte changes |
| Source note or access-limit text only, outside reviewed meaning and release projection | Impact review | Impact review | — | — | — | Invalidates only if a bound dependency digest changes |
| Claim statement, locator, applicability, scope, Region/account/configuration/time sensitivity, freshness horizon, premises, or decision criterion | — | Invalidates | Invalidates mapped lesson review | Invalidates supporting questions | Invalidates supporting questions | Invalidates |
| Lesson claim mapping, record field affecting projection, or Markdown prose | — | — | Invalidates | — | — | Invalidates |
| Question stem, option ID/text/order, key, question type, selection count, explanation, internal rationale, claim/objective mapping, or citation projection | — | — | — | Invalidates | Invalidates | Invalidates |
| Requirement, prioritizer, material constraint, requirement-option matrix, key, option, or rationale | — | — | — | Invalidates when question target changes | Invalidates | Invalidates |
| Originality finding or content-review dependency | — | — | — | Invalidates | Invalidates by dependency | Invalidates |
| Reviewer private/contact note excluded from target and all bound dependencies | — | — | — | — | — | No automatic invalidation; audit record required |
| Validator version/report or deterministic blocking result | — | May block eligibility | May block eligibility | May block eligibility | May block eligibility | Invalidates if bound report digest changes or a required report fails |
| Compiler version, projection rule, selected artifact, approval dependency, compiled learner-facing byte, candidate digest, or release-evidence dependency | — | — | — | — | — | Invalidates |

Freshness expiry does not rewrite a claim approval. It marks the approved revision stale, blocks dependents, and requires a new claim revision/approval or an explicitly modeled reaffirmation over unchanged bytes and refreshed dependency evidence.

## Release boundary

Compilation produces an unapproved candidate. Pack-release approval targets that candidate and its candidate evidence. The final evidence manifest then binds the immutable release approval without altering the candidate. Installation or release is a separate, unimplemented and separately authorized operation.
