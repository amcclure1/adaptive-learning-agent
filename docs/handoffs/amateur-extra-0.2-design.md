# Amateur Extra 0.2A Design Handoff

Date: 2026-07-18
Status: design complete; review required; implementation unauthorized

## Outcome

The proposed first real-content slice is NCVEC question group E1A within Extra subelement E1. It contains exactly 11 current official questions (E1A01–E1A11), has direct FCC citations, teaches meaningful band-edge and special-operation concepts, and needs no diagrams. The pilot proposes two objectives, two lessons, 11 official questions, and zero generated questions.

No Amateur Extra wording, choices, keys, explanations, lessons, pack files, or engine behavior were implemented.

## Source baseline

- Pool: 2024–2028 Extra Class FCC Element 4 Question Pool and Syllabus.
- Publisher/maintainer: NCVEC Question Pool Committee.
- Effective: 2024-07-01 through 2028-06-30.
- Consolidated errata reviewed: fourth errata, 2026-02-04.
- Official withdrawals recorded: E2A13, E4D05, E6D07, and E9E10; none in E1A.
- Rules relevant to E1A: 47 CFR §§ 97.5, 97.11, 97.219, 97.301, 97.303(h), 97.305, 97.307(b), and 97.313(k)–(l).
- Exam structure: Element 4 has 50 questions with 37 required to pass; E1 contributes six questions from six groups.

Links and source limitations are recorded in [the pilot proposal](../amateur-extra-pilot-0.2.md).

## Proposed format and engine boundary

Proposed ADR 0009 introduces explicit JSON/Markdown format `0.2` because strict format 0.1 cannot safely accept new semantics as optional fields. It adds only multiple lessons, language/tags, official/generated origin and official IDs, pool/effective/errata metadata, source/citation records, and scoped rights.

Required future core work is limited to versioned pack models/parsing/validation/digesting and additive tool results for sourced metadata, multiple lessons, origin/official IDs, and post-answer citations. The Hermes skill would present those fields accurately. SQLite schema, scoring, attempts, confidence, sessions, retry behavior, quarantine, and objective progress require no change.

## Licensing boundary

NCVEC explicitly states that it releases the pool into the public domain. Project legal review remains unresolved. That statement must not be assumed to cover original explanations, lessons, third-party study text, seals, logos, or website presentation. The pilot needs a separate component-level license/notice for original prose and must copy no unofficial material.

## Review gate before implementation

1. Review Proposed ADR 0009 and the format schema.
2. Resolve the component-level rights notice.
3. Decide source snapshot/digest and tool capability-version questions.
4. Define a named human content-review approval record.
5. Recheck current NCVEC errata and current Part 97.
6. Author content in a separately authorized change with golden source comparisons and all AE-01–AE-12 tests.

## Documents produced

- [Roadmap](../roadmap.md)
- [0.1.0 release record](../releases/0.1.0.md)
- [0.2A pilot proposal](../amateur-extra-pilot-0.2.md)
- [Pack format 0.2 proposal](../pack-format-0.2-proposal.md)
- [Proposed ADR 0009](../decisions/0009-sourced-pack-format-0.2.md)

Stop here for design review. Do not begin question import, lesson/explanation authoring, loader changes, database changes, tool changes, or skill expansion under this handoff.
