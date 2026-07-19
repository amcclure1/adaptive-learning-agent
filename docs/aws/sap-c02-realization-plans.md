# SAP-C02 Progressive Realization Plans

Status: 0.3A planning examples; human approval required

Architecture: `aws-sap-c02-learning-architecture` version `0.3A.1`

All plans preserve the complete architecture while selecting a smaller build/study scope. “Deferred” means not in this realization; it never means not required for the full certification outcome.

## A. Full certification preparation

**Recommendation:** preferred when the learner's stated goal is complete current SAP-C02 preparation and no strong prior evidence is available.

- **Selected objectives:** SAP-FND-01/02; SAP-ORG-01..05; SAP-NEW-01..06; SAP-IMP-01..05; SAP-MIG-01..04. SAP-EMG-01 is optional freshness context.
- **Sequence:** foundations; organization-scale boundaries; new-solution patterns; corresponding improvement objectives; migration assessment/mechanisms/targets/modernization; cross-domain synthesis.
- **Prerequisites:** included normally. Existing evidence may replace content after objective-level review; blocking claims receive diagnostics.
- **Bridges:** used only for isolated gaps discovered after diagnostics, not as a substitute for broad missing foundations.
- **Deferred:** deep console procedures, exhaustive APIs, unrelated in-scope services, and production labs unless chosen as enrichment.
- **Coverage gaps:** none against the current four-domain/20-task outline after all selected objectives complete; emerging pretest content remains optional and explicitly non-scored. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)
- **Expected evidence:** reviewed lessons/claims for every objective, successful original scenario opportunities, cross-domain architecture critiques, current-source freshness checks, and resolved or visible waivers.
- **Assessment approach:** objective checks followed by domain-cluster and cross-domain scenarios matching the approved blueprint. Do not mirror the official 75-item exam or predict a score.
- **Risks:** breadth, service churn, fatigue, and false confidence if scenario review is replaced by recall quizzes.

## B. One-domain pilot

**Recommendation:** select **Domain 1 task 1.4, SAP-ORG-04 — design a multi-account AWS environment** for manually reviewed 0.3B.

- **Selected objectives:** SAP-ORG-04 plus bounded checks for SAP-FND-01 and SAP-FND-02.
- **Prerequisite handling:** SAP-FND-01/02 included as short bridges; the relevant subset of SAP-ORG-02 (policy evaluation, federation, centralized audit) supplied by bridge. SAP-ORG-01 and SAP-ORG-05 are recommended context and omitted unless a question makes network sharing or cost allocation material.
- **Bridge content:** requirements/account-boundary analysis; identity policy versus organizational guardrail; central evidence ownership and delegated administration.
- **Deferred:** other Domain 1 objectives and all Domains 2-4.
- **Coverage gaps:** 19 official task statements and most of Domain 1 remain unrealized. This is a task pilot, not complete Domain 1 or certification preparation.
- **Expected evidence:** approximately 24-30 approved claims across official Organizations, Control Tower, IAM Identity Center, CloudTrail, Config, Security Hub, RAM, multi-account guidance, and Well-Architected sources; exactly five original scenario questions after human review.
- **Assessment approach:** three single-response and two multiple-response design opportunities, each with explicit unique-best rationale.
- **Risks:** multi-account services evolve quickly; sample style confidence is medium; reviewer must distinguish SCP boundaries, IAM permissions, service delegation, and ownership precisely.
- **Why this pilot:** it is narrow but exercises professional governance judgment, several authoritative sources, meaningful security/operations/cost tradeoffs, plausible distractors, and cross-domain bridges without an AWS account.

## C. Experienced-architect gap remediation

**Recommendation:** preferred for a learner with current, substantial AWS design experience and reviewable evidence.

- **Selected objectives:** initially all 22 required objectives are candidates; the realization selects only those not satisfied by accepted evidence/diagnostic.
- **Prerequisite handling:** prior-learning assertions are recorded but not accepted for blocking edges until a diagnostic or evidence review. Recent architecture decisions, incident reviews, migration plans, and current credentials may support mappings but do not automatically cover every objective.
- **Bridges:** concise current-service/freshness updates for otherwise demonstrated competencies.
- **Deferred:** objectives supported by current evidence or successful diagnostics; each deferral records basis and date.
- **Coverage gaps:** none if every omitted required objective has accepted evidence/diagnostic; otherwise the gap remains visible.
- **Expected evidence:** objective mapping from work products with sensitive details removed, diagnostic decisions on unseen scenarios, and current-source checks for claims.
- **Assessment approach:** begin with cross-domain diagnostics; drill down only when a rationale is incomplete, factually stale, or constraint handling fails.
- **Risks:** over-crediting job title/certification, evidence confidentiality, stale habits, and diagnostics that accidentally test recall rather than judgment.
- **Completion boundary:** complete preparation coverage may be claimed only when every required objective is included or validly evidenced/diagnosed and no blocking waiver remains.

## D. Time-boxed preparation

**Assumption:** 40 focused hours. **Recommendation:** use only when the learner accepts incomplete depth and explicit omissions; do not call it complete preparation.

- **Selected objectives:** SAP-FND-01/02; SAP-ORG-01..04; SAP-NEW-02..06; SAP-IMP-01..04; SAP-MIG-01..04. SAP-ORG-05 and SAP-IMP-05 receive a combined cost bridge rather than full realization; SAP-NEW-01 receives a deployment bridge.
- **Prerequisite handling:** included foundations; bridges for deployment and cost; diagnostic bypass allowed for already strong objectives.
- **Deferred:** deep service-specific implementation, optional labs, SAP-EMG-01, and extended repetitions. Full objective authoring for SAP-ORG-05, SAP-NEW-01, and SAP-IMP-05 is deferred even though bounded bridges are included.
- **Coverage gaps:** reduced assessment practice and shallow treatment of deployment/change and organizational/existing cost work. Domain weights do not justify pretending these tasks are optional. [Official guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)
- **Expected evidence:** one successful opportunity per selected objective/bridge and four cross-domain synthesis cases; unresolved gaps listed in completion report.
- **Assessment approach:** scenario-first diagnostic, focused evidence review after each failure, then a different original scenario.
- **Risks:** insufficient repetition, untested edge cases, stale service facts, and reduced confidence. No readiness or pass probability may be inferred.

## E. Learner-selected focus example — migration and modernization only

**Learner request:** “Focus only on migration and modernization.”

### Mapping and dependency detection

Requested scope maps to SAP-MIG-01..04. The graph detects blocking SAP-FND-01/02; blocking network/security foundations for SAP-MIG-02; and bridge/recommended context from governance, reliability, performance, cost, and deployment. [Dependency model](sap-c02-dependency-model.md)

### Smallest coherent recommendation

1. Include SAP-FND-01/02 as concise requirement/boundary modules with checks.
2. Include focused bridges from SAP-ORG-01 (hybrid connectivity/DNS/transfer constraints), SAP-ORG-02 (identity/encryption/security), and SAP-ORG-04 (landing/governance model).
3. Realize SAP-MIG-01, then -02, -03, and -04.
4. Add short reliability/performance/cost/deployment bridges only when material to a selected workload.
5. Omit full SAP-ORG/NEW/IMP modules with explicit warnings.

- **Prerequisite dispositions:** FND included; network/security/governance supplied by bridges; reliability/performance/cost/deployment either evidenced/diagnosed or bridged per workload.
- **Deferred content:** all complete Domain 1-3 objectives.
- **Coverage gaps:** 80% of published scored-domain weight lies outside Domain 4, and even the realized migration tasks use cross-domain competency. This plan cannot be described as complete SAP-C02 preparation. [Official domain weights](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)
- **Expected evidence:** portfolio disposition, wave plan, mechanism choice, target-platform decision, modernization roadmap, and original scenarios.
- **Assessment approach:** one integrated workload evolves through assessment, transfer/cutover, target architecture, and modernization; separate scenarios prevent memorized continuity from determining later keys.
- **Risks:** hidden weakness in security/network/reliability and insufficient breadth for the certification.
- **Recommendation:** preserve the learner's migration goal, provide the bridges, and label completion “migration and modernization realization,” not SAP-C02 completion.

## Governing partial-scope algorithm demonstrated

For any partial request:

1. Map the request to stable objective IDs in the complete architecture.
2. Traverse incoming edges and classify missing prerequisites.
3. Require inclusion/evidence/diagnostic for blocking edges; propose bridges for bounded edges.
4. Recommend the smallest plan that preserves the stated goal.
5. Warn about recommended-context and downstream omissions without forcing them into scope.
6. Record included, bridged, prior-learned, evidenced, diagnostically satisfied, waived, omitted, and deferred states distinctly.
7. Refuse only when the requested completion claim contradicts the selected coverage—for example, calling a single-task pilot complete certification preparation.

No plan state is stored in SQLite or a pack by this exercise. These files demonstrate the future behavior without choosing final serialization.
