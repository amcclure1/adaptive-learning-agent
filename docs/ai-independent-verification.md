# Independent AI Verification

Status: implemented policy candidate; ADR 0021 remains Proposed

## Normative rule

No AI-authored factual or assessment content may reach human approval until a separate source-grounded verifier has independently reviewed every applicable artifact and all material findings have been resolved.

The mandatory sequence is drafting, deterministic structural validation, independent AI verification, author revision, independent reverification, and qualified human approval. Lessons and questions begin only after their prerequisite source/claim approvals. AI verification is evidence, never approval.

## Independence

The verifier is a fresh invocation with a stable run identity and role `independent_ai_verifier`. It receives exact target records, accepted blueprint/architecture/realization references, the formal protocol, and the passing deterministic report. It receives no private chain of thought, hidden author reasoning, suggested answer, or silent defect hint. It must independently reopen authoritative sources and check all in-scope artifacts rather than infer correctness from schema validity or source ownership.

The verifier cannot mutate target artifacts, approve/review as a human, compile, install, activate, publish, tag, or release. Public-web or approved research capabilities operate outside the deterministic module. The module merely accepts bounded evidence records.

## Evidence model

- An `ai_verification_run` binds project/commit, protocol, invocation/model metadata where available, exact target digests, accepted architecture, deterministic report, independently consulted sources, findings, per-artifact dispositions, counts, questions, and completion state.
- A `verification_finding` binds exact disputed language/field and target digest to category, severity, official source/locator, explanation, required action, dependencies, confidence, status, and blocking policy.
- A `finding_resolution` preserves the exact finding and old/new target references plus the author's accepted, modified, or disputed response. It never edits or closes the original finding by itself.

Controlled dispositions are `verified`, `verified_with_nonblocking_note`, `revision_required`, `blocked`, and `unable_to_verify`. Severities are `critical`, `high`, `medium`, `low`, and `informational`. Finding categories are factual error, missing qualification, overbroad assertion, outdated behavior, source mismatch, weak locator, unsupported recommendation, insufficient premises, internal contradiction, taxonomy/classification error, scope drift, freshness concern, rights concern, and unable to verify.

## Eligibility

The gate is exact-digest and fail-closed. Human review cannot begin without a current completed run and an eligible disposition. Critical/high/medium open or disputed findings block. Any explicitly blocking finding blocks. Low/informational notes may proceed only when the run labels them nonblocking. `blocked` and `unable_to_verify` dispositions require resolution or explicit human adjudication outside approval.

A changed artifact has no current disposition until reverified. A derived recommendation additionally requires current verification and human approval of each exact premise. The AI verifier cannot be named as the human approver. Human disagreement is recorded with reasoning; it never rewrites AI evidence.

## Bounded operations

`AuthoringOperations` exposes `create_verification_run`, `register_verification_source`, `add_verification_finding`, `finalize_verification_run`, `verification_eligibility`, `create_finding_resolution`, `compare_verification_runs`, and `generate_experiment_metrics`. Requests are closed JSON-compatible objects under the project-confined authoring root. None retrieves a URL or exposes shell/filesystem/network authority.

## Revision loop

An author responds to every finding, creates a new artifact revision, updates dependencies, records a resolution, reruns structural validation, and requests a fresh complete verification. The new verifier receives prior findings only as explicit checks to confirm resolution and must still review the entire changed artifact. Disputed findings remain open for human adjudication and cannot be silently treated as resolved.
