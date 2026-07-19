# SAP-C02 Assessment Blueprint

Status: accepted with overall medium confidence

Blueprint ID: `aws-sap-c02-assessment-blueprint`

Version: `0.3A.1`

Research cutoff: 2026-07-18

Structured companion: [sap-c02-assessment-blueprint.json](sap-c02-assessment-blueprint.json)

## Identity and baseline

The target is **AWS Certified Solutions Architect - Professional (SAP-C02)**. The baseline combines the official version-1.2 PDF, whose retrieved bytes and HTTP revision metadata are recorded in the [source register](sap-c02-source-register.md), with the current unversioned HTML guide retrieved on 2026-07-18. The overlay is necessary because the HTML guide contains an Emerging Topics pretest section absent from the PDF. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) [Version-1.2 PDF](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf)

Target candidate: a solutions architect with at least two years of AWS design/implementation experience who can evaluate requirements, make deployment recommendations, and guide architectural design across multiple projects in a complex organization. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Domain references

| Domain | Weight | Task references |
|---|---:|---|
| 1. Design Solutions for Organizational Complexity | 26% | 1.1 connectivity; 1.2 security controls; 1.3 resilience; 1.4 multi-account environment; 1.5 cost visibility/optimization. [Official domain](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html) |
| 2. Design for New Solutions | 29% | 2.1 deployment; 2.2 continuity; 2.3 security; 2.4 reliability; 2.5 performance; 2.6 cost. [Official domain](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain2.html) |
| 3. Continuous Improvement for Existing Solutions | 25% | 3.1 operations; 3.2 security; 3.3 performance; 3.4 reliability; 3.5 cost. [Official domain](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain3.html) |
| 4. Accelerate Workload Migration and Modernization | 20% | 4.1 assess/select; 4.2 migration approach; 4.3 target architecture; 4.4 modernization. [Official domain](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain4.html) |

Emerging security/responsible-AI controls are tracked as unscored pretest-only content, not a weighted domain. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Assessment grammar

### Formats and response rules

- Multiple choice: exactly one correct response and three distractors.
- Multiple response: two or more correct responses among five or more options; all correct responses must be selected for credit.
- Unanswered items are incorrect; guessing has no penalty.
- The exam contains 75 items: 65 scored and 10 unidentified unscored items. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

The future authored format must always state the selection count for multiple-response items. This is a project quality rule based on the official public samples; AWS's guide states only that all correct responses must be selected. [Official samples](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf)

### Scenario profile

Inferred authoring target: generally 75-175 words before options, 2-5 material requirements/constraints, and enough architectural context to require judgment. Shorter items are acceptable for a precise diagnostic. This is an inference from ten public official samples, not an AWS-published length rule.

Expected ingredients:

- an organization/workload and current or proposed state;
- a business or technical trigger;
- explicit scale, failure, compliance, migration, performance, cost, or operational constraints where material;
- one clear command;
- a prioritizing criterion whenever several approaches would otherwise work.

### Cognitive-depth profile

Primary operations are evaluate, select, design, diagnose, optimize, migrate, modernize, compare, govern, and justify. Service recall supports these operations but should not be the sole reason an item is difficult. The expected learner must trace consequences across accounts, Regions, components, and operational ownership, then choose the option satisfying all material constraints.

### Requirement categories and tradeoffs

- security, identity, encryption, auditability, and compliance;
- resilience, availability, RTO/RPO, backup, and recovery;
- performance, scale, latency, quotas, caching, and data access patterns;
- cost, utilization, purchasing, data transfer, and managed-service tradeoffs;
- migration feasibility, transfer mechanism, cutover, modernization, and reversibility;
- operational overhead, automation, deployment safety, observability, and ownership.

These categories follow the current guide's task scope and its Well-Architected alignment. [Current guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

### Common command forms

Observed/inferred forms include: which solution meets the requirements; which combination should be selected; what should the architect do; which approach most reduces a stated burden; and which approach satisfies the goal with the least change/overhead/cost. These are generic command forms only; official sentences are not retained.

### Expected option patterns

- single-response options: four parallel solution proposals;
- multiple-response options: at least five independently selectable actions, normally with an explicit “Select TWO/THREE” instruction;
- similar grammatical structure and comparable specificity;
- real services/patterns used plausibly, including more than one broadly workable approach when the priority makes one uniquely best;
- no key-revealing length, terminology, citation, or absoluteness cue.

### Distractor taxonomy

1. technically invalid or nonexistent configuration;
2. violates one explicit requirement;
3. solves only part of the scenario;
4. excessive operational burden;
5. unnecessary cost;
6. insufficient resilience or recovery behavior;
7. inappropriate identity, network, encryption, or account boundary;
8. wrong migration/modernization pattern;
9. wrong consistency, replication, or data-access model;
10. valid only under an unstated assumption;
11. deprecated or superseded approach;
12. right service for the wrong purpose;
13. addresses a symptom rather than the stated cause;
14. larger architecture change than the prioritizer permits.

Every future distractor must store one or more categories plus a factual and scenario-specific failure rationale.

### Cross-domain behavior

An item has one primary objective but may require supporting competencies from other domains. Cross-domain facts must be explicit in the claim chain. Do not force a scenario into a single-domain silo, and do not use an unrelated service merely to increase density.

### Diagrams, exhibits, logs, policies, code, and calculations

The public ten-question sample contains no external diagram/exhibit, policy document, code block, or log exhibit. It includes embedded quantities, requirement lists, architectural descriptions, and one response-code diagnostic. One item requires a modest throughput/cost check. This evidence supports text-only 0.3B questions but is insufficient to claim that live SAP-C02 never uses exhibits or calculations. [Official samples](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf)

## Rights, evidence, and prohibitions

- Evidence IDs: AWS-CERT-001 through AWS-CERT-010, AWS-LEGAL-001, and AWS-ARCH-001 in the [source register](sap-c02-source-register.md).
- The official sample PDF is analysis-only. No sample wording, scenario, option ordering, key, or rationale may enter authored content.
- Generated content must be labeled original and not official, recalled, actual, or AWS-endorsed.
- Prohibited inputs: dumps, recalled live questions, leaked answers, unauthorized banks, “actual current questions,” suspicious derivatives, and unclear-provenance question corpora.
- Boundary: **Copy the assessment grammar, not the assessment sentences.** See [rights and reuse](sap-c02-rights-and-reuse.md).

## Confidence and uncertainty

| Dimension | Confidence | Uncertainty and recommendation |
|---|---|---|
| Exam identity | High | Current official pages agree |
| Domain coverage | High | PDF/HTML agree on four weighted domains and tasks |
| Question formats | High | Explicit official rules |
| Response rules | High | Explicit official rules |
| Scenario style | Medium | Only ten public examples were inspected; authorize a non-copying review of the current Official Practice Question Set for 0.3B if the user wants stronger calibration |
| Distractor model | Medium | Taxonomy is supported but frequency/universality is unknown; qualified review is required |
| Difficulty profile | Medium | Professional target and judgment style are clear, but exact live-form equivalence is not published |
| Rights/reuse | High | Fail-closed analysis-only conclusion is supported; formal legal advice remains outside scope |

Other uncertainties:

- AWS does not display a revision date/version for the current HTML guide.
- The current HTML Emerging Topics overlay is absent from the version-1.2 PDF.
- The official sample's copyright year is 2022 and HTTP object revision is 2023-12-15; its representativeness after later guide changes is unknown.
- No official distribution for stem length, constraint count, distractor categories, or multiple-response frequency is published.

## Review record

Review status: `accepted` by explicit repository-user instruction on 2026-07-18. Acceptance confirms the dual PDF/HTML baseline, medium style/difficulty confidence, analysis-only sample use, and text-only 0.3B default. Any exam-code, guide, domain/task, response-rule, or source-rights change triggers impact review and may require a superseding blueprint version. See [the 0.3A acceptance](../handoffs/aws-sap-c02-0.3a-acceptance.md).
