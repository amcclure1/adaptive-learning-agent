# ADR 0018: Claim-Centered Evidence for Authored Content

Status: Proposed
Date: 2026-07-18

## Context

Direct source citations do not by themselves show which factual premise supports a lesson, answer, or distractor. Professional AWS scenarios also depend on conditions such as Region, account configuration, time, and explicit architectural priorities. Derived recommendations require several factual premises rather than one source link.

## Proposed decision

Make approved atomic claims the evidence boundary between approved sources and authored lessons/questions.

Each claim has a stable ID, concise statement, category, source citations with precise locators, applicability constraints, service/architecture scope, Region/account/configuration/time sensitivity, retrieval and review dates, freshness horizon, reviewer, review status, and supersession/invalidation state.

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
- Full claim records remain authoring-workspace records under ADR 0017's proposal; released packs retain learner-facing citations and explanations, while the release-evidence manifest preserves the claim chain.

## Alternatives considered

- Cite sources directly from questions only: rejected because it hides the atomic premise and its applicability.
- Treat paragraphs as claims: rejected because they are difficult to review, supersede, and reuse precisely.
- Let a model decide current truth during compilation: rejected because generation and retrieval are not approval.

## Open points before acceptance

- Exact claim versioning and ID rules.
- Whether claims may have multiple independent approving reviewers.
- Default freshness horizons by category; 0.3B records explicit horizons rather than relying on defaults.

