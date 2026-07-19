# ADR 0018: Claim-Centered Evidence for Authored Content

Status: Accepted
Date: 2026-07-18

## Context

Direct source citations do not by themselves show which factual premise supports a lesson, answer, or distractor. Professional AWS scenarios also depend on conditions such as Region, account configuration, time, and explicit architectural priorities. Derived recommendations require several factual premises rather than one source link.

## Decision

Make approved atomic claims the evidence boundary between approved sources and authored lessons/questions.

Each claim has a stable ID, explicit schema version and revision, concise atomic statement, category, source citations with precise locators and source digests, applicability constraints, service/architecture scope, Region/account/configuration/time sensitivity, explicit freshness horizon, validation and human-review state, supersession/invalidation state, and a domain-separated canonical digest.

Supported categories are:

- authoritative documented fact;
- service limitation;
- derived architectural recommendation;
- scenario assumption;
- cost or operational tradeoff;
- time-sensitive fact;
- Region-sensitive fact;
- account/configuration-dependent fact.

A derived recommendation references every supporting factual claim and states its decision criterion and applicability. A citation cannot substitute for that derivation.

Questions reference approved claim IDs. Key and distractor rationales identify the claims and scenario requirements on which they rely. Stale or invalid claims block dependent question and pack approval until impact review resolves them.

## Consequences

- Factual defects can be corrected and impact-traced independently of prose.
- Applicability and freshness become explicit rather than hidden in author memory.
- Claim review adds editorial work and stable-ID/version requirements.
- Full claim records remain authoring-workspace records under ADR 0017; released packs retain learner-facing citations and explanations, while the release-evidence manifest preserves the claim chain.

## Alternatives considered

- Cite sources directly from questions only: rejected because it hides the atomic premise and its applicability.
- Treat paragraphs as claims: rejected because they are difficult to review, supersede, and reuse precisely.
- Let a model decide current truth during compilation: rejected because generation and retrieval are not approval.

## Fixed implementation contract

- Claim IDs are stable across revisions and independent of filenames. Revisions are positive integers; an approved revision is immutable, while an editable draft may be replaced only with expected-prior-digest conflict checking.
- One claim contains one independently reviewable assertion. Compound prose must be split unless the conditions are inseparable from that single assertion.
- Source references bind source ID, source revision, source canonical digest, precise locator, and supported proposition.
- Derived recommendations bind every approved premise claim by ID/revision/digest and state a decision criterion plus applicability conditions. Derived-claim graphs must be acyclic.
- Multiple claim approvals may exist, but release eligibility requires at least one current qualifying approval and no current revocation or unresolved conflict. No quorum is required for the bounded pilot.
- Every claim records an explicit date or rule-based freshness horizon. No category default silently grants currency.

The exact record shape and controlled vocabularies are normative in [the schema contract](../aws/sap-c02-0.3b-schemas.md).
