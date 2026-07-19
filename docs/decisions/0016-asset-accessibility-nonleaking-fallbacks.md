# ADR 0016: Asset Accessibility and Non-Leaking Fallbacks

Status: Accepted
Date: 2026-07-19

## Context

A required figure can exclude terminal and screen-reader users. An improvised model description may be inaccurate, reveal an answer, or change after restart. A caption alone does not convey figure content, while a fully interpretive description can solve the assessment.

## Decision

Every format-0.3 asset requires digest-covered title, caption, meaningful alt text, and terminal fallback. Project-authored accessibility prose has a separate rights reference. The text describes printed labels and relationships without interpreting the tested function, classification, value, or identity.

Deterministic validation rejects empty fields, prohibited answer markers, and complete normalized keyed-option text in pre-answer accessibility fields. Human approval remains mandatory because lint cannot establish semantic equivalence or non-leakage.

Require explicit human approval of asset identity, fidelity, source, rights, alt text, caption, fallback, question mappings/order, and absence of leakage for every referencing question. Agent authors cannot approve their own accessibility prose.

Adapters present the exact asset when a verified surface supports it and otherwise present the approved fallback. The skill confirms access before asking for an answer, never uses model vision or improvised description, and permits challenge/quarantine when access or fidelity is defective.

For pinned Hermes v0.18.2, implementation must test whether a public plugin mechanism can present local image output. If verified, the adapter may resolve a core-issued logical reference and present the exact PNG without alteration, interpretation, or scoring. If not verified, it uses approved alt text and terminal fallback, records native rendering as unsupported or unverified, and does not modify Hermes core or configuration. Native rendering unavailability alone does not block format-0.3 acceptance.

## Consequences

- Asset questions remain usable offline in text-only runtimes.
- Accessibility text and mappings become immutable reviewed pack content.
- Some figures will be ineligible when a useful description necessarily reveals the key.
- Native Hermes image display is optional at the portable-core boundary and must be verified separately for each supported surface/version.

## Alternatives considered

- Let the model describe the figure: rejected as nondeterministic, potentially leaking, and non-authoritative.
- Require image rendering only: rejected because terminal and screen-reader access would fail.
- Caption-only fallback: rejected because identity is not equivalent access.
- Accept empty alt text for official figures: rejected because question-required assets are not decorative.

## Revisit triggers

Revisit only if evidence shows the accepted accessibility representation cannot provide meaningful non-leaking access, or a later format/runtime introduces a reviewed equivalent mechanism. A text fallback remains mandatory for format 0.3.
