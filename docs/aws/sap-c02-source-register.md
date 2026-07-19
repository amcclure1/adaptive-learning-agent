# SAP-C02 Source Register

Status: draft 0.3A research artifact; human review required

Research date: 2026-07-18 (America/Chicago)

Register version: 0.3A.1

This register is the authoritative source inventory for the manual 0.3A exercise. `Retrieved` means the page or file was inspected on the research date. No source snapshot is committed. The two PDF digests were calculated from ephemeral downloads, and the temporary files and dedicated temporary directory were deleted after inspection. Authority and reuse are separate classifications.

## Assessment and policy sources

| Source ID | Title / publisher | URL | Retrieved | Publication or revision | Category | Snapshot / digest | Intended use | Authority | Rights and reuse |
|---|---|---|---|---|---|---|---|---|---|
| AWS-CERT-001 | AWS Certified Solutions Architect - Professional / AWS | [official certification page](https://aws.amazon.com/certification/certified-solutions-architect-professional/) | 2026-07-18 | No revision date displayed | Certification page | Not retained | Current name, format, duration, languages, delivery, validity | Tier 1 | Reference-only under AWS Site Terms |
| AWS-CERT-002 | AWS Certified Solutions Architect - Professional (SAP-C02), HTML exam guide / AWS | [current HTML guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html) | 2026-07-18 | No revision date displayed; current page includes an Emerging Topics section absent from the version-1.2 PDF | Exam guide | Not retained | Current identity, candidate, response rules, scoring, domains, tasks, emerging pretest topics | Tier 1 | AWS documentation is CC BY-SA 4.0 under [AWS Site Terms](https://aws.amazon.com/terms/); attribution/share-alike required for copied documentation text |
| AWS-CERT-003 | AWS Certified Solutions Architect - Professional (SAP-C02) Exam Guide, version 1.2 / AWS | [official PDF](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf) | 2026-07-18 | PDF says version 1.2; HTTP `Last-Modified` 2025-02-19T22:00:24Z and `x-amz-meta-version` 2025-02-19T21:59:27.773Z | Exam guide PDF | Not retained; SHA-256 `e11f5a66162786ad41a62985f4c3da0f040cb5f080741c72b58650f11addeb7a` | Versioned baseline, locators, domain/task text, in-scope service list | Tier 1 | Analysis/reference-only for this project; no PDF-specific redistribution grant was found |
| AWS-CERT-004 | AWS Certified Solutions Architect - Professional (SAP-C02) Sample Exam Questions / AWS | [official PDF](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf) | 2026-07-18 | Copyright 2022; HTTP `Last-Modified` 2023-12-15T13:53:31Z | Ten official sample questions and rationales | Not retained; SHA-256 `f9c8d0cfa40f0a6d5672c941cc6eb0a5daec06ceb9f56e185e8e9effeb4754f6` | Assessment-style analysis only | Tier 1 | **Analysis-only**; PDF says all rights reserved and no redistribution permission was found |
| AWS-CERT-005 | After Testing / AWS Certification | [policy page](https://aws.amazon.com/certification/policies/after-testing/) | 2026-07-18 | No revision date displayed | Scoring and retake policy | Not retained | Scaled scoring, passing standard, results, retakes | Tier 1 | Reference-only |
| AWS-CERT-006 | Recertification / AWS Certification | [policy page](https://aws.amazon.com/certification/policies/recertification/) | 2026-07-18 | No revision date displayed | Certification policy | Not retained | Three-year validity and Professional recertification | Tier 1 | Reference-only |
| AWS-CERT-007 | AWS Certified Solutions Architect - Professional content outline updated / AWS Training and Certification Blog | [official announcement](https://aws.amazon.com/blogs/training-and-certification/aws-certified-solutions-architect-professional-content-outline-updated-to-align-with-latest-trends-and-innovations/) | 2026-07-18 | 2022-10-18 | Effective-date announcement | Not retained | SAP-C02 first test date and SAP-C01 last date | Tier 1 | Reference-only |
| AWS-CERT-008 | New courses and updates, November 2022 / AWS Training and Certification Blog | [official announcement](https://aws.amazon.com/blogs/training-and-certification/new-courses-and-updates-from-aws-training-and-certification-in-november-2022/) | 2026-07-18 | 2022-11-15 | Exam/preparation announcement | Not retained | Corroborate updated exam availability and official practice resources | Tier 1 | Reference-only |
| AWS-CERT-009 | 5 tips for AWS Certification exams / AWS Training and Certification Blog | [official preparation guidance](https://aws.amazon.com/blogs/training-and-certification/5-tips-for-aws-certification-exams-from-aws-solutions-architects/) | 2026-07-18 | 2023-02-20 | Official preparation guidance | Not retained | Official practice-set purpose, elimination, concept rather than verbatim recurrence | Tier 1 | Style evidence only; reference-only |
| AWS-CERT-010 | AWS Certification Program Agreement / AWS | [agreement](https://aws.amazon.com/certification/certification-agreement/) | 2026-07-18 | Current page; no version retained | Certification integrity and validity | Not retained | Prohibited unauthorized content and three-year validity | Tier 1 | Reference-only |
| AWS-LEGAL-001 | AWS Site Terms / AWS | [terms](https://aws.amazon.com/terms/) | 2026-07-18 | Last updated 2025-06-04 | Rights policy | Not retained | Site-content restrictions and docs.aws.com CC BY-SA 4.0 / MIT-0 rule | Tier 1 | Governing rights source |

## Architecture and pilot knowledge sources

| Source ID | Title / publisher | URL | Retrieved | Publication or revision | Category | Snapshot | Intended use | Authority | Rights and reuse |
|---|---|---|---|---|---|---|---|---|---|
| AWS-ARCH-001 | AWS Well-Architected Framework / AWS | [framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) | 2026-07-18 | Publication date 2024-11-06 | Architecture guidance | Not retained | Cross-pillar tradeoff method and quality attributes | Official factual/guidance | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-ARCH-002 | Organizing Your AWS Environment Using Multiple Accounts / AWS | [whitepaper](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/aws-organizations.html) | 2026-07-18 | Living documentation; no date displayed on inspected page | Multi-account architecture | Not retained | OU/account design and cross-account governance | Official guidance | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-ORG-001 | Service control policies / AWS Organizations | [user guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | SCP semantics and boundaries | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-ORG-002 | Best practices for the management account / AWS Organizations | [user guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html) | 2026-07-18 | Living documentation; includes a dated 2026-07-10 default-control note | Service guidance | Not retained | Management-account isolation and delegation | Official guidance | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-CT-001 | What is AWS Control Tower? / AWS | [user guide](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Landing-zone, account-factory, and control concepts | Official factual/guidance | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-IIC-001 | Configure access to AWS accounts / AWS IAM Identity Center | [user guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Central multi-account workforce access | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-CTRAIL-001 | Creating a trail for an organization / AWS CloudTrail | [user guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Organization-wide event logging | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-CONFIG-001 | Multi-Account Multi-Region Data Aggregation / AWS Config | [developer guide](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Central read-only configuration/compliance aggregation | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-SH-001 | Central configuration in Security Hub CSPM / AWS | [user guide](https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Delegated, cross-account security configuration | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-RAM-001 | What is AWS Resource Access Manager? / AWS | [user guide](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html) | 2026-07-18 | Living documentation | Service documentation | Not retained | Cross-account resource-sharing tradeoffs | Official factual | CC BY-SA 4.0 documentation; cite and paraphrase |
| AWS-SRA-001 | AWS Security Reference Architecture / AWS | [prescriptive guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/introduction.html) | 2026-07-18 | Document history December 2025 | Reference architecture | Not retained | Security-account and delegated-administration context | Official guidance | CC BY-SA 4.0 documentation; cite and paraphrase |

## Capability sources

| Source ID | Title / provider | URL | Retrieved | Publication or revision | Category | Snapshot | Intended use | Authority | Rights and reuse |
|---|---|---|---|---|---|---|---|---|---|
| CAP-AWS-001 | Agent Toolkit for AWS: AWS MCP Server / AWS | [user guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html) | 2026-07-18 | Current GA documentation; GA announced 2026-05-06 | Managed MCP capability | Not retained | Documentation search, regional availability, optional authenticated API access | Official provider | Reference-only; returned content retains source rights |
| CAP-AWS-002 | AWS Knowledge MCP Server / AWS Labs | [provider documentation](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server) | 2026-07-18 | Living documentation | Remote public MCP | Not retained | Public AWS knowledge/document search without an AWS account | Official provider | Reference-only; returned content retains source rights |
| CAP-AWS-003 | AWS Documentation MCP Server / AWS Labs | [provider documentation](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server) | 2026-07-18 | Living documentation | Local open-source MCP | Not retained | Search/read official AWS documentation | Official provider | Server code Apache-2.0; returned documentation retains source rights |
| CAP-AWS-004 | AWS API MCP Server / AWS Labs | [provider documentation](https://awslabs.github.io/mcp/servers/aws-api-mcp-server) | 2026-07-18 | Page says superseded by official AWS MCP Server | Local authenticated MCP | Not retained | Future private AWS inspection or mutation only | Official provider, superseded | Not recommended for new setup |
| CAP-AWS-005 | Document Loader MCP Server / AWS Labs | [provider documentation](https://awslabs.github.io/mcp/servers/document-loader-mcp-server) | 2026-07-18 | Living documentation | Local document processing MCP | Not retained | Optional structured PDF/DOCX extraction | Official provider | Server code Apache-2.0; input-content rights remain separate |
| CAP-HERMES-001 | MCP feature guide at Hermes tag `v2026.7.7.2` / Nous Research | [tagged guide](https://raw.githubusercontent.com/NousResearch/hermes-agent/v2026.7.7.2/website/docs/user-guide/features/mcp.md) | 2026-07-18 | Hermes package 0.18.2, release 2026-07-07 | Runtime compatibility | Not retained | Verify stdio/HTTP transport and filtering support in the selected runtime | Official provider/version | Repository license applies; reference-only here |
| CAP-LOCAL-001 | Invoke-WebRequest / Microsoft | [PowerShell documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.6) | 2026-07-18 | PowerShell 7.6 documentation | Local retrieval utility | Not retained | Reproducible source retrieval | Official provider | Reference-only |
| CAP-LOCAL-002 | Get-FileHash / Microsoft | [PowerShell documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.5) | 2026-07-18 | PowerShell 7.5 documentation | Local digest utility | Not retained | SHA-256 calculation | Official provider | Reference-only |

## Search and rejection log

Searches began with the official certification page and current AWS exam-guide index, then followed official links to the HTML/PDF guide, sample PDF, policies, preparation guidance, service documentation, Architecture Center/Well-Architected guidance, and provider documentation for capabilities. Search-result summaries were used only to locate underlying official pages.

Excluded without inspection or retention:

- domains or snippets advertising “actual exam questions,” “dumps,” “latest dumps,” guaranteed pass banks, or recalled questions;
- scraped mirrors of official/commercial banks;
- candidate recollections, answer keys, or discussion that purported to reveal live items;
- commercial practice content without an explicit license suitable for this project;
- sources whose publisher or provenance could not be verified.

No Tier 2 reusable assessment-question source was found. No Tier 3 source was needed to establish the blueprint; official evidence was sufficient for a qualified, medium-confidence style model.

## Reproducibility and limitations

- Live capabilities used: the session's public web search/browser, PDF text inspection, PowerShell, `curl` HTTP-header inspection, and Git/local file tools.
- No MCP server, connector, plugin, or skill was installed or configured.
- No AWS account, AWS credential, private Skill Builder content, or paid practice exam was accessed.
- The official practice question set named on the certification page was not opened because it requires the Skill Builder application/account path. This limits style evidence to the public ten-question official sample and official preparation descriptions.
- The current HTML guide contains an Emerging Topics section that is absent from the version-1.2 PDF. AWS exposes no revision date on the HTML page. The baseline therefore pins both the versioned PDF and the dated retrieval of the current HTML overlay.
- PDF snapshots were not retained. The recorded hashes identify the exact bytes inspected on 2026-07-18 but do not grant redistribution rights.
