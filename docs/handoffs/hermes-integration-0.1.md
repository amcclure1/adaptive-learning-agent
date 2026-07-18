# Hermes Integration 0.1 Handoff

Date: 2026-07-18
Status: Hermes v0.18.2 CLI compatibility verified

## Delivered boundary

This change adds only the version-0.1 Hermes boundary accepted by ADR 0007: a project-local plugin that delegates exactly ten tools to the public runtime-independent core and one concise workflow skill. It adds no tutoring, scoring, selection, pack parsing, database access, subject-specific adapter logic, authoring, evidence review, pilot content, mastery, or scheduling behavior.

## Installation and profile

- Official release: Hermes Agent `v0.18.2 (2026.7.7.2)` / tag `v2026.7.7.2` / commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`.
- Installation: pinned PyPI package with `uv tool install --python 3.13 'hermes-agent==0.18.2'`.
- Hermes runtime: CPython `3.13.14`.
- Isolated profile: `C:\Users\amccl\AppData\Local\hermes\profiles\adaptive-learning-dev`.
- Terminal settings: repository `terminal.cwd`; `terminal.home_mode: profile`.
- Learner data: `<profile>/adaptive-learning/user-data`, specifically `C:\Users\amccl\AppData\Local\hermes\profiles\adaptive-learning-dev\adaptive-learning\user-data`.
- OpenClaw: not discoverable before installation and not changed.

Launch from the trusted repository root:

```powershell
$env:HERMES_ENABLE_PROJECT_PLUGINS='1'
& "$env:USERPROFILE\.local\bin\hermes.exe" -p adaptive-learning-dev --skills adaptive-learning:adaptive-learning
Remove-Item Env:HERMES_ENABLE_PROJECT_PLUGINS
```

The environment gate is intentionally process-local. The profile has an explicit `plugins.enabled` YAML list containing only `adaptive-learning`. Project discovery must never be enabled globally or from an untrusted repository.

## Provider configuration

- Provider: `openai-codex`
- Model: `gpt-5.5`
- Authentication: successful Hermes device-code flow; Hermes owns the profile-local auth store.
- Non-sensitive health/chat request: successful.

No token, credential, `.env` value, auth payload, or existing Codex credential was read, copied, printed, committed, or included here.

## Python compatibility and CI

The package was built, installed, and tested in external isolated environments:

| Python | Core-only baseline | Final full suite | Result |
|---|---:|---:|---|
| CPython 3.12.13 | 25 | 29 | Passed |
| CPython 3.13.14 | 25 | 29 | Passed |
| CPython 3.14.6 | 25 | 29 | Passed |

All three final runs executed identical test names and outcomes with no package/test warnings. A real packaging defect found by the first installed-package run was fixed by removing the redundant legacy license classifier; the SPDX expression remains. `.github/workflows/test.yml` performs only checkout, Python setup for 3.12/3.13/3.14, package installation, and unittest execution.

Hosted CI result: [GitHub Actions Test run #1](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29665581746) completed successfully for all three matrix jobs (`3.12`, `3.13`, and `3.14`) after the integration changes were pushed.

Core coverage, measured with `coverage 7.15.2` under CPython 3.14.6, is **87%** (614 statements, 81 missed). All AT-01 through AT-12 behaviors have direct tests. Important untested areas remain defensive/malformed branches in pack validation, the runtime-neutral tool contract, storage path/configuration failure, and application not-found/error paths. Coverage is diagnostic, not a gate; no percentage-only tests were added.

See `docs/handoffs/core-implementation-review.md` for the exact reviewed commit range, changed files, AT mapping, concerns, and commands.

## Plugin

Location: `.hermes/plugins/adaptive-learning/`

Registered mappings:

| Hermes tool | Core operation |
|---|---|
| `ala_system_health` | `system.health` |
| `ala_learner_initialize` | `learner.initialize` |
| `ala_pack_validate` | `pack.validate` |
| `ala_pack_install` | `pack.install` |
| `ala_study_start` | `study.start` |
| `ala_study_next` | `study.next` |
| `ala_study_submit` | `study.submit` |
| `ala_study_status` | `study.status` |
| `ala_study_finish` | `study.finish` |
| `ala_question_challenge` | `question.challenge` |

The adapter registers strict JSON schemas with `additionalProperties: false`, checks exact adapter argument sets, invokes `ApplicationService` through `ToolContract`, emits compact valid JSON, and maps unexpected adapter exceptions to a safe `ADAPTER_INTERNAL_ERROR`. It does not import `sqlite3` or the core storage module. The database path is fixed from `HERMES_HOME`; only pack validate/install accept caller paths, which remain subject to core checks.

For project-local development the adapter resolves this repository's `src/` tree from its own path. This avoids installing the project into Hermes' managed tool environment and leaves the core independently installable/testable. A future globally packaged plugin may depend on the installed core package; no global plugin was installed here.

## Skill

Location: `skills/adaptive-learning/SKILL.md`
Qualified Hermes name: `adaptive-learning:adaptive-learning`

The plugin uses the tagged `ctx.register_skill` API, because v0.18.2 does not automatically discover repository skills. The skill is explicitly preloaded, concise, and workflow-only. It requires health/initialize/status bootstrap on fresh conversations, treats tools as authoritative, preserves question/feedback meaning, collects confidence, supports challenge, and forbids mastery/readiness claims. It also forces a learner-facing turn boundary after displaying a question so an answer supplied before the current presentation cannot be consumed.

No `subject-builder` or `content-reviewer` behavior exists.

## Direct adapter tests

`tests/test_hermes_plugin.py` uses a fake registration context and temporary profile home. It verifies:

- exactly ten schemas register under the `adaptive_learning` toolset;
- all names map to exact runtime-neutral operations;
- the qualified skill registers;
- all ten handlers execute during a full fixture flow and every response parses as JSON;
- `ala_study_next` omits answer and explanation fields;
- adapter argument and unexpected errors remain structured and safe;
- adapter source does not import SQLite/storage internals.

Result: 4 adapter test methods passed; final repository suite 29/29 on every supported Python version. The actual v0.18.2 loader separately reported all ten `ala_*` names and the registered qualified skill with no plugin error.

## Real Hermes acceptance

Primary first process, session `20260718_182316_115e77`, had no parent session and called:

```text
health → learner.initialize → study.status → pack.validate → pack.install
→ study.start → study.next → study.submit
```

The fixture installed and a session started. Choice `a` with confidence `4` produced deterministic incorrect feedback identifying `b`, its reviewed explanation, and objective counts. The process then exited completely.

Primary restart process, session `20260718_182444_ecda7e`, also had no parent session and no resume flag. It called:

```text
health → learner.initialize → study.status → study.start → study.next
→ question.challenge → study.status → (study.next → study.submit) × 3
→ study.next → study.finish → study.status
```

It reconstructed the active session from tools, challenged `q-002` with the learner-provided reason, observed `challenged_count: 1`, completed the remaining eligible questions, finished the session, and verified there was no active session. The finished summary was four answered attempts, one correct, and one quarantined question. A read-only database snapshot found one completed session, four immutable attempts, and one challenge. A post-completion resubmit was rejected with `SESSION_NOT_ACTIVE`; before/after attempt snapshots and their hash were identical.

Sanitized exports were written outside the repository under `C:\Users\amccl\AppData\Local\adaptive-learning-agent-dev\`. Automated inspection confirmed both primary sessions used provider `openai-codex`, model `gpt-5.5`, had no parent transcript, and that no `ala_study_next` tool result contained `correct_option_ids` or `explanation`.

A supplemental learner-facing check started a new session and visibly returned the exact fixture lesson, exact first prompt/options, and a request for answer plus confidence before submission. Resuming that Hermes conversation with choice `b`, confidence `5`, returned the deterministic correct feedback. Three remaining supplemental questions were completed directly through the public core contract afterward so the development profile was not left with an active test session.

Acceptance status: **passed** for the Hermes v0.18.2 CLI/profile target.

## Context-behavior review

- Invented learner state: none observed; the fresh restart bootstrapped from health, learner initialization, and status.
- Tool avoidance: none; all required state transitions used `ala_*` tools.
- Answer leakage: none in `study.next` results or learner-facing presentation.
- Question-changing paraphrase: none in the explicit learner-facing check; the exact prompt/options were displayed.
- Confidence: supplied and persisted on every submitted test answer; the supplemental visible turn explicitly requested it.
- Deterministic feedback: used in final responses without a competing model score.
- Excessive context: the single namespaced skill was preloaded; no pack/SQLite files or unrelated skills were loaded by the model.
- Prior-conversation reliance: none in the primary restart; both session records had no parent and the restart used tools before continuing.
- Mastery/readiness claim: none.

Initial scripted one-shot input included an answer before the question was visibly displayed. Although tool behavior remained correct, the final response skipped directly to feedback. The skill was narrowed to end the turn after question presentation and reject pre-presentation answers; the supplemental run then displayed the lesson/question and waited correctly. No core behavior changed.

## Tagged-release differences and known issues

- `hermes plugins enable` does not manage a project-only plugin in this tested release, even when project scanning is enabled. The isolated profile needs a manually represented YAML allow-list plus the launch-time environment gate.
- `hermes config set plugins.enabled '["adaptive-learning"]'` stored a string rather than a list; the profile file was corrected to a YAML sequence.
- Tagged prose contains a `codex-oauth` name in one place, while tagged CLI/source and the verified flow use `openai-codex`.
- Project-local skills are not auto-discovered; explicit plugin registration and qualified preload are required.
- Project plugin discovery uses process CWD, so launch from the trusted repository root. `terminal.cwd` does not replace this discovery requirement.
- Windows CLI behavior is verified; Desktop, gateway, aliases, profile export/import, non-Windows platforms, and other Hermes versions are unverified.
- The profile reports config schema version 0 with a migration available. No migration was run because the minimal explicit settings are valid and migration could add unrelated defaults.

Full source/document findings are in `docs/hermes-compatibility-0.18.2.md`.

## Deviations from the vertical slice

No deterministic core deviation was required. The development adapter imports the repository source tree rather than installing the project inside Hermes' uv tool environment; this is a project-local development packaging choice, not a boundary change. The qualified plugin skill is explicitly preloaded because tagged skill discovery does not scan repository skills. No deferred schema, tool, algorithm, subject, or agent behavior was added.

## Cleanup and uninstall

These commands remove only artifacts created for this task. Run from outside an active Hermes process:

```powershell
& "$env:USERPROFILE\.local\bin\hermes.exe" profile delete adaptive-learning-dev
& 'C:\Users\amccl\AppData\Local\adaptive-learning-agent-dev\uv-bin\uv.exe' tool uninstall hermes-agent
Remove-Item -LiteralPath 'C:\Users\amccl\AppData\Local\adaptive-learning-agent-dev' -Recurse -Force
```

The first command removes the isolated profile, including its Hermes-owned OAuth and learner test state. The second removes the isolated Hermes tool. The final command removes only this task's uv binary, test interpreters/environments, tagged source checkout, and sanitized exports. Review the exact paths before running. The repository's committed plugin/skill remain until removed with normal Git changes. No OpenClaw cleanup is needed because it was never touched.
