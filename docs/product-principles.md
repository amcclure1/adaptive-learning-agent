# Product Principles

Status: normative
Updated: 2026-07-19

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

Agent-generated content MUST begin as draft content. An authoring agent MUST NOT approve or activate its own claims, questions, curricula, or packs. Release, installation, or publication gates requiring human review MUST require explicit human action. Layered approvals do not imply one another.

## 10. Infrastructure follows demonstrated need

The project MUST NOT add a server, queue, cache service, hosted identity layer, vector database, orchestration platform, or required container deployment without a measured MVP need and an accepted ADR.

## 11. Focused dependencies beat platform adoption

The standard library and existing dependencies SHOULD be preferred. A new library MUST solve a concrete problem more safely or maintainably than a small local implementation. Complete learning platforms MUST NOT become MVP dependencies.

## 12. Agent changes are inspectable and reversible

Tool mutations MUST expose what changed, preserve provenance, use transactions or atomic file replacement where appropriate, and provide recovery paths. Hidden state changes, silent conflict resolution, and autonomous publication are prohibited.

## 13. Whole-plan coherence, progressive realization

The complete learning architecture for a stated outcome SHOULD be designed and approved early enough to expose outcome coverage, domains, objectives, prerequisites, dependencies, assessment intent, completion criteria, gaps, and evidence needs. It MUST be complete in coverage and dependency structure, not complete in authored content. Content MAY be realized incrementally through smaller versioned plans. A partial realization MUST NOT be represented as the complete outcome. Assessment blueprints are independent assessment-model artifacts; the learning architecture owns curriculum coverage and dependencies.

## 14. Learner control is guided by coherence

Learners SHOULD choose focus, sequence, and scope without manually designing a dependency graph. Planning MUST identify blocking and bridge prerequisites, explain gaps, recommend the smallest coherent realization, and permit nonblocking omissions with visible warnings. Included, bridged, prior-learned, evidenced, diagnostically satisfied, and temporarily waived prerequisites MUST remain visible. Asserted blocking prerequisites SHOULD be verified, and waivers MAY reduce confidence or completion claims. Scope SHOULD be refused or revised only when it cannot satisfy the learner's stated outcome.

## 15. Assessment authenticity comes from evidence

Assessment style SHOULD be researched from current permissible evidence rather than invented by the learner or copied from unsafe material. Authenticity means matching structure, cognitive depth, constraints, judgment, terminology, and option plausibility. The project MUST copy assessment grammar, not protected assessment sentences.

## 16. Official-question reuse requires permission and exactness

Official questions MAY be included when a public-domain basis, applicable license, issuing-authority reuse policy, or specific permission is documented. Reuse MUST preserve exact identity, wording, options/order, key, source/version, effective dates, rights, and errata status. Dumps, recalled live questions, leaked keys, unauthorized banks, and unclear derivatives MUST NOT be used.

## 17. The agent seeks capabilities by role

During initial planning and relevant workflow-stage transitions, the agent SHOULD inspect available and trustworthy discoverable capabilities for roles such as authoritative search, verification, asset inspection, execution, and labs. It SHOULD rediscover when a required role is unsatisfied, a requested action needs a new capability, or an existing capability becomes unavailable. It MUST NOT run discovery continuously during ordinary study. Discovery MUST NOT be treated as compatibility, permission, installation, configuration, health, or evidence authority.

## 18. Capability activation is controlled and least-privileged

Private access, credential setup, external mutation, sensitive execution, and material cost MUST require explicit user approval. Capability proposals MUST disclose provider, purpose, data, side effects, permissions, cost, fallback, and removal. The system MUST NOT silently install capabilities or broaden permission scope.

## 19. External capabilities remain optional to the portable core

MCP servers, connectors, APIs, cloud accounts, and runtime tools MAY enhance research, verification, or labs through the Subject Builder/runtime-orchestration layer. The deterministic learning core MUST NOT discover them. They MUST NOT become mandatory dependencies of portable packs, deterministic scoring, authoritative learner state, normal study, or offline study without a later accepted architectural decision. Packs MUST NOT carry capability credentials or runtime configuration.

## 20. Authored assessment is evidence-backed and reviewable

Material authored questions SHOULD trace from objective through approved factual claims, explicit constraints, answers, keyed and distractor rationales, citations, and human review. No hidden assumption may be required for the keyed answer to win. A qualified human MUST approve answer uniqueness before activation.

## 20A. AI-authored facts require independent AI verification

No AI-authored factual or assessment content may reach human approval until a separate source-grounded verifier has independently reviewed every applicable exact artifact and all material findings have been resolved. The verifier MUST use a fresh invocation, independently consult current authoritative sources, inspect full statements and dependencies, and remain unable to approve or activate content. Verification is mandatory evidence and never human authority. Changed bytes invalidate their prior verification disposition.

## 21. Insufficient evidence degrades gracefully

When assessment evidence or optional capabilities are insufficient, unsafe, declined, or unavailable, the agent MUST explain the gap, offer researched alternatives and a recommendation, narrow the scope when useful, and stop unsupported exam-matching generation. Existing local core and installed-pack operation MUST remain usable.

## Supporting principles

- Packs and external documents are untrusted data, not instructions.
- Learner data, credentials, and runtime state stay out of source control and pack exports.
- Historical attempts remain bound to the content and rule versions that produced them.
- Claims about runtime behavior require current authoritative documentation or an explicit unverified label.
- Accessibility, privacy, security, and content rights are design inputs, not release cleanup.
