# Amateur Extra Official-Asset Pilot Plan

Status: 0.2B design complete; implementation and content import not authorized
Updated: 2026-07-19

## Purpose

Version 0.2B is a bounded official-content asset pilot. It should prove that one active Amateur Extra question group requiring an official figure can be validated, installed, and studied offline without broadening into curriculum planning, generated content, or subject building.

Format 0.2 explicitly excludes assets. The completed design proposes explicit format 0.3, PNG-only static assets, and no changes to formats 0.1 or 0.2. The proposal is not accepted or implemented. See [the detailed candidate and pilot research](amateur-extra-asset-pilot-0.2b.md), [format proposal](asset-pack-format-proposal.md), and [accessibility policy](asset-accessibility-policy.md).

## Selected design pilot

Fresh review of the current NCVEC **2024–2028 Extra Class FCC Element 4 Question Pool and Syllabus**, consolidated through the fourth errata dated February 4, 2026, selected **E7B10–E7B12 with Figure E7-1**.

All nine figure-dependent groups were inventoried. E7B is the smallest strong shared-asset case: one monochrome circuit supports three active questions, has no listed figure errata, requires no color or interaction, and permits a connection-based alternative description without naming the tested functions or topology. E7D remains the closest fallback. E5C, E6A/B/C, E7G, E9B, and E9G add accessibility, density, asset-count, or errata complexity.

The selection comes from the [official consolidated NCVEC pool](https://ncvec.org/downloads/2024-2028%20Extra%20Class%20Question%20Pool%20and%20Syllabus%20Public%20Release%20with%204th%20Errata%20Feb%204%202026.pdf), official figure files, and [official release/errata page](https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release), not model memory. No question or figure content is imported by this plan. E7B is proposed, not approved content; a fresh source/errata check and human rights, fidelity, accessibility, and non-leakage approval remain mandatory before import.

## Bounded capabilities to prove

The later pilot should test:

- static asset declarations in a new explicit pack format;
- confined regular-file paths and strict declared-file inventory;
- allowed safe media types and bounded dimensions/file sizes;
- source, revision, retrieval, and component-rights metadata;
- SHA-256 over exact retained asset bytes;
- exact official figure identity and relationship to its official source;
- question-to-asset references without duplicating the asset;
- human-reviewed accessibility alternative text that does not reveal an answer;
- a useful terminal fallback when image display is unavailable;
- runtime-neutral delivery of asset identity/path/metadata;
- Hermes display behavior verified separately from core behavior;
- offline validation, installation, restart, and study;
- immutable historical pack versions when a figure or erratum changes.

## Proposed asset boundary

The completed proposal defines stable asset ID, normalized relative path, PNG media type, SHA-256, dimensions, source/figure identity, separate figure/accessibility rights, title/caption/alt/fallback, and direct ordered lesson/question references. Exact raw bytes and asset paths participate in a format-0.3 pack digest. These remain proposed fields. Key decisions are:

- asset-wide accessibility text must be safe for every reference; context-specific variants are deferred;
- the pilot uses exact PNG bytes embedded in the official DOCX rather than conversion;
- a conditional derivation record is defined but no conversion pipeline is proposed;
- PNG is the only media type; JPEG and SVG are deferred;
- strict signature/chunk/dimension/file/count limits are designed for standard-library validation;
- lessons and questions may reference declared assets directly in deterministic order;
- adapters receive a logical installed-pack reference rather than an arbitrary filesystem path.

## Rights and evidence gates

The existing NCVEC public-domain statement is relevant but not assumed to settle every diagram-file, derivative, attribution, or accessibility-text question. A later review must explicitly establish:

- figure publisher and exact source;
- whether the figure bytes and any separate diagram download are covered by the reuse basis;
- whether logos, marks, annotations, or non-pool elements are present;
- whether conversion, cropping, or other derivatives are permitted and necessary;
- original alternative-text authorship and license;
- current errata, including figure-specific changes;
- exact identity between question references and distributed asset.

No retained authoritative snapshot or asset should be published until redistribution is explicitly approved. NCVEC's public-domain statement reasonably supports the proposal but does not separately enumerate diagram bytes or transformations; that legal interpretation remains unresolved and is not formal legal advice.

## Accessibility and presentation

Every asset needs concise reviewed alternative text describing the information required to understand the figure without disclosing the keyed answer. If equivalent nonvisual presentation is impossible, the terminal fallback must state the limitation rather than invent a substitute. Accessibility review is a release gate, not runtime improvisation.

The core should eventually return deterministic asset metadata. Hermes may display the image or fallback but must not parse it to decide correctness, rewrite alternative text, infer hidden facts, or make network availability part of study. Another runtime must be able to consume the same core result.

## Acceptance outline

Future acceptance should cover exact asset digest and identity, path traversal and link rejection, undeclared/missing/changed assets, media and size limits, question reference integrity, source/rights resolution, alternative-text presence and answer safety, terminal fallback, no-network installation/study, restart reconstruction, format-0.1/0.2 compatibility, and real Hermes display.

## Explicit non-goals

- No generated questions or authored-question workflow.
- No curriculum architecture, realization planning, or subject builder.
- No capability/MCP discovery or AWS content.
- No scoring, selection, attempt, confidence, challenge, progress, or SQLite change.
- No archives, executable assets, remote asset fetching, OCR dependency, image generation, or diagram editing.
- No implementation, imported question wording, figure bytes, pack field, test fixture, tool change, or Hermes workflow change in this task.

## Implementation prerequisites

1. Human-review and accept or revise Proposed ADRs 0014–0016.
2. Resolve the asset-specific rights interpretation and approve exact embedded-PNG redistribution.
3. Independently compare E7-1 identity/fidelity and approve alt text, caption, fallback, mappings, and non-leakage.
4. Verify a public native-image path for pinned Hermes v0.18.2 or formally accept fallback-only behavior for that surface.
5. Name independent content, rights, and accessibility reviewers.
6. Explicitly authorize implementation and content import in separate scope.
