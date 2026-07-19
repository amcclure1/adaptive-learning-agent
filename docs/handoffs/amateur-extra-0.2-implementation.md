# Amateur Extra 0.2A Implementation Handoff

Date: 2026-07-18
Status: superseded by completed independent review and release-readiness verification

## Outcome

Format 0.2 was implemented without changing format 0.1, SQLite schema 1, deterministic scoring, confidence, attempts, sessions, restart behavior, progress, or challenge quarantine. The subsequent independent review passed and the E1A pack is approved, installable, pushed, and acceptance-verified. See [the independent-review handoff](amateur-extra-0.2-independent-review.md) and [release-readiness handoff](amateur-extra-0.2-release-readiness.md). No release or tag has been created.

## Authoritative baseline

All sources were retrieved on 2026-07-18 from authoritative publishers only.

| Source | Publisher | Effective/revision | Retained snapshot |
|---|---|---|---|
| 2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026 | NCVEC Question Pool Committee | 2024-07-01 through 2028-06-30; consolidated fourth errata 2026-02-04 | SHA-256 `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517` |
| 2024-2028 Extra Class Question Pool Release | NCVEC Question Pool Committee | consolidated fourth errata 2026-02-04 | not retained |
| 47 CFR Part 97 — Amateur Radio Service | Federal Communications Commission via eCFR | point-in-time XML current through 2026-07-16 | SHA-256 `7b86cd2b22f11437adc8720a19fd244529295a1f76728c214cb91b4e3c4583e3` |

Exact HTTPS URLs are recorded in `pack.json`. The current § 97.503(c) standard remains 50 Element 4 questions with 37 required to pass; § 97.523 describes pool structure. The official E1A06 notation points to § 97.303(h)(1), while the current CW center-frequency provision is § 97.303(h)(3). The pack preserves the official notation and cites the current provision in project prose. The reviewer explicitly accepted this treatment; see [the discrepancy record](amateur-extra-0.2-source-discrepancy.md).

## Pack inventory and mapping

Path: `packs/amateur-extra-e1a/`

```text
pack.json
NOTICE.md
lessons/01-band-edges.md
lessons/02-special-operations.md
```

Official IDs are E1A01, E1A02, E1A03, E1A04, E1A05, E1A06, E1A07, E1A08, E1A09, E1A10, and E1A11. E1A01–E1A04 and E1A06 map to `obj-band-edges` and lesson 1. E1A05 and E1A07–E1A11 map to `obj-special-operations` and lesson 2. There are 11 official-pool questions, zero generated questions, and no diagrams/assets.

Rights are separate: `rights-ncvec-pool` is public domain only for NCVEC wording/choices/keys/identifiers and cites the release statement; `rights-original-prose` is CC-BY-4.0 for contributor lessons/explanations; `rights-external-references` is reference-only metadata/links.

The approval record now lists all nine required scopes as approved by Anthony McClure at `2026-07-19T01:12:29.8952607Z`. `load_pack()` accepts the pack and produces digest `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`.

## Core, tool, and Hermes changes

Changed core files are `pack_model.py`, `pack_validation.py`, `pack_digest.py`, and `application_service.py`. Dispatch is exact by format version. Format 0.2 closes every record shape, confines files, rejects unexpected files and unsafe references, resolves provenance/rights/citations, applies snapshot-digest conditions, enforces pool withdrawals and approval, and hashes the complete manifest plus ordered lessons and optional notice without network access.

The ten operations and contract version remain 0.1. Health advertises the two formats and sourced capabilities. Format-0.2 validate/install receipts add format, lesson/source/citation/official counts, origin, pool, and approval summaries. Start adds ordered lessons; next adds origin/official ID/pool identity without answers; submit adds complete post-score citation/source provenance.

The Hermes adapter remains a serializer/delegator. The skill now presents ordered lessons, labels official IDs, distinguishes generated/project content, shows concise sources only after feedback, supports “show sources” from returned provenance, and forbids calling project explanations official NCVEC commentary.

## Verification after approval

- Local suite: 45/45 passed.
- Local matrix: Python 3.12.13, 3.13.14, and 3.14.6 each passed 45/45.
- Format-0.1 golden digest: `12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf`.
- Approved source comparison: all 11 records matched the fresh official DOCX exactly by ID, prompt, ordered option labels/text, answer key, and printed locator. The committed golden fixture and mutation tests preserve that approved transcription.
- Coverage: 87% statement coverage (1,064 statements, 141 missed), using coverage.py already present in an isolated external environment; no package was installed.
- Hosted CI: [run 29668355434](https://github.com/amcclure1/adaptive-learning-agent/actions/runs/29668355434) passed Python 3.12, 3.13, and 3.14 for implementation commit `2c3d364df410a9408e9c4f558d23904749de5207`.
- Real Hermes v0.18.2 acceptance passed validation/install, delivery, confidence scoring, source display, independent restart reconstruction, challenge quarantine, and immutable retry rejection.

## Independent review procedure

1. Retrieve the authoritative consolidated NCVEC source afresh and confirm its revision/digest or document any change.
2. Compare each ID, prompt, option label/order/text, key, and printed notation for E1A01–E1A11. Treat punctuation and Unicode apostrophes as significant.
3. Explicitly accept or revise the documented E1A06 treatment.
4. Review both lessons for original prose and regulatory accuracy.
5. Review every explanation against its cited current Part 97 locator, including important distractor statements.
6. Confirm all citations, source titles/publishers/URLs/dates/digests, withdrawal list, effective dates, rights scopes, and notice.
7. Record the human designation and actual UTC completion time, change only `approval.status` to `approved`, and describe the E1A06 disposition in notes. The authoring model must not perform this step.
8. Create an approved local golden transcription fixture and tests that fail on IDs, omissions/duplicates, prompts, option order/text, or keys.
9. Run validation/install, the full Python matrix, offline format-0.2 restart/challenge tests, and real Hermes question/answer/confidence/source/restart acceptance.
10. Push focused commits, wait for hosted CI, record its URL and final coverage diagnostic, update this handoff, and stop without a final release/tag.

## Commands after approval

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v

$env:HERMES_ENABLE_PROJECT_PLUGINS='1'
& "$env:USERPROFILE\.local\bin\hermes.exe" -p adaptive-learning-dev --skills adaptive-learning:adaptive-learning
Remove-Item Env:HERMES_ENABLE_PROJECT_PLUGINS
```

In Hermes, ask to validate and install `packs/amateur-extra-e1a`, initialize the local learner, study `us-amateur-extra-e1a` version `0.2.0`, answer the displayed official question with an option ID and confidence 1–5, then ask “show sources.” Exit Hermes completely, relaunch with the same command, and require it to reconstruct the active session from health/initialize/status tools.

## Closure

The previously outstanding independent approval, approved golden evidence, real E1A Hermes acceptance, hosted CI, and push gates are complete. No source was fetched during pack validation/study, no schema migration or deferred feature was introduced, and no release/tag was created. The two closure handoffs contain the detailed final evidence.
