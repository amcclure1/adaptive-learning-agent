# Amateur Extra 0.2A Implementation Handoff

Date: 2026-07-18
Status: independent-review checkpoint; pilot activation blocked

## Outcome

Format 0.2 is implemented without changing format 0.1, SQLite schema 1, deterministic scoring, confidence, attempts, sessions, restart behavior, progress, or challenge quarantine. The E1A content draft is complete enough for independent review but intentionally fails validation because its approval status is `pending`. No release/tag has been created and the draft has not been pushed as approved content.

## Authoritative baseline

All sources were retrieved on 2026-07-18 from authoritative publishers only.

| Source | Publisher | Effective/revision | Retained snapshot |
|---|---|---|---|
| 2024-2028 Extra Class FCC Element 4 Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026 | NCVEC Question Pool Committee | 2024-07-01 through 2028-06-30; consolidated fourth errata 2026-02-04 | SHA-256 `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517` |
| 2024-2028 Extra Class Question Pool Release | NCVEC Question Pool Committee | consolidated fourth errata 2026-02-04 | not retained |
| 47 CFR Part 97 — Amateur Radio Service | Federal Communications Commission via eCFR | point-in-time XML current through 2026-07-16 | SHA-256 `7b86cd2b22f11437adc8720a19fd244529295a1f76728c214cb91b4e3c4583e3` |

Exact HTTPS URLs are recorded in `pack.json`. The current § 97.503(c) standard remains 50 Element 4 questions with 37 required to pass; § 97.523 describes pool structure. The official E1A06 notation points to § 97.303(h)(1), while the current CW center-frequency provision is § 97.303(h)(3). The draft preserves the official notation and cites the current provision in project prose. This requires explicit reviewer disposition; see [the discrepancy record](amateur-extra-0.2-source-discrepancy.md).

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

The approval record lists all nine required scopes but remains `pending` with no claimed reviewer. `load_pack()` rejects it with `PACK_VALIDATION_FAILED: approval.status must be approved before validation or installation.`

## Core, tool, and Hermes changes

Changed core files are `pack_model.py`, `pack_validation.py`, `pack_digest.py`, and `application_service.py`. Dispatch is exact by format version. Format 0.2 closes every record shape, confines files, rejects unexpected files and unsafe references, resolves provenance/rights/citations, applies snapshot-digest conditions, enforces pool withdrawals and approval, and hashes the complete manifest plus ordered lessons and optional notice without network access.

The ten operations and contract version remain 0.1. Health advertises the two formats and sourced capabilities. Format-0.2 validate/install receipts add format, lesson/source/citation/official counts, origin, pool, and approval summaries. Start adds ordered lessons; next adds origin/official ID/pool identity without answers; submit adds complete post-score citation/source provenance.

The Hermes adapter remains a serializer/delegator. The skill now presents ordered lessons, labels official IDs, distinguishes generated/project content, shows concise sources only after feedback, supports “show sources” from returned provenance, and forbids calling project explanations official NCVEC commentary.

## Verification at this checkpoint

- Local suite: 42/42 passed.
- Local matrix: Python 3.12.13, 3.13.14, and 3.14.6 passed before the final documentation-only changes; rerun after approval is required.
- Format-0.1 golden digest: `12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf`.
- Draft source comparison: all 11 prompts and 44 option strings matched the retained official DOCX exactly; all 11 header lines exposed the expected IDs, keys, and printed rule notation. This is authoring evidence, not independent approval and not the final golden fixture.
- Coverage: Python `coverage` was unavailable without installing a package, which this task forbids. A standard-library `trace` diagnostic completed all 42 tests; its summary is not treated as a comparable statement-coverage percentage.
- Hosted CI: pending final approved bytes and push.
- Real Hermes E1A validation, delivery, confidence submission, source display, and restart/resume: blocked by the approval gate and therefore not attempted.

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

## Deviations and unresolved issues

The completion gate is not met because independent approval, approved golden evidence, real E1A Hermes acceptance, hosted CI, and final push remain outstanding. No source was fetched during pack validation/study, no schema migration or deferred feature was introduced, and no release/tag was created.
