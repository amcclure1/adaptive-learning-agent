# ADR 0021: Mandatory Independent AI Verification Before Human Approval

Status: Proposed

Date: 2026-07-19

## Context

The first `SAP-ORG-04` source-and-claim pass satisfied closed schemas and deterministic structural validation, yet a separate source-grounded review found material source-fit, qualification, classification, and premise-sufficiency defects. Schema correctness cannot establish factual truth. Sending AI-authored factual or assessment content directly from structural validation to a human reviewer also wastes scarce human attention on defects another independent research pass can contain earlier.

No generative model can guarantee an error-free first draft. The enforceable process goal is therefore independent defect containment, not a claim of infallible generation.

## Proposed decision

Require this rule for all AI-authored factual or assessment content:

> No AI-authored factual or assessment content may reach human approval until a separate source-grounded verifier has independently reviewed every applicable artifact and all material findings have been resolved.

The normative lifecycle becomes:

```text
drafting
→ deterministic structural validation
→ independent AI verification
→ author revision
→ independent AI reverification
→ qualified human approval
→ downstream authoring
```

The verifier is a fresh invocation and role. It receives exact artifacts and accepted architecture, but no hidden author reasoning. It independently reopens authoritative sources, checks complete assertions and exceptions, inspects every in-scope artifact, and binds findings and dispositions to exact digests. It cannot approve, edit target records, compile, install, activate, publish, or release.

Verification is mandatory evidence and never human authority. Human approval remains an independent exact-digest decision. A human may disagree only through an explicit adjudication with reasoning.

Apply the same pattern to source/claim facts, lesson factual coverage, question content and keys, distractor rationales, adversarial answer uniqueness, learner explanations, and compiled projection fidelity. Answer uniqueness uses a separate adversarial AI pass before human uniqueness review.

## Fail-closed gate

Human review is ineligible when an exact current artifact lacks a completed disposition, a blocking critical/high/medium finding remains, the disposition is `blocked` or `unable_to_verify`, validation or verification targets stale bytes, a revision has not been reverified, or a derived recommendation has an unverified or unapproved premise. Low/informational findings proceed only when explicitly nonblocking. Passing verification grants no approval.

## Records and operations

Add closed, canonical, file-backed AI verification run, verification finding, and finding-resolution records. Add bounded authoring operations to create/finalize runs, register independently consulted sources, add findings, query eligibility, record author responses, compare runs, and generate experiment metrics. Research remains outside the deterministic core; the operations expose no shell, unrestricted filesystem/network, approval, installation, activation, publication, or release.

The records remain authoring evidence outside installed packs and SQLite. Changed target bytes invalidate prior verification eligibility while preserving history.

## Consequences

- Humans receive content after two independent machine stages rather than one.
- Source research and model invocations increase, but defects should be found earlier.
- Verification quality remains model- and evidence-dependent; human judgment is still required.
- Exact model configuration may be unavailable, so reproducibility metadata is recorded where available and limitations remain explicit.
- Existing approved releases are not retroactively invalidated. New or revised AI-authored content follows the new gate after acceptance.

## Alternatives

- Deterministic validation followed directly by human review: rejected because baseline A demonstrated semantic defects despite a clean structural result.
- Author self-critique: rejected because it is not independent and can repeat the same assumptions.
- AI verification as approval: rejected because model judgment is non-authoritative.
- Sampling: rejected by default; an explicitly designed experiment may authorize it, but normal evidence-sensitive work reviews every applicable artifact.
