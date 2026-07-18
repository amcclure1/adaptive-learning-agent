# Subject Pack Format

Status: version `0.1` profile accepted; broader `1.0` proposed
Design baseline: 2026-07-18

## Accepted version 0.1 profile

Version 0.1 uses the unpacked JSON-plus-Markdown format defined in [`mvp-vertical-slice.md`](mvp-vertical-slice.md) and accepted by [ADR 0008](decisions/0008-json-markdown-pack-serialization.md). A pack contains `pack.json` and one referenced `lesson.md`; structured objectives and five fixture questions are in JSON. YAML, archives, assets, sources, claims, reviews, signing, export, and dual-format parsing are not accepted in 0.1.

The remainder of this document is a deferred format-1.0 proposal and must not drive the first implementation.

## Deferred format 1.0 YAML proposal

## Goals

The format is readable in Git, editable with ordinary text tools, deterministic to validate, safe to install, and independent of any agent runtime. YAML carries structured records; Markdown carries explanatory content. A pack contains no Python, prompts tied to Hermes, learner data, or executable hooks.

### Canonical layout

```text
<pack-id>/
├── pack.yaml
├── objectives.yaml
├── questions.yaml
├── sources.yaml
├── claims.yaml                 # optional unless critical Markdown claims are declared
├── reviews.yaml
├── content/
│   ├── index.md
│   └── <topic>.md
├── assets/                     # optional static images; no active content
└── LICENSE                     # recommended
```

Only these paths are canonical in format 1.0. File names are case-sensitive even on case-insensitive platforms. Paths use `/`, are relative, and must be Unicode NFC. Archives use ZIP with deterministic metadata.

## Identifier and version rules

- `pack_id`: lowercase reverse-DNS or community slug, for example `org.example.aws-sap-c02`; regex `^[a-z0-9]+(?:[._-][a-z0-9]+)+$`.
- Record IDs: lowercase ASCII segments separated by `-`; regex `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`.
- `format_version`: exact major/minor string; MVP accepts `1.0` only.
- `version`: three numeric components with optional prerelease suffix, for example `1.2.0` or `1.2.0-rc.1`.
- IDs are stable within a pack. Renaming an objective or question creates a new identity.
- Timestamps are RFC 3339 UTC. Calendar dates are ISO 8601 `YYYY-MM-DD`.

## `pack.yaml`

```yaml
format_version: "1.0"
pack_id: org.example.aws-sap-c02
version: 0.1.0
status: draft                 # draft | release
title: AWS SAP-C02 Practice
description: Original practice for the SAP-C02 blueprint.
language: en-US
license: CC-BY-4.0
authors:
  - id: alex
    name: Alex Example
subject:
  kind: certification
  jurisdiction: global
  exam_code: SAP-C02
  applicable_version: "exam guide retrieved 2026-07-18"
validity:
  effective_from: 2026-07-18
  effective_until: null
learning_policy:
  mastery_threshold_micros: 800000
  minimum_evidence_per_objective: 3
  objective_weights:
    design-organizational-complexity: 260000
    design-new-solutions: 290000
    improve-existing-solutions: 250000
    accelerate-workload-migration: 200000
evidence_policy:
  mode: required
  allowed_authority_classes: [vendor_primary]
  independent_review: true
  fail_on_superseded: true
  default_review_days: 180
content:
  index: content/index.md
release:
  canonical_sha256: null       # filled and verified for a release export
```

Objective weights must total 1,000,000. A draft may omit `release.canonical_sha256`; a release archive must contain the computed value according to the digest procedure below.

## `objectives.yaml`

```yaml
objectives:
  - id: design-new-solutions
    title: Design solutions for new workloads
    description: Select architectures that meet stated business and technical needs.
    parent_id: null
    tags: [architecture, sap-c02]
    content_refs: [content/new-solutions.md]
```

Parents must exist and form an acyclic forest. Every scored question references at least one leaf or independently assessable objective.

## `questions.yaml`

```yaml
questions:
  - id: q-cross-account-private-access
    type: single_choice
    status: active             # draft | active | retired
    prompt: >-
      A workload needs private, service-specific access across accounts with
      the smallest exposed surface. Which design best fits?
    options:
      - id: a
        text: Use the reviewed private endpoint pattern.
      - id: b
        text: Peer every VPC and route all address space.
      - id: c
        text: Expose a public endpoint restricted by source IP.
    answer:
      option_ids: [a]
    rationale: >-
      The accepted design exposes the service rather than broad network reachability.
    objective_weights:
      design-new-solutions: 1000000
    difficulty: 3              # integer 1..5; author metadata, not learner state
    tags: [networking, private-access]
    evidence_refs:
      - source_id: aws-private-connect-docs
        locator: "Concepts > access a service through an interface endpoint"
        support: Private connectivity can expose a service through endpoint interfaces.
    authored_by: alex
    review_by: 2027-01-14
```

Common required fields are `id`, `type`, `status`, `prompt`, `answer`, `rationale`, `objective_weights`, `evidence_refs`, and `authored_by`. Objective weights total 1,000,000.

### Question types

#### `single_choice`

Requires two or more options with unique IDs and exactly one `answer.option_ids` entry.

#### `multiple_choice`

Requires two or more options and one or more accepted IDs. `scoring.mode` is `exact` by default or `partial_v1` by explicit opt-in.

#### `numeric`

```yaml
type: numeric
answer:
  value: "14.250"
  unit: MHz
  tolerance:
    kind: absolute             # absolute | relative
    value: "0.001"
  unit_aliases:
    mhz: MHz
```

Numbers are strings parsed as decimal values. Scientific notation and locale-specific separators are rejected in format 1.0 unless explicitly added in a later format version.

#### `short_answer`

```yaml
type: short_answer
answer:
  accepted: ["frequency modulation", "FM"]
  normalization:
    unicode: NFC
    casefold: true
    collapse_whitespace: true
    strip_punctuation: false
```

No regular expressions, scripts, or model grading are allowed in format 1.0.

## `sources.yaml`

```yaml
sources:
  - id: aws-private-connect-docs
    title: AWS PrivateLink concepts
    publisher: Amazon Web Services
    authority_class: vendor_primary
    url: https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html
    retrieved_at: 2026-07-18
    effective_version: null
    review_by: 2027-01-14
    applicable_to: [SAP-C02]
    local_snapshot_sha256: null
    supersedes: []
    superseded_by: null
    license_notes: Link and paraphrase; do not redistribute full documentation.
```

## `claims.yaml`

Critical claims in Markdown use markers such as `<!-- claim: private-access-scope -->`. The structured record is:

```yaml
claims:
  - id: private-access-scope
    content_ref: content/new-solutions.md
    evidence_refs:
      - source_id: aws-private-connect-docs
        locator: "Concepts"
        support: Supports the bounded private-access explanation.
```

Format 1.0 validates that the marker and record agree. It does not parse natural-language claims automatically.

## `reviews.yaml`

```yaml
reviews:
  - id: review-q-cross-account-private-access-1
    target_type: question
    target_id: q-cross-account-private-access
    target_sha256: "<64 lowercase hex characters>"
    reviewer:
      id: sam
      name: Sam Reviewer
    reviewed_at: 2026-07-18T20:15:00Z
    outcome: accepted          # accepted | changes_requested | rejected
    checks:
      answerability: pass
      correctness: pass
      objective_alignment: pass
      evidence_support: pass
      distractor_quality: pass
      explanation_quality: pass
      currency_scope: pass
      rights_originality: pass
    notes: Verified against the cited section; wording is original.
```

The target digest is computed from the canonical target record, its evidence references, and the canonical source records those references use; review records are excluded. Only the latest accepted review for the current transitive digest satisfies the gate.

## Markdown and assets

- Markdown is CommonMark-compatible text with relative links to pack content or assets.
- Raw HTML, remote embedded content, scripts, iframes, forms, and data URLs are rejected in MVP release packs.
- Allowed asset types are PNG, JPEG, SVG without scripts/external references, and plain text. SVG validation may conservatively reject any active or external content.
- Default limits: 5 MiB per file, 25 MiB unpacked pack size, 1,000 files, path length 240 characters, YAML nesting depth 40, and 100,000 scalar nodes per file.
- Accessibility text is required for instructional images through adjacent Markdown alt text.

## Canonicalization and digest

1. Parse allowed YAML files using safe loading with aliases disabled or bounded.
2. Validate types, required keys, and cross-references.
3. Serialize structured data as UTF-8 canonical JSON: sorted object keys, array order preserved, no insignificant whitespace, NFC strings, LF line endings.
4. Normalize Markdown and text files to UTF-8 NFC with LF line endings and one terminal newline.
5. Hash each canonical file with SHA-256.
6. Build a sorted manifest of `relative_path`, byte length, and file digest, excluding `pack.release.canonical_sha256` itself by treating that value as null during canonicalization.
7. Hash the canonical JSON manifest to obtain the pack digest.
8. Store that digest in the release `pack.yaml` and archive metadata. Verification repeats the same procedure with the field treated as null.

ZIP entries are sorted by path, use a fixed timestamp, store normalized permissions for regular files, and contain a single top-level pack directory. This makes identical input produce identical bytes.

## Validation profiles

- `draft`: schema and safety errors fail; missing content, evidence, and reviews are diagnostics.
- `release`: all required fields, canonical digest, evidence policy, review gates, dates, and references must pass.
- `install`: includes release validation plus archive safety, digest/version conflict, and local compatibility checks.

Validation output is deterministic and ordered by severity, file path, logical path, and code.

## Compatibility

- A validator rejects an unknown major `format_version`.
- A validator may accept a newer minor version only when the pack declares no required feature unknown to the implementation.
- Unknown optional fields are preserved but ignored with an informational diagnostic.
- Historical pack versions are immutable. A corrected pack uses a higher version and may declare `replaces_version` in a future optional metadata field.

## Export and install

Export includes only canonical pack files and allowed assets. It never includes `.git`, SQLite files, temporary files, authoring chat, caches, credentials, or learner history. Installation stages, validates, verifies the digest, and then performs an atomic move into the pack store. No pack is uploaded or published by these operations.
