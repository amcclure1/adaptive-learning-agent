# AWS SAP-C02 Pilot Plan

Status: 0.3A research/design complete and pending human acceptance; no 0.3B content or capability setup authorized
Updated: 2026-07-19

## Purpose

The SAP-C02 line tests whether the project can research a current, changing certification target, design a coherent curriculum, and author original evidence-backed scenario questions without copying protected exam material. It is split into three separately reviewed stages so architecture, manual content quality, and agent assistance are not conflated.

The 2026-07-18 0.3A exercise verified the current target and recorded the assessment guide, domains, task statements, policies, sample evidence, rights boundary, architecture, and proposed pilot from authoritative sources. It did not rely on the historical `SAP-C02` label in this plan. See [the assessment research](aws/sap-c02-assessment-research.md), [source register](aws/sap-c02-source-register.md), and [rights analysis](aws/sap-c02-rights-and-reuse.md).

## 0.3A — Research and curriculum architecture

Status: complete as a manual research/design exercise; human approval remains an exit gate.

Deliver design and review artifacts, not a full AWS pack:

- automatic assessment research and evidence inventory;
- source tier, allowed-use, rights, and freshness classifications;
- assessment identity/version and human-reviewable assessment blueprint;
- full learning architecture for the stated SAP-C02 outcome;
- objective dependencies, depth, completion criteria, and blueprint mappings;
- evidence gaps, confidence, and guided fallback;
- capability-role discovery and least-privileged proposals;
- one or more candidate realization plans;
- curriculum version and impact-report design evidence.

0.3A exit requires human approval of the research baseline, blueprint, whole architecture, and a bounded 0.3B realization. It does not require a full pack, MCP installation, AWS account, private environment access, generated questions, or a generalized builder implementation.

### 0.3A result

- Verified target: **AWS Certified Solutions Architect - Professional (`SAP-C02`)**.
- Guide baseline: current AWS HTML guide plus official PDF version 1.2, whose retained HTTP metadata reports revision on 2025-02-19; the HTML guide's emerging topics are possible unscored content only.
- Blueprint confidence: medium overall, with high identity/domain/format/response-rule confidence and bounded uncertainty for universal style, distractors, difficulty, and reuse rights.
- Whole architecture: 22 required objectives (two cross-cutting foundations plus all 20 official task statements), with optional emerging-topic awareness outside scored coverage.
- Proposed 0.3B realization: Domain 1 task 1.4 / `SAP-ORG-04`, design a multi-account AWS environment.
- Capability result: public official web retrieval was sufficient; official AWS Knowledge MCP or AWS Documentation MCP is recommended only as optional Level 0 research assistance for a later approved task.

Artifacts are indexed in [the 0.3A handoff](handoffs/aws-sap-c02-0.3a-research-and-architecture.md).

## 0.3B — Manually reviewed SAP-C02 pilot

Status: proposed; not authorized.

Subject to human approval, select current Domain 1 task 1.4 / `SAP-ORG-04` from the 0.3A architecture. The proposed envelope is two original lessons, approximately 24-30 approved claims, and exactly five future original scenario questions: three single-response and two multiple-response. Build a deliberately small realization containing:

- a bounded set of authoritative factual claims;
- original cited lessons;
- exactly five original scenario questions;
- explicit material scenario constraints;
- keyed-answer rationales;
- a documented failure reason for every distractor;
- authoritative AWS citations for material factual claims;
- human claim approval;
- qualified human question and answer-uniqueness approval;
- human pack-release approval.

The five questions are project-authored and must never be labeled official, recalled, actual, or representative of exact live questions. Official examples may inform the approved blueprint only within their allowed use and rights. No unstated assumption may be required to make a keyed answer win.

0.3B is manual-first: the project proves review quality and artifact boundaries before generalizing automation. Selection, scoring, attempts, and learner state remain deterministic.

The five non-learner-ready design specifications and explicit non-goals are in [the pilot proposal](aws/sap-c02-0.3b-pilot-proposal.md).

## 0.3C — Agent-assisted construction

After 0.3B demonstrates a reviewable manual chain, add a conversational authoring workflow that can:

1. research sources and assessment evidence;
2. propose an assessment blueprint;
3. propose a whole curriculum architecture;
4. negotiate a realization plan and bridges;
5. recommend optional capabilities and permissions;
6. draft claims, lessons, scenarios, answers, and rationales;
7. run deterministic structural validation;
8. produce impact and review queues;
9. require human approval at claim, question, and pack-release layers;
10. activate only approved immutable content.

0.3C is not autonomous publishing. The agent cannot approve its own artifacts, install capabilities silently, or use memory as evidence or state.

## Assessment authenticity

The pilot follows [Assessment Research and Authenticity Policy](assessment-research-policy.md): use reusable official questions only when rights permit; otherwise use permissible evidence to learn assessment grammar and author original sentences and scenarios. Dumps, recalled questions, leaked keys, unauthorized commercial banks, and suspicious derivatives are excluded.

The blueprint should capture scenario density, constraints, cognitive depth, option plausibility, terminology, command language, exhibits/labs, and known uncertainty. It should not retain protected examples merely to run similarity checks.

## Curriculum and guided scope

The approved 0.3A learning architecture covers the complete declared outcome even though 0.3B realizes only one slice. The selected slice must identify blocking prerequisites, bridge prerequisites, recommended context, and independent objectives. The plan states which overall SAP-C02 coverage remains absent and must not imply complete preparation.

If the official guide changes, a new architecture version and impact report identify affected objectives, dependencies, claims, lessons, questions, sources, learner evidence, and content gaps. Installed pack versions remain immutable pending review.

## Evidence-backed question quality

For each 0.3B question, reviewers should be able to trace:

```text
objective → approved claims → explicit constraints → candidates
→ keyed rationale + distractor rationales → citations → approvals
```

Derived architectural recommendations must expose factual premises, tradeoffs, and applicability. Source authority alone does not prove that the recommendation is unique. Qualified human review remains necessary.

## Optional capabilities

Public AWS documentation search may be sufficient for 0.3A and may not require an AWS account. A future AWS documentation/knowledge MCP or connector can be proposed only after current official-provider and Hermes compatibility verification. Private environment inspection requires scoped Level 1 approval. Lab creation or mutation requires Level 2 or Level 3 approval, cost boundaries, and teardown instructions.

No AWS MCP, account, cloud access, lab, or external capability is required by this architecture or installed by this task. Declining a capability yields a narrower/manual fallback rather than loss of core operation.

## Implementation prerequisites and unresolved decisions

- Obtain human acceptance of the 0.3A identity/source baseline, medium-confidence blueprint, complete architecture, and selected task 1.4 realization.
- Decide the standalone serialization of blueprint, curriculum, realization, claims, rationales, and layered reviews.
- Define reviewer qualifications for factual claims, architectural recommendations, and answer uniqueness.
- Define originality/similarity review without retaining unsafe material.
- Decide how freshness changes invalidate claims, questions, and approvals.
- Decide the minimum deterministic validation and whether a new pack format/tool contract is required.
- Confirm or revise the proposed two-lesson, 24-30-claim, five-question 0.3B envelope after 0.3A evidence is approved.
- Explicitly authorize every implementation, content, capability, and private-access task separately.

## Persistent non-goals

No exam dumps, recalled live questions, exact exam simulation, passing prediction, autonomous approval, generalized automatic subject creation in 0.3B, mandatory cloud account, production mutation, web application, hosted multi-user service, or runtime-specific learning core.
