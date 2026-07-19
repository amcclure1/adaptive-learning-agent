# Amateur Extra E7B Asset Content Review

Status: **PENDING — explicit human review required**  
Candidate: `us-amateur-extra-e7b` version `0.2.1-alpha.1`  
Format: `0.3`  
Draft digest: `9c43be04bc38910f12ddf1d90eb62e69cd916ed06fccf44c0770e6fbf2218d43`  
Asset SHA-256: `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`

This is a human decision record, not an agent approval. The public validator and installer reject this candidate while `approval.status` is `pending`. Any content change after review changes the digest and invalidates the decision.

## Authoritative baseline

On 2026-07-18, the current [NCVEC Extra Class release page](https://www.ncvec.org/index.php/2024-2028-extra-class-question-pool-release) still identified the fourth errata dated February 4, 2026 as current. The current DOCX SHA-256 is `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7`; the current consolidated PDF SHA-256 is `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517`. No consolidated errata entry affects E7B10, E7B11, E7B12, or Figure E7-1.

The complete machine-readable retrieval and mapping evidence is [amateur-extra-e7b-source-verification.json](evidence/amateur-extra-e7b-source-verification.json). The exact candidate image is [figure-e7-1.png](../../packs/amateur-extra-e7b/assets/figure-e7-1.png). Compare it with the official [figure PDF](https://www.ncvec.org/downloads/Extra_Figures_2024-2028-1.pdf), page 2, or the official [page-2 JPEG](https://www.ncvec.org/downloads/2024-2028%20Amateur%20Extra%20Class%20Pool%20Diagrams_Page_2.jpg).

## Deterministic source-member mapping

- DOCX member: `word/media/image5.png`
- DOCX relationship: `rId10` → `media/image5.png` (one document embed)
- Exact member length: 41,357 bytes
- Exact member SHA-256: `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`
- PNG IHDR: 796×674, 8-bit truecolor
- PNG structure/chunk CRCs: valid
- Identity printed in the exact pixels: `Figure E7-1`
- Candidate file comparison: byte-for-byte equal to the extracted member
- Transformations: none; no crop, redraw, recolor, annotation, regeneration, normalization, thumbnail, or metadata rewrite

These facts are deterministic evidence. The reviewer must still decide identity, visual fidelity, and redistribution policy.

## Official-question comparison

| ID | Official key | Exact prompt | Exact ordered options | Status |
|---|---|---|---|---|
| E7B10 | B | In Figure E7-1, what is the purpose of R1 and R2? | A Load resistors; B Voltage divider bias; C Self bias; D Feedback | Pending |
| E7B11 | D | In Figure E7-1, what is the purpose of R3? | A Fixed bias; B Emitter bypass; C Output load resistor; D Self bias | Pending |
| E7B12 | C | What type of amplifier circuit is shown in Figure E7-1? | A Common base; B Common collector; C Common emitter; D Emitter follower | Pending |

The golden record is [amateur-extra-e7b-official.json](../../tests/fixtures/amateur-extra-e7b-official.json). It pins IDs, prompts, ordered option labels/text, keys, locators, source digest, member mapping, asset digest, byte length, and dimensions.

## Accessibility candidate

Caption:

> Official NCVEC Figure E7-1.

Alt text:

> Black-and-white transistor circuit labeled Figure E7-1. IN connects through C1 to a junction shared with the transistor's left lead, the lower end of R1, and the upper end of R2. R1 continues to the top rail; R2 continues to ground. The top rail, marked with a plus sign at its right end, also connects through a vertical unlabeled resistor to the transistor's upper-right lead. That upper-right junction connects through C2 to OUT. The transistor's lower-right lead joins the upper end of R3 and the left side of C3. R3 continues to ground, and C3 continues to a separate ground symbol.

Terminal fallback:

> Orientation: IN is at the left, OUT is at the right, a plus-marked rail is at the top, and ground symbols are at the bottom.  
> Input node: IN connects through C1 to one junction. That junction connects to the transistor's left lead, the lower end of R1, and the upper end of R2.  
> R1 and R2: R1 connects from the input junction to the top rail. R2 connects from the input junction to ground.  
> Upper-right transistor node: The transistor's upper-right lead shares a junction with the lower end of a vertical unlabeled resistor and the left side of C2. The resistor's upper end connects to the top rail. C2 continues right to OUT.  
> Lower-right transistor node: The transistor's lower-right lead shares a junction with the upper end of R3 and the left side of C3. R3 continues to ground. C3 continues right and then down to a separate ground symbol.

Deterministic lint currently passes: no explicit answer marker and no complete normalized keyed-option text appears in the title, caption, alt text, or fallback. Lint cannot establish semantic safety. Review all text separately against E7B10, E7B11, and E7B12.

## Rights disposition proposed for review

- Official E7B10–E7B12 records: public domain under the NCVEC release statement, as project policy.
- Exact E7-1 geometry and labels in the embedded PNG: public domain under the same project-policy interpretation, pending explicit approval that this basis supports redistribution of the exact container member.
- Caption, alt text, fallback, lessons, and explanations: CC-BY-4.0 original project prose.
- External sources: reference metadata and links only.
- This is project policy, not legal advice or formal legal review.

## Review checklist

| Review item | Evidence or target | Human result |
|---|---|---|
| E7B10 official identity, wording, options/order, key, locator | Golden record and current DOCX/PDF | Pending |
| E7B11 official identity, wording, options/order, key, locator | Golden record and current DOCX/PDF | Pending |
| E7B12 official identity, wording, options/order, key, locator | Golden record and current DOCX/PDF | Pending |
| Figure identity | Exact candidate pixels print `Figure E7-1`; compare official page 2 | Pending |
| Source member mapping | DOCX `rId10` → `word/media/image5.png`; one embed | Pending |
| Source hashes and current errata | Evidence JSON; baseline matches; no E7B/E7-1 change found | Pending |
| Visual fidelity and absence of alteration | Exact member and official figure distribution comparison | Pending |
| Redistribution policy | NCVEC public-domain statement and proposed project disposition | Pending |
| Caption | Candidate above | Pending |
| Alt text | Candidate above, reviewed against all three questions | Pending |
| Terminal fallback | Candidate above, reviewed against all three questions | Pending |
| Question-to-asset mappings/order | One shared E7-1 asset first/only for E7B10–E7B12 | Pending |
| Lesson 1 | `01-reading-figure-e7-1.md` | Pending |
| Lesson 2 | `02-reasoning-from-connections.md` | Pending |
| Explanations | Three project-authored post-answer explanations in `pack.json` | Pending |
| Citations/source locators | Four source records and per-content citations in `pack.json` | Pending |
| Component rights and `NOTICE.md` | Public-domain/project-policy, CC-BY-4.0, reference-only separation | Pending |
| No leakage across E7B10–E7B12 | Accessibility text and pre-answer descriptors; lint is only supporting evidence | Pending |
| Final activation of exact candidate digest | Must be an explicit human decision | Pending |

## Approval boundary

To approve, the reviewer must explicitly identify themselves and approve all of these scopes for the exact candidate: source mapping; visual fidelity; redistribution policy; official content; caption, alt text, and fallback; all mappings/order; non-leakage across all three questions; lessons, explanations, and citations; component rights; and final activation.

After that statement, the implementation agent will record the actual reviewer name and actual UTC completion time, replace the pending approval with the complete scope list, calculate the resulting approved digest, and then run installability, real Hermes fallback acceptance, the Python 3.12–3.14 matrix, hosted CI, and readiness closure. No release or tag will be created.
