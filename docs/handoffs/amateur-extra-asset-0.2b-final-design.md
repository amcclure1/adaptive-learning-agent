# Amateur Extra Static-Asset 0.2B Final Design Handoff

Date: 2026-07-19
Status: Accepted design; implementation and content import not authorized

## Closure outcome

ADRs 0014–0016 are Accepted. They establish the bounded format-0.3 and E7B pilot direction without authorizing implementation, official-question import, asset import, content activation, Hermes changes, or a release.

The accepted pilot is exactly E7B10, E7B11, and E7B12 with one shared official Figure E7-1 asset. No other figure group is in this milestone. Formats 0.1 and 0.2 remain unchanged.

## Accepted ADRs

- [ADR 0014: Explicit Asset-Capable Pack Format 0.3](../decisions/0014-explicit-asset-capable-pack-format-0.3.md)
- [ADR 0015: Static Local Asset Security and Integrity](../decisions/0015-static-local-asset-security-integrity.md)
- [ADR 0016: Asset Accessibility and Non-Leaking Fallbacks](../decisions/0016-asset-accessibility-nonleaking-fallbacks.md)

Acceptance fixes format-0.3 behavior. It does not permanently select media types, universal limits, or runtime-specific rendering mechanisms for later pack formats. A later format may revise those through a new decision without changing format 0.3.

## Accepted format and limits

- exact `format_version: "0.3"`;
- strict unpacked directory packs using UTF-8 JSON plus Markdown;
- static local assets only;
- exactly `image/png` for format 0.3; JPEG and SVG are unsupported;
- no generic multimedia abstraction, remote asset, executable content, network retrieval, archive, or conversion pipeline;
- at most 16 assets;
- at most 2 MiB for one asset;
- at most 8 MiB total asset bytes;
- dimensions from 1×1 through 4096×4096 pixels;
- no SQLite migration;
- the existing ten operations and contract version 0.1 remain.

Format 0.3 adds a closed ordered asset array and ordered `asset_ids` on questions and lessons. One declaration/file may be referenced by many records and is never duplicated per question.

## Accepted asset record

The minimum record contains asset ID, exact media type, confined relative path, title, caption, alt text, terminal fallback, authoritative source ID, official-asset rights ID, accessibility-prose rights ID, raw content SHA-256, width, height, official figure identifier, and language.

A derivation record is conditional and permitted only if conversion is separately authorized later. It must record source media type/hash, reproducible process/tool/version/parameters/fonts/environment, output hash, and fidelity-review requirement. The accepted pilot preference requires no conversion.

## Asset integrity and digest

`content_sha256` covers exact raw distributed asset bytes without decoding or normalization. The format-0.3 domain-separated pack digest covers, in order:

1. canonical manifest content;
2. normalized declared lesson paths and Markdown in lesson order;
3. normalized declared asset paths and exact raw bytes in asset order;
4. optional normalized `NOTICE.md`.

Filesystem enumeration order is irrelevant. A byte, metadata, accessibility, source/rights, order, or reference change changes the pack digest. Changed content under the same pack ID/version is rejected. Corrections require a new version and renewed approval.

Validation rejects missing/undeclared files, unsafe or aliased paths, duplicate IDs/targets/hashes/bytes, non-PNG types/signatures, malformed PNG structure, digest/dimension/size mismatches, unresolved references, empty accessibility fields, prohibited leakage markers, remote runtime assets, and missing approval scopes. Validation/install/study remain offline.

## Selected provisional bytes

The preferred representation remains provisional pending independent human source/fidelity approval:

- source member: `word/media/image5.png` in the current official NCVEC DOCX;
- expected figure: E7-1;
- media type: `image/png`;
- dimensions: 796×674;
- byte length: 41,357;
- SHA-256: `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`;
- source DOCX SHA-256: `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7`.

Acceptance does not approve these bytes for import or redistribution. A human must independently confirm that the member is exactly Figure E7-1, is visually faithful, and satisfies project-policy redistribution requirements.

## Rights policy

For this pilot, accepted project policy treats official E7-1 geometry, labels, and question-to-figure references as official NCVEC pool material under NCVEC's public-domain statement. Exact embedded-PNG redistribution still requires human confirmation of source mapping and project-policy approval.

Project-authored caption, alt text, terminal fallback, lessons, and explanations use the existing original-prose license, CC-BY-4.0. They are not public-domain merely because the source figure is. Screenshots, crops, redraws, generated replacements, third-party renderings, and unrecorded transformations are excluded.

This is project policy, not legal advice or formal legal review. It does not claim that the NCVEC statement legally reaches every distributed container byte or transformation.

## Accessibility and human approval

Caption identifies provenance. Alt text gives concise meaningful visual information. Terminal fallback provides a longer line-oriented representation. Accessibility text may state printed labels and connections but must not reveal a keyed answer, component purpose, or tested topology.

Deterministic lint must reject empty fields, prohibited answer markers, and complete normalized keyed-option text. Lint is necessary but cannot establish semantic safety. Human approval is mandatory for:

- asset identity;
- source/container mapping;
- visual fidelity;
- rights metadata and redistribution disposition;
- caption;
- alt text;
- terminal fallback;
- question-to-asset mappings and order;
- non-leakage across E7B10–E7B12.

The authoring agent cannot approve its own work. The skill must present the available representation and confirm access before requesting an answer. If neither image nor fallback is accessible, it must not solicit an answer and must permit challenge/quarantine or exit.

## Logical-reference decision

Study tools return a core-issued logical installed-asset reference in the `ala-pack-asset-v1` family, not raw bytes or an arbitrary filesystem path. Exact token encoding remains an implementation detail, but each reference must be:

- produced only by the core;
- bound to pack ID, pack version, installed pack digest, and asset ID;
- resolvable only within the controlled installed pack store;
- rejected when stale, malformed, mismatched, or outside that store.

The adapter may resolve only this core-issued reference. No user-controlled absolute path is exposed through study tools.

## Tool and storage boundary

Contract version 0.1 and all ten operations remain. Format-0.3 results add capabilities, validation/install asset summaries, ordered lesson/question descriptors, and post-score figure references only where applicable. Pre-answer results contain no key, explanation, or interpretive annotation.

SQLite schema 1 remains. Installed pack identity/version/path/digest and existing session/presentation records are sufficient to reload, revalidate, and reconstruct an asset descriptor after restart. Assets remain pack files, not database blobs or learner state. If implementation cannot pass restart/resume with schema 1, it must identify the failing acceptance test and stop for a new decision.

## Hermes native-rendering contingency

Implementation must test whether pinned Hermes v0.18.2 exposes a public plugin mechanism for presenting local image output.

If verified, the adapter may resolve the logical reference and present the exact installed PNG. It must not alter, interpret, annotate, or score the image.

If not verified, the adapter/skill must use the approved alt text and terminal fallback, clearly record native image presentation as unsupported or unverified, and leave Hermes core and configuration unchanged. Native rendering unavailability alone does not block the remaining format-0.3 acceptance.

## Remaining human gates

1. Freshly confirm the current authoritative NCVEC pool/errata/source hashes before import.
2. Confirm `word/media/image5.png` is exactly E7-1 and visually faithful.
3. Approve exact embedded-PNG redistribution under project policy.
4. Name and record content, rights, fidelity, and accessibility reviewers.
5. Approve caption, alt text, terminal fallback, all three mappings/order, and non-leakage.
6. Separately authorize implementation and, later, official content/asset import.
7. Test pinned Hermes native rendering or record fallback-only behavior.

These gates do not reopen the accepted format-0.3 architecture unless evidence demonstrates a contradiction requiring a new ADR.

## Exact future implementation scope

Only a separately invoked implementation task may add a strict format-0.3 model/loader/digest/install branch, standard-library PNG structure/integrity/limit checks, logical installed-asset resolution, additive contract-0.1 capabilities/descriptors, thin Hermes exact-image/fallback handling, and the accepted A03 test matrix.

Official E7B10–E7B12 records and E7-1 bytes may be imported only under a separately explicit content task after the human gates above pass. Implementation and content import may remain separate reviews.

## Exact non-goals

No changes to formats 0.1/0.2; SQLite; scoring, selection, confidence, attempts, sessions, retries, challenge, or progress; operation count or contract version; YAML/archives; JPEG/SVG/remote/executable/HTML/video/audio/animated/interactive assets; network retrieval; OCR; image generation; conversion/normalization; thumbnails; generated questions; any second figure group; full Amateur Extra; curriculum architecture; subject builder; capability discovery; MCP; AWS; mastery/scheduling/readiness/exam simulation; autonomous approval/publication; Hermes core/configuration; or release creation.

## Scope confirmation

This design-closure task changed documentation only. It imported no asset bytes or official question content and changed no core code, tests, SQLite schema, pack implementation, tool behavior, Hermes adapter/skill/configuration, dependency, tag, or release.
