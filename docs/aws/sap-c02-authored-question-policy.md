# SAP-C02 Evidence-Backed Authored Question Policy

Status: accepted 0.3A policy foundation; 0.3B record details remain Proposed design

Applies to: future original AWS questions, beginning with manually reviewed 0.3B

## Claim categories

| Category | Meaning | Minimum evidence | Review/freshness rule |
|---|---|---|---|
| Authoritative documented fact | Directly stated AWS behavior or definition | Current official AWS documentation with precise page/section locator | Human factual review; recheck before question and release approval |
| Source-bound service limitation | Quota, boundary, supported operation, consistency, scope, or prerequisite tied to a service/version | Current user/developer/API/quotas/region documentation; quote no more than rights allow | Treat as time/region-sensitive unless the source proves stability; any changed limit invalidates dependent approvals |
| Derived architectural recommendation | Project conclusion from documented facts and explicit tradeoffs | All factual premises cited; Well-Architected/decision/prescriptive guidance where applicable | Qualified architect reviews applicability and unique-best reasoning; source authority alone is insufficient |
| Scenario assumption | Original fact created for the scenario, such as organization policy or acceptable downtime | Explicit in the stem or design specification; no external citation unless it asserts real behavior | Question reviewer confirms it is visible and internally consistent |
| Cost or operational tradeoff | Relative cost, staffing, complexity, automation, or management burden | Current pricing/guidance for factual premises; explicit scenario scale and time horizon | Recheck before release; avoid exact costs unless essential and current |
| Time-sensitive fact | Availability, deprecation, product name, feature, policy, or current best practice likely to change | Dated official source and retrieval timestamp | Short freshness horizon; mandatory pre-release revalidation |
| Region-sensitive fact | Feature/service availability or cross-Region behavior | Official regional-availability and service documentation for named Regions/partitions | Scenario states Region/partition; recheck before approval/release |
| Account/configuration-dependent fact | Behavior depends on enabled features, organization mode, permissions, quotas, or existing configuration | Official conditional behavior plus explicit scenario state | All prerequisite configuration must be stated; human checks no default is silently assumed |

The current official task outline is the scope authority; service documentation supplies facts. [Current SAP-C02 guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Required evidence chain

```text
learning objective
→ approved factual claims
→ scenario requirements and constraints
→ candidate options
→ keyed-answer rationale
→ distractor rationales
→ citations
→ human review
→ activation
```

### Inspectability at each step

1. **Objective:** stable architecture objective/version, official task mapping, intended cognitive operation, and prerequisite disposition.
2. **Claims:** claim ID/version, exact statement, category, source IDs/locators, applicability conditions, freshness date/horizon, draft/approval status, and derivation premises when applicable.
3. **Scenario:** original scenario ID, explicit assumptions, every material requirement, every prioritizer, prohibited hidden assumptions, and provenance showing independent construction.
4. **Candidate options:** stable labels/order, service/pattern represented, claims relied upon, and requirement coverage/failure matrix.
5. **Key rationale:** why every material requirement is satisfied, why the prioritizer selects it, and which approved claims support each step.
6. **Distractor rationale:** one or more taxonomy categories, exact failed requirement or invalid premise, citations for factual failure, and explanation of plausibility.
7. **Citations:** stable source IDs, URLs, title/publisher, retrieval/revision dates, precise locator, rights/use status, and snapshot digest where applicable.
8. **Human review:** reviewer identity/qualification attestation, reviewed artifact versions/digests, factual/architectural/originality/ambiguity/uniqueness findings, decision, date, and unresolved concerns.
9. **Activation:** separate pack-release decision over exact immutable content; no earlier approval implies activation.

## Answer-uniqueness gate

A future question is not approvable unless:

- every material requirement and scenario assumption is explicit;
- the key satisfies every material requirement;
- each distractor fails for a stored, evidence-backed reason;
- no unstated assumption is needed to make the key win;
- if multiple approaches are technically workable, a stated priority makes exactly one response—or the stated response set—best;
- selection count is explicit for multiple response;
- time-, Region-, price-, quota-, and configuration-sensitive facts have current scope/freshness evidence;
- all material factual premises are sourced;
- a qualified human confirms technical correctness, objective alignment, ambiguity control, and answer uniqueness.

If no uniquely best key exists, revise constraints or replace the design. Do not use prose in the explanation to repair an ambiguous stem.

## AWS distractor taxonomy

| Category | Quality rule |
|---|---|
| Technically invalid | Cite the exact unsupported/nonexistent behavior; avoid trivia-only gotchas |
| Violates one explicit requirement | Name the requirement and preserve other plausible strengths |
| Partial solution | Identify the unaddressed component/failure path |
| Excessive operational burden | State the operational work and why the scenario prioritizes reducing it |
| Unnecessary cost | Establish scale/time horizon and a documented cheaper approach satisfying all requirements |
| Insufficient resilience | Trace the remaining failure domain or unmet RTO/RPO |
| Inappropriate security boundary | Identify the incorrect identity, network, key, account, trust, or data boundary |
| Wrong migration pattern | Show why downtime, compatibility, transfer volume, change tolerance, or sequence conflicts |
| Wrong consistency/replication model | State the required write/read/recovery behavior and mismatch |
| Valid only under unstated assumption | Identify the missing premise; prefer making it explicit or replacing the distractor |
| Deprecated or superseded | Require current official deprecation/supersession evidence and a short freshness horizon |
| Right service, wrong purpose | Explain the service's relevant purpose and why it does not solve the stated problem |
| Symptom rather than cause | Trace why the failure mechanism remains |
| Excessive architecture change | Tie the extra change to “least change,” migration risk, or operational constraints |

Every distractor stores at least one category and a scenario-specific rationale. A category label by itself is not a rationale.

## Assessment-grammar rules

- Use the approved [assessment blueprint](sap-c02-assessment-blueprint.md), including medium-confidence limitations.
- Label all project questions original. Never claim they appeared or will appear on an AWS exam.
- Use four options for single response and five or more for multiple response.
- Keep options parallel and comparable in specificity.
- Avoid answer cues from option length, absolute words, service recency, citations, or atypical detail.
- Cross-domain facts must trace to approved supporting claims and prerequisites.
- Text-only is the 0.3B default; no diagram is required.
- Apply the [rights/similarity boundary](sap-c02-rights-and-reuse.md): copy grammar, not sentences.

## Layered approval

| Stage | Who/what may draft | Deterministic checks later | Required human judgment | Invalidated by |
|---|---|---|---|---|
| Source approval | Agent/model or human may propose sources | Required fields, URL/source-ID uniqueness, dates, digest format, allowed-use vocabulary | Authority, rights, relevance, provenance, freshness | Source byte/revision/terms/rights/identity change |
| Claim approval | Agent/model may draft claims and derivations | References resolve; categories/locators/freshness present; no approval self-reference | Factual truth, source fit, conditions, derived reasoning | Claim text/premise/source/applicability/freshness change |
| Question approval | Agent/model may draft design and item | Objective/claim references, option counts, selection count, rationales, requirement matrix, approval completeness | Originality, difficulty, realism, ambiguity, architecture judgment, answer uniqueness | Stem/requirement/option/order/key/rationale/citation/objective/claim change |
| Pack-release approval | Agent/model may assemble a draft | Exact versions/digests, all required approvals, rights/notices, no stale dependencies | Realization completeness, editorial quality, distribution rights, activation decision | Any digest-covered content or dependency approval change |

An authoring model must never approve its own source classification, claims, questions, uniqueness determination, or pack release. Model critique and automated validation are advisory evidence, not approval. A person may hold more than one reviewer role only if later policy explicitly permits it and qualifications/conflicts are recorded; no such rule is approved here.

## Reviewer qualification proposal for 0.3B

- **Source/rights reviewer:** can evaluate provenance and project rights policy; formal legal opinion is not implied.
- **Claim/architecture reviewer:** current professional AWS multi-account architecture experience, or equivalent demonstrable expertise with Organizations, Control Tower, IAM Identity Center, and centralized governance/security services.
- **Question/uniqueness reviewer:** understands SAP-C02 task 1.4 and professional item construction; must inspect every requirement-option relationship.
- **Pack-release reviewer:** confirms exact approved versions, notices, scope/non-claims, and all earlier approvals.

The same authoring model cannot occupy any reviewer role. Human identity authentication and storage remain unresolved implementation questions.

## Failure behavior

- Unsupported claim: stop the chain and request a better official source, narrower claim, or removal.
- Conflicting official sources: record both, prefer the current product documentation for current behavior and the exam guide for assessed scope, then require human resolution.
- Stale source: revalidate before dependent question review; no silent date bump.
- Ambiguous item: return to scenario constraints/options; do not activate.
- Similarity concern: replace the scenario rather than lightly paraphrase it.
- Reviewer disagreement: preserve both findings and keep status draft until resolved by an authorized reviewer.

This policy defines logical artifacts and gates only. It does not add pack fields, SQLite tables, tools, state machines, or activation behavior.
