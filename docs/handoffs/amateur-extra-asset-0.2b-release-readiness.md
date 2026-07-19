# Amateur Extra Static-Asset 0.2B Release-Readiness Handoff

Date: 2026-07-18

Status: **PASS; published as prerelease `v0.2.1-alpha.1`**

Anthony McClure completed the mandatory human review and gave the exact candidate an overall PASS at `2026-07-19T03:45:57.7429288Z`. The pack is approved, publicly valid and installable with digest `ac93a973ca85fbd1938ea5adbd10dc5a663126451f15b45d36ead06b3b07b826`.

## Completed verification

- Offline validation, install, fallback descriptor, deterministic scoring, restart/resume reconstruction, idempotent retry, conflicting-retry rejection, and challenge quarantine passed.
- The 77-test suite passed on CPython 3.12.13, 3.13.14, and 3.14.6.
- [GitHub Actions run 29672473830](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29672473830) passed the Python 3.12, 3.13, and 3.14 jobs for approval commit `fc8cd0286ebdf052c520eee3cbf6781115e4d3d4`.
- Pinned Hermes v0.18.2, using the isolated `adaptive-learning-dev` profile and only the process-local project-plugin gate, validated and installed the approved pack with the exact approved digest. No Hermes configuration or credential was read or modified.
- SQLite remains schema 1. No scoring, session, attempt, operation-count, contract-version, format-0.1, or format-0.2 behavior changed.
- The approval diff changes only the approved pack/notice, its golden expectation, and review/status documentation. It changes no core, adapter, schema, or Hermes plugin file.

## Real Hermes v0.18.2 acceptance

Anthony McClure explicitly authorized completion of the old active E1A acceptance session because that milestone was already passed. Hermes completed its remaining eligible questions with the approved official keys and finished it, preserving the learner history rather than resetting state.

Hermes then started E7B session `session-da98d25e41fd42f7895961e733c8d7c6`. Presentation `presentation-438856ad30554f809b951129641caaff` delivered E7B10 without a key or explanation before submission. Answer B at confidence 4 produced correct immutable attempt `attempt-b1731be1d45b410f8ce8bcac81e6418f` with the approved project explanation and NCVEC provenance.

A fresh Hermes process reconstructed the same active session from deterministic state, not conversation memory. It presented E7B11 as `presentation-224d81a003b7486389d72297c2260ca4`, returned the exact approved E7-1 title, caption, alt text, and terminal fallback before an answer, and exposed asset SHA-256 `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`. The pre-answer result omitted `correct_option_ids` and `explanation`. Hermes confirmed fallback access and quarantined the presentation as challenge `challenge-63c402fc26704e80ab76b92a45db238e` without submitting an answer.

An identical E7B10 resubmission reconstructed the original attempt ID and result. A conflicting answer A returned non-retryable `ATTEMPT_CONFLICT` and did not replace the original attempt. Native custom-plugin image output remains unsupported; the approved fallback-only path passed. No Hermes configuration or credential was read or modified.

## Coverage disposition and final PASS

Coverage.py was not installed in the available interpreters, and no package was installed merely to produce a diagnostic. After reviewing the acceptance results and suggested follow-up work, Anthony McClure explicitly gave the test and release-readiness checkpoint a final PASS at `2026-07-19T04:08:51.3070005Z`. This human disposition treats a new coverage measurement as non-blocking for this bounded pilot given the passing 77-test local Python 3.12–3.14 matrix, hosted three-version CI, offline lifecycle, and real Hermes acceptance. It does not claim a new coverage percentage.

At Anthony McClure's request, the remaining E7B12 item was answered with approved key C and scored correctly. E7B session `session-da98d25e41fd42f7895961e733c8d7c6` then completed with two correct answers and one challenged item. Authoritative learner status reports no active session. A process-level check reports no Hermes process running.

Native custom-plugin image output remains unsupported in the pinned Hermes v0.18.2 Windows CLI; the accepted path is approved fallback-only presentation. Native rendering unavailability is not itself a blocker.

All required 0.2B acceptance gates are complete or explicitly dispositioned. The annotated tag `v0.2.1-alpha.1` resolves to `b597401b92520a1cb7bd655cb14c94cc940cc14f`, and the [GitHub prerelease](https://github.com/amcclure1/adaptive-learning-agent/releases/tag/v0.2.1-alpha.1) was published on 2026-07-19. No other release or tag was created by this release task.
