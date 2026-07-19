# Amateur Extra 0.2A Release-Readiness Handoff

Date: 2026-07-19
Status: PASS; no release or tag created

## Verified implementation

The verified implementation commit is `2c3d364df410a9408e9c4f558d23904749de5207`. It includes the approved pack, golden fixture, and approved-pack workflow test. Documentation closure follows that implementation commit; the pushed repository HEAD is reported in the completion response because a document cannot contain its own commit hash.

The approved pack validates and installs with digest `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`. The format-0.1 golden digest remains `12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf`.

## Automated verification

- Local standard-library suite: 45/45 passed.
- CPython matrix: 3.12.13, 3.13.14, and 3.14.6 each passed 45/45.
- Statement coverage: 87% (1,064 statements, 141 missed), measured with coverage.py 7.15.2 already present in an external isolated environment; no package was installed.
- Hosted CI: [GitHub Actions run 29668355434](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29668355434) passed Python 3.12, 3.13, and 3.14 for the verified implementation commit.
- Golden mutation checks cover missing/extra/duplicate IDs, prompts and punctuation, Unicode differences, ordered options and text, answer keys, and printed locators.
- Offline approved-pack workflow covers validation/install, digest identity, ordered lessons, answer-safe delivery, scoring/provenance, restart reconstruction, immutable retry, and challenge quarantine without network access.

## Real Hermes v0.18.2 acceptance

The pinned Windows executable `C:\Users\amccl\.local\bin\hermes.exe` was run with the isolated `adaptive-learning-dev` profile and a process-local project-plugin gate. Configuration and credentials were not modified or read.

Hermes session `20260718_201929_0814d2` validated and installed the approved pack, initialized the persisted learner, loaded both lessons in order, and presented E1A01 with its exact official ID, prompt, and options without revealing the answer or explanation. Submission `D` with confidence 4 scored correct deterministically. Feedback clearly labeled the explanation as project-authored and returned concise source information; “show sources” displayed the eCFR provenance fields. A conflicting resubmission returned non-retryable `ATTEMPT_CONFLICT`, and read-only SQLite inspection confirmed the original attempt remained the only attempt for that presentation.

Fresh Hermes session `20260718_202102_ac94e8` had no parent session and reconstructed the active core session from deterministic tools, not conversation memory. It presented exact E1A02 without answer leakage and quarantined it through a challenge. Read-only Hermes state inspection confirmed both acceptance sessions have `parent_session_id = NULL`; learning-state inspection confirmed the same active core session, one E1A01 attempt, and one E1A02 challenge.

## Boundary audit

- `src/adaptive_learning/schema.py` is unchanged from the released baseline; SQLite remains schema version 1.
- The core and Hermes adapter contain no Amateur Extra, NCVEC, or E1A subject constants.
- The core imports no Hermes, MCP, model-provider, or network client.
- The adapter remains serialization/delegation only and does not own storage or scoring.
- Pre-answer results do not disclose answer keys or explanations; post-answer provenance comes from the validated pack.
- Agent memory is non-authoritative. Restart recovery and conflict behavior are reconstructed from SQLite and core tool responses.

## Scope closure

No packages were installed, no Hermes configuration was changed, and no implementation feature outside accepted 0.2A scope was added. No release or tag was created. Remaining limitations and deferred work are recorded in [current status](../current-status.md) and [the roadmap](../roadmap.md).
