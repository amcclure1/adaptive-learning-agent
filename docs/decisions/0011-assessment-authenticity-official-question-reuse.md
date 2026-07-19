# ADR 0011: Assessment Authenticity and Official-Question Reuse

Status: Proposed
Date: 2026-07-19

## Context

The NCVEC pilot proves that some official questions can be reused exactly under a documented public-domain basis. AWS-like assessments usually provide examples that can inform style but cannot automatically be redistributed. Without a common policy, “authentic” could be mistaken for copying protected or unsafe exam material.

## Proposed decision

Classify assessment material as reusable official content, study-only evidence, or excluded material. Reuse official questions only under an explicit public-domain, license, permission, or issuing-authority reuse basis, with exact identity, bytes, key, source version, effective dates, rights, and errata handling.

Use permissible study-only evidence to infer assessment grammar, not sentences. Exclude dumps, recalled live questions, leaked answers, unauthorized commercial banks, and suspicious derivatives from all research and authoring.

Require assessment research to classify evidence by tier, allowed use, rights, confidence, and uncertainty. Require generated content to be labeled original and forbid claims that it is official exam content.

## Consequences

- The project can use genuinely reusable official material without adopting a blanket prohibition.
- Assessment authenticity becomes an evidence-backed structural goal rather than textual imitation.
- Research must track rights separately from authority and confidence.
- Low or unsafe evidence causes guided fallback rather than speculative generation.
- Similarity and provenance review add editorial work before authored questions can activate.

## Alternatives considered

- Ban all official questions: rejected because it would discard lawful public-domain or licensed material such as NCVEC.
- Treat all official samples as reusable: rejected because public access does not establish redistribution rights.
- Use public candidate recollections for realism: rejected because provenance, rights, and live-exam integrity are unsafe.
- Ask learners to define question style without research: rejected because it shifts specialist work to the user and weakens authenticity.

## Acceptance prerequisites

- Review the tier/use vocabulary and its relationship to existing format-0.2 source and rights records.
- Decide whether assessment blueprints remain standalone authoring artifacts or later become pack components.
- Define a practical originality/similarity review for 0.3B without storing protected examples.
