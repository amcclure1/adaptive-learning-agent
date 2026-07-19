# ADR 0015: Static Local Asset Security and Integrity

Status: Accepted
Date: 2026-07-19

## Context

Pack assets add untrusted binary files, decoder exposure, path/inventory risks, duplicate-byte ambiguity, and new digest inputs. Supporting every common image type would expand security and compatibility before one official figure proves the need.

## Decision

Format 0.3 permits only declared local `image/png` regular files. It rejects remote references, links/reparse points, traversal, absolute or non-normalized paths, undeclared files, duplicate IDs/targets/hashes/bytes, unsupported signatures, malformed PNG structure, dimension/size/count violations, and digest mismatches.

Use SHA-256 over exact raw asset bytes and include declared paths plus raw bytes in a format-0.3 domain-separated pack digest in manifest order. Do not normalize, re-encode, crop, annotate, or thumbnail installed assets. Installed `(pack_id, version)` content is immutable.

Format-0.3 bounds are 16 assets, 2 MiB per asset, 8 MiB total, and 4096×4096 pixels. Validation and study perform no network access. Core code owns validation, installed-path confinement, digest verification, and logical asset resolution; adapters receive no user-controlled arbitrary path.

SVG and JPEG are deferred. SVG's XML/script/external-reference/font surface is unnecessary for the pilot. JPEG is lossy and the official E7-1 distribution already offers an embedded PNG.

## Consequences

- The initial validator can reasonably use Python standard-library hashing, path, struct, and zlib facilities.
- Exact official E7-1 PNG bytes can be retained without a conversion pipeline.
- Runtime renderers remain a decoder boundary, mitigated by exact-source review and strict limits.
- A future media type or higher limit requires evidence, validation rules, compatibility tests, and a new decision.

## Alternatives considered

- Allow PNG, JPEG, and SVG: rejected as unnecessary breadth.
- Trust filename extensions or declared MIME: rejected because signatures and structure must agree.
- Digest pixels after decoding: rejected because decoder/output differences undermine byte identity.
- Store assets as SQLite blobs: rejected because pack files are portable content and existing receipts already pin an installed digest/path.
- Build an image-normalization pipeline: rejected because the pilot has exact official PNG bytes.

## Revisit triggers

A later pack format may revise media types or limits only through a new decision with evidence, validation rules, compatibility tests, and migration/dispatch behavior. Format 0.3 keeps these accepted limits and PNG-only security boundary.
