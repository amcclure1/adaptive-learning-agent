# ADR 0013: Evidence-Backed Authored Questions and Layered Approval

Status: Accepted
Date: 2026-07-19

## Context

Format 0.2 can label generated questions and require one pack approval, but it does not represent claim review, distractor rationales, answer-uniqueness review, or a staged authoring workflow. Complex scenario questions can appear plausible while relying on hidden assumptions or unsupported recommendations.

## Decision

Future authored questions follow an inspectable chain from objective through approved claims, explicit scenario constraints, candidate answers, keyed and distractor rationales, citations, human question review, and pack activation.

Separate claim approval, question approval, and pack-release approval. A qualified human must approve answer uniqueness. Agent-authored content remains draft and may not approve itself. Deterministic validation should eventually check record completeness and cross-references, while humans remain responsible for truth, judgment quality, and uniqueness.

## Consequences

- Factual and pedagogical defects can be reviewed at the layer where they originate.
- Original AWS-like scenarios can be auditable without being represented as official questions.
- Authoring artifacts become more detailed than the current pack format.
- Qualification expectations, reviewer identity, record shapes, and change invalidation rules need later decisions.

## Alternatives considered

- One pack-level approval only: insufficient for tracing claim and question-level review.
- LLM self-critique as approval: rejected because authors cannot activate their own work and model judgment is non-authoritative.
- Citation presence as proof of answer uniqueness: rejected because citations cannot establish that distractors fail or all constraints are explicit.

## Deferred milestone details

Acceptance establishes the evidence chain, quality requirements, human uniqueness review, and layered approval direction. It does not choose exact records, pack-format version, JSON schema, database representation, tool-contract changes, reviewer qualifications, or implementation modules. Milestone-specific reviews must still:

- define minimum claim and question review records for the five-question 0.3B pilot;
- decide who qualifies to approve AWS architectural conclusions and uniqueness;
- define which edits invalidate each approval layer;
- decide whether records are embedded, adjacent portable files, or review-only build artifacts.
