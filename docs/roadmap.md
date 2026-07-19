# Roadmap

Status: Proposed sequence; only accepted ADRs and explicitly authorized tasks are implementation commitments.
Updated: 2026-07-18

## 0.1.0 — Runtime proof

Status: complete

Proves the deterministic Python/SQLite learning core, strict synthetic format-0.1 pack, runtime-neutral ten-operation contract, and thin Hermes v0.18.2 Windows CLI/profile integration. This is an architecture proof, not a useful subject release.

## 0.2A — Small sourced-content pilot

Status: design finalized; implementation not authorized

Target one real, reviewable slice: Amateur Extra question group E1A within subelement E1. Accepted format 0.2 adds only the semantics needed for two ordered lessons, authoritative source/citation records, official question identity and origin, pool/errata metadata, language/tags, component rights, conditional retained-snapshot digests, and human approval. Tool contract 0.1 gains only additive capabilities/provenance. Scoring, attempts, sessions, quarantine, objective counts, and SQLite schema remain unchanged.

Design exit criteria completed:

- ADR 0009 and the exact format-0.2 semantics are accepted.
- Component rights, source snapshot/digest behavior, approval, errata, and capability signaling are defined.
- The future validation matrix covers format 0.1 unchanged and format 0.2 provenance/errata behavior.

Before implementation begins, a separate task must explicitly authorize the exact parser/tool/Hermes/test scope. Before a real pack is released, content work must name a human reviewer, recheck authoritative sources, record any retained-source digests, and pass the accepted validation matrix.

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
