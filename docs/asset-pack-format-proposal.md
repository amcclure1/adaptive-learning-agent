# Asset-Capable Pack Format 0.3 Proposal

Status: Proposed; implementation not authorized  
Updated: 2026-07-19  
Proposed decisions: [ADR 0014](decisions/0014-explicit-asset-capable-pack-format-0.3.md), [ADR 0015](decisions/0015-static-local-asset-security-integrity.md), and [ADR 0016](decisions/0016-asset-accessibility-nonleaking-fallbacks.md)

## Decision summary

Use an explicit `format_version: "0.3"`, not an extension of format 0.2. Strict 0.2 validation rejects unknown fields and undeclared files; assets alter pack-digest inputs; an old loader could not safely present a required figure; and question presentation now has a required pre-answer asset step. Formats 0.1 and 0.2, their digests, validation, installed content, tool responses, and study behavior remain unchanged.

Format 0.3 is a strict superset in concept, not a permissive parser mode. It retains unpacked UTF-8 JSON and Markdown, source/pool/rights/approval records, deterministic scoring, and offline operation. It adds only static local PNG assets and ordered references from lessons/questions. It adds no remote or executable content.

## Narrow directory layout

```text
amateur-extra-e7b/
├── pack.json
├── lessons/
│   ├── 01-reading-the-circuit.md
│   └── 02-reasoning-from-connections.md
├── assets/
│   └── figure-e7-1.png
└── NOTICE.md
```

Only `pack.json`, declared Markdown lessons, declared files under `assets/`, and optional `NOTICE.md` are permitted. Every entry must be a regular file. Directories are structural only; symbolic links, junctions/reparse points, hard-link aliases, device files, absolute paths, traversal, empty segments, backslashes, case collisions, duplicate normalized targets, and undeclared entries fail validation.

Paths use relative POSIX form and NFC-normalized Unicode. Asset paths must begin `assets/`, have a lowercase `.png` suffix, and match exactly one declaration.

## Minimum asset record

The closed record is:

```json
{
  "id": "asset-figure-e7-1",
  "media_type": "image/png",
  "path": "assets/figure-e7-1.png",
  "title": "NCVEC Figure E7-1",
  "caption": "Official NCVEC Figure E7-1.",
  "alt_text": "<reviewed non-leaking description>",
  "terminal_fallback": "<reviewed line-oriented representation>",
  "source_id": "ncvec-extra-pool-docx-fourth-errata",
  "rights_id": "rights-ncvec-official-figure",
  "accessibility_rights_id": "rights-original-accessibility-text",
  "content_sha256": "<sha256 of exact distributed PNG bytes>",
  "width": 796,
  "height": 674,
  "official_figure_id": "E7-1",
  "language": "en-US"
}
```

Required fields are exactly those shown. `id` is stable within a pack version. `media_type` is exactly `image/png`. `source_id`, `rights_id`, and `accessibility_rights_id` must resolve. `content_sha256` is 64 lowercase hexadecimal characters for the exact installed file bytes. Width and height are positive integers and must match PNG IHDR values. `official_figure_id` is the identity printed by the issuing authority, not a filename inference.

`title`, `caption`, `alt_text`, and `terminal_fallback` are non-empty, trimmed, bounded Unicode text. Caption and accessibility fields are project-authored unless the source explicitly supplies them; their separate rights reference prevents the official figure's rights status from being applied to original prose.

### Derived representation record

The E7-1 pilot should use exact official embedded PNG bytes and omit derivation. If a future authorized import demonstrates conversion is unavoidable, the asset must additionally contain this closed record:

```json
{
  "derivation": {
    "kind": "format_conversion",
    "source_media_type": "image/svg+xml",
    "source_content_sha256": "<digest of exact source asset bytes>",
    "process": "<reproducible tool, version, command/parameters, fonts, and environment>",
    "fidelity_review_required": true
  }
}
```

The converted output is a project-derived representation. Both source and output digests are retained, conversion provenance is digest-covered, and visual human approval is mandatory. Format 0.3 does not include or implement a normalization/conversion pipeline.

## Asset references and ordering

Assets are declared once in a top-level ordered `assets` array. Lessons and questions may each add one required `asset_ids` array containing unique existing IDs in presentation order. The E7B pilot uses no lesson assets and gives E7B10–E7B12 the same single ID.

Direct references are preferred over separate presentation records because format 0.3 supports only one approved presentation per asset. Asset-wide caption, alt text, and fallback must be safe for every referring question. If context-specific descriptions or transformations become necessary, that use case requires a later format decision rather than optional 0.3 fields.

Every asset must be referenced by at least one lesson or question. Every question whose official wording references a figure must declare that figure. The same asset ID may be used by many records; the file appears once and is never copied per question.

## Supported media decision

Format 0.3 supports **PNG only**.

| Type | Fidelity and digest | Safety | Hermes/fallback | Decision |
|---|---|---|---|---|
| PNG | Lossless pixels; digest exact bytes; dimensions available in a fixed header | No script or external references; still bounded because decoders have risk | Widely supported as an image; independent reviewed text fallback | **Accept** |
| JPEG | Lossy, page composites in NCVEC distribution, possible resave/metadata variation, poor line-art fidelity | Non-executable but decoder surface remains | Generally displayable; fallback still required | Defer; no pilot need |
| SVG | Exact official individual figures and scalable line art | XML can contain scripts, external references, links, CSS/font dependencies, and complex parser behavior | Pinned Hermes rendering path unverified; terminal cannot render it | Defer/reject in 0.3 |

The official E7-1 DOCX contains an exact PNG, so PNG requires extraction but no image transformation. Standard-library code can validate PNG signature, IHDR, chunk framing/CRC, dimensions, IEND, declared size, and digest without decoding pixels. A future implementation may demonstrate that a small image library is safer, but no dependency is accepted by this design.

Initial limits are deliberately small: at most 16 assets, 2 MiB per asset, 8 MiB total asset bytes, and dimensions from 1×1 through 4096×4096. Limits apply before any renderer receives the file. Changing them requires evidence and review.

## Canonicalization and digesting

Each asset has two integrity layers:

1. `content_sha256` is SHA-256 over the exact raw distributed file bytes, with no newline, metadata, color-profile, compression, or pixel normalization.
2. The format-0.3 pack digest covers both the complete canonical manifest (including every asset digest and accessibility field) and every raw asset byte sequence.

Use a new format-0.3 domain marker and the existing length-framing approach. Digest inputs, in order, are:

1. canonical `pack.json` bytes;
2. each lesson's normalized path and normalized Markdown in declared lesson order;
3. each asset's normalized path and **raw bytes** in declared asset order;
4. normalized `NOTICE.md` bytes when present.

The manifest's declared arrays remain ordered. No filesystem enumeration order participates. Reordering asset declarations or references changes the manifest and digest. Path normalization happens before uniqueness and inventory comparison. Duplicate asset IDs, normalized paths, content hashes, or byte-identical assets are rejected; authors must reference one declaration instead.

Changing asset bytes, metadata, alt text, caption, fallback, source, rights, ordering, or reference mapping changes the pack digest. Installed `(pack_id, version)` content is immutable: replacement under the same version is rejected as a conflict. Corrections require a new pack version and renewed approval; historical sessions remain pinned to their installed digest.

No network byte, runtime cache, generated thumbnail, renderer output, absolute install path, or SQLite value participates in the pack digest.

## Validation

In addition to all applicable format-0.2 rules, validation rejects:

- missing or undeclared asset files and any undeclared pack file;
- absolute, traversing, non-normalized, linked, aliased, or duplicate paths;
- duplicate asset IDs, targets, hashes, or byte-identical declarations;
- media types other than `image/png`;
- missing/invalid PNG signature, malformed chunk structure, invalid critical-chunk order/CRC, trailing bytes, or IHDR mismatch;
- declared dimensions that differ from IHDR or exceed limits;
- individual/count/total size-limit violations;
- content SHA-256 mismatch;
- lesson/question references to missing assets, unreferenced assets, or duplicate references;
- source, rights, or accessibility-rights references that do not resolve;
- empty alt text, caption, or terminal fallback;
- prohibited answer markers or a complete normalized keyed option reproduced in pre-answer accessibility fields;
- remote URLs used as asset paths or required runtime asset locations;
- executable/script-bearing content or non-PNG signatures;
- missing required asset approval scopes.

Validation is offline. URLs remain provenance only and are never dereferenced during validate, install, or study.

Deterministic leakage lint cannot establish semantic equivalence or safety. Human approval remains required for fidelity, rights, accessibility, mapping, and non-leakage.

## Runtime-neutral contract behavior

Keep contract version `0.1` and the existing ten operations. Add response fields only when serving format 0.3; formats 0.1 and 0.2 remain byte/semantics compatible at their public boundary.

### `system.health`

Additive capability data advertises:

```json
{
  "supported_pack_formats": ["0.1", "0.2", "0.3"],
  "static_local_assets": true,
  "supported_asset_media_types": ["image/png"],
  "asset_reference_scheme": "ala-pack-asset-v1"
}
```

This advertises core capability, not a guarantee that the current conversational surface can display images.

### `pack.validate` and `pack.install`

Add `asset_summary` containing count, sorted unique media types, integrity status, accessibility structural/lint status, source/right resolution status, and official figure IDs. It does not claim human truth or legal certainty beyond the approved record.

### `study.start`

Each returned lesson may add ordered `assets` descriptors if its `asset_ids` is non-empty. The E7B pilot has none, so start otherwise retains current behavior.

### `study.next`

For an asset question, add ordered descriptors before answer collection:

```json
{
  "asset_id": "asset-figure-e7-1",
  "asset_ref": "ala-pack-asset-v1:<pack-digest>:asset-figure-e7-1",
  "media_type": "image/png",
  "title": "NCVEC Figure E7-1",
  "caption": "Official NCVEC Figure E7-1.",
  "alt_text": "<approved text>",
  "terminal_fallback": "<approved text>",
  "official_figure_id": "E7-1",
  "width": 796,
  "height": 674,
  "content_sha256": "<approved digest>"
}
```

`asset_ref` is a logical non-network reference bound to an installed pack digest and asset ID. It is not an arbitrary or user-supplied filesystem path. A runtime adapter resolves it only through the core's controlled installed-pack resolver and never returns raw binary in the JSON contract. The descriptor contains no answer, explanation, or answer-revealing annotation.

### `study.submit`

After scoring, the result may add the same figure identity and project-authored explanatory references. It must not mutate or annotate the asset.

## Core, adapter, and skill boundary

### Core

- Parse and validate format 0.3, asset metadata, files, signatures, limits, references, and digests.
- Copy installed bytes without transformation, include them in the pack digest, and revalidate after copy/restart.
- Resolve logical asset references only inside the controlled installed pack and return structured descriptors.
- Remain independent of Hermes, display libraries, model vision, and network clients.

### Hermes adapter

- Delegate learning decisions to the core and resolve only core-issued logical asset references.
- Attach/display the exact PNG only through a public Hermes mechanism proven for the pinned target; otherwise return/present the approved fallback.
- Never rewrite bytes, invent descriptions, inspect pixels for scoring, expose arbitrary paths, or fetch URLs.

Hermes currently documents plugins as JSON-string tool handlers in [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins). Its [Vision & Image Paste guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/vision.md) documents image input, native/fallback vision routing, and PNG storage, but does not verify generic local-image output from a v0.18.2 custom tool. Native presentation is **unverified** until a separate implementation task tests the pinned CLI. The required text fallback preserves usability.

### Skill

- Present the asset/fallback before options and confirm access before accepting an answer.
- Preserve official labels and approved accessibility text exactly.
- Never ask a model to describe the image, infer the key, or add answer-revealing prose.
- Treat deterministic tool results—not memory—as the authoritative descriptor and study state.

## SQLite impact

No schema change is proposed. The existing installed-pack receipt stores identity, version, controlled path, and pack digest; sessions/presentations already pin the installed content and question. On restart, the core reloads the installed pack, recomputes the format-0.3 pack and asset digests, and reconstructs the question descriptor.

An asset table, blob store, cache receipt, or presentation snapshot is unnecessary. If implementation cannot pass restart/resume and immutable-version tests with existing schema 1, it must document the exact failing acceptance test and stop for a new design decision rather than migrate implicitly.

## Future acceptance plan

| ID | Test | Expected result |
|---|---|---|
| A03-01 | Existing 0.1/0.2 golden fixtures and full workflows | Unchanged digests, responses, and behavior |
| A03-02 | Exact version dispatch | 0.3 loads only through strict 0.3 branch |
| A03-03 | Missing asset | Reject |
| A03-04 | Changed asset bytes/hash | Reject digest mismatch |
| A03-05 | JPEG/SVG/other declaration | Reject unsupported media type |
| A03-06 | PNG declaration with wrong magic/type | Reject signature mismatch |
| A03-07 | Duplicate ID/path/hash/bytes | Reject |
| A03-08 | Missing question/lesson asset target | Reject |
| A03-09 | Traversal, absolute, backslash, link/reparse, case collision | Reject |
| A03-10 | Unexpected asset or other file | Reject |
| A03-11 | Missing source/rights/accessibility-rights target | Reject |
| A03-12 | One asset referenced by E7B10–E7B12 | One stored file; ordered descriptors for all three |
| A03-13 | Change raw asset bytes | Pack digest changes |
| A03-14 | Change alt/caption/fallback | Pack digest changes |
| A03-15 | Empty accessibility field | Reject |
| A03-16 | Prohibited marker or complete keyed option in pre-answer text | Reject; human semantic review still required |
| A03-17 | Image unavailable | Approved terminal fallback precedes answer request |
| A03-18 | Block all network access | Validate/install/study succeed offline |
| A03-19 | Exit/restart during asset question | Same asset ID/hash/descriptor reconstructed |
| A03-20 | Challenge asset question | Quarantine behavior unchanged |
| A03-21 | Pinned Hermes native presentation | Exact PNG and alt text shown before answer, if public API is verified |
| A03-22 | Pinned Hermes forced fallback | Approved fallback shown; no model-generated substitute |
| A03-23 | Inspect pre-answer transcript/tool result | No key, explanation, prohibited marker, or interpretive annotation |
| A03-24 | Fresh authoritative comparison | Distributed bytes match approved official embedded PNG hash and visual figure identity |
| A03-25 | Draft/missing asset approval scopes | Pack is not installable |

Additional limit/chunk/CRC tests must cover malformed/truncated PNG, oversized dimensions, oversized file/pack totals, unknown critical chunks as required by the chosen minimal parser, and no trailing data. The existing standard-library suite and Python 3.12–3.14 matrix remain gates.

## Exact future implementation scope

A separately authorized task may add a format-0.3 model/loader/digest/install branch, standard-library PNG integrity checks, logical asset resolution, additive contract-0.1 descriptors/capabilities, thin Hermes presentation/fallback behavior, the tests above, and—only after independent rights/content/accessibility approval—the exact E7B10–E7B12 records and E7-1 PNG.

## Non-goals

No format-0.1/0.2 change; YAML or archives; SQLite migration; new operation or contract version; remote assets; executable content; arbitrary HTML; SVG; JPEG; video/audio/animation; interaction; external embed; network retrieval; OCR; image generation; conversion/normalization pipeline; thumbnails; responsive variants; lesson authoring system; generated questions; subject builder; AWS; scoring/mastery/scheduling change; or autonomous approval/publication.
