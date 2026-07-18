# MVP Requirements

Status: proposed for review  
Design baseline: 2026-07-18

Keywords MUST, MUST NOT, SHOULD, and MAY are normative.

## Runtime and installation

- **R-001** Hermes MUST be the first conversational application.
- **R-002** The learning core MUST run without importing or launching Hermes.
- **R-003** The normal project installation MUST require only an existing Hermes installation, Python, Git, and small Python dependencies. The initial dependency target is the Python standard library plus a YAML parser.
- **R-004** The project MUST NOT require a web server, separate API server, container, database service, queue, or vector store.
- **R-005** This design phase MUST NOT install packages or change Hermes configuration.
- **R-006** A runtime-neutral JSON command boundary MUST be usable directly for tests and future adapters.
- **R-007** Hermes integration MUST be a thin adapter that translates Hermes tool calls to the runtime-neutral boundary.

Acceptance: core tests can run with a fake clock and temporary SQLite database without Hermes installed; adapter tests use a fake Hermes registration context.

## Learners and sessions

- **L-001** A local installation MUST support one or more named learner profiles without implying hosted multi-tenancy.
- **L-002** A learner MUST be able to start, resume, and finish a study session against one exact pack version.
- **L-003** The core MUST choose the next question deterministically from due items, objective priority, prior exposure, and a seeded tie-breaker.
- **L-004** Presenting a question MUST persist its ID, content hash, and session ordinal before an answer is accepted.
- **L-005** Submitting an answer MUST atomically write the attempt and all affected progress rows.
- **L-006** Retrying the same mutating request with the same idempotency key MUST return the original result without a second state change.
- **L-007** Learners MUST be able to view pack, objective, coverage, due-item, and calibration summaries.
- **L-008** A user MUST be able to export or back up operational learner data separately from pack export.

## Deterministic assessment

- **S-001** Python MUST score every MVP question. The agent MUST NOT provide or override a score.
- **S-002** MVP question types MUST be limited to deterministic forms: single choice, multiple choice, numeric, and normalized short answer.
- **S-003** Each attempt MUST record the scoring-rule version, normalized response, result, confidence, timestamps, and relevant question hash.
- **S-004** Mastery and scheduling transitions MUST be versioned, documented, and reproducible from the attempt stream.
- **S-005** The system MUST use integer fixed-point values for stored scores and mastery to avoid platform-dependent floating-point drift.
- **S-006** Pack updates MUST NOT silently reinterpret historical attempts; attempts remain bound to their original pack version and question hash.
- **S-007** Explanations MAY be conversationally rephrased, but the score, accepted answer, and cited rationale MUST originate from the validated pack.
- **S-008** Open-ended model grading MAY be explored later only as non-authoritative feedback and is outside the MVP score.

## Subject packs

- **P-001** A pack MUST be a versioned directory containing YAML metadata/structured content and Markdown lessons or notes.
- **P-002** A pack MUST use stable, pack-scoped IDs for objectives, questions, sources, and reviews.
- **P-003** A pack archive MUST contain no executable code, symlinks, absolute paths, path traversal, secrets, or learner data.
- **P-004** Validation MUST be available without installing the pack.
- **P-005** Installation MUST verify structure, schema version, identifiers, references, evidence policy, review gates, archive limits, and a canonical content digest.
- **P-006** Installed packs MUST be immutable by `(pack_id, version, digest)`. A changed digest requires a new version or explicit rejection as tampering.
- **P-007** Export MUST create a deterministic archive from validated canonical files and MUST exclude drafts, caches, databases, and runtime files.
- **P-008** The pack format MUST NOT mention Hermes tools or rely on Hermes prompts.
- **P-009** Unknown optional fields SHOULD be retained on round-trip; unknown required schema versions MUST fail clearly.
- **P-010** The MVP MUST support the AWS SAP-C02 and US Amateur Extra pilot packs.

## Conversational authoring and review

- **A-001** A user MUST be able to create a draft pack, add objectives, sources, Markdown content, and questions through tool calls made in conversation.
- **A-002** Agent-authored content MUST enter a draft state; no tool may publish it autonomously.
- **A-003** Every mutation MUST run structural validation immediately and return actionable diagnostics.
- **A-004** The author MUST be able to preview a question without exposing the answer key in learner mode.
- **A-005** A human MUST explicitly accept or reject each required question review.
- **A-006** Release export MUST require a clean validation result and all policy-required reviews.
- **A-007** The authoring workflow MUST record who attested to a review, when, against which content digest, and with what outcome.
- **A-008** Local identity is an attestation label, not cryptographic proof; the UI and metadata MUST not claim otherwise.

## Evidence and safety

- **E-001** Packs MUST declare evidence mode as `none`, `recommended`, or `required`.
- **E-002** In `required` mode, every scored question MUST cite at least one allowed authoritative source and have an accepted review bound to its current digest.
- **E-003** Source records MUST include title, publisher, locator, authority class, retrieval date, and applicability/version notes.
- **E-004** The validator MUST flag missing, stale, superseded, inaccessible, or disallowed evidence according to pack policy.
- **E-005** Automatic URL retrieval MAY assist authoring but MUST NOT itself make a source authoritative or a question approved.
- **E-006** Agent memory and prior chat content MUST NOT satisfy an evidence requirement.
- **E-007** Packs MUST support effective and review-by dates so time-sensitive content can be blocked or warned.
- **E-008** Generated questions MUST be checked for answerability, answer correctness, distractor quality, objective alignment, evidence traceability, and prohibited copied content.

## Persistence, privacy, and resilience

- **D-001** SQLite MUST be the only operational data store.
- **D-002** Foreign keys MUST be enabled; mutating operations MUST use explicit transactions.
- **D-003** The database MUST maintain a schema version and forward-only migrations with backup guidance.
- **D-004** Pack files MUST remain the source of truth for pack content; SQLite MAY cache installation metadata and digests only.
- **D-005** Logs MUST avoid answer keys, OAuth tokens, secrets, and unnecessary raw learner responses.
- **D-006** The system MUST remain usable offline after Hermes/model access is unavailable for direct JSON/CLI operations such as validation, scoring fixtures, status, export, and backup. Conversation itself still depends on the configured model provider.
- **D-007** A corrupted or missing pack MUST not erase learner history; the tool MUST return a typed recovery error.
- **D-008** Database backup and restore MUST use SQLite-safe mechanisms rather than copying a live database blindly.

## Quality gates

- **Q-001** All deterministic behavior MUST have clock-controlled unit tests.
- **Q-002** The test suite MUST include malformed and hostile pack fixtures.
- **Q-003** Pack validation and export MUST be reproducible on Windows, macOS, and Linux path semantics.
- **Q-004** Each pilot pack MUST pass schema, evidence, review, install, study, and export round-trip tests.
- **Q-005** Hermes-specific behavior MUST be documented with official Hermes sources; unverified integration assumptions MUST be labeled.

