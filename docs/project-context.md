# Project Context

Status: durable project context
Updated: 2026-07-19

## Problem

Learning conversations can be productive, but conversation alone is a poor system of record. Model output varies, memory can be summarized or lost, and unreviewed material can look authoritative. Adaptive Learning Agent combines conversational guidance with deterministic assessment, durable local state, portable content, explicit evidence controls, and human activation.

## Agent-native vision

The agent harness is the application rather than a chat feature attached to a conventional learning platform. Hermes is the first runtime and supplies the initial conversational surface, provider integration, and tool invocation. The learning core, tool contract, learner data, and pack formats remain runtime-independent.

Agent conversation can research, explain, draft, and negotiate scope. Python owns deterministic validation, scoring, state transitions, and future structural planning checks. SQLite is authoritative operational learner state. Versioned files are authoritative content and review artifacts. Agent memory is never authority for progress, correct answers, sources, curriculum approval, or activation.

## Lightweight custom kernel

The project prefers a focused Python kernel, standard-library facilities, local SQLite, and inspectable files over complete learning platforms or distributed infrastructure. Optional tools, connectors, APIs, MCP servers, and labs may improve research or practice, but they do not become mandatory core/pack dependencies and do not justify hidden credential or cloud requirements.

## Subject packs and human authority

Portable packs contain reviewed content and provenance, not learner data, credentials, runtime configuration, or executable code. Format 0.1 is the original strict synthetic JSON/Markdown proof. Accepted format 0.2 adds ordered lessons, authoritative sources/citations, official question identity, pool/errata metadata, component rights, and digest-covered human approval.

Official questions may be reused only with documented rights and exact identity/version/errata handling. Otherwise, permissible evidence informs assessment grammar and project authors create original material. Dumps, recalled live questions, leaked answers, unauthorized banks, and suspicious derivatives are excluded.

Agent-authored claims, questions, curricula, and packs remain drafts. Future claim, question, and pack-release approvals remain distinct human decisions.

## Whole curriculum, progressive realization

Future subject building first designs a complete, versioned learning architecture for the stated outcome, including objectives, dependencies, depth, evidence, assessment mapping, sequence, and completion criteria. A separate realization plan selects the coherent portion built now. Learners can focus on a domain, weak areas, foundations, or a time-boxed path without being required to construct dependency graphs.

Architecture changes produce impact reports rather than silently rewriting packs or learner progress. The exact serialization and implementation of curriculum artifacts remain proposed.

## Assessment and capability research

The future Subject Builder automatically researches current assessment identity, official guides, domains/tasks, format, response rules, cognitive depth, scenarios, exhibits/labs, examples, rights, and uncertainty. It produces a human-reviewable assessment blueprint and uses guided fallback when evidence is weak or unsafe.

Before significant research or authoring, the agent seeks useful capabilities by role. Discovery can be automatic; private access, credentials, mutation, sensitive execution, and cost require explicit least-privileged approval. Capability output remains untrusted until classified and verified.

## Pilot sequence

- **0.1.0:** released runtime/architecture proof.
- **0.2A / 0.2.0-alpha.1:** released sourced-content pilot with independently approved NCVEC E1A questions and real Hermes acceptance.
- **0.2B designed, not implemented:** E7B10–E7B12 with official Figure E7-1; proposed explicit format 0.3, PNG-only exact bytes, accessibility/fallback, offline install/study, no SQLite or curriculum/AWS scope.
- **0.3A proposed:** assessment research, blueprint, whole curriculum architecture, realization planning, and capability proposals.
- **0.3B proposed:** one manually reviewed current SAP-C02 slice with approved claims, original lessons, and five original scenario questions.
- **0.3C proposed:** agent-assisted construction after manual artifacts and layered approvals are proven.

No 0.2B or 0.3 implementation is currently authorized. ADRs 0010–0013 are Accepted architecture direction. Asset ADRs 0014–0016 are Proposed and require human review; they define the 0.2B format/media/digest/accessibility direction but do not authorize question/figure import, code, schema, tool, or Hermes changes. Other milestone-specific serialization, schema, storage, provider, reviewer, similarity, and module decisions remain deferred.

## Open-source and rights objective

Original engine, adapter, schema, and skill code uses Apache License 2.0. Original pilot prose uses its recorded content license. Pack maintainers remain responsible for compatible licensing, attribution, trademarks, source-use constraints, freshness, and human review. Project policy is not formal legal advice.
