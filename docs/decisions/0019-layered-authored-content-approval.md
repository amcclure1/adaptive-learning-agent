# ADR 0019: Layered Authored-Content Approval and Invalidation

Status: Proposed
Date: 2026-07-18

## Context

ADR 0013 requires claim, question, uniqueness, and pack approval but leaves exact pilot layers and invalidation behavior open. Source provenance/rights decisions also need an explicit human gate before claims can rely on them.

## Proposed decision

Require five separate human approval types for authored-content release:

1. source approval;
2. claim approval;
3. question content approval;
4. answer-uniqueness approval;
5. pack-release approval.

Every approval is an immutable decision record over an exact artifact ID, version, and digest. It records reviewer identity, reviewer role/qualification attestation, decision, UTC timestamp, scope, findings/conditions, and the prerequisite approval IDs it relied upon.

The drafting model or drafting human cannot approve the same artifact they authored. A single human may fill several reviewer roles for the small pilot when each role is explicitly recorded and qualifications/conflicts are visible. Model critique and deterministic validation are evidence only.

Question content and answer uniqueness are independent approvals. Content approval covers correctness, objective alignment, originality, clarity, option/distractor quality, and evidence. Uniqueness approval independently confirms that explicit requirements make exactly one response or response set best.

## Invalidation

- Source identity, content, revision, terms, rights, or authority changes invalidate source approval and all dependent claim/question/pack approvals.
- Claim statement, category, premise, citation, locator, applicability, or freshness changes invalidate claim approval and downstream question/pack approvals.
- Question stem, material requirement, constraint, option, option order, key, selection count, rationale, claim link, or blueprint mapping changes invalidate question-content, uniqueness, and pack approvals.
- Editorial explanation/citation changes always invalidate pack approval and invalidate question-content/uniqueness approval when they change material reasoning.
- Blueprint, objective, realization, or compiler-version changes trigger deterministic impact analysis; affected approvals remain blocked until a human records the resolution.
- Freshness expiry marks dependent content blocked/stale without deleting historical approval records.

No approval layer implies another, and pack-release approval cannot cure an invalid prerequisite.

## Consequences

- Authority and invalidation are auditable and fail closed.
- Minor post-review edits may require renewed approvals; this is deliberate for a five-question pilot.
- Reviewer identity is a local attestation, not cryptographic proof.

## Alternatives considered

- One pack approval: rejected because it cannot localize factual or uniqueness defects.
- Merge content and uniqueness review: rejected because technical correctness does not prove a unique best answer.
- Permit model self-approval after validation: rejected by product principles and ADR 0013.

## Open points before acceptance

- Final reviewer identity format and privacy/redaction rules.
- Whether a later larger workflow needs quorum or independent dual review.
