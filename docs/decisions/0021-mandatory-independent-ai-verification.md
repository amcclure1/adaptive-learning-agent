# ADR 0021: Mandatory First-Pass Self-Audit and Independent AI Verification

Status: Accepted

Date: 2026-07-19

## Context

Deterministic validation proves structure, not truth. In the `SAP-ORG-04` repeat experiment, generalized author instructions also failed to improve first-pass quality: baseline B had nine first-pass findings versus baseline A's seven. The independent loop nevertheless contained all 21 recorded logical findings before human review. This one-pilot result supports a fail-closed containment process, not a model-quality or statistical claim.

## Decision

Every AI-authored factual or assessment artifact must complete the normative [first-pass authoring protocol](../authoring-first-pass-quality-protocol.md). The author records an immutable, exact-digest `author_self_audit` before deterministic validation. Deterministic validation then precedes a separately invoked, source-grounded AI verifier. Every applicable artifact is reviewed; material findings require author revision and independent reverification before qualified human approval.

```text
draft -> author self-audit -> deterministic validation -> independent AI verification
      -> author revision -> new self-audit -> validation -> reverification
      -> qualified human approval -> downstream authoring
```

The author stage must reopen cited sources; test exceptions, exclusions, classification, Region/account/configuration/time/freshness sensitivity, recommendation premises and decision criteria, internal contradictions, and plausible falsifiers; and narrow language when evidence does not support a universal statement. The audit records concerns, revisions, exact targets, author identity, protocol version, and workspace commit. Changed bytes require a new audit; records are immutable and never imply approval.

The verifier is a fresh invocation and role with exact artifacts and accepted architecture but no hidden author reasoning. It independently reopens authoritative sources and binds findings and dispositions to exact digests. A separate invocation establishes role and context separation only. It does not prove different model weights, provider independence, statistical independence, or freedom from correlated error; unavailable model/provider metadata remains explicitly unverifiable.

The same lifecycle applies to sources and claims, lesson factual coverage, question content and keys, distractor rationales, answer uniqueness, learner explanations, and compiled projection fidelity. Answer uniqueness uses a separate adversarial pass before human uniqueness review.

## Fail-closed gates

Author self-audit eligibility requires a completed current record covering the exact digest. Deterministic validation fails without it. Independent verification additionally requires a passing validation report covering the same exact targets. Human review is ineligible when verification is missing or stale, material findings remain, the disposition is `revision_required`, `blocked`, or `unable_to_verify`, or a derived recommendation has an unverified or unapproved premise. Low or informational findings proceed only when explicitly nonblocking. No machine stage grants human approval.

The gate before lesson or question work also requires: accepted ADR 0021; accepted protocol and lifecycle contracts; current exact-digest source/claim self-audits, passing validation, and independent verification with no material residual findings; and separately authorized qualified human source/claim approvals. The repeat experiment did not create retrospective self-audits or human approvals, so downstream content remains blocked.

## Records and operations

Closed canonical file-backed records comprise author self-audits, verification runs, findings, and resolutions. Bounded authoring operations create/query self-audits; create/finalize verification runs; register consulted sources; add findings; query eligibility; record responses; compare runs; and generate metrics. They expose no shell, unrestricted filesystem/network, approval, compilation, installation, activation, publication, or release.

Experiment metrics must distinguish stored finding records, semantic logical findings, exact duplicates, repeats against changed target digests, explicit superseding records, resolutions, and residual findings. Immutable correction copies remain visible and are never counted as new logical defects merely because they are stored separately.

## Consequences and limits

- Human attention begins after three machine stages, while human authority remains mandatory.
- More author discipline, research, records, and invocations are required.
- The process can contain observed defects but cannot guarantee correct first drafts, discover every latent error, replace qualified human review, or establish statistical improvement.
- Historical experiment records and approved releases remain immutable and are not silently retrofitted.
- Agent memory and hidden reasoning are non-authoritative.

## Alternatives

- Validation directly to human review: rejected; structural success did not prevent semantic defects.
- Unrecorded self-critique: rejected; it is neither auditable nor exact-digest bound.
- Self-audit instead of independent verification: rejected; author review is not independent.
- AI verification as approval: rejected; model judgment is non-authoritative.
- Default sampling: rejected for evidence-sensitive content; every applicable artifact is reviewed.
