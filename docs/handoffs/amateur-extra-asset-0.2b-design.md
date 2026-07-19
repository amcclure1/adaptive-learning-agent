# Amateur Extra Static-Asset 0.2B Design Handoff

Date: 2026-07-19  
Status: Design complete; Proposed ADR review required; implementation/content import not authorized

## Outcome

The smallest proposed backward-compatible extension is explicit pack format **0.3**, supporting only declared static local **PNG** assets. The selected official pilot is **E7B10–E7B12 with shared NCVEC Figure E7-1**. Formats 0.1 and 0.2, SQLite schema 1, deterministic learning rules, the ten operations, and contract version 0.1 remain unchanged.

This task changed documentation only. It did not import an official question or figure, implement a pack field, change core/test/schema/tool behavior, modify Hermes or its configuration, install a package, or create a release.

## Authoritative research

Research used the current [NCVEC 2024–2028 Extra Class release/errata page](https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release), current consolidated fourth-errata DOCX/PDF, official figure PDF, page JPEGs, and individual-SVG ZIP. The official page still identifies fourth errata dated 2026-02-04 as current. It lists the earlier E9-3 orientation correction and no correction to E7-1.

Verified snapshot hashes:

- consolidated PDF: `9cc63ae0c1c9ee63a617824555d5b4e73da8c8edb91566f97a66770eb200f517`;
- consolidated DOCX: `581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7`;
- official figure PDF: `591bb4c9fc9a9267e298b3ee23c93ab54ba3813f8ea3730123f9ccda1e4b80f2`;
- official SVG ZIP: `baf46fe88b6914f971f446bfdc1550622d0dcf89d1bfb938ef0dfdcaa85aa558`.

The full candidate table is in [the pilot research](../amateur-extra-asset-pilot-0.2b.md). It covers:

- E5C10–E5C12 / E5-1;
- E6A10–E6A11 / E6-1;
- E6B10 / E6-2;
- E6C08, E6C10–E6C11 / E6-3;
- E7B10–E7B12 / E7-1;
- E7D06–E7D08 / E7-2;
- E7G02, E7G07, E7G09–E7G11 / E7-3;
- E9B01–E9B06 / E9-1 and E9-2;
- E9G06–E9G07 / E9-3.

Every figure is distributed officially as an individual SVG, an embedded DOCX PNG, and within PDF/composite JPEG distributions. Only E9-3 has listed figure-specific errata, incorporated into current files. No candidate has unresolved current errata in the reviewed official materials.

## Pilot selection and rationale

E7B is selected because one unchanged monochrome circuit is reused by three questions and needs no color, animation, interaction, external software, or network. It is smaller than E7G/E9B, less graphically dense than E5C/E9B/E9G, and less likely than the symbol groups to have accessibility text directly name the tested identity.

The preferred pilot asset is the exact PNG embedded in the current official DOCX:

- identity: Figure E7-1;
- source member: `word/media/image5.png`;
- media type: `image/png`;
- dimensions: 796×674;
- length: 41,357 bytes;
- SHA-256: `e4e82c7b8c2db7db3a65ffa21d00a6f93d0e6176f0aa3700b8c449bbf80dfd63`.

This avoids rasterizing the official `E7-1.svg`, whose rendering can vary with font and tool behavior. The DOCX-member mapping and visual identity remain subject to independent fidelity approval before import.

## Rights analysis

The official NCVEC page places the public-domain statement, question-pool downloads, figure downloads, and figure errata together. The proposed project interpretation is:

- official figure geometry, labels/annotations, and question-to-figure references are official pool material under the NCVEC public-domain basis;
- exact embedded PNG bytes may be redistributed only after a human approves that interpretation and source mapping;
- project alt text, caption, fallback, lessons, and explanations are original project prose under their own component rights (proposed CC-BY-4.0), not public-domain by inheritance;
- external fonts/renderers/tools retain their own terms and are not pack content;
- screenshots, crops, third-party renderings, generated images, and unrecorded transformations are excluded.

The NCVEC statement does not separately enumerate “diagram bytes,” annotations, every container representation, or transformations. Its application to every byte/derivative is therefore an unresolved legal interpretation, not a verified legal conclusion. This project policy is not legal advice or formal legal review.

If conversion later proves necessary, format 0.3 proposes a derivation record containing source media type/hash, reproducible process/tool/version/parameters/fonts/environment, output hash, and mandatory fidelity review. No conversion or normalization pipeline is proposed.

## Pack-format and asset model

Proposed format 0.3 is required because strict format 0.2 rejects new fields/files, assets change digest semantics, old loaders cannot safely ignore a required figure, and question presentation changes.

The minimum asset record contains:

- stable asset ID;
- exact `image/png` media type;
- normalized confined relative path;
- title and caption;
- meaningful alt text and terminal fallback;
- authoritative source ID;
- official-figure rights ID and separate accessibility-text rights ID;
- raw-byte SHA-256;
- declared/verified width and height;
- official figure identifier;
- language;
- conditional derivation provenance only when conversion is unavoidable.

Assets are declared once in ordered manifest order. Lessons/questions use direct ordered `asset_ids`; shared bytes are not duplicated. Asset-wide accessibility text must be safe for every referencing question. Context-specific variants and presentation records are deferred.

## Media decision

PNG is the sole proposed type. It preserves line art losslessly, has deterministic raw bytes, has no script/external-reference language, and is present as an exact official E7-1 representation. The proposed validator can use standard-library facilities for signature, chunk/CRC, dimensions, limits, and hashing without decoding pixels.

JPEG is deferred because it is lossy and the official files are composite pages. SVG is deferred because XML scripts, external references, CSS/fonts, and renderer differences create unnecessary surface even though the current official ZIP contains individual figures. Initial proposed limits are 16 assets, 2 MiB each, 8 MiB total, and 4096×4096 pixels.

## Digest and installation behavior

Each `content_sha256` covers exact raw distributed bytes. The format-0.3 domain-separated pack digest covers canonical `pack.json`, normalized ordered lesson paths/content, normalized ordered asset paths plus exact raw bytes, and optional normalized `NOTICE.md`.

Filesystem enumeration order never participates. Normalized duplicate IDs/paths/hashes/bytes fail. Any byte, metadata, accessibility, source/rights, order, or mapping change changes the pack digest. Replacing content under the same `(pack_id, version)` is rejected; corrections require a new version and renewed approval. Validation/install/study never fetch a URL.

## Validation behavior

The future strict branch rejects all cases required by the task: missing/undeclared files, traversal/absolute/link/alias paths, duplicate IDs/targets/bytes, unsupported type, digest/signature/dimension/size mismatch, missing asset/source/rights targets, empty accessibility text, prohibited leakage markers, remote runtime assets, and executable/script-bearing content.

The full 25-test acceptance matrix, including format compatibility, shared assets, digest changes, restart/challenge, offline behavior, official comparison, and human approval, is in [the format proposal](../asset-pack-format-proposal.md).

## Accessibility and approval

Caption identifies provenance; alt text describes relevant visual information; terminal fallback provides a longer line-oriented substitute. For E7-1, approved text may reproduce printed labels and exact connections but must not name component purposes or amplifier topology.

Deterministic lint rejects explicit answer markers and complete normalized keyed-option text, but cannot prove semantic safety. Human approval is required for:

- official asset identity and fidelity;
- asset source/container mapping;
- asset rights metadata;
- alt text, caption, and fallback;
- all question-to-asset mappings/order;
- absence of answer leakage across E7B10–E7B12.

The authoring agent cannot approve its own work. Any covered change invalidates the prior digest/approval. See [the accessibility policy](../asset-accessibility-policy.md).

## Tool and Hermes behavior

The existing ten operations and contract version 0.1 remain. Proposed additive behavior is:

- `system.health`: format 0.3, `static_local_assets`, PNG types, and logical-reference scheme;
- `pack.validate`/`pack.install`: asset count/types, integrity, structural accessibility/lint, source/rights resolution, and figure IDs;
- `study.start`: ordered lesson assets only when declared;
- `study.next`: ordered structured descriptors with a logical `ala-pack-asset-v1` reference, metadata, approved alt/fallback, identity/dimensions/hash, but no raw binary/path/key/explanation;
- `study.submit`: post-score figure/explanatory references.

The core validates/resolves installed bytes and remains runtime-independent. The Hermes adapter resolves only core-issued logical references and either presents the exact PNG through a verified public runtime mechanism or uses approved fallback. The skill presents the representation before soliciting an answer, confirms access, preserves text/labels exactly, and never uses model vision to interpret or score.

Current official Hermes [plugin documentation](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) describes JSON-string handlers. Current official [vision documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/vision.md) describes image input and model routing, not a generic custom-tool local-image output API for pinned v0.18.2. Native image presentation is **unverified**. Implementation must prove it against v0.18.2 or clearly use fallback; it must not modify Hermes core/configuration to force support.

## SQLite impact

No schema migration is proposed. Existing installed-pack identity/version/path/digest and session/presentation relationships are sufficient. Restart reloads and revalidates the installed format-0.3 pack and reconstructs the descriptor. Assets remain pack files, not blobs or learner state.

If implementation cannot pass restart/resume/integrity with schema 1, it must identify the exact failing acceptance test and stop for a new decision.

## Proposed ADRs

- [ADR 0014: Explicit Asset-Capable Pack Format 0.3](../decisions/0014-explicit-asset-capable-pack-format-0.3.md)
- [ADR 0015: Static Local Asset Security and Integrity](../decisions/0015-static-local-asset-security-integrity.md)
- [ADR 0016: Asset Accessibility and Non-Leaking Fallbacks](../decisions/0016-asset-accessibility-nonleaking-fallbacks.md)

All three are Proposed. Existing ADRs 0001–0013 remain Accepted and unchanged.

## Unresolved decisions and gates

1. Human acceptance/revision of ADRs 0014–0016 and the proposed limits/record shapes.
2. Human/legal-policy approval that the NCVEC basis covers redistribution of the exact embedded figure PNG and labels.
3. Independent verification that DOCX `image5.png` is exact E7-1 and visually faithful.
4. Named reviewers and approved final alt text, caption, fallback, mappings, and non-leakage findings.
5. Verification of a public native-image presentation path in pinned Hermes v0.18.2, or explicit acceptance of fallback-only presentation for that surface.
6. Exact implementation module/schema details for the strict 0.3 parser and logical resolver; these may not broaden the accepted model.
7. Fresh authoritative source/errata/hash review immediately before any content import.

## Exact future implementation scope

Only a separately invoked and authorized task may implement a strict format-0.3 model/loader, PNG integrity/limit checks, raw-byte digest/install behavior, logical installed-asset resolution, additive contract-0.1 capabilities/descriptors, thin Hermes display/fallback handling, and the specified tests. Official E7B questions and E7-1 may be imported only in explicit content scope after rights, exactness, accessibility, and non-leakage approval.

## Exact non-goals

No changes to formats 0.1/0.2; SQLite; scoring, selection, confidence, attempts, sessions, retries, challenge, or progress; operation count or contract version; YAML/archives; JPEG/SVG/remote/executable/HTML/video/audio/animated/interactive assets; network retrieval; OCR; image generation; conversion/normalization; thumbnails; generated questions; full Amateur Extra; curriculum architecture; subject builder; capability discovery; MCP; AWS; mastery/scheduling/readiness/exam simulation; autonomous approval/publication; Hermes core/configuration; or release creation.

## Scope confirmation

No asset bytes, official question wording/options/keys, pack data, core code, tests, schema, JSON tool behavior, Hermes adapter/skill/configuration, dependency, tag, or release was created or changed. Product principles already treat accessibility, rights, portability, runtime independence, and human activation as normative, so `docs/product-principles.md` did not require an asset-specific amendment.
