# SAP-C02 Subject Builder Automation Gap Analysis

Status: accepted 0.3A automation-gap record; no implementation authorized

Research date: 2026-07-18

Workflow target: future runtime-independent Subject Builder

## Purpose and boundary

This document records how the SAP-C02 0.3A research and architecture exercise was performed manually, what a future Subject Builder could automate, and where human authority must remain. It is an automation design input, not a tool contract, database decision, pack schema, or implementation authorization.

The future workflow must retain whole-architecture progressive realization from [ADR 0010](../decisions/0010-whole-learning-architecture-progressive-realization.md), assessment and reuse controls from [ADR 0011](../decisions/0011-assessment-authenticity-official-question-reuse.md), capability lifecycle and permissions from [ADR 0012](../decisions/0012-capability-discovery-controlled-activation.md), and evidence-backed layered approval from [ADR 0013](../decisions/0013-evidence-backed-authored-questions-layered-approval.md).

## Classification vocabulary

- **Deterministic and automatable:** parsing, hashing, validation, comparison, or graph checks with explicit rules.
- **Model-assisted with deterministic validation:** synthesis or classification may use a model, but required fields, citations, graph integrity, and policy constraints can be checked mechanically.
- **Requires human approval:** rights, pedagogy, architectural judgment, answer uniqueness, or activation cannot be delegated to the drafting model.
- **Requires external capability:** needs a browser, documentation endpoint, local PDF processor, or another controlled integration.
- **Unresolved:** the correct automation boundary or authoritative policy is not yet established.

One step may have more than one classification.

## Manual 0.3A workflow and automation boundary

| Step performed | Manual 0.3A activity and output | Classification | Future deterministic checks | Required human authority or unresolved point |
|---|---|---|---|---|
| 1. Establish governing context | Read product principles, current status, accepted ADRs, project context, roadmap, pilot plan, and design handoffs before research | Deterministic and automatable | Required-document presence; accepted-ADR precedence; implementation-gate state | Human resolves genuinely conflicting current requirements |
| 2. Discover target identity | Located current official certification page, guide, guide PDF, and transition history; searched for replacement, beta, retirement, and revised-guide notices | Requires external capability; model-assisted with deterministic validation | Required identity fields; official-domain allowlist; exact-date normalization; conflict detection | Human approves target when official signals conflict or transition timing is ambiguous |
| 3. Retrieve and fingerprint sources | Read official HTML; temporarily downloaded two official PDFs; captured headers, byte counts, and SHA-256 digests; retained no repository snapshot | Requires external capability; deterministic and automatable | URL fetch, content type, retrieval time, digest, snapshot flag, safe storage policy | Human approves retention of copyrighted or licensed copies |
| 4. Register sources | Assigned stable IDs and recorded title, publisher, URL, dates, category, use, authority, rights, snapshot state, and limitations | Model-assisted with deterministic validation | Required fields; unique IDs; URL/digest format; category vocabulary; citation reachability | Human approves authority tier for contested sources |
| 5. Classify source authority | Separated official, licensed/openly reusable, public descriptive, and excluded categories | Model-assisted with deterministic validation; requires human approval | Provider/domain evidence; suspicious-source indicators; excluded-source quarantine | Human confirms borderline provenance and exceptions |
| 6. Classify rights and reuse | Read AWS terms and document-license boundary; classified exam PDFs as analysis-only pending a specific grant | Requires human approval; model-assisted | Fail-closed default; license field; reuse/action compatibility; attribution requirements | Legal or authorized human review resolves unclear grants; drafting model never upgrades its own rights classification |
| 7. Analyze assessment style | Counted official sample formats and selection behavior; summarized scenario, option, command, distractor, exhibit, and cross-domain patterns without copying text | Model-assisted with deterministic validation; requires external capability | Sample counts; selection-count extraction; quotation/similarity limits; evidence-versus-inference labels | Qualified human reviews whether the evidence supports generalization and whether style synthesis is independent |
| 8. Assign confidence | Rated identity, coverage, formats, response rules, style, distractors, difficulty, and rights separately, with resolution paths for non-high ratings | Model-assisted with deterministic validation; requires human approval | Allowed ratings; rationale and resolution required below high; evidence links | Human accepts risk and decides whether additional evidence is sufficient |
| 9. Build assessment blueprint | Translated verified facts and bounded inferences into Markdown and JSON artifacts | Model-assisted with deterministic validation | JSON parse/schema profile; required fields; evidence IDs exist; prohibited categories present; Markdown/JSON consistency | Human approves blueprint for authoring use; no implicit pack-schema commitment |
| 10. Derive learning objectives | Mapped every official domain task to a demonstrable objective and added two cross-cutting foundations | Model-assisted with deterministic validation; requires human approval | Full task coverage; unique objective IDs; competency verbs; source traceability; no orphan task statements | AWS-qualified instructional architect approves granularity, scope, and assessment intent |
| 11. Map dependencies | Classified blocking, bridge, recommended-context, and independent edges across domains | Model-assisted with deterministic validation; requires human approval | Endpoint existence; allowed edge types; cycle detection; blocking-prerequisite disposition | Human judges whether a bridge is sufficient and whether a dependency is genuinely blocking |
| 12. Define completion/freshness | Specified architectural completion evidence, waiver visibility, stale-claim handling, and confidence limits without scoring | Model-assisted with deterministic validation; requires human approval | Required-objective coverage; unresolved waiver/gap visibility; source freshness status | Human approves completion claims; no readiness probability generated |
| 13. Produce realization plans | Created full, one-domain, experienced, time-boxed, and learner-focus plans against the full architecture | Model-assisted with deterministic validation | Requested-scope mapping; prerequisite closure; gap list; bridge and waiver records; objective coverage diff | Human/learner chooses risk tolerance and accepts explicit omissions |
| 14. Discover capabilities | Verified official AWS and Hermes capability documentation; recorded lifecycle state, permissions, side effects, auth, cost, installation, health check, fallback, and disable path | Requires external capability; model-assisted with deterministic validation | Required candidate fields; permission ceiling; lifecycle transition rules; no configured/healthy claim without test evidence | User approves installation, credentials, account access, and any Level 1+ transition |
| 15. Select 0.3B pilot | Compared architecture slices and selected task 1.4 for professional judgment, narrowness, source depth, and account-free review | Model-assisted with deterministic validation; requires human approval | Pilot size limits; prerequisite closure; source diversity; exactly five spec slots; prohibited implementation checks | User approves the selected slice; qualified reviewer approves educational viability |
| 16. Design question specifications | Defined five original scenario-design records with requirements, constraints, comparisons, distractor classes, evidence needs, risks, and review concerns, but no learner-ready text | Model-assisted with deterministic validation; requires human approval | Required fields; blueprint linkage; objective linkage; no final stem/options/key; planned response mix and selection count | Human approves claims, originality, fairness, and eventual answer uniqueness |
| 17. Record reproducibility | Recorded dates, strategy, sources, exclusions, digests, access limits, rights uncertainty, and capabilities actually used | Deterministic and automatable | Audit completeness; digest verification; environment/credential redaction; snapshot-policy compliance | Human approves any private or licensed evidence retention |

## Candidate future operations

These are conceptual operations. Names are illustrative and do not authorize CLI, MCP, API, database, or pack changes.

| Candidate operation | Input | Output | Automation posture |
|---|---|---|---|
| Establish research project | target description, governing decisions, date | research scope and gate state | Deterministic setup plus human confirmation |
| Resolve assessment identity | official candidate sources | versioned identity candidates, conflicts, transition dates | Model-assisted discovery; deterministic comparison; human selection on conflict |
| Register source candidate | URL/file and intended use | normalized source candidate | Deterministic extraction with model-assisted category proposal |
| Fingerprint source | bytes or retained snapshot | digest, size, retrieval metadata | Deterministic |
| Classify source and rights | source candidate and terms evidence | authority/reuse proposal and uncertainty | Model-assisted; mandatory human approval for reuse |
| Extract assessment evidence | approved style sources | observations with locators and inference flags | Model-assisted; deterministic locator and copying-limit checks |
| Construct blueprint | approved evidence | reviewable blueprint candidate | Model-assisted; deterministic structural validation; human approval |
| Construct curriculum architecture | guide tasks and approved references | objectives, coverage map, completion/freshness rules | Model-assisted; deterministic coverage checks; human approval |
| Propose dependency edge | objectives and rationale | typed edge candidate | Model-assisted; deterministic graph checks; human approval for blocking edges |
| Realize requested scope | full architecture, learner goal, prior evidence | plan, bridges, waivers, gaps, risks | Model-assisted; deterministic prerequisite closure and gap reporting |
| Discover capability | role and provider evidence | capability candidate | Model-assisted; deterministic permission/lifecycle validation |
| Draft claim | approved source and objective | source-bound claim candidate | Model-assisted; deterministic locator/freshness checks; human approval |
| Draft question specification | blueprint, objective, approved claim categories | non-learner-ready design record | Model-assisted; deterministic field/policy checks; human approval |
| Request review | immutable candidate and evidence bundle | decision, reviewer identity, reasons, conditions | Human action; deterministic audit record |
| Invalidate approvals | changed source, claim, blueprint, or content | impact set and invalidated decision states | Deterministic dependency traversal; human reapproval |

## Candidate artifact ownership and lifecycle

Serialization and persistence remain open. Not every artifact belongs in SQLite or in a distributable subject pack.

| Artifact | Proposed owner | Lifecycle | Distribution posture |
|---|---|---|---|
| Assessment research project | Subject Builder workspace | create → research → review → close/archive | Authoring-only |
| Source candidate/register entry | Evidence subsystem | discovered → classified → approved/rejected → stale/superseded | Pack receives only allowed citation metadata if needed |
| Source snapshot/digest | Evidence subsystem or approved external archive | temporary/retained → verified → expired/replaced | Snapshot never bundled unless rights and need are explicit |
| Rights decision | Human governance record | proposed → approved → revisited on terms/use change | Relevant notice may be exported; review record remains authoring-side |
| Capability candidate | Capability registry | discovered → recommended → approved → configured → healthy/unavailable/revoked | Never pack content |
| Assessment blueprint | Assessment-design workspace | draft → human-reviewed → approved → superseded | May inform pack production; format not fixed here |
| Curriculum architecture | Curriculum-design workspace | draft → reviewed → approved → revised | Subject-wide authoring artifact; a realization may reference a version |
| Dependency graph | Curriculum-design workspace | draft → validated → reviewed → revised | May be projected into planning metadata later; no schema commitment |
| Realization plan | Learner/build planning workspace | proposed → accepted → executed/revised → completed/abandoned | Context-specific; not automatically part of the canonical pack |
| Claim draft | Evidence-backed content workspace | draft → validation → human approval → stale/invalidated | Only approved claims may support released content |
| Question design specification | Assessment-authoring workspace | draft → review → approved for authoring → superseded | Authoring-only unless a later decision says otherwise |
| Human review request/decision | Governance/audit record | requested → decided/returned → invalidated if dependencies change | Do not expose private reviewer notes in pack exports |

Before implementation, a separate design should decide canonical identifiers, concurrency, immutability, audit retention, privacy, export boundaries, and whether each record is a file, service record, database object, or derived view.

## Approval and invalidation graph

The minimum authority flow is:

```text
source evidence + rights decision
  → source approval
  → claim drafts + deterministic checks
  → human claim approval
  → question specification/draft + blueprint checks
  → human question approval
  → immutable release candidate checks
  → separate human pack-release approval
```

The authoring model may propose at every drafting stage but may approve none of them. A changed source, changed material claim, changed key/rationale, changed blueprint constraint, or changed rights basis invalidates downstream approval. Deterministic tooling should compute the affected set; a human decides whether re-review is sufficient.

## Failure and guided fallback behavior

| Failure state | Required behavior | Guided choices and recommendation |
|---|---|---|
| No official guide exists | Stop target-specific blueprint and full-coverage claims; preserve discovery evidence | Recommend (1) wait for an official guide, or (2) create a clearly labeled exploratory architecture from official role/outcome material. Do not present option 2 as exam-complete |
| Assessment version uncertain | Surface all candidate versions and exact effective/retirement dates; do not silently pick | Recommend the version currently bookable on the official exam page; require human choice when transition windows overlap |
| Official examples absent | Keep format facts from the guide; reduce style/distractor/difficulty confidence | Recommend a conservative blueprint plus later authorized first-party practice review; do not fill gaps with dumps |
| Only questionable sources found | Quarantine and record indicators without ingesting protected question text | Recommend stopping style research and proceeding only with supported identity/coverage facts, or waiting for approved evidence |
| Rights are unclear | Default to analysis-only and block verbatim/attributed reuse | Recommend original writing based on approved factual sources; route any reuse request to authorized rights review |
| Authoritative sources conflict | Preserve both claims, dates, URLs, and scope; mark conflict | Recommend the more specific/current controlling source only when its precedence is explicit; otherwise require human resolution |
| MCP server unavailable | Mark unavailable, retain the role, and invoke documented fallback | Recommend official web/document retrieval and local digest tooling; research must not depend on one MCP server |
| User declines a recommended capability | Do not configure it or repeatedly demand credentials | Recommend the least-privileged fallback and state the resulting time/confidence limitation; continue when the limitation is acceptable |
| Learner requests incoherent partial scope | Map the request to the full graph and show missing prerequisites | Recommend the smallest coherent realization with short bridges; offer explicit prior-learning diagnostic or visible waiver instead of silently expanding scope |
| Claim cannot be validated | Keep it out of the approved claim set and downstream questions | Recommend revising/removing the claim or obtaining a stronger official source; never convert uncertainty into scenario fact |
| No answer is uniquely best | Block question approval | Recommend making the prioritizing criterion explicit, revising options, or discarding the item; never rely on an unstated assumption |
| Content freshness cannot be established | Mark affected claim stale/unknown and block activation when material | Recommend re-retrieval from an authoritative source; if impossible, remove the time-sensitive dependency or defer the content |

The interface should present bounded choices, the recommended option, consequences, and a default-safe result. It should not ask a blank-ended question when the evidence supports a finite decision set.

## Validation capabilities needed before implementation

The future Subject Builder needs deterministic validators for at least:

1. required source metadata, stable IDs, URLs, dates, digests, and citation locators;
2. allowed authority, rights, confidence, dependency, permission, and lifecycle vocabularies;
3. blueprint evidence-reference integrity and Markdown/structured-artifact consistency;
4. objective-to-task coverage, dependency endpoint integrity, cycle reporting, and prerequisite disposition;
5. realization coverage/gap/waiver visibility;
6. claim-to-source locator and freshness status;
7. question-specification completeness, selection-count consistency, objective/claim/blueprint links, and stored distractor rationales;
8. separation of drafting identity from approving identity;
9. downstream approval invalidation when governed inputs change;
10. exclusion of credentials, private notes, runtime state, unapproved snapshots, and authoring-only records from exports.

Similarity detection may assist reviewers, but a numeric threshold should not be treated as proof of originality. The unresolved design need is a review protocol that combines source-aware comparison, protected-expression risk, and qualified human judgment.

## Capability boundary learned in 0.3A

Public official web retrieval and local file hashing were sufficient for 0.3A. No AWS account, AWS credential, MCP server, paid practice content, lab, or external mutation was needed. The candidate capability lifecycle and safe setup sequence are recorded in [the capability report](sap-c02-capability-report.md). A future implementation must not infer `configured` or `healthy` from documentation discovery alone.

## Recommended next design decision

Before Subject Builder implementation, approve a narrow operation/artifact contract for **source registration → source/rights review → blueprint candidate → human blueprint approval**, including approval identity and invalidation semantics. This is the smallest useful automation spine and does not require deciding pack serialization, SQLite ownership, or AWS-account integration.
