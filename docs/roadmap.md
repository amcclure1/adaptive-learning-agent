# Roadmap

Status: Proposed sequence; only accepted ADRs and explicitly authorized tasks are implementation commitments.
Updated: 2026-07-19

## 0.1.0 — Runtime proof

Status: complete

Proves the deterministic Python/SQLite learning core, strict synthetic format-0.1 pack, runtime-neutral ten-operation contract, and thin Hermes v0.18.2 Windows CLI/profile integration. This is an architecture proof, not a useful subject release.

## 0.2A — Small sourced-content pilot

Status: complete; published as pre-release `v0.2.0-alpha.1`

Target one real, reviewable slice: Amateur Extra question group E1A within subelement E1. Accepted format 0.2 adds only the semantics needed for two ordered lessons, authoritative source/citation records, official question identity and origin, pool/errata metadata, language/tags, component rights, conditional retained-snapshot digests, and human approval. Tool contract 0.1 gains only additive capabilities/provenance. Scoring, attempts, sessions, quarantine, objective counts, and SQLite schema remain unchanged.

Design exit criteria completed:

- ADR 0009 and the exact format-0.2 semantics are accepted.
- Component rights, source snapshot/digest behavior, approval, errata, and capability signaling are defined.
- The future validation matrix covers format 0.1 unchanged and format 0.2 provenance/errata behavior.

Implementation covers the strict parser/model/digest, additive contract results, narrow Hermes presentation, and scoped E1A pack without changing SQLite or learning behavior. Anthony McClure completed all nine approval scopes and explicitly accepted the E1A06 discrepancy treatment. Exact golden comparison, the full local Python matrix, hosted CI, and real E1A Hermes question/scoring/source/restart/challenge/immutable-attempt acceptance passed. The approved result is published as the `v0.2.0-alpha.1` pre-release.

## Later candidates

These are deliberately unordered until 0.2A produces evidence:

- Conversational subject construction with explicit draft, validation, and human activation gates.
- Evidence-review operations and portable review records, kept smaller than a general evidence graph.
- A second evidence-sensitive pilot, potentially a narrow AWS SAP-C02 domain slice, subject to AWS content-use rules.
- Export/install ergonomics, then optional archive support.
- Scheduling and mastery only after practice history supports a concrete algorithm and evaluation plan.
- Broader Hermes packaging/version/platform targets or an MCP adapter without changing core authority.

## Persistently out of scope for the lightweight path

No web application, separate API server, hosted multi-user service, PostgreSQL, Redis, Celery, vector database, mandatory cloud deployment, marketplace, autonomous publishing, multi-agent swarm, brain-dump content, or agent-memory authority.
