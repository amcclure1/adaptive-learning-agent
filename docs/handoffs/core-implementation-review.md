# Core Implementation Compatibility Review

Date: 2026-07-18
Reviewed implementation HEAD: `05b468fa5a7b3da9e87e94b98bd4b9e07060f762`
Commit immediately before implementation: `5a3990b74ea90aa4853c0e33f71fa29f68a36e84`
Exact reviewed range: `5a3990b74ea90aa4853c0e33f71fa29f68a36e84..05b468fa5a7b3da9e87e94b98bd4b9e07060f762`

## Implementation commits

In order:

1. `e60bab5` — `docs: clarify core vertical slice behavior`
2. `13b343e` — `feat: add pack model and validation`
3. `02b00f3` — `feat: add sqlite storage and schema`
4. `be87556` — `feat: add deterministic study operations`
5. `0d21eef` — `test: cover mvp vertical slice`
6. `f2b9dd9` — `test: verify core runtime independence`
7. `05b468f` — `docs: record core implementation handoff`

## Changed files

The range changed 27 files:

- Governance and project status: `AGENTS.md`, `CHANGELOG.md`, `README.md`, `docs/current-status.md`, `docs/project-context.md`, and `docs/mvp-vertical-slice.md`.
- Handoff: `docs/handoffs/core-implementation-0.1.md`.
- Packaging: `pyproject.toml`.
- Fixture pack: `packs/README.md`, `packs/fixture-basics/pack.json`, and `packs/fixture-basics/lesson.md`.
- Reserved-area notes: `schemas/README.md` and `skills/adaptive-learning/README.md`.
- Core: `src/adaptive_learning/__init__.py`, `application_service.py`, `errors.py`, `pack_digest.py`, `pack_model.py`, `pack_validation.py`, `schema.py`, `storage.py`, `time_and_ids.py`, and `tool_contract.py`.
- Tests: `tests/README.md`, `tests/test_pack_validation.py`, `tests/test_storage.py`, and `tests/test_vertical_slice.py`.

The range contains 2,183 insertions and 31 deletions.

## Module responsibilities

| Module | Responsibility |
|---|---|
| `application_service.py` | Public deterministic operations, transaction orchestration, scoring, question selection, retries, restart reconstruction, progress, and quarantine. |
| `errors.py` | Typed errors with public-safe JSON representations and invariant checks. |
| `pack_model.py` | Immutable in-memory objective, option, question, and pack records. |
| `pack_validation.py` | Strict format-0.1 JSON/Markdown loading, record and cross-reference validation, and lesson path confinement. |
| `pack_digest.py` | Unicode normalization, canonical JSON, normalized Markdown, and SHA-256 digests. |
| `schema.py` | Schema version 1, exactly eight application tables, constraints, foreign keys, and the one-active-session index. |
| `storage.py` | Controlled data paths, SQLite initialization, connection settings, reads, and `BEGIN IMMEDIATE` transactions. |
| `time_and_ids.py` | Injectable opaque identifiers and ordered RFC 3339 UTC timestamps. |
| `tool_contract.py` | Strict contract-0.1 envelopes, exact operation arguments, dispatch, and safe errors. |

No core module imports Hermes, an MCP implementation, a model provider, or a network client.

## Schema implementation

Schema version `1` creates exactly `schema_meta`, `learners`, `installed_packs`, `study_sessions`, `presentations`, `attempts`, `objective_progress`, and `question_challenges`. Foreign keys are enabled and checked on every connection. Writes use explicit immediate transactions. Uniqueness constraints provide operation-specific retry behavior; attempts have no update/delete application operation. The bundled SQLite `json_valid` function checks persisted selections and was available in all three tested CPython builds.

## Pack implementation

The implementation accepts only unpacked format-0.1 packs containing exactly `pack.json` and one sibling Markdown lesson. It rejects unknown/missing fields, invalid UTF-8/JSON, traversal, extra entries, duplicate identifiers, invalid references, and invalid answer-key shapes. Digests cover normalized manifest content and normalized lesson Markdown. Installation copies validated content into a digest-derived controlled directory and revalidates it before recording the database row.

## Tool implementation

`ToolContract` exposes exactly the ten specified runtime-neutral operations. Requests require the exact contract envelope and exact argument set. The service returns JSON-compatible values; expected failures retain stable error codes, while unexpected exceptions become a non-sensitive `INTERNAL_ERROR`. The contract does not depend on an agent runtime.

## Acceptance coverage

| Acceptance behavior | Direct coverage |
|---|---|
| AT-01 clean install/health | `test_at_01_clean_install_and_health` |
| AT-02 fixture validate/install/conflict | `test_at_02_fixture_validate_install_and_conflict` plus pack-validation tests |
| AT-03 learner initialization/restart | `test_at_03_learner_initialization_survives_restart` |
| AT-04 session start/retry/new completion session | `test_at_04_session_start_retry_and_new_after_completion` |
| AT-05 committed delivery/no answer leakage | `test_at_05_delivery_is_committed_without_answer_leakage` |
| AT-06 deterministic single/multiple scoring | `test_at_06_exact_scoring_and_multiple_response_rules` and invalid-selection coverage |
| AT-07 confidence persistence/non-scoring | `test_at_07_confidence_persists_and_does_not_change_scoring` |
| AT-08 process restart/digest checks | `test_at_08_process_restart_restores_and_rechecks_state` and changed-question-digest coverage |
| AT-09 persisted-state resume | `test_at_09_resume_uses_only_persisted_state` |
| AT-10 retry-safe challenge | `test_at_10_challenge_is_retry_safe` |
| AT-11 quarantine/exclusion/finish | `test_at_11_quarantine_excludes_question_and_allows_finish` and unresolved-finish coverage |
| AT-12 immutable attempt/retry reconstruction | `test_at_12_attempt_is_immutable_and_retry_reconstructs_original_result` |

All AT-01 through AT-12 behaviors have direct tests. Additional tests cover the exact schema, transaction rollback, strict tool catalog/envelopes, JSON serialization, runtime/network independence, absence of pilot constants, lesson traversal, and strict pack records.

## Python compatibility

An unmanaged `uv 0.11.29` installation created external virtual environments and installed the built package into each. The exact PowerShell command was:

```powershell
$uv='C:\Users\amccl\AppData\Local\adaptive-learning-agent-dev\uv-bin\uv.exe'
$base='C:\Users\amccl\AppData\Local\adaptive-learning-agent-dev\python-matrix'
foreach ($minor in @('3.12','3.13','3.14')) {
  $venv=Join-Path $base $minor
  & $uv venv --clear --python $minor $venv
  & $uv pip install --python (Join-Path $venv 'Scripts\python.exe') .
  & (Join-Path $venv 'Scripts\python.exe') --version
  & (Join-Path $venv 'Scripts\python.exe') -m unittest discover -s tests -v
}
```

Results:

| Requested version | Exact interpreter | Result | Warnings |
|---|---|---|---|
| 3.12 | CPython 3.12.13 | 25 tests passed | None from the package/test run |
| 3.13 | CPython 3.13.14 | 25 tests passed | None from the package/test run |
| 3.14 | CPython 3.14.6 | 25 tests passed | None from the package/test run |

All versions produced equivalent test names, counts, and outcomes. The first package build identified a metadata defect: setuptools 77+ rejects an SPDX `license` expression combined with the legacy Apache license classifier. Commit `5dc985b` removes only the redundant classifier, declares the two additional tested classifiers, and adds the matching GitHub Actions matrix. Clean installed-package reruns then passed on all versions.

## Coverage

Command, using the installed 3.14 package and `coverage 7.15.2` in the external diagnostic environment:

```powershell
python -m coverage run --source=adaptive_learning -m unittest discover -s tests
python -m coverage report -m
```

Overall statement coverage is **87%** (614 statements, 81 missed) in the final suite. Important unexecuted paths are malformed-pack variants in `pack_validation.py` (78%), malformed/unexpected request and exception branches in `tool_contract.py` (70%), invalid storage paths/configuration branches in `storage.py` (88%), and defensive/not-found branches in `application_service.py` (89%). These are primarily validation and defensive branches; every AT-01 through AT-12 behavior is covered. No tests were added merely to raise the percentage. Direct Hermes-adapter tests exercise adapter argument and error behavior.

## Deviations from the vertical slice

No implementation deviation from the current `docs/mvp-vertical-slice.md` was found. Commit `e60bab5` clarified three governing choices before implementation: completed sessions permit a new session, an unanswered challenged presentation is resolved for finishing, and an empty multiple-response selection is invalid while one valid option remains scoreable. The core follows those clarified rules. The Hermes boundary was intentionally absent from the reviewed core range and is addressed by the separately scoped integration work.

## Correctness and security observations

- Pack validation and installation are well confined, strict, and recheck the installed digest. As with most filesystem validation, an untrusted local process that can mutate the source concurrently creates a time-of-check/time-of-use surface; the controlled copy is revalidated, which limits the consequence to a rejected install.
- Opening an existing unexpected database runs idempotent schema creation before checking the exact table set/version. It then fails closed, but it can add missing expected tables or `schema_meta` to that database before rejection. This is undesirable mutation during validation, though it does not expose data and is outside the clean managed-data path.
- In a rare multi-process install failure, cleanup of a destination created by one process could race with another process recording the same destination. The MVP is single-user/local and database uniqueness prevents inconsistent rows in ordinary use, but pack-directory/database atomicity is not absolute across processes.
- Safe `INTERNAL_ERROR` mapping deliberately withholds exception detail. A future operator-only diagnostic channel may be useful, but adding logging now would exceed the slice and could disclose paths.
- Runtime data integrity relies on normal operating-system filesystem permissions; encryption at rest and hostile same-account process isolation are not claimed.

No issue above required changing deterministic scoring or persistence for this task.

## Complexity review

The most complex code is exact retry reconstruction in `_attempt_result`, which derives the progress snapshot as of the immutable attempt timestamp. That complexity is justified by the requirement to return the original result without adding a generic idempotency/result-cache table. `application_service.py` is otherwise large for one module, but splitting it solely for style would add churn without changing the public boundary. No vector store, event framework, generic repository layer, scheduler, or other unnecessary infrastructure was introduced.
