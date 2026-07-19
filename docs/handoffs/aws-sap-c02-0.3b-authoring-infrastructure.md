# AWS SAP-C02 0.3B Generic Authoring Infrastructure Handoff

Status: implementation complete; synthetic validation only; AWS content and release remain gated
Implementation date: 2026-07-18

## Outcome

The smallest generic, deterministic, file-backed implementation of the accepted 0.3B contracts now exists under `src/adaptive_learning/authoring/`. It uses only the Python standard library and contains no AWS- or SAP-C02-specific constants. No real authoring workspace, source, claim, lesson, question, pack, credential, AWS resource, Hermes/MCP change, installation, activation, publication, tag, or release was created.

## Implementation modules

| Module | Responsibility |
|---|---|
| `authoring.canonical` | UTF-8/NFC/LF canonical JSON and Markdown, portable paths, eight-byte framing, artifact/Markdown/file-set SHA-256 digests |
| `authoring.schemas` | Closed versioned project, source, claim, lesson, question-specification, question, approval, review, validation, release-candidate, and release-evidence records |
| `authoring.workspace` | Fixed directories, safe IDs, confined paths, deterministic initialization, expected-digest drafts, immutable revisions, atomic writes, and workspace lock |
| `authoring.approvals` | Exact-target immutable decisions, author/reviewer conflicts, current-decision resolution, revocation/supersession, and invalidation impact |
| `authoring.validation` | Structured authority-free findings and persisted validation reports over explicit dates/commit fields |
| `authoring.compiler` | Closed selections, fail-closed eligibility, strict format-0.2 projection, candidate digesting, and candidate/final evidence |
| `authoring.operations` | JSON-compatible bounded facade separate from learner tools |

No dependency was added to `pyproject.toml`.

## Operation surface

`AuthoringOperations` exposes:

- `initialize_project`;
- `validate_project`;
- `add_or_update_draft`;
- `freeze_draft`;
- `calculate_artifact_digest`;
- `create_decision`;
- `analyze_impact`;
- `store_selection`;
- `validate_release_candidate`;
- `compile_approved_project`;
- `generate_release_evidence`.

The facade is configured with one trusted authoring root. Requests accept stable IDs, exact references, and closed records rather than arbitrary paths. It exposes no shell, network, Git mutation, install, activation, publication, tag, or release operation. It is not added to the runtime-neutral learner contract, learner CLI, Hermes plugin, or MCP configuration.

## Persistence and authority behavior

Initialization creates one draft `project.json` plus the accepted empty directory structure. Draft writes require the exact prior digest. Freezing creates a new immutable revision with an exact `supersedes` reference. Immutable decisions and release records use create-if-absent semantics. Revocation and supersession are new records; historical decisions remain on disk.

Approval lookup requires the exact target ID, type, revision, and digest. Source, claim, question-content, answer-uniqueness, and pack-release approvals remain distinct. Lesson-content, question-specification, and originality decisions are immutable reviews. Artifact-author self-approval and question-author uniqueness approval fail closed. Validation reports explicitly state that they imply no human approval.

## Compiler behavior

The compiler accepts only `ala.authoring.selection.v1`, exact references, an explicit timestamp, an explicit workspace-commit field, and target format 0.2. It verifies current source/claim/question/review decisions, decision dependencies, validation-report coverage, claim state, project counts, response mix, source eligibility, and projection mappings.

Output is a pending candidate, not an installable pack. It uses the unchanged format-0.2 record layout, existing internal approval-skip review hook, and existing pack digest algorithm. Public pack loading remains unchanged and rejects the pending approval. The compiler projects lesson Markdown, stems, ordered options/keys, existing response semantics, learner explanation, learner-safe citations/source summaries, rights, and notice. Claims, matrices, rationales, findings, conflict declarations, private notes, and reviewer details are excluded.

Final evidence can bind a later human pack-release approval to the immutable candidate/evidence pair. It does not alter, install, activate, publish, or release that candidate.

## Deterministic synthetic baseline

The synthetic fixture uses invented publishers, components, objectives, evidence, lesson prose, and question wording. It is test data only.

- candidate format-0.2 pack digest: `269b4e96c4ecdd1bbea58c259a05091e5c54a9f5d07b69807040745e3da2d455`;
- candidate release-evidence digest: `3a79af6f6717e7c4c7d75a69e774a144827cd04e0ce7ae6f8d565b0b99543cb2`;
- compiler-input digest: `0b1dc52c8f201cc9a188563d67450c066838fb341aead3cb9660b13b95750fc6`;
- compiler-output file-set digest: `07c00c8f3fbd17f2fccd8690111b8eb3dbe62b86f69f591f04cda23529ff60af`.

Repeated clean compilation produces byte-identical output and evidence. Changing a selected input changes the pack and evidence digests.

## Preserved boundaries

- SQLite schema remains `1`; no authoring table or learner-state workspace file exists.
- The learner contract remains version `0.1` with exactly ten operations.
- Formats 0.1, 0.2, and 0.3 parsers and public behavior are unchanged.
- Scoring, sessions, attempts, progress, retry, and challenge behavior are unchanged.
- Hermes, its configuration, skill, plugin, providers, and OAuth data are unchanged.
- MCP and AWS capabilities remain unconfigured.

## Remaining gates

AWS source registration, claim/lesson/question authoring, reviewer assignment, factual/originality/uniqueness decisions, candidate compilation, final approved pack projection, installation, activation, and release each require later explicit authority. The compiler records the caller-supplied workspace commit and validates it against selected reports; a trusted host workflow must establish Git cleanliness because the bounded authoring facade intentionally exposes no Git command surface.
