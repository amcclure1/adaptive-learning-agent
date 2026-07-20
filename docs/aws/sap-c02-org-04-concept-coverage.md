# SAP-ORG-04 Concept Coverage

Status: current authored-content coverage record; human lesson/question decisions pending

Date: 2026-07-19

Target content commit: `cc0c86fadc50336de1442f9a71659be07377bdb7`

This matrix makes the bounded pilot's coverage visible. It is not itself a claim approval, a completeness guarantee, or an instruction to add a separate claim for every row. Anthony McClure separately approved all exact current source and claim records at `2026-07-19T19:14:33Z`. The controlled statuses are `covered`, `partially covered`, `intentionally omitted`, `accidentally omitted`, `blocked by source or verification issue`, and `outside pilot scope`.

| Concept | Status | Current evidence | Boundary or follow-up |
|---|---|---|---|
| AWS account boundary concepts | covered | `clm-b-management-resource-guidance`, `clm-b-management-scp-gap`, `clm-b-ram-owner`, `clm-b-ram-permission-ceiling` | Covers management/member and resource-owner/consumer boundaries needed by this pilot. |
| Management-account usage | covered | `clm-b-management-resource-guidance`, `clm-b-management-scp-gap`, `clm-b-rec-isolate-management` | AWS guidance is represented as guidance, not a universal service invariant. |
| Organizational units | covered | `clm-b-ou-policy-target`, `clm-b-ou-control-guidance`, `clm-b-rec-control-aligned-ous` | Covers policy targeting and the conditional grouping recommendation. |
| Policy inheritance | covered | `clm-b-scp-parent-chain` | Limited to principals subject to SCPs and does not imply final authorization. |
| SCP maximum-permission behavior | covered | `clm-b-scp-ceiling` | Explicitly excludes service-linked roles. |
| SCP non-grant behavior | covered | `clm-b-scp-ceiling` | Combined atomically with the maximum-permission boundary. |
| SCP evaluation qualifications | covered | `clm-b-scp-feature-mode`, `clm-b-scp-parent-chain`, `clm-b-management-scp-gap`, `clm-b-scp-ceiling` | Includes all-features/SCP enablement, hierarchy, management-account, policy-layer, and service-linked-role qualifications. |
| Workforce federation | partially covered | `clm-b-identity-temp-creds`, `clm-b-permission-set-reuse`, `clm-b-permission-set-role` | Covers centralized workforce assignments and temporary access; external identity-provider federation mechanics are outside the selected claim slice. |
| Permission sets and account assignments | covered | `clm-b-permission-set-reuse`, `clm-b-permission-set-role` | Covers reuse across accounts and account-local role projection. |
| Temporary workforce credentials | covered | `clm-b-identity-temp-creds` | Requires an account assignment. |
| Delegated administration | covered | `clm-b-delegation-service-specific`, `clm-b-securityhub-central-authority` | Service-specific authority is distinguished from general organization administration. |
| Organization trails | covered | `clm-b-org-trail-scope`, `clm-b-org-trail-new-account`, `clm-b-org-trail-member-lock`, `clm-b-rec-org-trail` | Includes Region/opt-in conditions and member administration limits. |
| Centralized audit evidence | covered | `clm-b-org-trail-scope`, `clm-b-org-trail-new-account`, `clm-b-rec-org-trail` | Covers centrally managed CloudTrail activity evidence, not a complete logging architecture. |
| AWS Config aggregation | covered | `clm-b-config-org-auth`, `clm-b-config-readonly`, `clm-b-config-source-enabled` | Covers Organizations authorization, source enablement prerequisite, and aggregation behavior. |
| Config read-only behavior | covered | `clm-b-config-readonly` | Explicitly does not treat the aggregator as a deployment mechanism. |
| Security Hub central configuration | covered | `clm-b-securityhub-central-authority`, `clm-b-securityhub-policy-targets`, `clm-b-securityhub-region-unit` | Bound to centrally managed targets, governed settings, and the home/linked-Region unit. |
| GuardDuty organization administration where retained | intentionally omitted | No current Baseline-B source or claim retains GuardDuty. | The pilot selected Security Hub CSPM, Config, CloudTrail, IAM Identity Center, Organizations, and RAM. GuardDuty must not be inferred from those records. |
| AWS RAM sharing | covered | `clm-b-ram-principals`, `clm-b-ram-owner`, `clm-b-ram-permission-ceiling`, `clm-b-ram-regional` | Limited to supported resource types and recorded Organizations/RAM prerequisites. |
| Resource-owner versus participant responsibilities | covered | `clm-b-ram-owner`, `clm-b-ram-permission-ceiling` | Owner retains the resource; consumer permissions remain bounded by both share permissions and identity policy. |
| Regional considerations | covered | CloudTrail, Config, Security Hub, and RAM claim clusters | Region sensitivity is service-specific; no generic cross-service Region rule is asserted. |
| Preventive versus detective controls | partially covered | SCP, Config, CloudTrail, and Security Hub claim clusters; `clm-b-rec-complement-config-securityhub` | The distinct mechanisms are represented without conflation, but the pilot does not claim an exhaustive control taxonomy. |
| Identity permissions versus governance guardrails | covered | `clm-b-identity-temp-creds`, permission-set claims, SCP claims, `clm-b-rec-pair-access-guardrail` | The recommendation requires both workforce access and the organization-level maximum-permission boundary. |
| Derived architectural tradeoffs | covered | All five `clm-b-rec-*` claims and their exact premise graphs | Recommendations are conditional and criterion-bound; they are not universal AWS service behavior. |

## Current lesson and assessment realization

| Major distinction | Lesson coverage | Question coverage | Disposition |
|---|---|---|---|
| Account, management-account, and control-aligned OU boundaries | `les-sap-org-04-foundations-governance` | `q-sap-org-04-account-boundaries` | Taught and assessed. |
| Policy inheritance and SCP maximum-permission/non-grant behavior | `les-sap-org-04-foundations-governance` | `q-sap-org-04-workforce-guardrails` | Taught; the access-versus-guardrail judgment is assessed, while detailed chain evaluation is taught but not directly assessed. |
| Central workforce assignments, permission sets, roles, and temporary credentials | `les-sap-org-04-foundations-governance` | `q-sap-org-04-workforce-guardrails` | Taught and assessed as a coordinated select-two design. |
| Organization trails, joining-account coverage, member protection, and Region conditions | `les-sap-org-04-central-operations` | `q-sap-org-04-audit-evidence` | Taught and assessed; delivery prerequisites are explicitly a scenario precondition or deferred lesson boundary. |
| Config read-only aggregation versus Security Hub central authority | `les-sap-org-04-central-operations` | `q-sap-org-04-central-visibility` | Taught and assessed as complementary capabilities. |
| Service-specific delegated administration | `les-sap-org-04-central-operations` | `q-sap-org-04-central-visibility` | Taught and assessed without implying general organization authority. |
| RAM eligibility, OU principals, ownership, layered permissions, and Region scope | `les-sap-org-04-central-operations` | `q-sap-org-04-resource-sharing` | Taught and assessed. |
| Guidance versus service behavior and conditional recommendations | both lessons | all five questions | Taught throughout and assessed through explicit scenario requirements and prioritizers. |

Concepts taught but not independently assessed include the complete root-to-account SCP evaluation chain, Config authorization detail, the Security Hub global-resource-control exception, and the RAM trusted-access/service-linked-role setup distinction. They remain learner-relevant caveats rather than separate trivia items.

Intentionally deferred concepts are event-notification strategy, the AWS Control Tower/AWS Organizations relationship, GuardDuty organization administration, external identity-provider federation mechanics, and an exhaustive preventive/detective control taxonomy. These deferrals are visible and do not create an accidental gap inside the five selected architectural judgments.

The remaining gap is qualified-human review: lesson content, question content/originality, and answer uniqueness have not been approved. This matrix does not claim complete SAP-ORG-04, Domain 1, or SAP-C02 coverage.

## Derived-recommendation premise graph

| Recommendation | Exact current premises | Decision criterion |
|---|---|---|
| `clm-b-rec-complement-config-securityhub` r3 | `clm-b-config-org-auth` r1; `clm-b-config-readonly` r1; `clm-b-config-source-enabled` r1; `clm-b-securityhub-central-authority` r3; `clm-b-securityhub-policy-targets` r1; `clm-b-securityhub-region-unit` r3 | Satisfy distinct visibility and configuration-authority requirements without treating a read-only aggregator as a deployment mechanism. |
| `clm-b-rec-control-aligned-ous` r4 | `clm-b-ou-control-guidance` r2; `clm-b-ou-policy-target` r1 | Simplify policy management and troubleshooting for accounts with a common security-control baseline. |
| `clm-b-rec-isolate-management` r3 | `clm-b-management-resource-guidance` r1; `clm-b-management-scp-gap` r1 | Keep non-required resources and data outside the uniquely privileged management-account boundary. |
| `clm-b-rec-org-trail` r3 | `clm-b-org-trail-member-lock` r1; `clm-b-org-trail-new-account` r2; `clm-b-org-trail-scope` r2 | Meet organization coverage, automatic new-account onboarding, and member-admin trail-protection requirements without per-account trail creation. |
| `clm-b-rec-pair-access-guardrail` r3 | `clm-b-identity-temp-creds` r1; `clm-b-permission-set-reuse` r1; `clm-b-permission-set-role` r1; `clm-b-scp-ceiling` r2; `clm-b-scp-feature-mode` r1 | Provide reusable temporary workforce access while enforcing an organization-level maximum-permission boundary in member accounts. |

## Operative MVP threshold

Content may proceed to qualified human review when declared-scope coverage is explicit; every material claim is source-backed; every active artifact has current exact-digest self-audit, deterministic-validation, and independent-verification evidence; no unresolved critical, high, or medium issue remains; simplifications are not materially misleading; and decision-relevant omissions are documented. Low or informational issues require an explicit nonblocking rationale. This threshold does not require encyclopedic completeness and grants no human approval.
