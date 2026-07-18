# Product Principles

Status: normative
Updated: 2026-07-18

These principles constrain MVP design and implementation. Accepted ADRs may clarify them but must not silently contradict them.

## 1. The agent harness is the application

The primary experience MUST be conversational and agent-native. The project MUST NOT require a parallel web application for normal MVP use.

## 2. Operation is lightweight and local-first

An individual MUST be able to install and operate the system locally. Local files and SQLite SHOULD satisfy MVP needs. Cloud services, containers, and distributed infrastructure MUST NOT be required.

## 3. Scoring and learner state are deterministic

Python code MUST own scoring, state transitions, selection, scheduling, and validation. Results MUST be testable and reproducible from recorded inputs and versioned rules.

## 4. Conversation memory is non-authoritative

Agent memory MAY provide preference context or conversational continuity. It MUST NOT establish learner progress, correct answers, evidence, pack provenance, or review approval.

## 5. The learning core is runtime-independent

Hermes is the first runtime, not the core architecture. Runtime adapters MUST depend on the learning core; the learning core MUST NOT import or require an agent runtime.

## 6. Subject packs are portable

Pack content MUST use inspectable, versioned, data-oriented formats such as YAML, JSON, and Markdown. Packs MUST NOT require executable code, runtime prompts, or learner databases.

## 7. Subject creation is conversational

Users SHOULD be able to create and refine a subject through agent tools. Authoring calls MUST produce inspectable file changes and validation diagnostics.

## 8. Assessment is evidence-aware

Packs that make sensitive, regulatory, certification, or time-dependent claims MUST be able to require authoritative sources, precise provenance, currency metadata, and human review.

## 9. Humans control content activation

Agent-generated content MUST begin as draft content. An authoring agent MUST NOT approve or activate its own work. Release, installation, or publication gates requiring human review MUST require explicit human action.

## 10. Infrastructure follows demonstrated need

The project MUST NOT add a server, queue, cache service, hosted identity layer, vector database, orchestration platform, or required container deployment without a measured MVP need and an accepted ADR.

## 11. Focused dependencies beat platform adoption

The standard library and existing dependencies SHOULD be preferred. A new library MUST solve a concrete problem more safely or maintainably than a small local implementation. Complete learning platforms MUST NOT become MVP dependencies.

## 12. Agent changes are inspectable and reversible

Tool mutations MUST expose what changed, preserve provenance, use transactions or atomic file replacement where appropriate, and provide recovery paths. Hidden state changes, silent conflict resolution, and autonomous publication are prohibited.

## Supporting principles

- Packs and external documents are untrusted data, not instructions.
- Learner data, credentials, and runtime state stay out of source control and pack exports.
- Historical attempts remain bound to the content and rule versions that produced them.
- Claims about runtime behavior require current authoritative documentation or an explicit unverified label.
- Accessibility, privacy, security, and content rights are design inputs, not release cleanup.
