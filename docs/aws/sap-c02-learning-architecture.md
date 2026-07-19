# SAP-C02 Complete High-Level Learning Architecture

Status: accepted 0.3A structural baseline

Architecture ID: `aws-sap-c02-learning-architecture`

Version: `0.3A.1`

Target: current SAP-C02 at research cutoff 2026-07-18

Assessment blueprint: [`aws-sap-c02-assessment-blueprint` version `0.3A.1`](sap-c02-assessment-blueprint.md)

## Outcome and non-claims

Outcome: the learner can evaluate complex AWS requirements and justify secure, reliable, performant, cost-conscious, operable, and migration-aware architectures across the full current SAP-C02 task outline. The target is professional architectural judgment, not memorization of a service catalog. The official guide validates advanced design skills aligned to the AWS Well-Architected Framework. [Current exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

This architecture is complete in coverage and dependency structure. It is not a lesson set, claim bank, question bank, exam simulation, readiness score, or passing-probability model. Completion does not guarantee an AWS result.

## Depth vocabulary

- **Required / professional judgment:** independently select or critique an architecture from a multi-constraint scenario and justify tradeoffs.
- **Required / working detail:** know behavior and boundaries well enough to eliminate plausible alternatives and trace consequences.
- **Bridge:** concise prerequisite sufficient for a selected objective, with a completion check.
- **Optional enrichment:** useful hands-on or implementation depth beyond the exam-guide competency; never required for architecture completion unless a realization explicitly adds it.

## Competency areas and coverage

The official task statements define the assessment-traceable competency areas. Each area has one high-level demonstrated-competency objective below; supporting service knowledge is evidence for the competency, not a separate objective merely because a service is named.

| Domain | Competency areas | Objective mapping |
|---|---|---|
| Cross-domain foundations | requirements/tradeoff analysis; architecture boundary and dependency tracing | SAP-FND-01..02 |
| Domain 1 — organizational complexity | organization-scale networking; security controls; resilience; multi-account governance; cost governance/visibility | SAP-ORG-01..05 / tasks 1.1..1.5 |
| Domain 2 — new solutions | deployment/change; continuity; security; reliability; performance; cost optimization | SAP-NEW-01..06 / tasks 2.1..2.6 |
| Domain 3 — existing solutions | operational excellence; security improvement; performance improvement; reliability improvement; cost improvement | SAP-IMP-01..05 / tasks 3.1..3.5 |
| Domain 4 — migration/modernization | portfolio assessment; migration method; target architecture; modernization opportunities | SAP-MIG-01..04 / tasks 4.1..4.4 |
| Optional freshness watch | emerging responsible-AI/security controls identified for possible unscored pretest use | SAP-EMG-01 |

This grouping covers all 20 scored task statements from the current official guide. The optional freshness watch does not create a fifth scored domain. [Current exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Competency architecture

Each official task is covered by at least one demonstrated-competency objective. Official task knowledge/skill details remain authoritative and are not exhaustively copied here.

### Foundations shared across domains

| Objective | Demonstrated competency | Depth | Assessment intent | Completion evidence |
|---|---|---|---|---|
| SAP-FND-01 | Extract functional and nonfunctional requirements, rank explicit constraints, expose assumptions, and justify a decision across relevant Well-Architected pillars | Required / professional judgment | Make a unique-best choice without hidden assumptions | Two reviewed architecture decision records plus scenario assessment |
| SAP-FND-02 | Trace identity, network, data, dependency, failure, operational-ownership, account, and Region boundaries through an architecture | Required / working detail | Diagnose cross-boundary consequences | Annotated text architecture and failure/ownership trace |

The six current Well-Architected pillars are operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Sustainability is a cross-cutting design lens, not a separately weighted SAP-C02 domain. [Well-Architected pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) [Current exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

### Domain 1 — Design Solutions for Organizational Complexity (26%)

| Objective | Task | Demonstrated competency | Depth | Completion evidence |
|---|---|---|---|---|
| SAP-ORG-01 | 1.1 | Evaluate multi-VPC, hybrid, DNS, segmentation, endpoint, Region/AZ, latency, and traffic-observability requirements to select and troubleshoot connectivity strategies | Professional judgment | Comparative design plus traffic-flow diagnosis |
| SAP-ORG-02 | 1.2 | Prescribe cross-account identity, federation, least privilege, network controls, encryption, certificate, audit, detection, and centralized security controls | Professional judgment | Security-control matrix plus scenario assessment |
| SAP-ORG-03 | 1.3 | Design recovery, backup, scaling, and automatic-recovery architectures from RTO, RPO, failure-domain, and business-continuity requirements | Professional judgment | DR decision record plus failure-mode assessment |
| SAP-ORG-04 | 1.4 | Design a multi-account environment with justified account/OU boundaries, governance controls, workforce access, resource sharing, central logging, event notification, and delegated administration | Professional judgment | Multi-account decision record plus five-scenario opportunity in pilot |
| SAP-ORG-05 | 1.5 | Design organization-scale cost allocation, visibility, guardrails, purchasing, and rightsizing strategies while preserving required performance and ownership | Professional judgment | Cost-governance design plus tradeoff assessment |

Official task scope: [Domain 1](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html).

### Domain 2 — Design for New Solutions (29%)

| Objective | Task | Demonstrated competency | Depth | Completion evidence |
|---|---|---|---|---|
| SAP-NEW-01 | 2.1 | Select deployment, IaC, configuration, change, rollback, and managed-service strategies that meet business and operational requirements | Professional judgment | Deployment decision record and failure-safe rollout assessment |
| SAP-NEW-02 | 2.2 | Design business continuity across AZs/Regions using explicit RTO/RPO, replication, routing, backup, monitoring, recovery, and test requirements | Professional judgment | Continuity plan and recovery scenario |
| SAP-NEW-03 | 2.3 | Select least-privilege identity, network, endpoint, credential, encryption, patch, web-protection, detection, and compliance controls for a new solution | Professional judgment | Threat/control mapping and scenario assessment |
| SAP-NEW-04 | 2.4 | Design for availability, elasticity, loose coupling, quotas, managed recovery, data replication, and appropriate DNS routing | Professional judgment | Reliability design and failure-injection thought exercise |
| SAP-NEW-05 | 2.5 | Select compute, storage, database, caching, buffering, replica, and elasticity patterns from workload access patterns and measurable performance objectives | Professional judgment | Performance decision record and bottleneck scenario |
| SAP-NEW-06 | 2.6 | Model and optimize infrastructure, storage tiering, data transfer, pricing, rightsizing, and expenditure controls without violating solution goals | Professional judgment | Cost model and constraint-based selection |

Official task scope: [Domain 2](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain2.html).

### Domain 3 — Continuous Improvement for Existing Solutions (25%)

| Objective | Task | Demonstrated competency | Depth | Completion evidence |
|---|---|---|---|---|
| SAP-IMP-01 | 3.1 | Evaluate an existing solution's logging, monitoring, deployment, configuration, automation, remediation, and recovery exercises and prioritize operational improvements | Professional judgment | Prioritized improvement plan and operations scenario |
| SAP-IMP-02 | 3.2 | Audit and improve secrets, least privilege, traceability, layered security, vulnerability response, patching, backup, retention, and remediation | Professional judgment | Security gap analysis and scenario assessment |
| SAP-IMP-03 | 3.3 | Translate business goals into metrics, find bottlenecks, test remediation, rightsize, and justify global/managed-service performance improvements | Professional judgment | Metric-to-remediation analysis and scenario |
| SAP-IMP-04 | 3.4 | Identify single points of failure, quota/scaling risks, replication gaps, and inadequate recovery behavior; prioritize reliability remediation | Professional judgment | Reliability review and remediation scenario |
| SAP-IMP-05 | 3.5 | Analyze usage, unused/overused resources, pricing commitments, transfer charges, allocation, alarms, and granular cost data to prioritize savings | Professional judgment | Cost-review findings and scenario assessment |

Official task scope: [Domain 3](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain3.html).

### Domain 4 — Accelerate Workload Migration and Modernization (20%)

| Objective | Task | Demonstrated competency | Depth | Completion evidence |
|---|---|---|---|---|
| SAP-MIG-01 | 4.1 | Assess a portfolio, apply the 7Rs, compare TCO and constraints, prioritize workloads, and construct a defensible migration-wave sequence | Professional judgment | Portfolio disposition and wave-plan assessment |
| SAP-MIG-02 | 4.2 | Select application, database, data-transfer, connectivity, DNS, identity, security, and governance migration mechanisms from volume, downtime, change, and risk constraints | Professional judgment | Migration-method decision record and scenario |
| SAP-MIG-03 | 4.3 | Select target compute, container, storage, and database platforms for an existing workload from compatibility, performance, resilience, cost, and operational requirements | Professional judgment | Target-platform comparison and scenario |
| SAP-MIG-04 | 4.4 | Identify and justify decoupling, serverless, container, purpose-built database, storage, and integration modernization opportunities without exceeding change tolerance | Professional judgment | Modernization roadmap and scenario assessment |

Official task scope: [Domain 4](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain4.html).

### Emerging, unscored monitoring objective

| Objective | Status | Demonstrated competency | Completion effect |
|---|---|---|---|
| SAP-EMG-01 | Optional freshness watch | Recognize current documented patterns for content/regulatory controls, agentic access control, and human approval workflows | Does not count toward scored-domain completion; reassess when the guide changes |

The current guide describes this as possible unscored pretest content. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Required versus optional learning depth

Required content covers the 22 required objectives above: both foundations and all 20 official tasks. Service-by-service console procedures, exhaustive API flags, memorized quotas without scenario relevance, production implementation, and every service in the non-exhaustive in-scope appendix are optional enrichment. A service becomes required only to the depth needed to satisfy a mapped objective and approved claim set.

Hands-on work is strongly useful but not an architectural completion requirement for this research-only plan. No official SAP-C02 lab component is described on the current exam page or guide; the assessment formats are multiple choice/multiple response. [Certification page](https://aws.amazon.com/certification/certified-solutions-architect-professional/) [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Assessment strategy

- Objective checks: short original scenarios and architecture critiques, with explicit requirements and rationales.
- Cluster checks: cross-domain scenarios that combine a primary objective with named supporting prerequisites.
- Completion opportunity: each required objective receives at least one successful human-reviewed assessment opportunity; high-risk or repeatedly missed objectives receive more than one in a realization.
- Evidence: approved claims and citations must precede authored questions; no final questions exist in 0.3A.
- Blueprint alignment: option/constraint/distractor design follows [the assessment blueprint](sap-c02-assessment-blueprint.md), with medium-confidence style limitations visible.

## Completion model without mastery scoring

An architecture realization may be called complete for its declared scope only when:

1. every selected required objective has reviewed learning coverage and at least one successful assessment opportunity;
2. all blocking prerequisites are included or satisfied by approved evidence/diagnostic;
3. bridge prerequisites have their own completion check;
4. skipped required objectives and temporary waivers remain visible;
5. no material claim is unreviewed, unsupported, or past its freshness horizon;
6. no question awaits uniqueness review;
7. the completion statement names the realized scope and does not imply full certification preparation for a partial plan.

Temporary waivers prevent an unqualified full-completion claim. Stale or unreviewed claims qualify or suspend the affected objective's completion. This model defines evidence conditions, not a readiness score or predicted pass likelihood.

## Evidence and freshness policy

| Evidence class | Preferred source | Freshness expectation |
|---|---|---|
| Exam identity, domains, response rules | Current AWS certification page and guide | Check at planning, before question approval, and before release |
| Service behavior/limitations | Current AWS user/developer/API guide or service FAQ | Check at claim approval and when the page/revision/service changes |
| Architectural recommendation | Well-Architected, decision guide, prescriptive guidance, Architecture Center plus service facts | Revalidate premises at question approval; record that it is derived guidance |
| Price, quota, Region availability, deprecation | Current pricing, quotas, regional-services, and announcement pages | Treat as time/region-sensitive; verify immediately before approval/release |
| Scenario assumption | Explicit project-authored statement | Stable only within that scenario; no external truth claim unless cited |

The source register stores retrieval dates and optional digests. A changing live page never silently rewrites an approved claim; it triggers review and an impact record.

## Sequence and alternate paths

Recommended full sequence:

1. SAP-FND-01 and SAP-FND-02.
2. Organization-scale boundary competencies: SAP-ORG-01, -02, -04, then -03 and -05.
3. New-solution design: SAP-NEW-01 through -06, ordered locally by dependencies rather than guide number alone.
4. Existing-solution improvement: SAP-IMP-01 through -05, using the corresponding new-design competencies as context.
5. Migration: SAP-MIG-01, -02, -03, -04, bringing network/security/governance/reliability/cost bridges forward as needed.
6. Cross-domain synthesis and optional SAP-EMG-01 freshness review.

Experienced architects may start with diagnostics and preserve only failed or unsupported prerequisites. Migration-focused learners may start at SAP-MIG-01 if foundation, network, identity/security, data, and governance prerequisites are evidenced or bridged. See [realization plans](sap-c02-realization-plans.md).

## Gaps and uncertainty

- No lessons, complete claims, or learner-ready questions are authored.
- Objective IDs and versions are standalone 0.3A design identities, not pack fields or database records.
- Reviewer qualifications, diagnostic thresholds, and serialization remain proposals for later approval.
- Style/difficulty confidence remains medium until a qualified reviewer optionally inspects current authorized Skill Builder examples without copying them.
- The HTML/PDF guide revision mismatch requires a freshness check at every later approval stage.
