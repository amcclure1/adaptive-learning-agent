# SAP-C02 0.3B Approval Model

Status: final design proposal; no approval storage implemented
Design date: 2026-07-18

## Governing rule

Approval is an explicit human decision over exact artifact bytes and dependencies. Successful generation, model critique, deterministic validation, compilation, Git commit, or source authority does not imply approval. The drafting model must not approve its own source classifications, claims, lessons, questions, uniqueness determinations, packs, or activation.

## Minimum approval record

Each approval record is immutable and file-backed, with:

- stable approval ID and approval type;
- artifact kind, ID, version, and SHA-256/canonical digest;
- decision: `approved`, `changes_requested`, or `rejected`;
- human reviewer identity and role;
- qualification/conflict attestation;
- reviewed scope and explicit exclusions;
- prerequisite approval IDs and validator-report IDs;
- UTC decision time;
- findings, conditions, unresolved concerns, and notes visibility (`public`, `release_evidence`, or `private_local`);
- invalidation state, trigger, time, and superseding approval ID when applicable.

An approval status stored on an artifact is a derived convenience and must resolve to the immutable decision record.

## Five separate approval layers

| Layer | Exact review target | Human judgment | Prerequisites | Does not approve |
|---|---|---|---|---|
| Source approval | Source record, retrieved identity/revision/digest, intended use, authority, rights, freshness policy | Provenance, authority, relevant scope, allowed use, rights classification, acceptable freshness | Structural source validation | Any factual claim or copied expression |
| Claim approval | Atomic claim, citations/locators, applicability, sensitivities, derivation premises, freshness horizon | Truth, source fit, completeness of conditions, derived reasoning, current applicability | All cited sources approved and current; claim validation passed | Lesson/question prose or uniqueness |
| Question content approval | Exact stem, ordered options, key, explanation, distractor rationales, claims, blueprint/objective mapping, originality record | Factual correctness, objective alignment, originality, clarity, realism, difficulty, distractor quality, no prohibited expression | Claims current/approved; question structural checks passed; originality review complete | Answer uniqueness or pack release |
| Answer-uniqueness approval | Exact question plus requirement-option matrix and content approval | All requirements stated, key satisfies all, distractors fail explicitly, no hidden assumption, prioritizer selects one answer/set, current claims | Current question-content approval; freshness recheck; uniqueness diagnostics passed | Other questions or pack release |
| Pack-release approval | Exact compiled pack digest plus release-evidence manifest and all content/dependency approvals | Scope completeness, editorial quality, rights/notices, compilation fidelity, non-claims, activation decision | All selected sources/claims/lessons/questions/content/uniqueness approvals current; pack validation passed | Later content/version or external publication beyond scope |

Lesson/content approval may be recorded as a content-review record analogous to question content approval. It is a prerequisite of pack release but does not replace any of the five listed layers.

## Author and reviewer separation

Every artifact records its drafting identity. The approving identity must be distinguishable. For 0.3B, a single qualified human may approve source, claim, question-content, uniqueness, and pack-release layers if:

1. the model or another recorded identity drafted the artifacts;
2. each reviewer role is recorded separately;
3. the reviewer attests the relevant qualifications and conflicts;
4. each decision is separately expressed over exact artifacts;
5. no earlier approval is inferred from a later one.

Independent human reviewers are preferred for originality/uniqueness and pack release, but a second human is not an absolute pilot requirement. If a human authors or materially rewrites a question, that person cannot provide its uniqueness approval; another qualified human is required.

## Answer-uniqueness checklist

The uniqueness reviewer must explicitly confirm, for each question:

- every material requirement and scenario assumption is stated;
- the keyed answer or answer set satisfies every material requirement;
- each distractor fails for a documented reason supported by current claims where factual;
- no unstated assumption is needed to make the key win;
- the explicit prioritizing criterion makes one answer or exact response set uniquely best;
- response type, selection count, and keyed-answer cardinality agree;
- time-, Region-, and configuration-sensitive claims remain current and applicable;
- the item is independently expressed and not overly similar to reviewed official samples or unauthorized material;
- learner-facing explanation does not repair ambiguity absent from the stem.

Any `no`, `uncertain`, or unresolved conflict results in `changes_requested` or `rejected`, never conditional activation.

## Invalidation matrix

| Change | Source | Claim | Question content | Uniqueness | Pack release |
|---|---:|---:|---:|---:|---:|
| Source URL/title metadata correction with no identity/use effect | impact review | impact review | impact review | impact review | invalidated because compiled bytes changed |
| Source content/revision/rights/authority change | invalidated | invalidated if dependent | invalidated if dependent | invalidated if dependent | invalidated |
| Claim statement/category/citation/locator/applicability change | — | invalidated | invalidated if linked | invalidated if linked | invalidated |
| Claim freshness expires | — | blocked/stale | blocked if linked | blocked if linked | blocked/invalidated before activation |
| Design specification material requirement or blueprint mapping changes | — | — | invalidated for realized question | invalidated | invalidated |
| Stem, requirement, option text/order, key, selection count, or rationale changes | — | — | invalidated | invalidated | invalidated |
| Learner explanation/citation editorial change | — | impact review | invalidated | impact review; invalidate if reasoning changes | invalidated |
| Reviewer/private note only, excluded from compiled/review target | — | — | no automatic invalidation | no automatic invalidation | no automatic invalidation; audit entry required |
| Compiler/version/projection rule changes | — | — | impact review | impact review | invalidated; recompile/reapprove |

All digest-covered release changes invalidate pack-release approval. Impact review may conclude that an upstream approval remains valid only when the reviewed artifact bytes and material meaning did not change; that conclusion is itself recorded.

## Freshness behavior

Freshness is evaluated at claim approval, question-content review, uniqueness review, and pack-release review. Expiry does not erase a prior approval. It marks the claim `stale`, blocks dependent content, and produces an impact report. Revalidation records the retrieved source identity/date and creates a new claim approval or explicit reaffirmation over the unchanged claim digest.

## Activation boundary

Compilation produces a candidate. Pack validation proves structure. Pack-release approval authorizes the exact candidate for activation. Activation/install is a separate deterministic action and must reject missing, stale, invalidated, mismatched, or self-approved dependencies. No activation operation is implemented by this design.
