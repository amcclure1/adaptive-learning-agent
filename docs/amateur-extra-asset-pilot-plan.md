# Amateur Extra Official-Asset Pilot Plan

Status: proposed 0.2B research and design plan; implementation not authorized
Updated: 2026-07-19

## Purpose

Version 0.2B is a bounded official-content asset pilot. It should prove that one active Amateur Extra question group requiring an official figure can be validated, installed, and studied offline without broadening into curriculum planning, generated content, or subject building.

Format 0.2 explicitly excludes assets. Therefore 0.2B requires a new proposed pack-format decision and version; it must not add fields to format 0.2 or change its accepted semantics. The exact future format number and fields remain unresolved.

## Research-first candidate

The current NCVEC **2024–2028 Extra Class FCC Element 4 Question Pool and Syllabus**, consolidated through the fourth errata dated February 4, 2026, provides an authoritative shortlist:

- **Primary research candidate: E7B.** The official pool references Figure E7-1 from three questions in one group. One shared circuit figure offers a small test of identity, question references, rendering, alternative text, and digest behavior.
- **Fallback: E7D.** The official pool references Figure E7-2 from three questions in one group and provides a similarly bounded circuit case.
- **Broader fallback: E9B.** The official pool references Figures E9-1 and E9-2 across multiple antenna-pattern questions. It exercises more assets and graphical interpretation but is a larger first slice.

This shortlist comes from the [official consolidated NCVEC pool](https://ncvec.org/downloads/2024-2028%20Extra%20Class%20Question%20Pool%20and%20Syllabus%20Public%20Release%20with%204th%20Errata%20Feb%204%202026.pdf), not model memory. No question or figure content is imported by this plan. E7B is only the first group to research, not approved content. Final selection requires a fresh pool/errata check, exact active-question inventory, figure-file inventory, asset-specific rights determination, technical inspection, and human approval.

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

## Logical asset requirements for later design

The future design will likely need stable asset ID, normalized relative path, media type, byte length, SHA-256, source/figure locator, rights reference, accessibility text, and question references. These are logical requirements, not accepted fields. It must decide:

- whether alternative text is asset-wide or question-context-specific;
- whether the original official file is retained as-is or a permitted normalized derivative is distributed;
- how derivative provenance and both source/derived digests are represented;
- which image formats are permitted and whether SVG is treated as active content or rejected;
- image decoding limits and validation without a heavy dependency;
- how terminal fallback avoids answer leakage;
- whether assets can appear in lessons as well as questions;
- how runtime adapters receive safe local asset references.

## Rights and evidence gates

The existing NCVEC public-domain statement is relevant but not assumed to settle every diagram-file, derivative, attribution, or accessibility-text question. A later review must explicitly establish:

- figure publisher and exact source;
- whether the figure bytes and any separate diagram download are covered by the reuse basis;
- whether logos, marks, annotations, or non-pool elements are present;
- whether conversion, cropping, or other derivatives are permitted and necessary;
- original alternative-text authorship and license;
- current errata, including figure-specific changes;
- exact identity between question references and distributed asset.

No retained authoritative snapshot should be published until redistribution is explicitly approved.

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

1. Complete authoritative E7B/E7D/E9B inventory and select the smallest useful group.
2. Resolve asset-specific rights and derivative policy.
3. Inspect exact official asset files and accessibility needs.
4. Propose and accept a narrow new pack-format ADR with security limits and compatibility rules.
5. Specify core/tool/runtime behavior and negative-test matrix.
6. Name independent content, rights, and accessibility reviewers.
7. Explicitly authorize implementation and content import in separate scope.
