# Current Status

Status: pre-alpha / 0.2.0-alpha.1 and 0.2.1-alpha.1 published / SAP-C02 0.3B lesson and question human review pending
Updated: 2026-07-20

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

## Version 0.2.1-alpha.1 release

The generic format-0.3 implementation and final acceptance are complete and published as the [`v0.2.1-alpha.1` GitHub prerelease](https://github.com/amcclure1/adaptive-learning-agent/releases/tag/v0.2.1-alpha.1). The annotated tag resolves to release commit `b597401b92520a1cb7bd655cb14c94cc940cc14f`. The release includes exact version dispatch, closed ordered asset records/references, standard-library PNG framing/chunk/CRC/IHDR validation, accepted count/size/dimension limits, exact raw-byte and pack digesting, strict inventory/path/reference/rights/accessibility checks, deterministic leakage lint, core-issued `ala-pack-asset-v1` logical references, additive contract-0.1 summaries/descriptors, and the fallback-first Hermes skill. Formats 0.1/0.2, SQLite schema 1, scoring, sessions, attempts, retry, progress, and quarantine remain unchanged.

Fresh NCVEC retrieval on 2026-07-18 matched the accepted DOCX/PDF/figure hashes and still identified the fourth errata dated February 4, 2026 as current. No errata affects E7B10–E7B12 or E7-1. DOCX relationship `rId10` targets `word/media/image5.png`; the exact member is a structurally valid 796×674 PNG, 41,357 bytes, SHA-256 `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`, and visibly prints `Figure E7-1`. The separate official figure distribution supplies the review comparison.

The `us-amateur-extra-e7b` candidate contains exactly E7B10–E7B12, the one exact E7-1 member, two bounded original lessons, three original explanations, component rights, source evidence, golden records, and reviewed accessibility text. Anthony McClure reviewed the complete checklist and gave an overall PASS at `2026-07-19T03:45:57.7429288Z`. The reviewed draft digest was `9c43be04bc38910f12ddf1d90eb62e69cd916ed06fccf44c0770e6fbf2218d43`; the digest-covered approved pack is publicly valid and installable at `ac93a973ca85fbd1938ea5adbd10dc5a663126451f15b45d36ead06b3b07b826`.

Pinned Hermes v0.18.2 maps to source tag `v2026.7.7.2`. Its public ordinary-plugin contract supports JSON-string tool results but no learner-facing local-image output API. Native custom-plugin output is therefore recorded as unsupported for the pinned CLI, and the skill uses the approved text fallback without Hermes core/configuration changes or model vision. Anthony McClure authorized completion of the old E1A acceptance session. Real E7B acceptance then passed validation/install, answer-safe fallback presentation, correct scoring/provenance, fresh-process restart reconstruction, challenge quarantine, idempotent retry, and conflicting-retry rejection without Hermes configuration changes.

The offline approved-pack lifecycle passes validation/install, fallback descriptors, scoring, restart/resume, immutable retry/conflict behavior, and challenge quarantine. The 77-test standard-library suite passes locally on CPython 3.12.13, 3.13.14, and 3.14.6; hosted [GitHub Actions run 29673147507](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29673147507) passed all three jobs for the tagged release commit. Independent human review and real pinned-Hermes acceptance are PASS. Anthony McClure explicitly dispositioned a new coverage measurement as non-blocking and gave final release readiness a PASS at `2026-07-19T04:08:51.3070005Z`. The E7B acceptance session is completed and no Hermes process remains running. See [the human review package](reviews/amateur-extra-e7b-asset-content-review.md), [independent review](handoffs/amateur-extra-asset-0.2b-independent-review.md), and [release-readiness handoff](handoffs/amateur-extra-asset-0.2b-release-readiness.md).

## Next-phase architecture checkpoint

Accepted architecture now separates two future lines:

- **0.2B / 0.2.1-alpha.1** is implemented, human-approved, final-acceptance PASS, and published as a prerelease. E7B10–E7B12 and exact Figure E7-1 bytes are installable.
- **0.3A–C** progresses from assessment/curriculum research, to a manually reviewed five-question SAP-C02 slice, to agent-assisted construction with mandatory human gates.

Accepted ADRs 0010–0013 establish whole learning architecture with progressive realization, assessment authenticity and official-question reuse, capability discovery with controlled activation, and evidence-backed authored questions with layered approval. Acceptance establishes architectural direction only and does not authorize implementation.

The target Subject Builder flow distinguishes independent assessment blueprints from learning architectures, keeps architectures complete in coverage/dependencies rather than authored content, guides partial scope through visible prerequisite dispositions, researches assessment grammar automatically, seeks optional capabilities at defined planning/stage triggers, and degrades gracefully when evidence or access is insufficient. External capabilities remain optional to the core and packs.

For 0.2B, format version, PNG-only media/limits, asset/digest model, approval scopes, logical-reference boundary, Hermes fallback, and no-schema/no-new-operation boundaries are implemented and acceptance-verified. Reviewer designation, exact candidate approval, activation, Hermes/CI evidence, and the coverage disposition are complete. Other next-phase serialization, database representation, provider behavior, similarity algorithms, lifecycle persistence, and concrete modules remain deferred to their milestone-specific reviews.

See [Subject Builder architecture](subject-builder-architecture.md), [assessment policy](assessment-research-policy.md), [curriculum planning](curriculum-planning.md), [capability discovery](capability-discovery.md), [asset pilot plan](amateur-extra-asset-pilot-plan.md), and [SAP-C02 plan](aws-sap-c02-pilot-plan.md).

## Version 0.3A acceptance and 0.3B final-design checkpoint

The documentation-only 0.3A manual research and architecture exercise is accepted and closed. As verified on 2026-07-18, the current official target remains **AWS Certified Solutions Architect - Professional (SAP-C02)**. The public exam page states 180 minutes, 75 multiple-choice or multiple-response questions, Pearson VUE test-center or online-proctored delivery, and three-year certification validity. The current HTML guide supplies the four-domain/task baseline and includes emerging topics only as possible unscored content; the official PDF is version 1.2 and carries an AWS object revision timestamp of 2025-02-19. See [the assessment research](aws/sap-c02-assessment-research.md), [source register](aws/sap-c02-source-register.md), and [0.3A acceptance](handoffs/aws-sap-c02-0.3a-acceptance.md).

0.3A produced a rights classification, independent assessment blueprint, complete high-level learning architecture, cross-domain dependency model, five realization examples, capability-discovery report, evidence-backed question policy, bounded pilot proposal, and Subject Builder automation-gap analysis. Structural exam identity, domain, format, and response-rule evidence is high confidence. The overall blueprint is medium confidence because ten first-party public samples cannot establish universal scenario/distractor/difficulty behavior, official practice material was not accessed, and official sample-question reuse rights remain analysis-only pending a specific grant or authorized rights review.

The accepted 0.3B slice is Domain 1 task 1.4 / `SAP-ORG-04`, design a multi-account AWS environment: two original lessons, approximately 24-30 approved claims, and exactly five future original scenario questions (three single-response and two multiple-response). ADRs 0017-0020 are Accepted, and the implementation contract fixes the file-backed workspace, closed record schemas, canonical digests, immutable approvals and invalidation, validation reports, deterministic compiler, release-evidence manifest, format-0.2 projection, reviewer conflicts, learner-explanation boundary, and text-only default. Draft/review records remain outside installed packs and SQLite. The original design acceptance did not authorize implementation or content; the later explicit infrastructure task authorized only the generic implementation described below. See [the pilot proposal](aws/sap-c02-0.3b-pilot-proposal.md), [final design handoff](handoffs/aws-sap-c02-0.3b-final-design.md), and [design acceptance](handoffs/aws-sap-c02-0.3b-design-acceptance.md).

The explicitly authorized generic infrastructure task is complete. `adaptive_learning.authoring` now provides standard-library canonicalization, all accepted closed record schemas, confined deterministic workspace initialization, atomic draft/revision writes, immutable approvals/reviews/revocations, exact-digest current-decision resolution, fail-closed impact analysis and validation, explicit selections, deterministic pending format-0.2 candidate compilation, and external candidate/final release evidence. The separate `AuthoringOperations` facade is not registered in the ten-operation learner contract or Hermes plugin.

Only synthetic non-AWS fixtures were used to test the generic infrastructure. Real-workspace preflight exposed four generic draft-validation and project-binding cases, bringing the full local suite to 135 tests. All 135 pass on CPython 3.12.13, 3.13.14, and 3.14.6; hosted GitHub Actions also passed all three jobs in [run 29675321310](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29675321310). SQLite remains schema 1 with no authoring tables; formats 0.1/0.2/0.3, scoring, learner operations, Hermes, and MCP configuration remain unchanged. The deterministic synthetic candidate digest is `269b4e96c4ecdd1bbea58c259a05091e5c54a9f5d07b69807040745e3da2d455`; candidate release-evidence digest is `3a79af6f6717e7c4c7d75a69e774a144827cd04e0ce7ae6f8d565b0b99543cb2`. See [the infrastructure handoff](handoffs/aws-sap-c02-0.3b-authoring-infrastructure.md) and [review](handoffs/aws-sap-c02-0.3b-infrastructure-review.md).

The later source-and-claim authoring task created `authoring/aws-sap-c02-org-04/` with 14 public official-AWS source drafts and 30 atomic claim drafts: 20 documented facts, 3 service limitations, and 7 derived recommendations. A persisted deterministic report checked all 45 artifacts and returned no findings. Every source and claim decision remains pending, there are no approval records, and compilation eligibility is false. See the [authoring handoff](handoffs/aws-sap-c02-0.3b-source-and-claim-authoring.md) and [human-review package](reviews/aws-sap-c02-org-04-source-and-claim-review.md).

Accepted ADR 0021 now requires an immutable exact-digest author self-audit before deterministic validation and separate source-grounded AI verification before qualified human approval. Closed self-audit/verification/finding/resolution records, bounded operations, stale-digest gates, revision invalidation, verifier/approver conflicts, and synthetic lifecycle tests are implemented. Both machine stages remain evidence only and cannot approve, compile, install, activate, publish, or release.

The SAP-ORG-04 repeat experiment preserved baseline A and independently created baseline B without exposing baseline-A defects to the new author. Baseline A had 7 advisory findings; baseline B's first pass had 9 blocking findings, so first-pass quality did not improve. Three revision cycles produced 17 verified sources and 30 verified claims with zero residual recorded finding. The audit reconciles 21 logical findings with 30 stored records: nine immutable copies corrected workspace-commit binding and are not new defects. This demonstrates recorded-defect containment, not statistical significance, exhaustive correctness, or human approval. See the [experiment audit](experiments/sap-org-04-experiment-audit.md) and [closure](handoffs/sap-org-04-experiment-closure.md).

The generic validator projects the latest current authored revision, requires exact-digest author self-audits, enforces the closed question-spec distractor vocabulary for new drafts and current projections, and preserves immutable history. All 153 tests pass locally on CPython 3.12.13, 3.13.14, and 3.14.6. SQLite schema 1, the ten learner operations, scoring, pack formats, Hermes, and MCP configuration remain unchanged.

The separately authorized current-digest continuation is now complete. The author audit reopened all 17 official AWS sources and checked all 30 current claims, finding two material service-linked-role qualification gaps and one dependent-premise rebinding requirement. One author revision cycle created `clm-b-scp-ceiling` r2, `clm-b-scp-parent-chain` r3, and `clm-b-rec-pair-access-guardrail` r3. Exact target commit `bd84b01f3a6253ee0412823f3f30d7318652b09b` then passed deterministic validation. Two separate fresh full verification contexts each reopened all 17 URLs and reviewed all 47 current artifacts; both returned 47 verified, zero findings, and zero unresolved questions. The final closure run digest is `59d66aa533fc436a696c707c285a972a003cc91188e8e3afb6ae32b0a00959ec`.

The declared-scope matrix records 20 concepts covered, two partially covered, and GuardDuty organization administration intentionally omitted. Anthony McClure then approved all 17 exact sources and 30 exact claims at `2026-07-19T19:14:33Z` as project owner and technical reviewer, with recorded AWS architecture/source-evidence experience and no conflict preventing independent review. Source decisions bind identity, authority, rights, freshness, locator, and citation scope. Claim decisions bind full evidence, normativity, applicability, sensitivity, consistency, and objective scope; derived decisions additionally bind exact premise approvals and criteria. Post-approval deterministic validation checks 164 records with zero finding. This completes the source/claim human gate but is not separate authorization to author lessons or questions. See the [pre-human closure](handoffs/aws-sap-c02-0.3b-source-and-claim-prehuman-closure.md), [completed human-review handoff](handoffs/aws-sap-c02-0.3b-qualified-human-review-ready.md), and [concept matrix](aws/sap-c02-org-04-concept-coverage.md).

No lesson, question specification, learner-ready question, candidate pack, installation, activation, publication, release, or tag was created. Core behavior, SQLite schema 1, the ten learner operations, scoring, pack formats, Hermes, MCP configuration, AWS credentials, and AWS resources remain unchanged.

## SAP-ORG-04 lesson and question authoring checkpoint

The explicitly authorized content task produced exactly two text-only cited lessons and five original scenario questions: three single-response and two select-two. Separate specifications, stable options, keys, learner explanations, internal per-option rationales, complete requirement matrices, exact approved claim references, citations, and originality material are preserved in the Baseline-B workspace.

The author self-audit and independent-review process identified and revised complementary-key matrix semantics, overbroad lesson language, missing prerequisites, citation locators, matrix truth values, an alternate select-two pair, concrete-premise gaps, rationale/presentation issues, five specification-vocabulary defects, and three final strict-sufficiency/matrix-linkage defects. Immutable history and exact-digest response records remain preserved. The final deterministic report checked 318 artifacts and passed with only the expected 22 informational notices for human gates that remain pending.

Fresh full lesson verification completed with two low, nonblocking citation-presentation notes and no unresolved material finding. Final fresh full question verification returned all ten current specifications/questions verified, zero findings, and zero unresolved questions. The separate final adversarial uniqueness pass returned nine verified and one verified with a low, nonblocking internal possessive-encoding note; every key and select-two pair remains unique. The three prepared human packages remain distinct, and AI review grants no approval.

No candidate pack has been compiled. SQLite schema 1, ten learner operations, scoring, pack formats, Hermes, MCP configuration, credentials, and AWS resources are unchanged. Nothing was installed, activated, published, released, or tagged.

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

0.3B lesson-content, question-content, answer-uniqueness, and eventual pack-release human approvals and pack realization; the conversational Subject Builder adapter; capability configuration; expansion beyond E1A/E7B; scheduling; mastery; readiness; exam simulation; YAML; archives; export ergonomics; signing; marketplaces; broader Hermes distribution; hosted identity; servers; cloud deployment; and stronger local-process isolation remain deferred. The exact source/claim set is human-approved, but the authored lessons/questions are not an installed pack or authorization to compile, activate, or release. No MCP server, connector, AWS access, or database change was added.
