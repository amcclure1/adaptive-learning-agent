# Amateur Extra Static-Asset 0.2B Implementation Handoff

Date: 2026-07-18

Status: Generic implementation PASS; exact content human-approved and installable; final acceptance in progress

## Outcome

Accepted ADRs 0014–0016 are implemented without changing formats 0.1/0.2, SQLite schema 1, scoring, sessions, attempts, selection, confidence, retry, progress, challenge quarantine, the ten-operation catalog, or contract version 0.1.

The implementation adds exact format-0.3 dispatch, ordered closed PNG asset records and references, standard-library structural PNG validation, raw-byte and pack digesting, strict local inventory/path/reference/rights/accessibility checks, deterministic leakage lint, core-issued installed-asset references, additive tool results, and a thin Hermes fallback-first workflow.

## Fresh authoritative verification

The official NCVEC release page and files were retrieved again on 2026-07-18. The page still identifies the fourth errata dated February 4, 2026 as current and releases the pool into the public domain. No consolidated errata affects E7B10, E7B11, E7B12, or Figure E7-1.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Current consolidated DOCX | 674,155 | `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7` |
| Current consolidated PDF | 952,745 | `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517` |
| Official figure PDF | 78,505 | `591bb4c9fc9a9267e298b3ee23c93ab54ba3813f8ea3730123f9ccda1e4b80f2` |
| Official page-2 JPEG | 168,703 | `6b085fb7461331899b33c24a0e9eb690bc0d555e00775086538cd5b8742931a9` |

DOCX relationship `rId10` targets `media/image5.png` and is embedded once. Exact member `word/media/image5.png` is 41,357 bytes, SHA-256 `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`, and a valid 796×674 8-bit truecolor PNG. Its exact pixels print `Figure E7-1`; the separate official page-2 distribution supplies a human comparison target. See [the machine-readable evidence](../reviews/evidence/amateur-extra-e7b-source-verification.json).

## Format-0.3 implementation

- `pack_model.py` adds immutable asset records and ordered lesson/question asset IDs.
- `pack_validation.py` keeps exact 0.1/0.2 branches and adds a separate strict 0.3 branch. The public loader requires full human approval; a narrow review loader accepts only the defined pending record so a candidate digest can be reviewed without becoming installable.
- `png_validation.py` checks signature, chunk framing/length/type/CRC, IHDR position/shape, valid bit-depth/color combinations, PLTE/IDAT critical ordering, dimensions, one terminal IEND, unknown critical chunks, and trailing bytes without decoding pixels.
- Accepted limits are 16 assets, 2 MiB each, 8 MiB total, and 1–4096 pixels per dimension.
- Inventory validation rejects traversal, absolute/backslash/non-NFC paths, links/reparse points, hard-link aliases, case collisions, missing/undeclared files, duplicates, remote/non-PNG assets, and unresolved source/rights/accessibility references.
- The 0.3 digest uses a new domain marker and frames canonical manifest bytes, ordered lesson paths/text, ordered asset paths/exact bytes, and optional notice text. The 0.1 and 0.2 algorithms are untouched.
- `asset_reference.py` implements canonical `ala-pack-asset-v1` tokens bound to pack ID, version, installed digest, and asset ID. `ApplicationService.resolve_asset_reference()` rechecks the installed receipt/digest and confines resolution to the controlled pack store.

## Contract and storage boundary

`system.health` advertises formats 0.1–0.3, `static_local_assets`, `image/png`, and `ala-pack-asset-v1`. Format-0.3 validation/install results add asset summaries. Start/next/submit add descriptors only for 0.3 records that declare assets. Pre-answer results contain no key, explanation, raw bytes, arbitrary path, or interpretive annotation.

The SQLite schema and schema module were not changed. Assets remain immutable pack files; restart reconstructs descriptors from the installed receipt/path/digest and existing presentation record.

## Pending candidate

`packs/amateur-extra-e7b/` contains exactly E7B10–E7B12, one exact E7-1 asset referenced by all three questions, two original lessons, original post-answer explanations, authoritative NCVEC citations, component rights, and `NOTICE.md`. There are no generated questions or other figures.

- Review digest: `9c43be04bc38910f12ddf1d90eb62e69cd916ed06fccf44c0770e6fbf2218d43`
- Approval: `pending`, null reviewer/time, empty scopes
- Public validation/install: rejected as designed
- Golden comparison: exact IDs, prompts, ordered options/text, keys, locators, asset member/hash/bytes/dimensions

The authoring/implementation agent has made no figure identity, fidelity, redistribution, caption, alt, fallback, mapping, non-leakage, content, rights, or activation approval. See [the human review package](../reviews/amateur-extra-e7b-asset-content-review.md).

## Hermes investigation

The installed Hermes runtime is package 0.18.2/release `2026.7.7.2`, matching official source tag `v2026.7.7.2` and release commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`. Tagged documentation/source and runtime introspection expose JSON-string ordinary tool handlers but no public learner-facing local-image output method. Native custom-plugin image output is recorded as unsupported for the pinned Windows CLI.

The adapter remains a serializer/delegator. The skill presents the returned caption/alt/fallback first, requests access confirmation, and only then presents the exact question/options and asks for answer/confidence. It does not use model vision, private multimodal envelopes, arbitrary paths, or Hermes configuration changes. See [the investigation record](../reviews/evidence/hermes-0.18.2-static-asset-presentation.md).

## Verification at checkpoint

- Local standard-library suite on CPython 3.14.3: 77/77 passed.
- Format-0.1 golden digest: `12bcb272e4c8059f06880df8ad15dd9abaea30149d02734c4a09a81618878cbf`.
- Format-0.2 approved E1A digest: `08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e`.
- Format-0.3 tests cover dispatch, closed fields, approval, PNG corruption/CRC/framing/dimensions/limits, inventory/path aliases, duplicate identities, references, rights, accessibility/lint, digest inputs/order, logical references, confinement, conflicts, restart, challenge, immutable attempts, answer safety, JSON compatibility, and no core network dependency.
- SQLite schema remains 1; no migration exists.

Post-approval update: independent review is PASS, the approved digest is `ac93a973ca85fbd1938ea5adbd10dc5a663126451f15b45d36ead06b3b07b826`, the offline lifecycle passes, and Python 3.12/3.13/3.14 each pass 77 tests. Coverage, hosted CI, complete real Hermes E7B presentation, and release-readiness closure remain pending as detailed in the release-readiness handoff.

## Required next action

The human reviewer must complete every row in [the review checklist](../reviews/amateur-extra-e7b-asset-content-review.md) and explicitly approve the complete scope. Only then may the actual reviewer/time/scopes be recorded, the approved digest calculated, the pack validated/installed, and final acceptance begin. No release or tag is authorized.
