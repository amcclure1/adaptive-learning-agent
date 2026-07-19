# Amateur Extra Pilot 0.2A

Status: Implementation draft complete; independent human review required before activation
Updated: 2026-07-18

## Verified official baseline

The current source is the **2024–2028 Extra Class FCC Element 4 Question Pool and Syllabus**, effective July 1, 2024 through June 30, 2028. It is developed and maintained by the National Conference of Volunteer Examiner Coordinators Question Pool Committee (NCVEC QPC). The current consolidated document found during this review incorporates the **fourth errata issued February 4, 2026**.

Authoritative source set:

- [NCVEC 2024–2028 Extra Class release and errata page](https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release) — publishing body, public-domain statement, and errata history.
- [NCVEC consolidated pool and syllabus with fourth errata](https://ncvec.org/downloads/2024-2028%20Extra%20Class%20Question%20Pool%20and%20Syllabus%20Public%20Release%20with%204th%20Errata%20Feb%204%202026.pdf) — current wording, ordered choices, keys, identifiers, rule citations, syllabus, and effective date.
- [NCVEC Amateur Question Pools](https://ncvec.org/index.php/amateur-question-pools) — QPC role, pool organization, numbering, and publication process.
- FCC rules via current eCFR: [§ 97.5](https://www.ecfr.gov/current/title-47/part-97/section-97.5), [§ 97.11](https://www.ecfr.gov/current/title-47/part-97/section-97.11), [§ 97.219](https://www.ecfr.gov/current/title-47/part-97/section-97.219), [§ 97.301](https://www.ecfr.gov/current/title-47/part-97/section-97.301), [§ 97.303](https://www.ecfr.gov/current/title-47/part-97/section-97.303), [§ 97.305](https://www.ecfr.gov/current/title-47/part-97/section-97.305), [§ 97.307](https://www.ecfr.gov/current/title-47/part-97/section-97.307), and [§ 97.313](https://www.ecfr.gov/current/title-47/part-97/section-97.313) — primary regulatory material cited by E1A.
- FCC rules via current eCFR: [§ 97.503](https://www.ecfr.gov/current/title-47/part-97/section-97.503) and [§ 97.523](https://www.ecfr.gov/current/title-47/part-97/section-97.523) — Element 4 and question-pool structure.

The eCFR is a continuously updated government source that describes itself as authoritative but unofficial; its pages link to the annually published official CFR on GovInfo. A production review should record both the access date and the regulation's point-in-time date.

### Exam structure relevant to this design

Under 47 CFR § 97.503(c), Element 4 is a 50-question written examination with a minimum passing score of 37. Section 97.523 requires one published pool per element, at least ten times the examination size. The NCVEC syllabus says subelement E1 contributes six examination questions from six groups and contains 68 pool questions. E1A is one of those six groups. The design inference is that an examination selects one E1A question; the cited NCVEC syllabus should remain the normative blueprint if selection rules are clarified.

The complete examination has no role in 0.2A: the pilot is practice for one group, not a 50-question simulation and not a readiness predictor.

### Errata status

The consolidated fourth-errata file records these current withdrawals without renumbering their groups:

- E9E10 in the first errata (January 31, 2024), alongside several modifications and citation corrections elsewhere;
- E2A13 in the second errata (November 8, 2024);
- E6D07 in the third errata (September 25, 2025), because it had more than one correct answer;
- E4D05 in the fourth errata (February 4, 2026).

No E1A identifier is listed as changed or withdrawn in those four errata. That is a source finding as of July 18, 2026, not a guarantee against future errata or regulation changes. A content review must compare E1A against the then-current NCVEC file and current FCC rules immediately before publication.

### Rights policy

The accepted [Subject-Pack Rights Policy](rights-policy.md) is normative. It records official NCVEC pool wording, choices, keys, and identifiers as `public_domain` on the basis of NCVEC's release statement; original project lessons and explanations as CC-BY-4.0 copyright Adaptive Learning Agent contributors; and external official sources as `reference_only`. Project code/schemas remain Apache-2.0 and that license does not cover educational prose.

The policy is a project decision, not legal advice or formal legal review. The pilot contains no logos, seals, screenshots, branding assets, unofficial third-party study text, or substantial redistributed FCC/NCVEC website content. Complete official source snapshots are not required inside the pack.

## Selected slice

Select **question group E1A within subelement E1 (Commission Rules)**. NCVEC describes it as frequency privileges; signal frequency range; automatic message forwarding; stations aboard ships or aircraft; and 630-/2200-meter power restrictions.

E1A is preferable for the first real pilot because:

- it has exactly 11 active official questions, E1A01 through E1A11;
- it supports conceptual teaching about occupied bandwidth and band edges rather than answer memorization alone;
- every question carries a direct Part 97 rule citation in the official pool;
- it spans operational judgment and precise regulatory limits, exercising explanation citations well;
- it needs no diagrams, image assets, rendering feature, new scoring type, or calculation engine;
- it has no recorded pool erratum, while still allowing synthetic mutation tests of the errata mechanism.

The label “E1A group” is used deliberately. E1 is the subelement; E1A is the syllabus group/subtopic. The pilot must not call E1A a complete Extra curriculum.

## Pilot definition

| Item | Proposal |
|---|---|
| Pack ID | `us-amateur-extra-e1a` |
| Format/version | Accepted design format `0.2`, initial pack `0.2.0` |
| Language | `en-US` |
| Scope | E1A01–E1A11 exactly |
| Objectives | 2 |
| Lessons | 2 |
| Official questions | 11 |
| Generated questions | 0 |
| Diagrams/assets | 0 |

Objective 1, **band edges and occupied signals**, covers E1A01–E1A04 and E1A06 using §§ 97.301, 97.303(h), 97.305, and 97.307(b). Lesson 1 teaches how a complete emission, not merely the displayed carrier, must fit the authorized band/segment, plus the special 60-meter CW center-frequency rule.

Objective 2, **special operations and LF/MF power**, covers E1A05 and E1A07–E1A11 using §§ 97.5, 97.11, 97.219, and 97.313(k)–(l). Lesson 2 teaches license/control responsibilities aboard vessels or aircraft, accountability in automatic message forwarding, and the distinction between PEP and EIRP limits.

This mapping is a proposed teaching organization; it does not alter NCVEC identifiers, text, option order, or answer keys.

## Content-authoring rules

- Import E1A01–E1A11 only from the current consolidated NCVEC source and compare each record byte-for-semantic-field against a checked extraction record.
- Preserve official ID, prompt, option order/labels/text, and answer key exactly. Normal newline/Unicode normalization must not change meaning.
- Write explanations originally from the cited FCC rules. Each explanation must cite at least one precise section/paragraph and be reviewed by a human familiar with Part 97.
- Clearly label official questions. Do not present generated, recalled, or reconstructed questions as pool questions.
- Include no generated conceptual questions in 0.2A. The origin field is exercised by validator-negative fixtures, not learner-facing content.
- Treat agent suggestions and memory as drafts only. Pack files and recorded review evidence are authoritative after human approval.
- Apply component rights exactly as defined in [rights-policy.md](rights-policy.md); never call original explanations official NCVEC commentary.
- Include one approval record with `status: "approved"` and all nine E1A review-scope labels before the pack is installable.
- Record whether each source snapshot was retained. Include `content_sha256` when retained; do not fetch or depend on a remote source during validation or study.

## Expected learner workflow

1. Validate/install the immutable sourced pack and show its pool name, effective interval, errata check date, scoped rights, and source list.
2. Initialize or reconstruct the one local learner from tools.
3. Start practice and present the two lessons in order with visible FCC citations.
4. Present each selected official question exactly, label its official ID/origin, and request choice plus confidence without exposing its key or explanation.
5. Submit through the deterministic core. Show the core's exact result, reviewed explanation, and source locators only after scoring.
6. Permit challenge/quarantine through existing behavior; do not improvise a corrected key.
7. Finish with answered/correct/quarantined counts and a narrow practice summary, never an exam-readiness or mastery claim.

Question selection, attempts, retries, confidence, challenges, progress, and finish behavior remain those of version 0.1.

## Pilot acceptance tests

| ID | Expected proof |
|---|---|
| AE-01 | Golden source extraction contains exactly E1A01–E1A11 in order, and installed/tool output preserves every official ID exactly. |
| AE-02 | Golden comparisons fail on any prompt, option ID/order/text, or answer-key difference; a reviewed source correction requires a new pack version/digest. |
| AE-03 | Validation/install and study-start output expose full pool name, publisher, effective dates, fourth-errata date, rights scopes, and resolvable source records. |
| AE-04 | If a selected E1A ID is injected into the withdrawn list, validation fails. A corrected higher pack version installs separately and never rewrites old attempts. |
| AE-05 | `official_pool` requires matching official ID/source; `generated` forbids an official ID. The distinction is visible before learner presentation. |
| AE-06 | Every lesson and explanation citation resolves to an allowed authoritative source and non-empty locator; missing or unofficial references fail pilot policy validation. |
| AE-07 | Repeated validation/install produces the same digest; repeated study under controlled IDs/time preserves deterministic selection, scoring, retries, progress, and quarantine. |
| AE-08 | No `study.next` output contains answer keys or explanations; `study.submit` returns citations only with post-score feedback. |
| AE-09 | Both lessons are digest-covered, path-confined, declared, and returned in manifest order; an undeclared or modified lesson fails or changes the digest. |
| AE-10 | The existing format-0.1 `fixture-basics` bytes, digest, validation, install, and full AT-01–AT-12 workflow work unchanged. |
| AE-11 | Pilot content has zero generated questions and zero diagram/assets; content inventory enforces 2 objectives, 2 lessons, and 11 questions. |
| AE-12 | A skill-level acceptance run displays official origin/ID and citations accurately, uses tool state after restart, and makes no mastery/readiness claim. |
| AE-13 | The pack has one approved human record covering official wording, option ordering, keys, IDs, lessons, explanations, citations, rights, and pool/errata metadata. |
| AE-14 | Component rights match the normative policy and no prohibited logo, seal, screenshot, branding asset, or third-party study text is present. |
| AE-15 | Source records obey retained-snapshot digest rules and validation/study work with network access disabled. |

The complete 19-case format gate is normative in [Pack Format 0.2](pack-format-0.2-proposal.md#required-future-validation-cases) and mirrored in [the test plan](test-plan.md#10-format-02-and-e1a-design-gates). Tests using real question material belong only to a later explicitly authorized content task. This design task adds no fixture.

## Engine impact classification

- **Pack parsing/validation:** add the explicit version branch, multiple lesson loading/digesting, and strict source/citation/pool/errata/rights/origin/language/tag records.
- **Storage:** no schema change. Existing installed pack version/digest/path and session pinning are sufficient.
- **Tool contract:** retain contract `0.1`; add optional capability/provenance fields, multiple lessons, pre-answer origin/official ID, and post-answer citations. No new operations or request arguments.
- **Hermes skill presentation:** display provenance/currency, ordered lessons, exact official labels, and post-feedback citations; prohibit authority/readiness invention.
- **No change required:** deterministic scoring, choice types, attempts, confidence, sessions, retry reconstruction, quarantine, objective progress, health, and learner initialization.

## Explicit non-goals

- No complete Extra pool, full E1 subelement, mock exam, passing prediction, or certification claim.
- No generated/recalled questions, brain dumps, or unsourced explanations.
- No diagrams, executable pack content, YAML, archive/export, network fetcher, RAG, embeddings, vector database, claim-level evidence graph, signing, or marketplace.
- No mastery, scheduling, adaptive algorithm, new scoring type, authoring agent, autonomous activation, or general review subsystem.
- No implementation in this task.

## Remaining execution inputs

No format-0.2 design question remains open. A future implementation/content task must still name the human reviewer, decide which source snapshots are actually retained and record their real hashes, recheck the pool/errata/current Part 97, author and review the content, and obtain any desired formal legal review. These are release inputs, not reasons for the engine to fetch sources or authenticate reviewers.
