# Evidence Policy

Status: proposed for review  
Design baseline: 2026-07-18

## Purpose

Evidence policy prevents a fluent agent response from becoming an unreviewed fact in a learning pack. It governs pack release validation, not general conversation. Agent memory, a chat transcript, search snippets, and model citations are discovery aids only.

## Evidence modes

Each pack declares exactly one mode:

- `none`: citations are optional. Structural and question reviews may still be required by pack policy.
- `recommended`: missing evidence produces warnings unless a stricter rule applies.
- `required`: release validation fails unless every scored question and every declared critical claim satisfies the evidence and review gates.

Draft packs may remain incomplete. They are clearly marked `draft` and cannot be installed for normal learner mode or exported as a release.

## Authority classes

From strongest to weakest:

1. `law_or_regulation`: official law, regulation, regulator order, or government publication.
2. `official_standard`: a standard or official question pool published by its responsible body.
3. `vendor_primary`: a vendor's official exam guide, product documentation, whitepaper, or service limits page.
4. `maintainer_primary`: an authoritative upstream project specification or documentation.
5. `recognized_secondary`: a reputable educational or professional source used for explanation, not to override primary material.
6. `community`: forums, personal sites, generated summaries, and other discovery sources.

A pack declares allowed classes. A secondary or community source cannot be the sole support for a scored answer in `required` mode unless the pack explicitly allows it and a review explains why no primary source applies.

## Source record

Every source has:

- stable `source_id`;
- title and publisher;
- canonical URL or bibliographic locator;
- authority class;
- retrieval date;
- effective/version date when known;
- applicability scope, such as exam version, rules edition, region, or service;
- optional content digest for a legally stored local snapshot;
- optional supersedes/superseded-by relationship;
- notes about access, licensing, and quotation limits.

A URL alone is not evidence. The locator must be specific enough for a reviewer to find the support, such as a section, heading, paragraph, rule number, or anchored fragment.

## Claim and question traceability

Evidence references live on the exact content they support:

- Each scored question lists one or more `evidence_refs`.
- Each reference names `source_id`, a precise locator, and a short paraphrased support note.
- Verbatim excerpts are optional and should be avoided when licensing is unclear.
- A critical Markdown claim uses a compact claim marker that maps a stable claim ID to source references in `claims.yaml`.

The validator checks references and policy mechanically. A human reviewer checks whether the cited material actually supports the accepted answer and rationale.

## Review gates

The default release checklist for each scored question is:

1. **Answerability**: all information needed is present; wording has one defensible interpretation.
2. **Correctness**: accepted response and deterministic scoring configuration are correct.
3. **Objective alignment**: the question tests the named objectives at the declared level.
4. **Evidence support**: citations support the accepted answer, rationale, and material distractor claims.
5. **Distractor quality**: incorrect options are plausible but unambiguously wrong under the cited scope.
6. **Explanation quality**: rationale explains why the answer is correct without relying on hidden agent reasoning.
7. **Currency and scope**: dates, exam version, jurisdiction, and service behavior are applicable.
8. **Rights and originality**: the item does not copy protected exam content or exceed source-use permissions.

A review has `accepted`, `changes_requested`, or `rejected` outcome and is bound to the SHA-256 digest of the canonical question object, its evidence references, and the canonical source records those references use. Editing any of them invalidates the acceptance.

Local reviewer names are attestations, not verified identities. If a pack declares `independent_review: true`, the validator requires distinct author and reviewer labels but must describe this as a consistency check, not proof of independence.

## Currency

Pack policy may define:

- `effective_from` and `effective_until` for the pack;
- `review_by` for each source or question;
- maximum source age by authority class;
- hard failure on superseded sources;
- warning or failure when a URL has not been rechecked.

Offline validation checks recorded metadata and digests. Network reachability checks are a separate, explicit operation and cannot change review outcomes automatically. An inaccessible URL does not prove the content false, and a reachable URL does not prove the content current.

## Pilot policies

### AWS SAP-C02

- Evidence mode: `required`.
- Primary classes: `vendor_primary`; `recognized_secondary` may supplement explanations only.
- Pack scope must state the SAP-C02 exam guide version or retrieval date.
- Service behavior, quotas, and feature availability require an official AWS source and a review-by date appropriate to volatility.
- Questions must be original and must not claim to be recalled or copied exam questions.
- Scenario questions must document why each material distractor conflicts with cited AWS guidance.

### US Amateur Extra

- Evidence mode: `required`.
- Primary classes: `law_or_regulation` and `official_standard`.
- Pack scope must identify the FCC rule edition/retrieval date and the exact Amateur Extra question-pool effective dates when pool content is used under its applicable terms.
- Regulatory answers must cite the applicable 47 CFR section; explanatory material may additionally cite recognized secondary sources.
- A change in rules or question-pool period makes affected questions due for review and may expire the pack.

## Validation outcomes

- `error`: blocks release export and normal installation.
- `warning`: permits release but is shown during validation and installation.
- `info`: traceability or maintenance note.

Minimum errors in `required` mode include missing source, disallowed authority class, missing precise locator, expired applicability, superseded source, unsupported accepted answer, missing accepted review, stale review digest, and prohibited copied-content attestation failure.

## Agent behavior

The agent may locate candidate sources, paraphrase them, draft questions, and prepare review checklists. It may not:

- promote a source to an authority class without user-visible metadata;
- accept its own generated review on behalf of a human;
- mark a pack released or published without an explicit user tool call;
- use memory or a prior conversation as a citation;
- change scoring because a conversational answer “seems close.”

When reviewed pack content is insufficient, the agent should say so and offer to enter authoring/review mode. It must not fill the gap with an uncited answer presented as pack authority.
