# Amateur Extra Official-Asset Pilot 0.2B

Status: Proposed research and design; implementation and content import are not authorized  
Updated: 2026-07-19

## Authoritative baseline

Research used only the NCVEC Question Pool Committee's current official material, retrieved on 2026-07-18:

- [2024–2028 Extra Class Question Pool release page](https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release), which identifies the fourth errata dated 2026-02-04 as current, withdraws E4D05, and links the current pool and figure distributions;
- [consolidated fourth-errata pool PDF](https://ncvec.org/downloads/2024-2028%20Extra%20Class%20Question%20Pool%20and%20Syllabus%20Public%20Release%20with%204th%20Errata%20Feb%204%202026.pdf), SHA-256 `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517`;
- the corresponding official DOCX, SHA-256 `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7`;
- [official three-page figure PDF](https://www.ncvec.org/downloads/Extra_Figures_2024-2028-1.pdf), SHA-256 `591bb4c9fc9a9267e298b3ee23c93ab54ba3813f8ea3730123f9ccda1e4b80f2`;
- official page JPEGs and the official `E4_2024-svgs.zip`, all linked from the release page.

The release page says the 2024–2028 Element 4 Extra Class Question Pool is released into the public domain. It separately records a January 31, 2024 correction rotating Figure E9-3 to the conventional orientation. No later figure-specific correction is listed. This review does not rely on model memory and does not copy any question or asset into the repository.

## Candidate inventory

The consolidated DOCX and its ten embedded PNGs were inspected directly. “Questions” below counts active questions that require the identified figure, not every question in the group. Every figure is available in the official distribution as an individual SVG, as an embedded PNG in the consolidated DOCX, and within the official PDF and composite page JPEGs.

| Group | Active figure questions | Figure | Reuse | Current errata finding | Accessibility | Rendering | Pilot suitability |
|---|---:|---|---|---|---|---|---|
| E5C | 3: E5C10–E5C12 | E5-1 impedance plot | One figure for 3 | No figure errata found | High: axes, coordinates, and eight labeled points | Medium | Medium; useful reuse but dense nonvisual description |
| E6A | 2: E6A10–E6A11 | E6-1 transistor symbols | One figure for 2 | No figure errata found | High: six similar symbols; descriptions can identify answers | Low | Medium-low |
| E6B | 1: E6B10 | E6-2 diode symbols | One figure for 1 | No figure errata found | High: eight similar symbols; answer-leak risk | Low | Low; no reuse |
| E6C | 3: E6C08, E6C10–E6C11 | E6-3 logic symbols | One figure for 3 | No figure errata found | High: symbol semantics are the tested knowledge | Low | Medium-low |
| **E7B** | **3: E7B10–E7B12** | **E7-1 amplifier circuit** | **One figure for 3** | **No figure errata found** | **Medium: connections and labels can be described without naming functions/topology** | **Low** | **High; selected** |
| E7D | 3: E7D06–E7D08 | E7-2 regulator circuit | One figure for 3 | No figure errata found | Medium-high: component purposes are tested directly | Low | High fallback, but a neutral description is harder |
| E7G | 5: E7G02, E7G07, E7G09–E7G11 | E7-3 op-amp circuit | One figure for 5 | No figure errata found | Medium: compact circuit, but formula relationships are central | Low | Medium; larger slice |
| E9B | 6: E9B01–E9B06 | E9-1 and E9-2 antenna plots | 3 questions per figure | No errata found for E9-1/E9-2 | High: polar scales and lobes require lengthy spatial alternatives | Medium | Low for a one-asset pilot |
| E9G | 2: E9G06–E9G07 | E9-3 Smith chart | One figure for 2 | **Corrected 2024-01-31; current files state the correction is incorporated** | Very high | Medium | Low; historically corrected and visually dense |

No candidate has unresolved current errata in the official release materials. “No figure errata found” means the current release page and consolidated pool list none; it is not a claim that NCVEC can never issue later errata.

## Selected pilot

Select exactly **E7B10, E7B11, and E7B12 using official Figure E7-1**.

The group is the smallest strong reuse case: one static monochrome circuit serves three questions, requires no color, animation, interaction, software, or network access, and has no listed figure errata. It exercises component-label fidelity, topology, shared references, accessibility, digesting, restart behavior, and fallback presentation without the graphical density of the coordinate and antenna plots.

### Asset identity and bytes

The preferred pilot representation is the **exact PNG embedded as `word/media/image5.png` in the current official DOCX**, not a screenshot or newly rendered image. Research inspection found:

- official figure identity: `Figure E7-1`;
- media type: `image/png`;
- dimensions: 796 × 674 pixels;
- byte length: 41,357;
- asset SHA-256: `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`;
- source-container SHA-256: `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7`.

Mapping `image5.png` to E7-1 was established from the DOCX's figure order and relationship/media inventory and must be independently compared visually and structurally before approval. The hash above is research evidence, not an approved release digest. No image bytes are added by this design.

The official standalone SVG `E7-1.svg` is also available, SHA-256 `246896b7c2ec1c8b2b3d0e99037b1e88aeeea5746a94e8913e9c14f717b397ca`, with view box `0 0 252 231`. It declares an Arial-family font. Rendering it to PNG would therefore create a project-derived representation with possible font, rasterization, and antialiasing differences. The embedded official PNG avoids that conversion.

### Objectives and lessons

The pilot should remain one group and may use two concise original lessons:

1. identify circuit nodes, labeled components, and signal/rail paths without naming a keyed answer;
2. reason from the visible connections to bias, feedback, and amplifier configuration.

Proposed objectives are to (a) trace the labeled bias and signal paths in E7-1 and (b) infer component purpose and amplifier configuration from those connections. The full E7B domain is not claimed.

### Rights finding

NCVEC's official release page places the pool, figure downloads, public-domain statement, and figure errata together. The project may reasonably propose that Figure E7-1, its labels, and the question-to-figure wording are included in the released pool. The page does **not** separately say “all diagram bytes and transformed formats are public domain,” and this project has no formal legal opinion. Asset redistribution therefore remains a required human rights-review scope before import or release.

For the pilot:

- the exact official E7-1 PNG bytes and official labels are proposed as `public_domain` under the NCVEC basis;
- question-to-figure references remain official question content under the same basis;
- project-authored alt text, caption, fallback, lessons, and explanations remain separately copyrighted project prose under CC-BY-4.0;
- fonts, renderers, and conversion tools are not pack content and retain their own terms;
- screenshots, crops, re-creations, third-party renderings, and generated images are prohibited;
- if exact embedded PNG use is rejected, any converted representation must be labeled project-derived and record both source and output hashes plus the complete conversion procedure.

This is project policy and an evidence finding, not legal advice. Whether the NCVEC statement legally reaches every distributed container byte or transformation is unresolved pending human review.

### Accessibility approach

Alternative text must describe labels, connections, orientation, and spatial relationships, not interpret R1/R2/R3, name the amplifier topology, or repeat any keyed option text. A separate terminal fallback may use a line-oriented node/connection list. Both must be reviewed against all three questions because one shared description can leak different answers in different contexts.

The caption should identify only the source and figure, for example “Official NCVEC Figure E7-1.” The learner must receive the figure or fallback before being asked to answer and must be able to report that it is inaccessible.

### Expected Hermes workflow

1. The deterministic core returns the question, ordered options, and a structured logical asset descriptor.
2. The adapter resolves only that validated installed-pack asset reference.
3. If a verified Hermes surface can attach/display the exact local PNG, it does so before the answer prompt and also exposes reviewed alt text.
4. Otherwise it displays the reviewed terminal fallback and clearly states that image rendering is unavailable.
5. The skill confirms access, then asks for the option and confidence. It never asks a model to inspect or paraphrase the diagram.
6. After deterministic scoring, `study.submit` may return project-authored explanation references to E7-1.

Hermes's current official [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) documents JSON-string tool handlers, and its [vision documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/vision.md) documents image input and vision routing. Neither verifies a generic custom-plugin local-image attachment path for the project's pinned Hermes v0.18.2 CLI. Native E7-1 image delivery is therefore **unverified** and must be proven against the pinned release; the text fallback is mandatory and runtime-neutral.

### Explicit non-goals

- No other question group, full E7B instruction, full Amateur Extra preparation, generated question, or assessment simulation.
- No SVG/JPEG support, remote asset, URL fetch, HTML, script, video, audio, animation, interaction, OCR, image generation, or conversion pipeline.
- No image interpretation or scoring by Hermes or a model.
- No SQLite, scoring, selection, session, retry, challenge, progress, capability-discovery, subject-builder, AWS, archive, or MCP change.
- No question or figure import in this design task.

## Approval and implementation gates

Before a separate implementation/content task, humans must approve official asset identity, visual fidelity, source/container mapping, rights metadata and redistribution basis, alt text, caption, terminal fallback, all three question-to-asset mappings, and absence of pre-answer leakage. A fresh NCVEC pool/errata check and exact figure comparison are required at that time.
