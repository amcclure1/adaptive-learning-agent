# SAP-C02 Assessment Research

Status: draft 0.3A research baseline; human approval required

Research date: 2026-07-18 (America/Chicago)

Target decision: design against current SAP-C02, with the current HTML guide as a freshness overlay on PDF guide version 1.2

## Verified assessment identity

As of 2026-07-18, AWS's current certification catalog and certification page identify **AWS Certified Solutions Architect - Professional** and the current exam guide identifies exam code **SAP-C02**. No official replacement, beta, transition, or retirement announcement was found in the current AWS certification catalog. This last sentence is a bounded inference from the official catalog and current target page, not a claim that AWS has promised no future change. [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

| Field | Verified value | Evidence |
|---|---|---|
| Certification | AWS Certified Solutions Architect - Professional | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) |
| Exam code | SAP-C02 | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Versioned guide | Version 1.2; official PDF HTTP metadata was last modified 2025-02-19 | [AWS-CERT-003](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf) |
| Current-guide overlay | The unversioned HTML guide includes a later Emerging Topics section not present in the version-1.2 PDF; AWS displays no revision date | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Target candidate | Solutions architect with 2 or more years using AWS services to design and implement cloud solutions; capable of evaluating requirements and advising across multiple applications/projects in a complex organization | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Total questions | 75 | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) |
| Scored / unscored | 65 scored and 10 unscored; unscored items are not identified | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Duration | 180 minutes | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) |
| Question types | Multiple choice and multiple response | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Response rules | Multiple choice: one correct and three distractors. Multiple response: two or more correct among five or more options; all correct responses are required. Unanswered is incorrect; no guessing penalty | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Result and scale | Pass/fail; scaled 100-1,000; minimum passing score 750; compensatory overall model, not a per-domain pass requirement | [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) |
| Delivery | Pearson VUE test center or online proctored | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) |
| Languages | English, Japanese, Korean, Portuguese (Brazil), Simplified Chinese, Spanish (Latin America) | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) |
| Certification validity | Three years; Professional recertification is by passing the current version of the corresponding exam before expiry | [AWS-CERT-001](https://aws.amazon.com/certification/certified-solutions-architect-professional/) [AWS-CERT-006](https://aws.amazon.com/certification/policies/recertification/) |
| Current effective start | First SAP-C02 test date: 2022-11-15; prior version's last test date: 2022-11-14 | [AWS-CERT-007](https://aws.amazon.com/blogs/training-and-certification/aws-certified-solutions-architect-professional-content-outline-updated-to-align-with-latest-trends-and-innovations/) |

AWS says scaled scores are statistically equated across forms and that 750 is the Professional/Specialty passing standard. The project must not infer a raw-number-correct threshold, domain threshold, readiness percentage, or passing probability. [AWS-CERT-005](https://aws.amazon.com/certification/policies/after-testing/)

## Current domain and task baseline

The four scored domains and weights are 26%, 29%, 25%, and 20% respectively. [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

1. **Design Solutions for Organizational Complexity — 26%.** Tasks: 1.1 architect network connectivity strategies; 1.2 prescribe security controls; 1.3 design reliable and resilient architectures; 1.4 design a multi-account AWS environment; 1.5 determine cost optimization and visibility strategies. [Domain 1](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html)
2. **Design for New Solutions — 29%.** Tasks: 2.1 design a deployment strategy; 2.2 ensure business continuity; 2.3 determine security controls; 2.4 meet reliability requirements; 2.5 meet performance objectives; 2.6 determine cost optimization strategy. [Domain 2](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain2.html)
3. **Continuous Improvement for Existing Solutions — 25%.** Tasks: 3.1 improve operational excellence; 3.2 improve security; 3.3 improve performance; 3.4 improve reliability; 3.5 identify cost optimizations. [Domain 3](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain3.html)
4. **Accelerate Workload Migration and Modernization — 20%.** Tasks: 4.1 select workloads/processes for migration; 4.2 determine the optimal migration approach; 4.3 determine a new architecture for existing workloads; 4.4 determine modernization/enhancement opportunities. [Domain 4](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain4.html)

The current HTML guide also identifies security and responsible-AI controls as **emerging topics that might occur only as unscored pretest content**. They must be tracked for freshness but must not be represented as a fifth scored domain or assigned a scored weight. [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## How competence is assessed

### Direct official evidence

The public sample contains ten questions, five single-response and five multiple-response. Four multiple-response samples require two selections and one requires three. This is a sample observation, not a published exam-wide distribution. [AWS-CERT-004](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf), questions 1-10.

| Characteristic | Observation from the ten official samples | Boundary |
|---|---|---|
| Scenario length | Stems range from compact operational cases to multi-paragraph architectures with explicit requirement lists; most establish an organization/application, existing state, problem, and desired outcome before the command | Observed in ten samples only; do not claim a universal word count |
| Scenario density | Commonly 2-5 named services or architectural elements plus 1-4 requirements/constraints; the longest cases include workload scale, traffic, failure behavior, or multiple tiers | Approximate manual coding, not AWS-published statistics |
| Cognitive operation | Select, diagnose, combine changes, optimize, or modernize; several require eliminating options that are technically possible but miss a priority | Direct observation; difficulty equivalence to live forms is not established |
| Prioritization language | The samples use commands such as “meet these requirements,” “MOST reduce costs,” “LEAST change,” and “minimize operational overhead” | Direct observation; not every sample uses a superlative |
| Option construction | Options are parallel solution proposals; some are one action and others are coordinated multi-step designs. Multiple-response options remain independently selectable | Direct observation |
| Plausibility | Several distractors use real AWS services or plausible actions but fail one constraint, solve the wrong layer, add overhead, or do not address the failure mechanism | Direct observation from AWS rationales |
| Artifacts | No diagram, exhibit, policy document, code block, or external log exhibit appears in the public ten-question PDF. One question embeds an HTTP status code and others embed requirements, quantities, or architecture descriptions | Absence in ten samples does not prove absence from live forms |
| Calculations | One cost scenario requires checking throughput against a stated service quota and comparing idle/consumption patterns; no extended arithmetic is shown | Direct observation; not a frequency claim |
| Cross-domain behavior | Individual scenarios combine, for example, organization/security/cost, or scaling/integration/reliability | Direct observation; domain mapping per item is not published |

AWS preparation guidance tells candidates to use official practice sets to learn concepts and exam style, use elimination, and not expect the practice questions verbatim on the live exam. [AWS-CERT-009](https://aws.amazon.com/blogs/training-and-certification/5-tips-for-aws-certification-exams-from-aws-solutions-architects/)

### Inferences for authored assessment design

The following are explicitly **inferences**, not published AWS item-writing rules:

- **Scenario target:** usually 75-175 words before options, with shorter diagnostic items allowed when the evidence does not justify added narrative. This range generalizes the public examples and intentionally avoids cloning any one stem.
- **Constraint target:** normally 2-5 material requirements/constraints, including at least one prioritizer when more than one architecture could work.
- **Cognitive depth:** professional architectural judgment should dominate bare service-name recall. Recall remains necessary as input, but the item should require mapping behavior to constraints, analyzing failure or scale, or comparing tradeoffs.
- **Option target:** four options for single response; five or more for multiple response. Keep options grammatically parallel and similar enough in specificity that length alone does not reveal the key.
- **Plausibility:** multiple options may be technically possible in a broad sense. The scenario must make one response—or the stated selection count—uniquely best by cost, resilience, security, performance, migration risk, or operational-overhead criteria.
- **Cross-domain construction:** a primary objective may draw supporting facts from other domains when a real architecture requires them, but the key rationale must state which requirement each supporting fact satisfies.
- **No artifact assumption:** text-only is the supported 0.3B default. Diagram/exhibit matching is not required by current public evidence and remains unproven for the live assessment.

## Typical tradeoffs and distractors

The guide's task verbs and knowledge lists, the Well-Architected alignment, and the samples support recurring tradeoffs across security, reliability/resilience, performance, cost, migration/modernization, and operational overhead. Sustainability is a current Well-Architected pillar, but it is not a separately weighted SAP-C02 domain in the current guide. [AWS-ARCH-001](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) [AWS-CERT-002](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

Observed distractor mechanisms include wrong service purpose, invalid configuration, partial solution, failure to meet an explicit control or selection count, unnecessary manual operation, architecture change larger than the prioritizer allows, and a solution aimed at a symptom rather than the stated failure. These are abstractions from the official rationales; the project retains no sample sentences or answer combinations. [AWS-CERT-004](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf), answer rationales pp. 6-7.

## Source hierarchy and exclusions

- **Tier 1 official:** certification page, current HTML guide, versioned PDF guide, public sample PDF, policies, official preparation guidance, and Skill Builder descriptions.
- **Tier 2 licensed/open:** none found for SAP-C02 question content.
- **Tier 3 descriptive:** none required for this baseline; any future use may corroborate general style only.
- **Excluded:** dumps, recalled live questions, leaked keys, “actual current questions,” unauthorized scraped banks, copied commercial banks, and suspicious derivatives.

Excluded-source indicators for future automation include “actual exam questions,” “100% pass,” “verified dump,” VCE/Q&A dump downloads, current live-answer claims, memory/recollection solicitations, unexplained answer-only banks, large current banks with no author/license, scraped brand pages, and mismatched publisher/domain identity. Detection is a rejection trigger, not merely a low-confidence signal.

## Confidence

| Dimension | Rating | Rationale / resolution |
|---|---|---|
| Exam identity | High | Current catalog, exam page, and guide agree on SAP-C02 |
| Domain coverage | High | Current HTML and version-1.2 PDF agree on four domains, weights, and 20 tasks |
| Question formats | High | Exam guide and public page agree |
| Response rules | High | Official guide explicitly defines option counts and all-or-nothing multiple response |
| Scenario style | Medium | Ten public official samples are strong but small and copyright-dated 2022; the private/free Skill Builder set was not accessed. Resolve by an authorized human reviewing the current Official Practice Question Set in 0.3B and recording characteristics only |
| Distractor model | Medium | Official rationales support a taxonomy, but ten items cannot establish frequency. Resolve with the same authorized, non-copying review |
| Difficulty profile | Medium | Target-candidate level and sample reasoning are clear, but sample-to-live equivalence is not published. Recommendation: calibrate through qualified AWS architect review rather than candidate recollection |
| Rights/reuse | High | The sample PDF says all rights reserved and no reuse grant was found; fail-closed analysis-only classification is clear. Formal legal advice has not been obtained |

Overall blueprint confidence is **medium**, with high confidence in identity/structure and medium confidence in style/difficulty. This supports a manually reviewed pilot but not a claim of exact live-exam simulation.
