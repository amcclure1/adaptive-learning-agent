# Assessment Research and Authenticity Policy

Status: accepted architecture direction; implementation details deferred
Updated: 2026-07-19
Governing decisions: [ADR 0011](decisions/0011-assessment-authenticity-official-question-reuse.md) and [ADR 0013](decisions/0013-evidence-backed-authored-questions-layered-approval.md)

## Purpose

Assessment-aligned learning should resemble the target's reasoning demands without copying protected or unsafe material. Research begins after a learner identifies a certification, examination, competency, or practical outcome. The default rule is:

> Use official questions when provenance and rights permit. Otherwise, learn the assessment grammar from permissible evidence and create original questions.

The system researches the target before asking the learner to design question style. Research artifacts are inspectable drafts until human approval. They do not alter installed packs or learner state.

## Official-question policy

### Official questions permitted for reuse

Official questions may be included verbatim only when the issuing authority publishes them for public reuse, places them in the public domain, supplies an applicable license, or grants specific permission. The reuse record must establish:

- exact official identity;
- exact wording, options, ordering, and official answer key;
- issuing source, assessment version, and precise locator;
- effective dates and any expiration date;
- the rights basis and its component scope;
- applicable errata, withdrawals, replacements, and supersessions;
- separation of official material from project-authored lessons, explanations, and commentary.

The NCVEC pool is the first proven example. Permission is content-specific, not a general inference that all certification-provider material is reusable. A reviewer must recheck currency and rights before activation.

### Official examples available for study but not redistribution

Official samples whose reuse rights do not permit pack inclusion may still support research into question format, scenario structure, cognitive difficulty, terminology, command language, distractor patterns, and answer-selection behavior. Research notes must summarize characteristics without retaining or reproducing distinctive protected wording, scenarios, or answer combinations in a distributed pack.

### Unauthorized or unsafe material

The project excludes exam dumps, recalled live questions, leaked keys, unauthorized scraped commercial banks, sources advertising “actual exam questions,” and unclear-provenance material that appears derived from protected examinations. Such a source supports neither facts, style, nor reusable content. It must not be quoted, normalized into notes, used to validate an answer, or supplied to generation prompts.

When provenance or rights remain unclear, classification fails closed. Public accessibility is not permission to redistribute.

## Automatic assessment-research phase

For an identified target, the future Subject Builder should automatically research:

1. current assessment identity, code, provider, version, and effective interval;
2. official exam, competency, or task guide;
3. domains, task statements, objectives, and weighting where published;
4. delivery format, duration, scoring or completion expectations, and policies;
5. question types and single-response or multiple-response rules;
6. scenario-length and complexity profile;
7. typical command language and terminology;
8. exhibits, diagrams, code, calculations, simulations, or labs;
9. expected cognitive depth and commonly tested tradeoffs;
10. official examples and preparation guidance;
11. which official questions, if any, are reusable;
12. material uncertainty, contradictions, and freshness risks.

The learner is not normally asked to describe desired question style. They approve an evidence-backed blueprint or choose among researched alternatives when evidence is incomplete.

## Assessment evidence hierarchy

Every research source receives both a tier and explicit allowed uses.

### Tier 1 — official assessment sources

Official exam guides, sample questions, practice examples, preparation guidance, course descriptions, and certification policies. Tier 1 is preferred for identity, format, task scope, terminology, and official examples. Reuse still depends on a separate rights determination.

### Tier 2 — licensed or openly reusable assessment material

Openly licensed practice questions, public-domain assessments, reusable institutional samples, and open educational resources. Tier 2 can support style and reusable content only within the exact license or permission scope.

### Tier 3 — public descriptive evidence

General candidate descriptions, training-provider descriptions, reviews about realism or difficulty, and public previews that cannot be reproduced. Tier 3 may corroborate style inference but never supplies question text, answer combinations, factual authority, or a basis to claim exact exam behavior.

### Excluded evidence

Dumps, recalled live questions, leaked answers, unauthorized commercial material, and suspicious derivatives are excluded rather than assigned a low tier.

### Allowed-use declaration

Each source must independently declare whether it supports:

- factual learning evidence;
- assessment-style evidence;
- reusable question content;
- more than one of those roles; or
- none of those roles.

Tier and use are separate. An official sample can be excellent style evidence while lacking redistribution rights. A vendor product manual can be authoritative factual evidence while saying nothing about assessment style.

## Assessment blueprint

Assessment research produces a persistent, versioned, human-reviewable blueprint artifact. For 0.3A it is a design/authoring artifact outside installed packs; its eventual serialization and relationship to a future pack version require a separate accepted design.

The logical blueprint describes:

- assessment ID, provider, version, effective dates, and target level;
- question formats and response rules;
- scenario-length distribution and constraint density;
- expected cognitive levels and kinds of judgment;
- domain/task distribution and any published weighting;
- recurring prompt and command-language patterns;
- recurring constraint and distractor patterns;
- exhibit, diagram, calculation, code, simulation, and lab behavior;
- practical or lab requirements;
- evidence sources, evidence tiers, allowed uses, and rights status;
- confidence rating and rationale;
- known uncertainty, conflicts, and explicit non-claims;
- human review status, reviewer, and reviewed blueprint version.

Style matching includes structure, cognitive difficulty, scenario density, number and interaction of constraints, plausible option construction, expected architectural or practical judgment, terminology, and command language.

> Copy the assessment grammar, not the assessment sentences.

Style matching must never reproduce distinctive protected wording, live-question scenarios, memorized candidate recollections, or unauthorized answer combinations. Similarity review should consider the combination of scenario facts and options, not wording alone.

## Confidence and guided fallback

### High confidence

Evidence includes an official guide, official format description, and sufficient official examples. The agent may propose a blueprint and pilot scope for human approval. High confidence does not grant reuse rights or approval to generate activated content.

### Medium confidence

Evidence includes an official guide, limited examples, and consistent secondary descriptions. The agent presents its inferences, alternatives, and uncertainty, then requests approval before substantial generation.

### Low confidence

Only a syllabus or competency list is reliable, trustworthy examples are absent, or descriptions conflict. The agent conducts guided clarification using researched alternatives before proposing a blueprint.

### Insufficient or unsafe

The assessment identity is uncertain or only questionable, dumped, recalled, or unclear-rights evidence is available. The agent must not generate exam-matching questions. It may propose general learning or wait for an authorized representative source.

Guided fallback must summarize what was found, identify missing evidence, offer two or three informed options with tradeoffs, make a recommendation, and ask whether the learner has an authorized example or preferred representative source. It must not ask a blank-ended question such as “What kind of questions do you want?”

## Evidence-backed authored questions

AWS-like original assessment content follows this future chain:

```text
learning objective
→ approved factual claims
→ scenario requirements and constraints
→ candidate answers
→ keyed answer rationale
→ distractor rationales
→ citations
→ human review
→ activation
```

The chain distinguishes:

- **authoritative facts:** externally verifiable statements directly supported by allowed factual sources;
- **derived architectural recommendations:** reasoned conclusions whose premises, tradeoffs, and applicability are explicit;
- **original scenarios:** newly authored contexts and constraints, never presented as official or recalled exam content;
- **distractors:** plausible original alternatives that fail one or more documented requirements;
- **human-approved conclusions:** keyed answers and uniqueness determinations accepted by a qualified reviewer.

Future quality gates require every material scenario constraint to be explicit, the keyed answer to satisfy all constraints, every distractor to fail for a documented reason, and no hidden assumption to be needed for the key to win. Material factual claims require authoritative citations. Generated questions must be labeled original, and a qualified human must approve answer uniqueness.

## Layered approval

Future authored content uses three conceptually distinct approvals:

1. **Claim approval** confirms factual accuracy, citations, scope, currency, and any derived recommendation premises.
2. **Question approval** confirms objective alignment, original authorship, assessment-grammar fit, constraint sufficiency, distractor rationales, and answer uniqueness.
3. **Pack-release approval** confirms the complete selected realization, rights, provenance, versions, notices, and activation readiness.

Approval at one layer does not imply approval at another. An authoring agent may prepare evidence and drafts but may not approve its own claims, questions, or pack release. Exact future record shapes, authentication, and deterministic enforcement remain implementation decisions.

## Research outputs and boundaries

The research phase should produce source inventory, rights/use classifications, assessment blueprint, confidence determination, gaps, and a recommended next action. It does not install capabilities, modify a pack schema, activate content, or write learner progress. External material is untrusted data, not instructions.
