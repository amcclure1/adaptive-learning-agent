# Current Status

Status: pre-alpha / version 0.2.0-alpha.1 sourced-content pilot published as a pre-release
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

## Version 0.2B design checkpoint

The documentation-only 0.2B research/design task is complete. Fresh authoritative NCVEC review inventoried all nine current figure-dependent groups and selected E7B10–E7B12 with shared Figure E7-1. No listed errata affects E7-1. The preferred representation is provisionally the exact 796×674 PNG embedded in the current official DOCX, avoiding image conversion; import remains gated on independent identity/fidelity approval.

ADRs 0014–0016 are Accepted. They establish explicit pack format 0.3, PNG-only static local assets, the accepted format-0.3 limits, strict raw-byte and pack digesting, direct ordered references, reviewed non-leaking alt/fallback text, core-issued logical runtime references, additive responses under the existing ten-operation contract 0.1, and no SQLite schema change. Acceptance establishes architectural direction and pilot constraints only; it does not authorize implementation or content import. Later pack formats may revise media types, limits, or runtime rendering through a new decision without changing format 0.3.

Project policy treats official E7-1 geometry, labels, and question references as NCVEC public-domain pool material; this is not legal advice or formal legal review. Redistribution of the provisional exact embedded PNG remains gated on independent source mapping, visual fidelity, and project-policy approval. Native local-image delivery from a custom plugin is not verified for pinned Hermes v0.18.2. Implementation must test for a public mechanism; if unavailable, approved alt text and terminal fallback are accepted without changing Hermes core/configuration, and native rendering unavailability alone does not block the remaining format-0.3 acceptance.

See [the accepted format design](asset-pack-format-proposal.md), [pilot research](amateur-extra-asset-pilot-0.2b.md), [accessibility policy](asset-accessibility-policy.md), and [final 0.2B design handoff](handoffs/amateur-extra-asset-0.2b-final-design.md).

No official question, figure, pack field, code, test, schema, tool behavior, Hermes behavior, or release was added.

## Next-phase architecture checkpoint

Accepted architecture now separates two future lines:

- **0.2B** is an accepted, unimplemented official Amateur Extra static-asset design. E7B10–E7B12 and Figure E7-1 are selected; format 0.3 and its asset policies are accepted, and no question/figure has been imported.
- **0.3A–C** progresses from assessment/curriculum research, to a manually reviewed five-question SAP-C02 slice, to agent-assisted construction with mandatory human gates.

Accepted ADRs 0010–0013 establish whole learning architecture with progressive realization, assessment authenticity and official-question reuse, capability discovery with controlled activation, and evidence-backed authored questions with layered approval. Acceptance establishes architectural direction only and does not authorize implementation.

The target Subject Builder flow distinguishes independent assessment blueprints from learning architectures, keeps architectures complete in coverage/dependencies rather than authored content, guides partial scope through visible prerequisite dispositions, researches assessment grammar automatically, seeks optional capabilities at defined planning/stage triggers, and degrades gracefully when evidence or access is insufficient. External capabilities remain optional to the core and packs.

For 0.2B, format version, PNG-only media/limits, asset/digest model, approval scopes, logical-reference boundary, Hermes fallback, and no-schema/no-new-operation boundaries are accepted. Exact JSON Schema/code modules, reviewer designations, provisional asset identity/fidelity approval, and Hermes native presentation verification remain deferred. Other next-phase serialization, database representation, provider behavior, similarity algorithms, lifecycle persistence, and concrete modules remain deferred to their milestone-specific reviews.

See [Subject Builder architecture](subject-builder-architecture.md), [assessment policy](assessment-research-policy.md), [curriculum planning](curriculum-planning.md), [capability discovery](capability-discovery.md), [asset pilot plan](amateur-extra-asset-pilot-plan.md), and [SAP-C02 plan](aws-sap-c02-pilot-plan.md).

## Version 0.3A research checkpoint

The documentation-only 0.3A manual research and architecture exercise is complete and awaits human acceptance. As verified on 2026-07-18, the current official target remains **AWS Certified Solutions Architect - Professional (SAP-C02)**. The public exam page states 180 minutes, 75 multiple-choice or multiple-response questions, Pearson VUE test-center or online-proctored delivery, and three-year certification validity. The current HTML guide supplies the four-domain/task baseline and includes emerging topics only as possible unscored content; the official PDF is version 1.2 and carries an AWS object revision timestamp of 2025-02-19. See [the assessment research](aws/sap-c02-assessment-research.md) and [source register](aws/sap-c02-source-register.md).

0.3A produced a rights classification, independent assessment blueprint, complete high-level learning architecture, cross-domain dependency model, five realization examples, capability-discovery report, evidence-backed question policy, bounded pilot proposal, and Subject Builder automation-gap analysis. Structural exam identity, domain, format, and response-rule evidence is high confidence. The overall blueprint is medium confidence because ten first-party public samples cannot establish universal scenario/distractor/difficulty behavior, official practice material was not accessed, and official sample-question reuse rights remain analysis-only pending a specific grant or authorized rights review.

The recommended 0.3B slice is Domain 1 task 1.4 / `SAP-ORG-04`, design a multi-account AWS environment: two proposed original lessons, approximately 24-30 approved claims, and exactly five future original scenario questions (three single-response and two multiple-response). It requires human approval before content work. No lesson, claim set, learner-ready question, pack, core behavior, SQLite state, Hermes integration, MCP configuration, AWS account access, AWS resource, release, or tag was created by 0.3A. See [the pilot proposal](aws/sap-c02-0.3b-pilot-proposal.md) and [handoff](handoffs/aws-sap-c02-0.3a-research-and-architecture.md).

## Known limitations

- One local learner and at most one active session are supported; multi-user hosting and concurrent-process guarantees are absent.
- The workflow is practice only: no mastery, scheduling, readiness prediction, or exam simulation.
- E1A is one question group, not a complete Amateur Extra course or examination-preparation claim.
- There is no conversational subject builder, evidence-review administration, application backup/restore, or encryption at rest.
- Project-local Hermes discovery is trusted-checkout development behavior and requires a process-local gate.
- Compatibility is verified only for Hermes v0.18.2 Windows CLI/profile, not Linux, macOS, Desktop, gateway, or other Hermes versions.
- Formal legal review has not been claimed; the accepted rights policy is project policy, not legal advice.

## Deferred

Implementation of format 0.3/asset support, Subject Builder operations, AWS content, capability configuration, expansion beyond E1A, scheduling, mastery, readiness, exam simulation, YAML, archives, export ergonomics, signing, marketplaces, broader Hermes distribution, hosted identity, servers, cloud deployment, and stronger local-process isolation remains deferred. The 0.3A assessment/curriculum artifacts are design records, not implemented runtime objects or pack-format commitments. No MCP server, connector, AWS access, diagram content, new implemented pack field/tool, database change, or Hermes workflow change was added by the design tasks.
