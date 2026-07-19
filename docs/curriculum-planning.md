# Curriculum Planning

Status: proposed design
Updated: 2026-07-19
Related proposal: [ADR 0010](decisions/0010-whole-learning-architecture-progressive-realization.md)

## Governing model

> Approve the whole learning architecture; realize content progressively.

The project separates the coherent design of an intended learning experience from the smaller portion built now. This avoids producing isolated lessons that look complete while hiding prerequisites, assessment gaps, or uncovered outcomes. It does not require authoring an entire curriculum before useful work begins.

## Learning architecture

The **learning architecture** is the complete approved structure for the intended outcome. It includes:

- the target outcome and learner-facing success statement;
- the relevant certification, examination, competency, or practical goal and version;
- domains, objectives, and their stable identities;
- prerequisite and cross-domain relationships;
- required and optional content;
- expected depth and cognitive performance for each objective;
- teaching and assessment strategy;
- the assessment blueprint and domain/task coverage expectations;
- completion criteria and explicit non-claims;
- recommended sequence and valid alternate paths;
- evidence classes, currency rules, and freshness requirements;
- known uncertainty, gaps, and deferred content.

The architecture is designed early enough to reveal dependencies and omissions. Approval means the structure is a reasonable complete plan for the stated outcome; it does not mean all lessons, claims, questions, or labs exist.

## Realization plan

The **realization plan** selects what to build now from an approved architecture. It may cover:

- the complete curriculum;
- one domain or selected objectives;
- learner weak areas;
- prerequisite foundations;
- an exam-focused subset;
- a short pilot; or
- a time-boxed learning path.

The plan identifies selected objective versions, required bridges, omitted areas, expected depth, evidence work, assessment items, completion boundary, schedule/budget assumptions if any, and the effect on the learner's stated outcome. It is versioned independently from the architecture and can expand without redefining the whole plan.

A realization is not silently described as complete preparation when it covers only a slice.

## Dependency categories

- **Blocking prerequisite:** required to perform the target objective safely or correctly. Omission makes the selected outcome incoherent; the plan must include it or revise the outcome.
- **Bridge prerequisite:** a narrow missing concept that can be supplied with concise bridge material instead of a complete prerequisite module.
- **Recommended context:** helpful for depth, transfer, or efficiency but not required for the selected result. It may be omitted with a visible warning.
- **Independent objective:** can be learned and assessed without a dependency on the selected path.

Relationships are directional and justified. A label alone is insufficient; the architecture records why the dependency exists and what competency satisfies it. The user should not need to understand or manually construct a graph.

## Guided partial-scope behavior

When a learner asks for a subset, the future planner should:

1. map the request to objective versions in the complete architecture;
2. detect missing prerequisites, cross-domain effects, and downstream gaps;
3. explain how the scope affects the stated outcome and assessment coverage;
4. recommend the smallest coherent realization;
5. offer concise bridge material when a full prerequisite module is unnecessary;
6. allow omission of recommended nonblocking context with a visible warning;
7. refuse or revise the scope only when it cannot meet the learner's stated outcome.

The response should lead with a recommendation and a concise impact summary, then offer choices. It should distinguish “not included” from “not required” and should never invent mastery from conversation memory.

## Examples

### Build one SAP-C02 domain

A learner asks for one domain only. The planner maps that domain into the complete current SAP-C02 architecture, identifies shared concepts from other domains, and proposes the domain plus only its blocking and bridge prerequisites. It visibly states that the realization is domain preparation, not complete SAP-C02 preparation, and shows uncovered blueprint weight and cross-domain tasks.

### Focus on weak security objectives

Persisted learner evidence identifies weak security objectives. The planner selects those objective versions, includes any blocking identity, encryption, or governance foundations, and preserves links to downstream architectural decisions. It does not rebuild unrelated strong areas, but warns if the requested focus leaves a material assessment gap.

### Skip foundations already known

The learner claims prior knowledge. The planner may omit a foundation if the dependency is nonblocking or if deterministic diagnostic evidence satisfies its completion criterion. The omission and basis are recorded in the realization plan. Conversation memory alone is not proof of competency.

### Add a short prerequisite bridge

A high-availability scenario depends on a narrow networking concept. Rather than inserting a full networking module, the planner adds a short, cited bridge with its own completion check, then returns to the selected objective.

### Exam-guide update

An official guide changes domains or task statements. Research produces a new architecture version rather than silently editing the old one. An impact report identifies changed objectives and dependencies, realization plans needing review, affected lessons/questions/sources, learner progress whose interpretation may change, and newly uncovered gaps. Installed packs remain immutable until reviewed replacements are approved.

## Versioning

Learning architectures and realization plans have stable identities and explicit versions. A realization references exactly one architecture version. A revision is immutable once approved; a changed architecture receives a new version and approval status.

The intended lifecycle is:

```text
draft → reviewed → approved → superseded
```

This lifecycle is a design target, not a new implemented state machine. Historical architectures remain available to explain installed packs and learner evidence.

## Curriculum impact report

A proposed architecture revision generates a human-reviewable impact report identifying:

- objectives added, removed, renamed, split, merged, or materially changed;
- dependency additions, removals, category changes, or changed justifications;
- lessons and bridge material affected;
- questions and assessments requiring review;
- sources requiring freshness or claim revalidation;
- learner progress potentially affected and why;
- newly created content or assessment gaps;
- realization plans that no longer satisfy their declared scope;
- whether existing installed packs remain structurally and editorially valid.

The report does not automatically migrate content or learner progress. Installed pack bytes and historical attempts remain immutable. A later implementation must define how maintainers acknowledge impacts and when a new pack version is required.

## Smallest future metadata

The minimum logical metadata likely needed later is:

- architecture ID, version, target ID/version, status, and approval reference;
- stable objective IDs and objective versions;
- dependency edges with category, rationale, and satisfaction criterion;
- required/optional classification, depth, and completion criterion;
- blueprint mappings and evidence/freshness policy references;
- realization-plan ID/version and referenced architecture version;
- selected, bridged, omitted, and deferred objective IDs with reasons;
- impact-report source and target versions plus categorized affected IDs.

These are requirements for later design, not new pack fields. Serialization, schemas, storage location, signatures, migration rules, and tool contracts remain unresolved.

## Deterministic and agent responsibilities

The agent may research, explain, propose mappings, and negotiate scope. Future deterministic code should validate identities, version references, dependency integrity, completeness claims, and impact-report coverage. Humans approve architecture, realization scope, material curriculum revisions, and content activation. SQLite learner state and pack bytes remain authoritative within their existing boundaries.

## Boundaries

This design adds no mastery algorithm, scheduler, learner-model inference, database schema, pack field, tool, or Hermes behavior. It defines the planning model needed before those implementation choices can be responsibly made.
