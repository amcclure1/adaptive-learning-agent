# SAP-C02 Capability Discovery Report

Status: accepted discovery report; public retrieval selected and all setup deferred

Research date: 2026-07-18

Selected runtime compatibility baseline: Hermes 0.18.2 (`v2026.7.7.2`)

## Roles sought

1. authoritative AWS documentation search;
2. exam-guide and official-sample retrieval;
3. source snapshotting and SHA-256 digests;
4. freshness and revision checks;
5. claim verification and architecture-guidance retrieval;
6. PDF/diagram inspection and structured extraction;
7. general web research and local document processing;
8. future private AWS environment inspection;
9. future hands-on lab execution.

0.3A used only Level 0 public web/browser/PDF capabilities and local read/write utilities. It did not need or request AWS credentials.

## Candidate matrix

| ID | Candidate / provider | Roles | Lifecycle | Permission | Recommendation |
|---|---|---|---|---|---|
| CAP-01 | Ordinary official-site browser/search / current agent runtime | 1, 2, 4, 5, 7 | recommended | Level 0 | Keep as universal fallback and citation verifier |
| CAP-02 | PowerShell retrieval + SHA-256 / Microsoft | 2, 3, 4, 7 | recommended | Level 0 | Use for approved ephemeral snapshots/digests; already locally available |
| CAP-03 | Managed AWS MCP Server, documentation-only mode / AWS | 1, 4, 5 | recommended | Level 0 in knowledge-only mode | Best optional 0.3B/0.3C addition after explicit setup approval |
| CAP-04 | AWS Knowledge MCP Server / AWS | 1, 4, 5 | discovered | Level 0 | Useful alternate remote search; not needed alongside CAP-03 initially |
| CAP-05 | AWS Documentation MCP Server / AWS Labs | 1, 4, 5 | discovered | Level 0 | Local stdio fallback if remote knowledge search is unsuitable |
| CAP-06 | Hermes 0.18.2 MCP client / Nous Research | Runtime host for 3-5 | discovered | Level 0 for public providers | Transport-compatible on paper; provider combinations remain untested |
| CAP-07 | AWS Skill Builder official practice material / AWS | Assessment-style calibration | discovered | Level 1 (account/private session) | Optional human-only style review; defer until user authorizes access |
| CAP-08 | Document Loader MCP Server / AWS Labs | 6, 7 | discovered | Level 0 for public/local authorized files | Defer; current browser/PDF extraction is sufficient |
| CAP-09 | Managed AWS MCP Server authenticated API mode / AWS | 8 and possible mutation | discovered | Level 1-3 by operation | Defer; unnecessary for 0.3B content pilot |
| CAP-10 | AWS Skill Builder Builder Labs or a dedicated AWS sandbox / AWS | 9 | discovered | Level 2 or 3 | Defer; not required for first five-question pilot |

Lifecycle labels are deliberately limited to `discovered` and `recommended`. None is marked approved, configured, healthy, unavailable, or revoked.

## Candidate records

### CAP-01 — Official-site browser/search

- **Official source:** the authoritative targets in the [source register](sap-c02-source-register.md), especially AWS certification and documentation pages.
- **Compatibility/install:** browser- and runtime-neutral; no repository dependency or MCP configuration.
- **Authentication/data:** none for public pages; queries and requested URLs leave the local machine through the active research provider.
- **Behavior/side effects/cost:** read-only network requests; no AWS resources; no direct AWS charge. Provider/network terms still apply.
- **Least privilege:** restrict research to public official domains; treat results as untrusted until the underlying page is opened.
- **Health check:** open the current exam guide, verify title/code, and retrieve a cited section.
- **Fallback/removal:** manual browser retrieval or user-supplied authorized source; disable the runtime's web access. Nothing to uninstall.

### CAP-02 — Local snapshot and digest utilities

- **Official source:** [Invoke-WebRequest](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.6) retrieves HTTP content; [Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.5) computes file hashes and defaults to SHA-256.
- **Compatibility/install:** available in the current Windows/PowerShell environment; no new dependency.
- **Authentication/data:** public URLs only for this task; retrieved bytes are written to an explicit temporary directory.
- **Behavior/side effects/cost:** local temporary writes and public HTTP reads; no AWS resource mutation or AWS account cost.
- **Least privilege:** explicit URLs, explicit temporary path, SHA-256, no credential/session persistence, no repository snapshot unless rights and need are approved.
- **Health check:** retrieve a known official file, require nonzero length, and calculate a 64-hex-character SHA-256.
- **Fallback/removal:** `curl` plus a trusted local SHA-256 utility; delete only the exact temporary snapshot after verification. Built-in utility is not uninstalled.

### CAP-03 — Managed AWS MCP Server, knowledge-only mode

- **Provider/source:** AWS; [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html), [tool list](https://docs.aws.amazon.com/aws-mcp/latest/userguide/understanding-mcp-server-tools.html), and [GA announcement dated 2026-05-06](https://aws.amazon.com/about-aws/whats-new/2026/05/aws-mcp-server/).
- **Roles:** current AWS documentation search/read, recommendations, regional availability, and claim-source discovery.
- **Runtime compatibility:** AWS says it works with MCP-compatible agents; Hermes 0.18.2 documents remote HTTP MCP support and tool filtering. Hermes is not listed in AWS setup examples, so this combination is a **reasonable transport-level inference, not verified compatibility**. [Tagged Hermes guide](https://raw.githubusercontent.com/NousResearch/hermes-agent/v2026.7.7.2/website/docs/user-guide/features/mcp.md)
- **Authentication/data:** AWS documentation search and service information are documented as available without authentication. Queries are sent to AWS's managed endpoint. API calls, scripts, and skills require IAM credentials. [AWS MCP overview](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html)
- **Read/write/effects:** knowledge tools are public read-only. The same server also exposes authenticated API and script tools capable of external effects, so the later setup must expose only knowledge tools for Level 0 research.
- **Cost:** Agent Toolkit has no additional charge; authenticated resource interactions incur normal AWS charges. Knowledge-only mode should create no AWS resources. [Agent Toolkit pricing](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html)
- **Installation:** remote endpoint configuration; no server package. Configuration still requires explicit user approval under project policy.
- **Least privilege:** no credentials; whitelist `search_documentation`, `read_documentation`, `recommend`, `list_regions`, and `get_regional_availability`; exclude API/script/presigned-URL/task tools; disable sampling if not needed.
- **Health check:** connect, list only approved tools, search for the current SAP-C02 guide, retrieve the official URL, and confirm no credentials were requested.
- **Fallback:** CAP-01, CAP-04, or CAP-05.
- **Disable/removal:** disable/remove the exact `mcp_servers` entry and restart/reload MCP. No AWS credentials should exist in Level 0 mode.

### CAP-04 — AWS Knowledge MCP Server

- **Provider/source:** AWS; [official AWS Labs documentation](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server).
- **Roles:** remote search across AWS documentation, What's New, architectural references, Well-Architected guidance, samples, and other official content.
- **Compatibility:** Streamable HTTP endpoint. Hermes 0.18.2 supports remote HTTP; exact handshake/tool-schema health is untested.
- **Authentication/data:** no AWS account or authentication; rate limited; public queries sent to AWS. AWS states collected telemetry is not used for ML training.
- **Behavior/effects/cost:** public read-only network access; no AWS resource mutation; no stated direct charge.
- **Installation:** add remote endpoint, or use a local `fastmcp` proxy if the client lacks HTTP. Hermes has HTTP support, so the proxy should not be the default.
- **Least privilege/permission:** Level 0; no credentials; whitelist documentation tools.
- **Health check:** `tools/list`, a current-guide search, and retrieval with official URL/citation.
- **Fallback/removal:** CAP-01 or CAP-05; disable/remove config entry. No package to uninstall in direct HTTP mode.
- **Recommendation:** discovered, not initially recommended because CAP-03 is the newer unified AWS-managed option.

### CAP-05 — AWS Documentation MCP Server

- **Provider/source:** AWS Labs; [official documentation](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server); Apache-2.0 server code.
- **Roles:** search/read AWS documentation, read sections, and recommendations.
- **Compatibility/install:** local stdio; requires `uv` and Python 3.10+. Hermes 0.18.2 supports stdio. Exact Windows/Hermes health is untested.
- **Authentication/data:** no AWS credentials; local server sends public documentation queries/URLs to AWS.
- **Behavior/effects/cost:** local subprocess and network reads; local package/cache writes during installation; no AWS resource mutation or direct AWS charge.
- **Least privilege:** exact package/version, global AWS partition, no credentials, tool whitelist, explicit environment, reviewed upstream source.
- **Health check:** server start, `tools/list`, official guide search/read, correct partition, clean shutdown.
- **Fallback/removal:** CAP-01/CAP-03; remove Hermes entry and uninstall the exact `uv` tool/cache only in an authorized setup-removal task.
- **Recommendation:** discovered fallback; a new local dependency is not justified for the first pilot while public web and CAP-03 suffice.

### CAP-06 — Hermes 0.18.2 MCP client

- **Provider/source:** Nous Research; [tagged version-specific guide](https://raw.githubusercontent.com/NousResearch/hermes-agent/v2026.7.7.2/website/docs/user-guide/features/mcp.md).
- **Roles:** hosts optional stdio or remote HTTP capabilities, discovers tools, filters per server, and can disable resource/prompt wrappers.
- **Authentication/data/effects:** varies by server. Hermes configuration can hold endpoint/header/auth details outside packs; installing a catalog entry may run bootstrap/install code, so catalog presence is not permission.
- **Cost/install:** MCP support ships in the standard 0.18.2 install according to the tagged guide. Server-specific costs and setup remain separate.
- **Least privilege:** use exact server config, `enabled: false` until approval, include-list read-only tools, omit secrets for public research, and review server source/bootstrap.
- **Health check:** connect/reload, verify expected prefixed tools only, run a read-only source lookup, inspect error logs, then stop.
- **Fallback/removal:** use direct web/local tools; disable/remove server configuration and any separately installed server package.
- **Recommendation:** discovered as a runtime route, not marked healthy for any AWS MCP provider in this task.

### CAP-07 — AWS Skill Builder official practice material

- **Provider/source:** AWS; the [certification page](https://aws.amazon.com/certification/certified-solutions-architect-professional/) links the Official Practice Question Set and Official Practice Exam.
- **Roles:** improve scenario/distractor/difficulty calibration through a qualified human review.
- **Authentication/data:** AWS Builder/Skill Builder account and private session; the practice exam may require a subscription. Account identifiers, responses, and progress are private data.
- **Behavior/effects/cost:** read/answer activity changes external learner progress; subscription may cost money. Treat as Level 1 for viewing and Level 2 for submitting activity if it records progress.
- **Install/compatibility:** web application; no MCP needed. Not suitable for automated scraping or source export.
- **Least privilege:** human opens the official set, records only aggregate/non-expressive style characteristics, and copies no item text/key.
- **Health check:** authorized human confirms target is SAP-C02 and records current title/date/terms without exposing private content.
- **Fallback/removal:** retain current medium-confidence blueprint; sign out/revoke session according to AWS account controls.
- **Recommendation:** optional for 0.3B, only with explicit user authorization; not required to proceed.

### CAP-08 — Document Loader MCP Server

- **Provider/source:** AWS Labs; [official provider page](https://awslabs.github.io/mcp/servers/document-loader-mcp-server).
- **Roles:** structured extraction from PDF, DOCX, spreadsheets, presentations, and images.
- **Authentication/data:** local/public files, potentially transmitted or processed according to server implementation; must not receive private/licensed documents without approval.
- **Behavior/effects/cost/install:** local package/process and file reads; installation required; no demonstrated MVP need for current public PDFs.
- **Permission/least privilege:** Level 0 for public authorized files in a dedicated directory; higher if private files are supplied.
- **Health/fallback/removal:** parse a benign official PDF and compare locators; fall back to browser/PDF text extraction; remove exact config/package in an authorized task.
- **Recommendation:** discovered and deferred.

### CAP-09 — Managed AWS MCP authenticated API mode

- **Provider/source:** AWS; [setup/authentication guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html) and [IAM behavior](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html).
- **Roles:** future environment inspection and optional lab operations.
- **Authentication/data:** OAuth or SigV4/IAM; private account configuration and results. AWS documents existing IAM policies as the downstream authorization boundary.
- **Behavior/effects/cost:** can call AWS APIs and run scripts; may read, create, change, or delete resources and incur normal service costs. Permission level is Level 1 for a strictly read-only operation, Level 2 for mutation, and Level 3 for production/destructive/costly work.
- **Install:** remote OAuth can avoid a proxy; SigV4 commonly uses `mcp-proxy-for-aws`. Hermes-specific OAuth/SigV4 compatibility is unverified.
- **Least privilege:** dedicated sandbox account/role, temporary credentials, explicit service/resource/Region allowlist, MCP condition keys, read-only tool filtering when possible, budgets, and operation-specific consent.
- **Health check:** only after authorization, use caller identity and a harmless allowed read; verify CloudTrail and no unexpected tools/actions.
- **Fallback/removal:** user-provided sanitized architecture description or manual console lab; revoke sessions/role trust, remove config/proxy, and verify credentials are gone.
- **Recommendation:** defer; no AWS account access is needed for the first content pilot.

### CAP-10 — AWS labs/sandbox

- **Provider/source:** the [certification page](https://aws.amazon.com/certification/certified-solutions-architect-professional/) identifies Builder Labs, Cloud Quest, and SimuLearn as preparation options.
- **Roles:** later hands-on validation of implementation behavior, not authoritative exam-style evidence.
- **Authentication/data/effects/cost:** authenticated learning or AWS environment; creates/changes lab resources and records progress; subscription and resource charges may apply depending on option.
- **Permission:** Level 2 in an isolated managed lab; Level 3 for personal/production accounts or material cost.
- **Least privilege:** provider-managed lab or dedicated sandbox, fixed budget/time, no production data, teardown instructions.
- **Health/fallback/removal:** run provider's benign starting check; fall back to architecture walkthroughs; terminate lab, verify teardown, sign out/revoke access.
- **Recommendation:** unnecessary for 0.3B; revisit only if 0.3C adds validated hands-on objectives.

## User-facing recommendation

Safest sequence for 0.3B/0.3C:

1. Keep ordinary official web research and local SHA-256 snapshotting as the baseline; neither needs AWS authentication.
2. If faster, more structured AWS research is desired, explicitly approve a **knowledge-only** managed AWS MCP Server configuration with no credentials and a strict tool include-list. Test it against Hermes 0.18.2 before calling it healthy.
3. Optionally authorize a human-only Skill Builder practice-set review to raise style confidence; record characteristics, never question text.
4. Defer AWS account inspection, authenticated MCP/API tools, document-loader installation, and labs. They do not materially improve the first five-question multi-account content pilot.
5. If later hands-on validation becomes an approved goal, prefer a dedicated sandbox/managed lab before any personal or production account and approve exact cost/teardown boundaries.

No capability was installed, configured, authenticated, or health-tested by 0.3A.
