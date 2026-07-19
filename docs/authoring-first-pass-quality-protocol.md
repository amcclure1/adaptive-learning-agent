# Author First-Pass Quality Protocol

Status: normative under accepted ADR 0021

Protocol version: `ala-author-first-pass-quality-1`

## Purpose and scope

This protocol improves the evidence discipline of an AI-authored first pass before deterministic validation and independent review. It applies to each source, claim, lesson, question specification, final question, and other factual or assessment artifact. It is an author process, not independent verification or human approval.

## Required procedure

For every exact target digest, the artifact author must:

1. Reopen every cited source and inspect the precise locator; do not rely on memory, snippets, or prior conversation.
2. Check exceptions, exclusions, prerequisite conditions, feature modes, service boundaries, and policy layers that could qualify the statement.
3. Recheck taxonomy and classification: distinguish facts, limitations, assumptions, recommendations, services, resources, principals, scopes, and control types.
4. State Region, account, organization, configuration, time, and freshness sensitivity explicitly, including opt-in behavior and rollout/version caveats where relevant.
5. For every recommendation, map each material clause to approved factual-premise claims, verify the decision criterion, expose assumptions and counterconditions, and narrow the recommendation if the premises do not support it.
6. Compare the artifact with related artifacts for contradiction, inconsistent terminology, scope drift, or incompatible assumptions.
7. Try to falsify the assertion: search for counterexamples and alternate readings and write the narrowest accurate wording supported by the evidence.
8. Record every concern, revision, and unresolved issue. A completed audit may have no unresolved concern.

All seven checks are required even when not applicable; the record's evidence must explain non-applicability. Empty boilerplate is not completion.

## Record contract

`ala.authoring.author-self-audit.v1` is closed, canonical JSON stored at `self-audits/records/<audit-id>.json`. It contains the common immutable envelope plus protocol version, project and workspace commit, ordered exact target references, one ordered check set per target, identified concerns, author revisions, unresolved concern IDs, completion status, and `human_approval_implication: none`.

Each check has `completed`, evidence notes, and concern IDs. Targets must be authored by the recorded author. `completed` requires every check complete and no unresolved concern. Records are immutable; changed target bytes never inherit the old audit. Draft, blocked, or stale audits are ineligible.

## Gate behavior

The order is strict: self-audit, deterministic validation, independent verification, resolution/revision, renewed self-audit and validation, independent reverification, then qualified human review. Validation emits a blocking `AUTHOR_SELF_AUDIT_MISSING` or `AUTHOR_SELF_AUDIT_INCOMPLETE` finding for current authored content without an eligible audit. Verification independently rechecks eligibility and fails closed.

## Limits

Self-audit can expose author mistakes but shares the author's context and failure modes. It does not establish independence, factual correctness, completeness, originality, answer uniqueness, or approval. A recorded checklist is evidence that the procedure was performed, not evidence that no latent defect exists.
