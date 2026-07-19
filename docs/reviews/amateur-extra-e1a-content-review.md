# Amateur Extra E1A Content Review

Status: pending independent human review
Reviewer: Anthony McClure
Prepared: 2026-07-18
Review completed: ☐ No

This checklist supports human review of `packs/amateur-extra-e1a/`. Automated comparison evidence is preparatory evidence only. It does not approve content, establish that the reviewer performed a review, or authorize activation.

## Fresh authoritative-source revalidation

Fresh copies were retrieved from the authoritative publishers on 2026-07-18 into an external review directory. They are not distributed in the pack.

| Source | Publisher | Current identity | Fresh SHA-256 | Comparison with implementation baseline |
|---|---|---|---|---|
| 2024-2028 Extra Class Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026 PDF | NCVEC Question Pool Committee | Effective 2024-07-01; consolidated fourth errata issued 2026-02-04 | `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517` | Exact hash match |
| 2024-2028 Extra Class Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026 DOCX | NCVEC Question Pool Committee | Effective 2024-07-01; consolidated fourth errata issued 2026-02-04 | `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7` | Exact hash match to retained authoring copy |
| 2024-2028 Extra Class Question Pool Release | NCVEC Question Pool Committee | Fourth errata remains latest; public-domain statement remains present | `ec568fe3d0a14206f05af87c2249acb24ff288e0d7614b68f25b1a390bf745a4` | No earlier page hash was declared; required facts match |
| 47 CFR Part 97 — Amateur Radio Service, point-in-time XML | Federal Communications Commission via eCFR | Up to date as of 2026-07-16; Title 47 last amended 2026-07-13 | `7b86cd2b22f11437adc8720a19fd244529295a1f76728c214cb91b4e3c4583e3` | Exact hash match |

Official URLs are recorded in `pack.json`. The NCVEC page still identifies the February 4, 2026 fourth errata as current and lists E4D05, E6D07, E2A13, and E9E10 as withdrawn across the consolidated errata history. It contains no newer E1A06 correction. Current § 97.503(c) still specifies 50 Element 4 questions and a passing score of 37; § 97.523 still requires one published pool per element containing at least ten times the examination question count.

Automated comparison against the freshly downloaded official DOCX found exactly 11 E1A records, E1A01 through E1A11 in order. Every pack ID, prompt, ordered option label/text pair, keyed answer, and printed NCVEC rule locator matched exactly. The reviewer must still inspect and confirm each row below.

## Question-by-question human review

Legend: every checkbox begins unchecked. Mark it only after direct human inspection. `Pending` must be replaced with the reviewer's disposition.

| Official ID | Prompt exact match | Option labels/order exact | Option text exact | Answer key exact | Printed NCVEC rule notation | Project explanation reviewed | Explanation citation reviewed | Reviewer disposition | Notes |
|---|---|---|---|---|---|---|---|---|---|
| E1A01 | ☐ | ☐ | ☐ | ☐ D | ☐ `[97.305, 97.307(b)]` | ☐ | ☐ | Pending | |
| E1A02 | ☐ | ☐ | ☐ | ☐ D | ☐ `[97.301, 97.305]` | ☐ | ☐ | Pending | |
| E1A03 | ☐ | ☐ | ☐ | ☐ C | ☐ `[97.305, 97.307(b)]` | ☐ | ☐ | Pending | |
| E1A04 | ☐ | ☐ | ☐ | ☐ C | ☐ `[97.301, 97.305]` | ☐ | ☐ | Pending | |
| E1A05 | ☐ | ☐ | ☐ | ☐ C | ☐ `[97.5]` | ☐ | ☐ | Pending | |
| E1A06 | ☐ | ☐ | ☐ | ☐ B | ☐ `[97.303(h)(1)]` | ☐ | ☐ `§ 97.303(h)(3)` | Pending | Explicit disposition required below. |
| E1A07 | ☐ | ☐ | ☐ | ☐ C | ☐ `[97.313(k)]` | ☐ | ☐ | Pending | |
| E1A08 | ☐ | ☐ | ☐ | ☐ B | ☐ `[97.219]` | ☐ | ☐ | Pending | |
| E1A09 | ☐ | ☐ | ☐ | ☐ D | ☐ `[97.313(l)]` | ☐ | ☐ | Pending | |
| E1A10 | ☐ | ☐ | ☐ | ☐ A | ☐ `[97.11]` | ☐ | ☐ | Pending | |
| E1A11 | ☐ | ☐ | ☐ | ☐ B | ☐ `[97.5]` | ☐ | ☐ | Pending | |

## E1A06 explicit disposition

The NCVEC printed locator appears stale: the consolidated fourth-errata source prints `[97.303(h)(1)]`, while current § 97.303 places the operative CW center-frequency requirement in paragraph (h)(3). The answer remains correct. The project has not altered the official ID, prompt, choices, option order, key, or printed locator. The project-authored explanation cites the current operative paragraph, § 97.303(h)(3).

- ☐ I verified that NCVEC still prints `[97.303(h)(1)]` and has not issued newer applicable errata.
- ☐ I verified that current § 97.303(h)(3) requires the CW carrier at the channel center frequency.
- ☐ I accept preserving the official question and printed locator unchanged while citing § 97.303(h)(3) in project prose.
- Reviewer disposition: Pending
- Reviewer notes:

## Lessons

### Lesson 1 — Band edges, privileges, and occupied signals

- ☐ Original project prose; no copied third-party study text.
- ☐ Regulatory claims are accurate under the cited current Part 97 text.
- ☐ USB/LSB occupied-signal reasoning is accurate and teaches concepts rather than answer letters.
- ☐ The 60-meter explanation accurately distinguishes the NCVEC printed locator from the current rule paragraph.
- ☐ Citations and locators are sufficient and correctly resolved.
- Reviewer disposition: Pending
- Notes:

### Lesson 2 — Special operations and regulatory limitations

- ☐ Original project prose; no copied third-party study text.
- ☐ Vessel/aircraft licensing, permission, and physical-control statements are accurate.
- ☐ Message-forwarding accountability is accurate.
- ☐ 2200-meter and 630-meter EIRP statements are accurate, including the Alaska qualification.
- ☐ Citations and locators are sufficient and correctly resolved.
- Reviewer disposition: Pending
- Notes:

## Sources, pool, rights, and notice

### Source metadata and snapshots

- ☐ Exact titles, publishers, HTTPS URLs, retrieval dates, revision identities, and source types reviewed.
- ☐ Fresh NCVEC PDF hash matches the declared retained digest.
- ☐ Fresh point-in-time eCFR XML hash matches the declared retained digest.
- ☐ NCVEC DOCX authoring snapshot hash recorded above and understood as comparison evidence, not a distributed pack file.
- ☐ `snapshot_retained` and `content_sha256` combinations are accurate.
- Disposition: Pending
- Notes:

### Assessment pool and errata

- ☐ Pool ID, title, publisher, effective date 2024-07-01, and effective-through date 2028-06-30 reviewed.
- ☐ Fourth-errata identity dated 2026-02-04 reviewed.
- ☐ Withdrawal list contains E2A13, E4D05, E6D07, and E9E10 exactly.
- ☐ No E1A01–E1A11 question is withdrawn or superseded.
- ☐ Current Element 4 standard of 50 questions with 37 required to pass reviewed.
- Disposition: Pending
- Notes:

### Rights metadata

- ☐ NCVEC official IDs, wording, ordered choices, and keys are limited to the `public_domain` component scope and linked to the NCVEC statement.
- ☐ Original lessons and explanations are `licensed` as `CC-BY-4.0`, copyright Adaptive Learning Agent contributors.
- ☐ External official source records are `reference_only` metadata and links.
- ☐ No logo, seal, screenshot, branding asset, commercial course prose, or unofficial study text is included.
- ☐ Project policy is understood not to be formal legal advice.
- Disposition: Pending
- Notes:

### NOTICE.md

- ☐ NOTICE accurately distinguishes official pool material, original project prose, and external references.
- ☐ NOTICE does not override or contradict machine-readable rights metadata.
- ☐ NOTICE accurately states that the current pack is a draft pending independent review.
- Disposition: Pending
- Notes:

## Approval scope confirmation

- ☐ `official_wording`
- ☐ `option_ordering`
- ☐ `answer_keys`
- ☐ `official_ids`
- ☐ `lessons`
- ☐ `explanations`
- ☐ `citations`
- ☐ `rights_metadata`
- ☐ `pool_and_errata_metadata`

## Human confirmation gate

Do not complete this section until every applicable item above has been reviewed.

- Reviewer: Anthony McClure
- Review completion time (actual UTC, recorded only after explicit confirmation): Pending
- Overall disposition: Pending
- ☐ All 11 questions were reviewed.
- ☐ Both lessons were reviewed.
- ☐ All explanations and citations were reviewed.
- ☐ Rights and source metadata were reviewed.
- ☐ The E1A06 treatment was explicitly accepted.
- Final reviewer notes:

After completing the review, Anthony McClure must explicitly confirm these five statements to Codex. Only then may Codex record the actual current UTC timestamp and change the digest-covered pack approval status to `approved`.
