# Current Status

Status: pre-alpha / 0.2.0-alpha.1 published / 0.2B final acceptance PASS and unreleased
Updated: 2026-07-19

## Released baseline

Version 0.1.0 proved the runtime-independent deterministic Python core, local SQLite state, strict portable pack input, runtime-neutral JSON tool contract, and thin Hermes adapter. The synthetic `fixture-basics` pack remains test data, not examination preparation. See [the 0.1.0 release record](releases/0.1.0.md).

## Version 0.2.0-alpha.1 release

Accepted ADR 0009 is implemented in a subject-neutral format-0.2 parser, immutable records, digest/install path, and additive contract-0.1 provenance. Format 0.1, SQLite schema 1, scoring, sessions, retries, progress, and quarantine remain unchanged.

The approved `amateur-extra-e1a` pack contains exactly two objectives, two ordered original lessons, E1A01–E1A11, zero generated questions, and no assets. Its approved digest is `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`. Anthony McClure completed all nine human-review scopes and gave an overall PASS at `2026-07-19T01:12:29.8952607Z`, including explicit acceptance of preserving the official E1A06 locator while citing the current operative rule in project prose.

Verification completed:

- Fresh authoritative NCVEC and eCFR snapshots matched the declared hashes and current revision identities.
- All eleven official records matched the fresh NCVEC DOCX exactly by ID, prompt, ordered option labels/text, answer key, and printed locator.
- The approved golden fixture detects omissions, extras, duplicate IDs, punctuation/Unicode changes, option reorder/text changes, key changes, and locator changes.
- The 45-test standard-library suite passed on CPython 3.12.13, 3.13.14, and 3.14.6; measured statement coverage was 87% (1,064 statements, 141 missed).
- Hosted GitHub Actions passed all three Python jobs for implementation commit `2c3d364df410a9408e9c4f558d23904749de5207`.
- Real pinned Hermes v0.18.2 acceptance passed validation/install, ordered lessons, answer-safe question display, confidence scoring, post-answer explanation/source display, independent restart reconstruction, challenge quarantine, and immutable retry rejection.

See [the independent-review handoff](handoffs/amateur-extra-0.2-independent-review.md) and [release-readiness handoff](handoffs/amateur-extra-0.2-release-readiness.md).

The approved pilot is published as the `v0.2.0-alpha.1` annotated tag and GitHub pre-release. See [the release record](releases/0.2.0-alpha.1.md). The Python distribution version is the PEP 440 equivalent `0.2.0a1`.

## Architecture boundary proven

- Python owns pack validation, deterministic selection and scoring, persistence, challenge quarantine, and progress counts.
- SQLite is authoritative for learner state; model conversation and agent memory are not.
- The Hermes plugin delegates exactly ten operations to the public core and owns no subject logic or storage.
- The JSON-compatible contract and Python core import no Hermes, MCP, model-provider, or network clients.
- Format 0.2 added sourced content without changing SQLite schema 1 or embedding Amateur Extra constants in the core or adapter.
- Format 0.3 adds bounded static PNG validation, exact-byte digesting, logical references, and additive descriptors without changing SQLite schema 1, scoring, or the ten-operation contract.

## Version 0.2B implementation checkpoint

The generic format-0.3 implementation and final acceptance are complete. It includes exact version dispatch, closed ordered asset records/references, standard-library PNG framing/chunk/CRC/IHDR validation, accepted count/size/dimension limits, exact raw-byte and pack digesting, strict inventory/path/reference/rights/accessibility checks, deterministic leakage lint, core-issued `ala-pack-asset-v1` logical references, additive contract-0.1 summaries/descriptors, and the fallback-first Hermes skill. Formats 0.1/0.2, SQLite schema 1, scoring, sessions, attempts, retry, progress, and quarantine remain unchanged.

Fresh NCVEC retrieval on 2026-07-18 matched the accepted DOCX/PDF/figure hashes and still identified the fourth errata dated February 4, 2026 as current. No errata affects E7B10–E7B12 or E7-1. DOCX relationship `rId10` targets `word/media/image5.png`; the exact member is a structurally valid 796×674 PNG, 41,357 bytes, SHA-256 `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`, and visibly prints `Figure E7-1`. The separate official figure distribution supplies the review comparison.

The `us-amateur-extra-e7b` candidate contains exactly E7B10–E7B12, the one exact E7-1 member, two bounded original lessons, three original explanations, component rights, source evidence, golden records, and reviewed accessibility text. Anthony McClure reviewed the complete checklist and gave an overall PASS at `2026-07-19T03:45:57.7429288Z`. The reviewed draft digest was `9c43be04bc38910f12ddf1d90eb62e69cd916ed06fccf44c0770e6fbf2218d43`; the digest-covered approved pack is publicly valid and installable at `ac93a973ca85fbd1938ea5adbd10dc5a663126451f15b45d36ead06b3b07b826`.

Pinned Hermes v0.18.2 maps to source tag `v2026.7.7.2`. Its public ordinary-plugin contract supports JSON-string tool results but no learner-facing local-image output API. Native custom-plugin output is therefore recorded as unsupported for the pinned CLI, and the skill uses the approved text fallback without Hermes core/configuration changes or model vision. Anthony McClure authorized completion of the old E1A acceptance session. Real E7B acceptance then passed validation/install, answer-safe fallback presentation, correct scoring/provenance, fresh-process restart reconstruction, challenge quarantine, idempotent retry, and conflicting-retry rejection without Hermes configuration changes.

The offline approved-pack lifecycle passes validation/install, fallback descriptors, scoring, restart/resume, immutable retry/conflict behavior, and challenge quarantine. The 77-test standard-library suite passes locally on CPython 3.12.13, 3.13.14, and 3.14.6; hosted [GitHub Actions run 29672473830](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29672473830) also passed all three jobs for approval commit `fc8cd0286ebdf052c520eee3cbf6781115e4d3d4`. Independent human review and real pinned-Hermes acceptance are PASS. Anthony McClure explicitly dispositioned a new coverage measurement as non-blocking and gave final release readiness a PASS at `2026-07-19T04:08:51.3070005Z`. The E7B acceptance session is completed and no Hermes process remains running. No release or tag has been created. See [the human review package](reviews/amateur-extra-e7b-asset-content-review.md), [independent review](handoffs/amateur-extra-asset-0.2b-independent-review.md), and [release-readiness handoff](handoffs/amateur-extra-asset-0.2b-release-readiness.md).

## Next-phase architecture checkpoint

Accepted architecture now separates two future lines:

- **0.2B** is implemented, human-approved, and final-acceptance PASS. E7B10–E7B12 and exact Figure E7-1 bytes are installable; no release or tag exists.
- **0.3A–C** progresses from assessment/curriculum research, to a manually reviewed five-question SAP-C02 slice, to agent-assisted construction with mandatory human gates.

Accepted ADRs 0010–0013 establish whole learning architecture with progressive realization, assessment authenticity and official-question reuse, capability discovery with controlled activation, and evidence-backed authored questions with layered approval. Acceptance establishes architectural direction only and does not authorize implementation.

The target Subject Builder flow distinguishes independent assessment blueprints from learning architectures, keeps architectures complete in coverage/dependencies rather than authored content, guides partial scope through visible prerequisite dispositions, researches assessment grammar automatically, seeks optional capabilities at defined planning/stage triggers, and degrades gracefully when evidence or access is insufficient. External capabilities remain optional to the core and packs.

For 0.2B, format version, PNG-only media/limits, asset/digest model, approval scopes, logical-reference boundary, Hermes fallback, and no-schema/no-new-operation boundaries are implemented and acceptance-verified. Reviewer designation, exact candidate approval, activation, Hermes/CI evidence, and the coverage disposition are complete. Other next-phase serialization, database representation, provider behavior, similarity algorithms, lifecycle persistence, and concrete modules remain deferred to their milestone-specific reviews.

See [Subject Builder architecture](subject-builder-architecture.md), [assessment policy](assessment-research-policy.md), [curriculum planning](curriculum-planning.md), [capability discovery](capability-discovery.md), [asset pilot plan](amateur-extra-asset-pilot-plan.md), and [SAP-C02 plan](aws-sap-c02-pilot-plan.md).

## Version 0.3A acceptance and 0.3B final-design checkpoint

The documentation-only 0.3A manual research and architecture exercise is accepted and closed. As verified on 2026-07-18, the current official target remains **AWS Certified Solutions Architect - Professional (SAP-C02)**. The public exam page states 180 minutes, 75 multiple-choice or multiple-response questions, Pearson VUE test-center or online-proctored delivery, and three-year certification validity. The current HTML guide supplies the four-domain/task baseline and includes emerging topics only as possible unscored content; the official PDF is version 1.2 and carries an AWS object revision timestamp of 2025-02-19. See [the assessment research](aws/sap-c02-assessment-research.md), [source register](aws/sap-c02-source-register.md), and [0.3A acceptance](handoffs/aws-sap-c02-0.3a-acceptance.md).

0.3A produced a rights classification, independent assessment blueprint, complete high-level learning architecture, cross-domain dependency model, five realization examples, capability-discovery report, evidence-backed question policy, bounded pilot proposal, and Subject Builder automation-gap analysis. Structural exam identity, domain, format, and response-rule evidence is high confidence. The overall blueprint is medium confidence because ten first-party public samples cannot establish universal scenario/distractor/difficulty behavior, official practice material was not accessed, and official sample-question reuse rights remain analysis-only pending a specific grant or authorized rights review.

The accepted 0.3B slice is Domain 1 task 1.4 / `SAP-ORG-04`, design a multi-account AWS environment: two original lessons, approximately 24-30 approved claims, and exactly five future original scenario questions (three single-response and two multiple-response). The exact proposed implementation boundary is designed: file-backed authoring records; atomic source-bound claims; distinct source, claim, question-content, uniqueness, and pack-release approvals; deterministic validation; and compilation into existing format 0.2 by default, or unchanged format 0.3 only for a separately justified supported PNG. Draft/review records remain outside installed packs and SQLite. Four focused ADRs 0017-0020 are Proposed and require later acceptance before implementation. See [the pilot proposal](aws/sap-c02-0.3b-pilot-proposal.md) and [final design handoff](handoffs/aws-sap-c02-0.3b-final-design.md).

No source/claim workspace, lesson, claim set, learner-ready question, compiler, pack, core behavior, SQLite state, Hermes change, MCP configuration, AWS account access, AWS resource, release, or tag was created by the 0.3A closure/0.3B design task.

## Known limitations

- One local learner and at most one active session are supported; multi-user hosting and concurrent-process guarantees are absent.
- The workflow is practice only: no mastery, scheduling, readiness prediction, or exam simulation.
- E1A is one question group, not a complete Amateur Extra course or examination-preparation claim.
- The approved E7B pilot is installable but is not a complete Amateur Extra course or examination-preparation claim.
- There is no conversational subject builder, evidence-review administration, application backup/restore, or encryption at rest.
- Project-local Hermes discovery is trusted-checkout development behavior and requires a process-local gate.
- Compatibility is verified only for Hermes v0.18.2 Windows CLI/profile, not Linux, macOS, Desktop, gateway, or other Hermes versions.
- Formal legal review has not been claimed; the accepted rights policy is project policy, not legal advice.

## Deferred

Publication of the final-acceptance-PASS format-0.3 E7B candidate, 0.3B authored content/workspace/compiler/approval implementation, Subject Builder operations, AWS content, capability configuration, expansion beyond E1A/E7B, scheduling, mastery, readiness, exam simulation, YAML, archives, export ergonomics, signing, marketplaces, broader Hermes distribution, hosted identity, servers, cloud deployment, and stronger local-process isolation remain deferred. The 0.3B design records and Proposed ADRs are not implemented runtime objects or pack-format commitments. No MCP server, connector, AWS access, or database change was added.
