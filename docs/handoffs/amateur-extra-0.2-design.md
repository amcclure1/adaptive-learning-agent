# Amateur Extra 0.2A Design Handoff

Date: 2026-07-18
Status: Superseded by `amateur-extra-0.2-final-design.md`; implementation unauthorized

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

## Finalized format and engine boundary

Accepted ADR 0009 introduces explicit JSON/Markdown format `0.2` because strict format 0.1 cannot safely accept new semantics as optional fields. It adds only multiple lessons, language/tags, official/generated origin and official IDs, pool/effective/errata metadata, source/citation records, scoped rights, and one human approval record.

Required future core work is limited to versioned pack models/parsing/validation/digesting and additive tool results for sourced metadata, multiple lessons, origin/official IDs, and post-answer citations. The Hermes skill would present those fields accurately. SQLite schema, scoring, attempts, confidence, sessions, retry behavior, quarantine, and objective progress require no change.

## Rights boundary

The accepted [rights policy](../rights-policy.md) scopes NCVEC pool material as `public_domain`, original lessons/explanations as CC-BY-4.0, and external official sources as `reference_only`. Project code and schemas remain Apache-2.0. This is project policy, not legal advice or formal legal review.

## Final status

The design questions listed in this handoff are resolved. The authoritative implementation-ready handoff is [amateur-extra-0.2-final-design.md](amateur-extra-0.2-final-design.md). Implementation remains separately gated; no question import, content authoring, parser, contract, database, test-code, or Hermes change is authorized here.

## Documents produced

- [Roadmap](../roadmap.md)
- [0.1.0 release record](../releases/0.1.0.md)
- [0.2A pilot proposal](../amateur-extra-pilot-0.2.md)
- [Pack format 0.2 proposal](../pack-format-0.2-proposal.md)
- [Accepted ADR 0009](../decisions/0009-sourced-pack-format-0.2.md)
- [Subject-Pack Rights Policy](../rights-policy.md)
- [Final design handoff](amateur-extra-0.2-final-design.md)

This historical handoff is superseded. Follow the final handoff and its explicit implementation-authorization gate.
