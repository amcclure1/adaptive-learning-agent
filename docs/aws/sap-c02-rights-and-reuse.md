# SAP-C02 Rights and Reuse Classification

Status: project-policy analysis; not legal advice

Research date: 2026-07-18

Decision: official AWS sample questions are analysis-only unless AWS grants specific reuse permission

## Governing conclusion

Public availability is not redistribution permission. The official sample-question PDF carries an AWS copyright notice stating that all rights are reserved, and no public-domain statement, open license, assessment reuse policy, or specific permission was found. The project therefore may inspect the sample to learn assessment grammar but may not include its wording, recognizable scenarios, ordered options, keys, or close paraphrases in an open-source pack. [Official sample PDF](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf) [AWS Site Terms](https://aws.amazon.com/terms/)

AWS Site Terms separately state that documentation hosted on `docs.aws.amazon.com` is licensed under CC BY-SA 4.0 and code in that documentation under MIT-0. That supports attributed use of service/exam-guide documentation within the license, but it does not apply that license to the separately hosted `d1.awsstatic.com` sample PDF. [AWS Site Terms](https://aws.amazon.com/terms/)

## Source-level classification

| Source / component | Classification | Allowed use now | Not allowed now | Basis |
|---|---|---|---|---|
| Official SAP-C02 sample PDF | **Analysis-only** | Manually record aggregate format, command language, constraint, option, and distractor characteristics | Redistribute questions/rationales; quote distinctive wording; store answer combinations; create close substitutes | Copyright notice; no explicit reuse grant found |
| Official Practice Question Set in AWS Skill Builder | **Style evidence only** pending authorized access | An authorized reviewer may record non-expressive characteristics and confidence | Copy, export, scrape, retain, or reproduce item text; treat account access as a license | Certification page describes it as exam-style preparation, not reusable content |
| Official Practice Exam in AWS Skill Builder | **Style evidence only** pending subscription/access | Same narrow analysis if later authorized | Same prohibitions; no live-item inference | Certification page; access not used in 0.3A |
| SAP-C02 HTML exam guide on `docs.aws.amazon.com` | **Reusable with attribution** under CC BY-SA 4.0 for documentation text; project preference is cite/paraphrase | Quote small task labels, attribute, link, preserve license obligations | Present as project-authored; imply AWS endorsement | AWS Site Terms |
| Version-1.2 exam-guide PDF on `d1.awsstatic.com` | **Analysis-only / reference-only** for fail-closed project use | Cite title/version/page locators and paraphrase factual scope | Redistribute PDF or assume docs-site license applies | No PDF-specific license found |
| AWS service user guides / Well-Architected pages on `docs.aws.amazon.com` | **Reusable with attribution** under CC BY-SA 4.0; use as factual/guidance evidence | Cite and paraphrase; copy only when license/attribution/share-alike is deliberately satisfied | Remove attribution; turn recommendations into universal facts | AWS Site Terms |
| AWS certification page, policy pages, and AWS blog pages | **Reference-only** | Cite and paraphrase facts | Redistribute substantial text or imagery; imply endorsement | AWS Site Terms' general site-content restrictions |
| Original project question designs and later questions | **Original project content, draft until human approval** | Develop from approved claims and independently authored scenarios | Label official, actual, recalled, or AWS-endorsed | ADR 0011 and ADR 0013 |

No source qualified as `reusable verbatim` without attribution. No official assessment question qualified as `reusable with attribution`. `Unresolved rights` is reserved for a later source whose terms genuinely cannot be determined; it is not a reason to copy while waiting.

## Similarity boundary

> Copy the assessment grammar, not the assessment sentences.

The project may reproduce abstract assessment characteristics:

- single-response and multiple-response structures and explicit selection counts;
- professional cognitive demand, scenario density, requirement count, constraint interaction, and command forms;
- realistic comparisons among AWS services or architectural patterns grounded in current documentation;
- prioritization by cost, resilience, performance, security, migration risk, or operational overhead;
- distractor categories and parallel option construction;
- cross-domain reasoning and text-only requirement lists.

The project must not reproduce:

- distinctive AWS sample wording or recognizable fact patterns;
- the same unusual combination of organization, workload, numbers, failure, options, and key;
- recalled live items, leaked keys, or candidate-memory composites;
- unauthorized commercial question text or answer combinations;
- synonym-swapped or reordered paraphrases that function as substitutes for a source item;
- official rationales translated into project questions with only cosmetic changes.

## Future similarity review

The 0.3B reviewer should compare each original design against the **abstract notes** in the blueprint, not against a retained dump or copied bank. Review should ask:

1. Was the scenario independently derived from an approved objective and claim set?
2. Does it reuse a distinctive combination of facts, numbers, roles, or option sequence from an official sample?
3. Would a reasonable reader familiar with the public sample recognize it as the same question despite different words?
4. Are services compared because the objective and evidence require them, rather than because a source item used them?
5. Is provenance available for every design decision without unsafe source material?

A `yes` or credible uncertainty on questions 2 or 3 sends the item back for replacement, not word-level editing. Exact algorithmic similarity thresholds remain unresolved because they can miss structural copying and would encourage retaining protected comparison corpora.

## Approval and change effects

- A human rights reviewer approves the source classification before content activation.
- Permission for one AWS component does not cover another component.
- A changed URL, copyright notice, site term, provider policy, or requested distribution mode invalidates the affected rights conclusion and requires renewed review.
- A later written AWS permission must be stored with its scope, date, grantor identity, allowed uses, attribution requirements, sublicensing/distribution terms, expiration, and revocation conditions.
- Pack-release approval cannot cure a missing rights basis.

## Unresolved issues

- Formal legal review has not been performed.
- It is unresolved whether AWS would grant specific open-source redistribution permission for the ten public sample questions. The recommendation is **do not seek or depend on that permission for 0.3B**; original questions are safer and better test the evidence-backed authoring chain.
- The current Skill Builder terms applicable to the Official Practice Question Set were not reviewed because no account/private material was accessed. If a human uses that material in 0.3B, record the then-current terms and keep the source analysis-only unless explicit permission says otherwise.
