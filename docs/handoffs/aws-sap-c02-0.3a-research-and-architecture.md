# AWS SAP-C02 0.3A Research and Architecture Handoff

Status: superseded as the pending handoff by accepted 0.3A closure

Research date: 2026-07-18

Repository integration updated: 2026-07-18

Target: AWS Certified Solutions Architect - Professional (`SAP-C02`)

Implementation authority: none granted by this handoff

## Outcome

Version 0.3A has been executed manually as the intended future Subject Builder workflow. It produced a reproducible official-source baseline, rights/reuse decisions, an assessment blueprint, a complete high-level learning architecture, cross-domain dependency structure, multiple progressive realizations, optional capability recommendations, an evidence-backed authored-question policy, a bounded 0.3B pilot proposal, and an automation-gap analysis.

The work is complete in coverage and dependency structure, not authored educational content. The repository user subsequently accepted the 0.3A decisions and the bounded 0.3B pilot; see [the acceptance handoff](aws-sap-c02-0.3a-acceptance.md). That acceptance does not itself approve or activate authored 0.3B content.

## Repository integration update

The concurrent E7B/format-0.3 work that was deliberately excluded from the original 0.3A documentation commits has since been completed as a coherent pre-approval checkpoint, validated, committed, and pushed on top of 0.3A:

- `957fe21` — `feat: add static png pack format 0.3`;
- `ffbf681` — `test: verify asset integrity and compatibility`;
- `49662f6` — `content: add pending amateur extra e7b asset pilot`;
- `c44976b` — `docs: finalize e7b review checkpoint`.

At integration baseline `c44976b4295736cdf6573cace96691482124fe7f`, local `main` and `origin/main` matched and the working tree was clean. The complete standard-library suite passed 77/77 tests on the available CPython 3.14 environment.

This subsequent work implements generic pack format 0.3 static-PNG support and adds an exact E7B10–E7B12/Figure E7-1 candidate. The candidate remains deliberately non-installable while human content review is pending. Independent-review PASS, release-readiness PASS, the final Python 3.12–3.14 matrix, hosted CI, real Hermes E7B acceptance, release, and tag remain absent. See [the 0.2B implementation handoff](amateur-extra-asset-0.2b-implementation.md), [human review package](../reviews/amateur-extra-e7b-asset-content-review.md), and [release-readiness handoff](amateur-extra-asset-0.2b-release-readiness.md).

The integration does not alter the 0.3A assessment identity, evidence baseline, rights conclusions, blueprint, learning architecture, dependency model, realization plans, capability recommendations, proposed 0.3B AWS scope, or the requirement for separate human authorization before AWS content work.

## Verified assessment identity

As verified from current official AWS sources on 2026-07-18:

- **Certification:** AWS Certified Solutions Architect - Professional.
- **Exam code:** `SAP-C02`.
- **Current guide baseline:** AWS's current HTML exam guide and official PDF version 1.2. The PDF object metadata reports `Last-Modified: Wed, 19 Feb 2025 22:00:24 GMT` and `x-amz-meta-version: 2025-02-19T21:59:27.773Z`; the retained-download SHA-256 was `e11f5a66162786ad41a62985f4c3da0f040cb5f080741c72b58650f11addeb7a`.
- **Domain structure:** design solutions for organizational complexity, 26%; design for new solutions, 29%; continuous improvement for existing solutions, 25%; accelerate workload migration and modernization, 20%.
- **Task structure:** 20 task statements across the four domains.
- **Candidate:** two or more years using AWS services to design and implement cloud solutions, with the professional capabilities stated in the guide.
- **Format:** 180 minutes; 75 questions; multiple choice and multiple response; Pearson VUE test center or online proctored.
- **Response rules:** multiple choice has one correct and three distractors; multiple response has two or more correct responses from five or more and requires all correct responses.
- **Scoring published by AWS:** 65 scored and 10 unidentified unscored questions; scaled 100-1,000; minimum passing score 750; compensatory overall scoring; no penalty for guessing and unanswered questions count incorrect.
- **Languages on the current exam page:** English, Japanese, Korean, Portuguese (Brazil), Simplified Chinese, and Spanish (Latin America).
- **Validity:** three years; recertification is by passing the current exam version before expiration.
- **Effective-history point:** AWS states SAP-C02 testing began 2022-11-15 and the prior exam's last test date was 2022-11-14.

The current HTML guide also lists emerging responsible-AI/security topics as possible unscored pretest content. They are not included in scored domain coverage. No official replacement, beta, transition, or retirement notice was found in the official pages and announcement searches reviewed. That absence is a bounded research conclusion, not proof that no unpublished change exists. Evidence and exact citations are in [the assessment research](../aws/sap-c02-assessment-research.md) and [source register](../aws/sap-c02-source-register.md).

## Assessment-blueprint confidence

**Overall: medium.**

- High: exam identity, domain coverage, question formats, and response rules.
- Medium: scenario style, distractor model, and difficulty profile. Ten official public sample questions are useful direct evidence but cannot establish universal behavior; no authenticated Skill Builder practice set was accessed.
- High: the operational rights/reuse conclusion is fail-closed. AWS documentation has an explicit CC BY-SA 4.0 boundary, while the separately hosted exam-guide and sample-question PDFs carry no specific open reuse grant identified in this research. Their content remains analysis-only unless an authorized rights review finds a controlling grant; this is project policy, not legal advice.

The structured blueprint parses as JSON and deliberately makes no pack-format or runtime-schema commitment. See [the Markdown blueprint](../aws/sap-c02-assessment-blueprint.md) and [structured blueprint](../aws/sap-c02-assessment-blueprint.json).

## Proposed 0.3B pilot

Recommend **Domain 1, task 1.4 / `SAP-ORG-04`: design a multi-account AWS environment**.

Proposed envelope:

- two original cited lessons;
- approximately 24-30 source-bound, human-approved claims;
- exactly five future original scenario questions;
- three single-response and two multiple-response specifications;
- prerequisite bridges for explicit architectural priorities, identity/evidence boundaries, and the distinction between permissions, guardrails, federation, audit, and delegated administration;
- no diagram, AWS account, lab, MCP server, or private capability;
- qualified human source, claim, question/uniqueness, and pack-release approvals.

The proposal includes five design specifications only. It contains no final learner-ready stems, options, answer keys, or rationales. See [the pilot proposal](../aws/sap-c02-0.3b-pilot-proposal.md).

## Recommended capabilities

For an explicitly authorized 0.3B or 0.3C task:

1. Keep official AWS web pages and local digest/PDF inspection as the baseline. This is Level 0 and sufficient for the first manual content pilot.
2. Optionally approve either the remote official AWS Knowledge MCP server or the local AWS Documentation MCP server for public read-only documentation retrieval. Both are recommended at Level 0; neither requires AWS credentials. Do not install both initially unless their distinct value is demonstrated.
3. Consider the official managed AWS MCP Server later with a strict read-only tool allowlist only if broader discovery materially improves 0.3C. Public documentation tools can operate without authentication, while API/script tools require IAM and may create Level 1-3 effects.
4. Defer AWS account inspection, authenticated Skill Builder practice access, and lab/sandbox execution. They are unnecessary for the first pilot. Account inspection would require explicit Level 1 approval and least-privileged credentials; mutations or labs require Level 2 or Level 3 approval, budgets, and teardown controls.

No MCP server was configured or health-tested. All candidates remain only `discovered` or `recommended`. Exact candidate fields, official capability citations, Hermes v0.18.2 transport evidence, fallbacks, and disable procedures are in [the capability report](../aws/sap-c02-capability-report.md).

## Rights and source issues

- The official sample-question PDF is copyright-marked and no specific open redistribution/adaptation grant was found. Classification: **analysis-only**.
- The official exam-guide PDF is also treated as analysis-only for copied expression; official facts may be cited and paraphrased.
- The `docs.aws.amazon.com` documentation license does not automatically extend to separate `d1.awsstatic.com` exam PDFs.
- No Tier 2 licensed/openly reusable SAP-C02 question bank was found or needed.
- Authenticated AWS Skill Builder official-practice content was not accessed; its detailed style and reuse rights remain unresolved.
- No formal legal review was performed. Any verbatim or close reuse request requires authorized rights review.
- The future originality process still needs a human similarity-review protocol. Automated matching may flag risk but cannot prove independent expression.

The operative boundary is: **copy the assessment grammar, not the assessment sentences**. See [rights and reuse](../aws/sap-c02-rights-and-reuse.md) and [authored-question policy](../aws/sap-c02-authored-question-policy.md).

## Reproducibility and capabilities actually used

Research used public web search/open-page retrieval, official AWS pages/PDFs, local PowerShell download/header inspection, and SHA-256 calculation. Official sources were preferred; search-result summaries were not used when the underlying source was available. Suspicious dumps, recalled-live-question claims, actual-current-question offers, leaked keys, unauthorized scraped/commercial banks, and unverifiable derivatives were excluded without ingesting their question text.

Two official PDFs were downloaded temporarily to compute byte digests and inspect content; both files and their dedicated temporary directory were then deleted. No source snapshot, licensed copy, browser state, credential, AWS data, or private file was added to the repository. No AWS account or external mutation was used. Known source-access and dating limitations are recorded in the source register.

## Documents created

- [Assessment research](../aws/sap-c02-assessment-research.md)
- [Source register](../aws/sap-c02-source-register.md)
- [Rights and reuse](../aws/sap-c02-rights-and-reuse.md)
- [Assessment blueprint](../aws/sap-c02-assessment-blueprint.md)
- [Structured assessment blueprint](../aws/sap-c02-assessment-blueprint.json)
- [Learning architecture](../aws/sap-c02-learning-architecture.md)
- [Dependency model](../aws/sap-c02-dependency-model.md)
- [Realization plans](../aws/sap-c02-realization-plans.md)
- [Capability report](../aws/sap-c02-capability-report.md)
- [Authored-question policy](../aws/sap-c02-authored-question-policy.md)
- [0.3B pilot proposal](../aws/sap-c02-0.3b-pilot-proposal.md)
- [Subject Builder gap analysis](../aws/sap-c02-subject-builder-gap-analysis.md)
- This handoff

## Documents updated

- [Current status](../current-status.md)
- [Roadmap](../roadmap.md)
- [Project context](../project-context.md)
- [AWS SAP-C02 pilot plan](../aws-sap-c02-pilot-plan.md)

The 0.3A task did not update the README because it did not present detailed 0.3 near-term milestone status requiring correction. The subsequent 0.2B integration updated the README for its own format-0.3/E7B checkpoint.

## 0.3A-specific change boundary

The following remained unchanged **by the 0.3A research/design task itself**:

- deterministic learning core, scoring, selection, scheduling, mastery, and state mutation;
- SQLite schema and learner/runtime state;
- pack formats, schemas, fixtures, and content;
- Hermes adapter, skills, plugins, configuration, and tool contract;
- MCP installation/configuration;
- AWS account, credentials, data, resources, or billing;
- releases and tags.

The later 0.2B commits are separately attributable: they implement format-0.3 static assets, add tests and a pending E7B candidate, and update the Hermes-facing fallback workflow. They do not implement Subject Builder operations or AWS content, modify SQLite schema 1 or scoring, access AWS, configure MCP, approve the E7B candidate, or create a release/tag. The earlier working-tree caveat is therefore resolved: those changes are now reviewed as a distinct committed checkpoint rather than left as unrelated uncommitted state.

## Human decisions resolved for 0.3A closure

The repository user explicitly resolved the earlier recommendations on 2026-07-18:

1. accepted the official-source baseline and medium-confidence blueprint with stated limitations;
2. accepted task 1.4 / `SAP-ORG-04` and the two-lesson, approximately 24–30-claim, three-single/two-multiple envelope;
3. retained qualified human factual, architectural, originality, distractor, uniqueness, and pack-release review requirements;
4. selected public web/manual documentation and deferred MCP installation and AWS-account access;
5. kept content authoring, compilation, implementation, activation, and release as later explicit tasks.

## Next implementation-design boundary

The smallest useful future Subject Builder automation spine is source registration, source/rights review, blueprint drafting, deterministic structural validation, and a distinct human blueprint-approval record. Artifact serialization, SQLite ownership, pack inclusion, capability setup, and AWS-account integration remain separate decisions. See [the automation-gap analysis](../aws/sap-c02-subject-builder-gap-analysis.md).
