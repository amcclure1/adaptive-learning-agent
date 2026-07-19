# Subject Builder Next-Phase Design Handoff

Date: 2026-07-19
Status: design complete for review; implementation not authorized

## Outcome

The next-phase design separates two milestones that must not be conflated:

- **0.2B** is a bounded official static-asset pilot using one current Amateur Extra figure group. It tests asset identity, rights, digests, accessibility, terminal fallback, offline behavior, and Hermes display—nothing from the Subject Builder or AWS line.
- **0.3A–C** establishes assessment/curriculum research, proves a small manually reviewed AWS SAP-C02 realization, and only then introduces agent-assisted construction.

The governing product direction is whole-plan coherence with progressive realization, guided learner control, evidence-backed assessment authenticity, capability-seeking agency with controlled activation, and layered human approval. The runtime-independent core, local-first operation, portable packs, deterministic scoring/state, and non-authoritative memory principles remain intact.

## Design decisions recorded

### Official-question policy

Official questions may be reused verbatim only when an issuing-authority reuse policy, public-domain basis, applicable license, or specific permission is established. Reuse preserves exact identity, wording, option order/text, key, source/version, effective dates, rights, and errata/withdrawal status, and separates official material from project prose.

Official examples that lack redistribution rights may inform format, scenarios, cognitive depth, command language, distractor patterns, and response behavior but may not be copied into packs. Dumps, recalled live questions, leaked keys, unauthorized scraped commercial banks, “actual questions” sources, and suspicious unclear-provenance derivatives are excluded entirely.

Normative rule: **Use official questions when provenance and rights permit. Otherwise, learn the assessment grammar from permissible evidence and create original questions.**

### Assessment research and blueprint

After a user identifies an outcome, the future agent automatically researches current assessment identity/version, official guides/domains/tasks, delivery and response rules, scenario complexity, cognitive depth, tradeoffs, exhibits/labs, samples, scoring/completion expectations, and rights. Sources are tiered as official, licensed/open, descriptive, or excluded and separately declare factual, style, and reuse roles.

Research produces a persistent, versioned, human-reviewable assessment blueprint covering identity, target level, formats, scenario/constraint profiles, cognitive demand, distribution, prompt/distractor patterns, exhibits/labs, evidence/rights, confidence, and uncertainty. The rule is: **Copy the assessment grammar, not the assessment sentences.**

Confidence is high, medium, low, or insufficient/unsafe. Medium and low confidence cause guided approval/clarification using researched choices. Unsafe evidence blocks exam-matching generation. Fallback summarizes evidence and gaps, offers two or three informed options, recommends one, and asks for an authorized example or preferred representative source rather than a blank-ended style question.

### Learning architecture and realization

The complete **learning architecture** defines the intended outcome, target/version, domains, objectives, prerequisites, content requirements, depth, assessment strategy/blueprint, completion criteria, sequence, cross-domain relationships, and evidence/freshness policy.

A versioned **realization plan** selects what to build now: a complete curriculum, one domain, weak areas, foundations, an exam subset, pilot, or time-boxed path. Principle: **Approve the whole learning architecture; realize content progressively.**

Dependencies are blocking prerequisites, bridge prerequisites, recommended context, or independent objectives. For partial scope, the planner maps the request into the complete architecture, finds prerequisites/downstream gaps, explains effects, recommends the smallest coherent realization, offers short bridges, allows warned omission of nonblocking context, and refuses/revises only when the stated outcome cannot be met.

Examples cover one SAP-C02 domain, weak security objectives, known foundations, a short prerequisite bridge, and an exam-guide revision.

### Curriculum version and impact

Architectures and realization plans have independent identities/versions; realizations pin one architecture version. Revision produces a human-reviewable impact report for changed objectives/dependencies, affected lessons/questions/sources, learner progress interpretation, new content gaps, realization validity, and installed-pack validity. No migration engine is designed and no installed bytes/progress are silently changed.

The smallest likely future metadata is identified, but serialization, pack integration, storage, and schemas remain unresolved and no fields were added.

### Evidence-backed authored assessment

The future chain is:

```text
objective → approved claims → explicit scenario constraints
→ candidate answers → keyed and distractor rationales
→ citations → human review → activation
```

Authoritative facts, derived recommendations, original scenarios, distractors, and human-approved conclusions remain distinct. Every material constraint is explicit; the key satisfies all constraints; each distractor fails for a documented reason; no hidden assumption makes the key win; factual claims use authoritative evidence; and generated content is never labeled official. A qualified human approves answer uniqueness.

Claim approval, question approval, and pack-release approval are separate. An authoring agent cannot supply any of them.

### Capability discovery and permission model

Capability discovery is a first-class future Subject Builder phase. The agent searches for roles such as authoritative document search, assessment research, source snapshots, claim verification, diagram inspection, OCR fallback, code/lab execution, cloud inspection, and freshness checks across runtime tools, MCP, connectors, skills, APIs, local utilities, and databases.

Discovery can be automatic; activation is controlled:

- Level 0: public read-only;
- Level 1: private read-only;
- Level 2: external mutation;
- Level 3: sensitive, destructive, production, or costly execution.

Every proposal explains provider/source, purpose, benefit, authentication, accessed data, read/write behavior, effects, cost, security/privacy, least privilege, fallback, and disable/removal. Private access, credentials, mutation, and sensitive work require explicit approval. The system never silently installs MCP, grants cloud access, stores credentials in packs, or broadens permission.

The guided setup flow covers provider verification, runtime compatibility, approval, setup, health testing, recorded scope, and removal. AWS documentation/knowledge MCP is only an illustration; no provider behavior or compatibility is claimed, no AWS account is required architecturally, and nothing was installed.

## Proposed ADRs

- [ADR 0010 — Whole Learning Architecture with Progressive Realization](../decisions/0010-whole-learning-architecture-progressive-realization.md)
- [ADR 0011 — Assessment Authenticity and Official-Question Reuse](../decisions/0011-assessment-authenticity-official-question-reuse.md)
- [ADR 0012 — Capability Discovery with Controlled Activation](../decisions/0012-capability-discovery-controlled-activation.md)
- [ADR 0013 — Evidence-Backed Authored Questions and Layered Approval](../decisions/0013-evidence-backed-authored-questions-layered-approval.md)

All four are **Proposed**. Repository governance does not treat this design task alone as sufficient formal acceptance, and none authorizes implementation.

## Revised roadmap

### 0.2B — official asset pilot

E7B is the research-first candidate because the current official consolidated NCVEC pool references one shared figure from three questions in that group. E7D is the comparable fallback; E9B is a broader two-figure fallback. No question wording or figure was imported. Final choice requires fresh authoritative inventory, asset-specific rights, accessibility review, and an accepted narrow pack-format ADR.

0.2B excludes generated questions, curriculum planning, subject building, capability discovery/MCP, AWS, scoring changes, and SQLite changes.

### 0.3A — research and curriculum architecture

Manually produce assessment research, rights/use classifications, an assessment blueprint, complete curriculum architecture, dependencies, realization candidates, guided scope evidence, impact design, and optional capability proposals. No full AWS pack is required.

### 0.3B — manually reviewed SAP-C02 pilot

After current authoritative AWS research, choose one domain/task from the approved architecture and create a small claim set, original lessons, exactly five original scenario questions, distractor rationales, authoritative citations, uniqueness review, and human claim/question/pack approvals. No generalized automatic builder.

### 0.3C — agent-assisted construction

Add conversational research, blueprint/curriculum proposals, scope negotiation, capability recommendations, drafting, deterministic validation, and mandatory human activation only after 0.3B proves the manual review chain.

## Implementation prerequisites

1. Review and accept, revise, or reject ADRs 0010–0013.
2. For 0.2B, complete official figure inventory, rights/derivative/accessibility review, security limits, exact format proposal, and content-review plan.
3. For 0.3A, verify current SAP-C02 target material and decide standalone artifact serialization/versioning.
4. Define stable objective/version semantics, impact rules, and human approval scopes.
5. Define blueprint and evidence-use validation without storing unsafe examples.
6. Define claim/question records, reviewer qualifications, uniqueness review, and change invalidation for 0.3B.
7. Define a runtime-neutral capability-role/discovery boundary, local non-secret availability records, approval audit, expiry, and failure behavior.
8. Verify any Hermes, MCP, AWS, connector, or API behavior from current official documentation during its later implementation task.
9. Explicitly authorize each implementation, content import, external setup, private access, or mutation task.

## Unresolved decisions

- Exact serialization and authoritative location for assessment blueprints, learning architectures, realization plans, impact reports, claims, rationales, and layered reviews.
- Whether any of those artifacts later become portable pack components and which explicit pack version carries them.
- Stable objective-version mapping between curriculum architecture and pack objectives.
- Which curriculum edits invalidate realization, content, assessment, or learner-progress interpretations.
- Practical originality/similarity review that does not retain protected or unsafe examples.
- Reviewer qualification and identity expectations for AWS claims, architectural recommendations, uniqueness, rights, accessibility, and release.
- Exact 0.2B asset format, safe media types/limits, SVG policy, derivative handling, alternative-text scope, and runtime reference behavior.
- Final 0.2B group after authoritative rights/accessibility research.
- Current 0.3B SAP-C02 domain/task and source baseline after 0.3A research.
- Runtime-neutral representation of capability roles, availability, permission scope, health, expiry, and revocation.
- Whether new deterministic tools or SQLite data are needed; neither is assumed by this design.

## Documents created

- [Subject Builder architecture](../subject-builder-architecture.md)
- [Assessment research policy](../assessment-research-policy.md)
- [Curriculum planning](../curriculum-planning.md)
- [Capability discovery](../capability-discovery.md)
- [AWS SAP-C02 pilot plan](../aws-sap-c02-pilot-plan.md)
- [Amateur Extra asset pilot plan](../amateur-extra-asset-pilot-plan.md)
- Proposed ADRs 0010–0013 listed above
- This handoff

## Documents updated

- [Product principles](../product-principles.md)
- [Roadmap](../roadmap.md)
- [Current status](../current-status.md)
- [Project context](../project-context.md)
- [README](../../README.md)

## Scope confirmation

This task changed documentation only. It added no implementation or test code, diagram/asset bytes, Amateur Extra question content, AWS claims/lessons/questions, subject pack, pack field/semantic, JSON tool, SQLite table/migration, Hermes workflow, MCP server, connector, skill, credential, cloud access, external mutation, or installed dependency. It did not modify released format 0.1/0.2 behavior or learner data.
