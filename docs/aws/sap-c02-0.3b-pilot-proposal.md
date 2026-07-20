# Accepted Scope and Final Design Specifications for the SAP-C02 0.3B Pilot

Status: pilot scope accepted; sources and claims approved; authored lessons/questions pending separate qualified-human review

Pilot ID: `aws-sap-c02-org-04-pilot`

Architecture: `aws-sap-c02-learning-architecture` version `0.3A.1`

## Selected scope

Select **Domain 1, task 1.4: Design a multi-account AWS environment**, realized as objective **SAP-ORG-04**. The official task requires evaluating account structure, central logging/event notifications, and a multi-account governance model, with AWS Organizations, AWS Control Tower, event notifications, and resource sharing in scope. [Official Domain 1 task 1.4](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html)

This is representative of professional-level judgment because requirements for isolation, autonomy, policy inheritance, workforce access, audit ownership, delegated administration, and sharing can make several broadly valid designs compete. AWS guidance recommends organizing accounts/OUs by security and operational needs rather than simply mirroring the reporting structure, and distinguishes Organizations' underlying governance from Control Tower's orchestration. [Multi-account design principles](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html) [Control Tower overview](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)

## Objective set and bridges

- **Primary:** SAP-ORG-04 — design a multi-account environment.
- **Bridge B1:** SAP-FND-01 — make requirements/priorities explicit and justify the chosen boundary/control.
- **Bridge B2:** SAP-FND-02 — trace identity, evidence, resource ownership, and administrative responsibility across accounts/OUs.
- **Bridge B3:** bounded SAP-ORG-02 — distinguish identity permissions, organizational guardrails, federation, audit, and delegated security administration.
- **Recommended context, not completed:** SAP-ORG-01 for shared-network cases and SAP-ORG-05 for allocation/cost-governance cases.

The realization does not complete Domain 1 or SAP-C02.

## Proposed content envelope

| Element | Proposal |
|---|---|
| Lessons | 2 original, cited lessons: (1) account/OU boundaries, guardrails, and workforce access; (2) centralized evidence, delegation, and resource sharing |
| Approved claims | Approximately 24-30; final count follows source/claim review rather than a quota |
| Questions | **Exactly five original scenario questions**; finalized design specifications below, no learner-ready text exists |
| Response mix | Three single-response; two multiple-response, each with an explicit selection count |
| Assessment depth | Evaluate/govern/justify, not service-name recall |
| Diagram | None by default; existing format-0.3 static PNG support may be considered only after a demonstrated material need and separate source/rights/accessibility/non-leakage review |
| AWS account | None required |

## Planned authoritative source set

1. [SAP-C02 Domain 1 task 1.4](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html) — assessment scope.
2. [Organizing Your AWS Environment Using Multiple Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/aws-organizations.html) and [design principles](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html) — account/OU strategy.
3. [Organizations SCP documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) — guardrail semantics, including that SCPs do not grant permissions and do not restrict management-account identities.
4. [Management-account best practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html) — workload isolation and delegation.
5. [Control Tower overview](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html) and [controls](https://docs.aws.amazon.com/controltower/latest/controlreference/controls.html) — landing-zone orchestration and OU-level controls.
6. [IAM Identity Center multi-account access](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html) — permission sets and centralized workforce access.
7. [CloudTrail organization trails](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html) — organization-wide audit logging.
8. [AWS Config aggregation](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html) — multi-account/multi-Region read-only configuration/compliance aggregation.
9. [Security Hub central configuration](https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html) — delegated central security configuration.
10. [AWS RAM overview](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html) — supported cross-account resource-sharing model and ownership.
11. [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/introduction.html) and [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — derived architectural guidance and tradeoff framing.

Service facts must use precise sections/locators in 0.3B claim records. Guidance is not treated as a universal fact; applicability is part of the reviewed derivation.

## Five future question design specifications

These are design specifications only. They intentionally omit final stems, answer text, option order, and keys.

All five are version `0.3B-design-1`, status `finalized_for_drafting`. This status approves the design boundary only; it is not question-content or answer-uniqueness approval.

Set-level differentiation is fixed:

| Specification | Primary judgment | Required distinct contribution |
|---|---|---|
| QSPEC-01 | Organizational structure | Account/OU boundaries, isolation, autonomy, management-account boundary |
| QSPEC-02 | Workforce and preventive controls | Federation/permission assignment versus SCP maximum-permission guardrails |
| QSPEC-03 | Audit evidence | Organization-wide activity evidence, central ownership, new-account coverage |
| QSPEC-04 | Security/configuration governance | Visibility versus configuration, delegated administration, drift reduction |
| QSPEC-05 | Shared-resource ownership | RAM eligibility, owner/consumer permissions, Region and operational tradeoffs |

No question may be rewritten into a generic “which SCP” item. The final set must preserve these different decision operations and use varied distractor categories.

### QSPEC-01 — Account and OU boundary design

- **Specification ID/version/status:** `QSPEC-01` / `0.3B-design-1` / `finalized_for_drafting`.
- **Format:** single response.
- **Selection rule:** select one from four options.
- **Target objective:** SAP-ORG-04; supporting SAP-FND-01/02.
- **Cognitive operation:** evaluate and justify organizational boundaries.
- **Scenario theme:** a growing enterprise needs workload isolation, distinct production/nonproduction controls, team autonomy, and room to add regulated workloads.
- **Material requirements:** isolate blast radius; group accounts by common controls/operational needs; keep the management account free of business workloads; permit governed growth.
- **Material constraints:** avoid needless hierarchy/operational complexity; preserve delegated team ownership.
- **Compared patterns:** reporting-line OUs versus control-based OUs; workloads in management account versus member accounts; deep versus shallow hierarchy; per-account controls versus OU-level controls.
- **Key characteristics:** satisfies all isolation/control/growth requirements with the smallest justified hierarchy and correct management-account boundary.
- **Distractor categories:** inappropriate security/account boundary; violates one requirement; excessive operational burden; partial solution.
- **Evidence:** multi-account whitepaper/design principles, management-account best practices, Control Tower/Organizations guidance.
- **Difficulty:** medium-high.
- **Blueprint match:** multi-paragraph organization scenario, 3-4 interacting constraints, unique-best prioritizer, four parallel architecture options.
- **Ambiguity/review concerns:** organization size and regulatory divergence must be explicit; avoid implying one universal OU tree.

### QSPEC-02 — Workforce access and guardrails

- **Specification ID/version/status:** `QSPEC-02` / `0.3B-design-1` / `finalized_for_drafting`.
- **Format:** multiple response, select two.
- **Selection rule:** select exactly two from at least five options.
- **Target objective:** SAP-ORG-04 with bounded SAP-ORG-02 bridge.
- **Cognitive operation:** distinguish permission grant, maximum-permission guardrail, federation, and management-account exception.
- **Scenario theme:** centrally managed workforce access across many accounts with least privilege and prohibited member-account actions.
- **Material requirements:** one workforce identity path; reusable role/permission assignments; enforce member-account guardrails; minimize long-lived credentials.
- **Material constraints:** business teams retain allowed in-account administration; management-account identities are handled explicitly.
- **Compared patterns:** IAM Identity Center permission sets; SCPs; duplicated IAM users; broad cross-account roles; management-account SCP assumptions.
- **Key characteristics:** coordinated identity assignment plus a correctly scoped organizational guardrail, with no claim that an SCP grants permission.
- **Distractor categories:** technically invalid; wrong security boundary; right service for wrong purpose; valid only under unstated assumption.
- **Evidence:** IAM Identity Center multi-account access/permission sets, SCP documentation, management-account best practices.
- **Difficulty:** high.
- **Blueprint match:** explicit selection count, several technically plausible mechanisms, cross-domain identity/governance reasoning.
- **Ambiguity/review concerns:** state organization feature mode, workforce identity source, target accounts, and prohibited action; verify two selections are both necessary and sufficient.

### QSPEC-03 — Central, tamper-resistant audit coverage

- **Specification ID/version/status:** `QSPEC-03` / `0.3B-design-1` / `finalized_for_drafting`.
- **Format:** single response.
- **Selection rule:** select one from four options.
- **Target objective:** SAP-ORG-04; supporting SAP-FND-02.
- **Cognitive operation:** design evidence ownership and organization-wide coverage.
- **Scenario theme:** security requires centrally controlled activity evidence for existing and newly added accounts across enabled Regions while workload administrators retain normal operational access.
- **Material requirements:** organization coverage; automatic inclusion of new member accounts; central evidence destination/ownership; member administrators cannot alter the central trail.
- **Material constraints:** minimize per-account manual setup; distinguish trail data from console Event history.
- **Compared patterns:** organization trail; independent member trails; Event history aggregation assumption; application-log-only collection.
- **Key characteristics:** uses the organization-level facility and correctly assigns management/delegated administration and destination controls.
- **Distractor categories:** partial solution; wrong service purpose; excessive operational burden; violates evidence-control requirement.
- **Evidence:** CloudTrail organization-trail documentation and management-account/delegation guidance.
- **Difficulty:** medium-high.
- **Blueprint match:** operational/security constraints, one unique best, options differing in ownership and coverage rather than brand recall.
- **Ambiguity/review concerns:** specify management versus data events if material, Regions/partition, destination prerequisites, and whether a delegated administrator is allowed.

### QSPEC-04 — Central security posture and configuration visibility

- **Specification ID/version/status:** `QSPEC-04` / `0.3B-design-1` / `finalized_for_drafting`.
- **Format:** multiple response, select two.
- **Selection rule:** select exactly two from at least five options.
- **Target objective:** SAP-ORG-04 with SAP-ORG-02 bridge.
- **Cognitive operation:** select complementary central-governance capabilities and distinguish visibility from mutation.
- **Scenario theme:** a security team needs organization-wide configuration/compliance visibility and centrally governed security standards while workload teams remain in member accounts.
- **Material requirements:** multi-account/multi-Region view; central policy administration for chosen OUs; delegated security ownership; no claim that visibility alone remediates resources.
- **Material constraints:** new accounts should inherit intended configuration where supported; minimize per-account configuration drift.
- **Compared patterns:** AWS Config aggregator; Security Hub central configuration; CloudTrail organization trail; per-account dashboards; management-account-only deployment.
- **Key characteristics:** selects complementary tools that together meet read-only aggregation and centralized security-configuration requirements, with delegated administration.
- **Distractor categories:** partial solution; wrong service purpose; valid only under unstated assumption; inappropriate management-account boundary.
- **Evidence:** Config aggregation, Security Hub central configuration, Organizations delegated administration, AWS SRA.
- **Difficulty:** high.
- **Blueprint match:** select-two with interacting requirements; cross-service and cross-account reasoning; plausible partial distractors.
- **Ambiguity/review concerns:** state which compliance/security configuration must be centralized; do not imply Config aggregators deploy rules or mutate source accounts.

### QSPEC-05 — Shared service versus duplicate resources

- **Specification ID/version/status:** `QSPEC-05` / `0.3B-design-1` / `finalized_for_drafting`.
- **Format:** single response.
- **Selection rule:** select one from four options.
- **Target objective:** SAP-ORG-04; recommended SAP-ORG-01 context only if a network resource is selected.
- **Cognitive operation:** compare centralized sharing with per-account duplication from ownership, isolation, operations, and Region constraints.
- **Scenario theme:** platform teams need to provide an eligible shared capability to selected OUs while preserving resource ownership and limiting consumer permissions.
- **Material requirements:** central ownership; scoped consumer actions; auditable sharing; avoid duplicate administration.
- **Material constraints:** the selected resource type must actually be shareable; Regional behavior and consuming-account IAM/SCP controls must be explicit.
- **Compared patterns:** AWS RAM resource share; duplicate per-account resources; broad cross-account administrator role; unsupported cross-Region/global assumption.
- **Key characteristics:** uses an eligible sharing model with correct owner/consumer permission boundaries and explicit Region scope.
- **Distractor categories:** technically invalid; excessive operational burden; wrong security boundary; valid only under unstated assumption.
- **Evidence:** AWS RAM overview, shareable-resource list at authoring time, Organizations/OU integration, IAM/SCP interaction.
- **Difficulty:** medium-high.
- **Blueprint match:** one priority (“least operational overhead” or equivalent) makes one broadly workable design uniquely best.
- **Ambiguity/review concerns:** choose and cite a currently shareable resource; recheck Region and permission behavior immediately before approval.

## Review and freshness gates

1. **Source approval:** authoritative identity, current URL/revision, allowed use, and rights.
2. **Claim approval:** qualified AWS multi-account reviewer validates 24-30 claims and all conditions.
3. **Question approval:** a qualified reviewer confirms original construction, blueprint fit, objective alignment, explicit requirements, distractor rationales, and answer uniqueness for each of five items.
4. **Pack-release approval:** separate human decision over exact immutable content and notices.

Freshness proposal:

- exam guide/code/domain/task: recheck before claim work, before question approval, and before release;
- Organizations/Control Tower/IAM/Security Hub/Config/CloudTrail/RAM claims: recheck at claim approval and again if more than 30 days pass before question/release approval;
- Region availability, quotas, pricing, renamed/deprecated features: recheck within 7 days of question approval and release;
- any provider announcement or documentation contradiction: immediate impact review.

These are editorial horizons, not implemented timers.

## Explicit non-goals

- no final question wording, options, key, or learner-ready rationale in 0.3A;
- no full lesson or complete claim set;
- no complete Domain 1 or SAP-C02 pack;
- no exam simulation, readiness score, or pass prediction;
- no diagram, asset, AWS account, lab, MCP setup, or resource creation;
- no pack-format, SQLite, deterministic-core, scoring, Hermes, or tool-contract change;
- no authoring-agent self-approval or autonomous activation.

## Acceptance and next gate

The repository user accepted task 1.4 / `SAP-ORG-04`, the two-lesson/approximately 24–30-claim envelope, the 3-single/2-multiple mix, public-source-only research, and deferral of MCP/AWS-account access on 2026-07-18. See [the 0.3A acceptance](../handoffs/aws-sap-c02-0.3a-acceptance.md).

The source-and-claim baseline is human-approved. The later explicitly authorized content task produced exactly two original cited lessons and five original questions with the accepted three-single/two-select-two mix, separate specifications, internal rationales, complete matrices, self-audits, deterministic validation, and independent AI review evidence. The [concept matrix](sap-c02-org-04-concept-coverage.md) distinguishes taught, assessed, and intentionally deferred concepts.

Qualified-human lesson-content, question-content/originality, answer-uniqueness, and later pack-release approvals remain pending in the [content-review handoff](../handoffs/aws-sap-c02-0.3b-content-review-pending.md). No pack was compiled, installed, activated, published, released, or tagged.
