# Static-Asset Accessibility and Non-Leakage Policy

Status: Proposed for asset-capable pack format 0.3  
Updated: 2026-07-19

## Purpose and scope

This policy applies only to reviewed static local assets in a future format-0.3 pack. It makes nonvisual access and answer safety release gates rather than runtime improvisation. It does not authorize format 0.3, asset import, or implementation.

## Required representations

Every question-required asset must have four distinct, digest-covered records:

- `title`: a short identity suitable for menus and diagnostics;
- `caption`: visible source/identity context, not a visual substitute;
- `alt_text`: a concise nonvisual description of the information encoded by the figure;
- `terminal_fallback`: a text-only representation usable when image display is unavailable.

Caption and alt text are not interchangeable. A caption may say “Official NCVEC Figure E7-1”; alt text must describe the diagram. The fallback may be longer and structured as nodes, connections, coordinates, or a table. All project-authored accessibility text has its own rights record and is not official or public-domain merely because the source figure is.

Decorative assets are outside format 0.3. Therefore empty alt text is always invalid for a declared asset.

## Equivalent access without solving

Accessibility text must expose the same relevant labels and relationships that a sighted learner can inspect, while avoiding interpretation that the figure leaves to the learner. For a circuit, describe component labels, nodes, connections, rails, polarity, and signal direction. Do not name the circuit type or the purpose of a component when that is what the question asks.

Spatial language must be unambiguous and screen-reader-friendly:

- establish orientation before detail;
- identify each label exactly as printed;
- describe connections by endpoints rather than relying only on “left,” “above,” or visual proximity;
- state crossing-without-connection and junctions when material;
- use ordered sections and short sentences;
- avoid ASCII art as the sole fallback because screen-reader traversal is unreliable.

If a faithful nonvisual representation would necessarily disclose the keyed answer, the asset/question combination is not eligible for format 0.3. The validator must not silently waive this requirement.

## Pre-answer leakage rules

Before submission, title, caption, alt text, fallback, asset identifiers, and adapter prose must not:

- state or imply which option is correct;
- use phrases such as “correct answer,” “keyed answer,” “choose option,” or “the answer is”;
- reproduce a keyed option's complete normalized text as an asserted interpretation;
- name the tested component function, circuit classification, plotted value, or symbol identity unless the figure itself prints that name;
- add arrows, highlights, annotations, crop focus, or explanations absent from the official asset;
- use model-generated descriptions or OCR output in place of the approved text.

A deterministic lint should reject prohibited answer-marker phrases and exact normalized keyed-option text in pre-answer accessibility fields. That lint is necessary but cannot prove semantic safety. Human review across every question referencing the asset remains authoritative.

After submission, project-authored explanations may interpret the figure, but must be labeled as project-authored, cite their sources, and remain distinct from official figure content.

## Presentation sequence

For an asset-backed question, every runtime adapter and skill must:

1. obtain the descriptor from deterministic core output;
2. present the exact validated asset if the surface supports it, otherwise present the approved fallback;
3. make alt text available with the asset;
4. confirm that the learner can access one of those representations;
5. only then request an answer and confidence;
6. permit challenge/quarantine when the asset or fallback is unusable or appears wrong.

The model must not paraphrase official labels, create a substitute description, infer an answer from pixels, or treat conversation memory as the accessibility record.

## Human approval scope

An installable asset-capable pack must record human approval of all of the following for the exact pack version and digest:

- official asset identity;
- visual fidelity and absence of alterations;
- authoritative asset source and source-container mapping;
- rights basis and component-rights metadata;
- alt text;
- caption;
- terminal fallback;
- every question-to-asset mapping and presentation order;
- absence of answer leakage across every referencing question.

The reviewer should be able to compare the distributed bytes with the authoritative source and evaluate the subject meaning of the accessibility text. One person may fill multiple roles, but every scope must be explicit. An agent author may not approve its own text.

Any change to asset bytes, dimensions, metadata, alt text, caption, fallback, question mapping, source, or rights invalidates the prior digest and requires a new pack version or renewed approval under the format's immutable-version rules.

## Runtime fallbacks and failures

- Image-display failure must degrade to the approved terminal fallback, not to network retrieval or model vision.
- If both image and fallback are inaccessible, do not solicit an answer; explain the limitation and allow challenge/quarantine or session exit.
- Screen-reader output must place asset identity and description before options and must avoid dense Markdown tables when a list is clearer.
- A terminal fallback must work offline and after process restart.
- Runtime-specific image support is a capability, not a pack dependency. Packs remain usable through the text fallback in other runtimes.

## Pilot-specific review

For E7-1, the accessibility text may name IN, OUT, R1, R2, R3, C1, C2, C3, the printed plus sign, and exact connections. It must not call R1/R2 a voltage divider, state R3's purpose, or name the amplifier configuration. Because E7B10–E7B12 test different interpretations of one figure, the same alt/fallback must be reviewed against all three keys and option sets.
