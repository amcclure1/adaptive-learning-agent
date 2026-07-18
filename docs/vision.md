# Adaptive Learning Agent: Vision

Status: proposed for review  
Design baseline: 2026-07-18

## Purpose

Adaptive Learning Agent is a lightweight, local-first system for deliberate practice. An agent provides the conversation, but deterministic Python owns assessment, scheduling, pack validation, and durable learner state. The first conversational runtime is Hermes; neither the learning core nor the subject-pack format depends on Hermes.

The project should make this loop easy:

1. Install or conversationally draft a portable subject pack.
2. Select a learner and learning goal.
3. Let the system choose an appropriate question.
4. Answer conversationally.
5. Score the response deterministically and persist the result transactionally.
6. Explain the result from reviewed pack content and select the next practice item.
7. Export, validate, review, and share packs without exporting learner data.

## Product promise

- Local by default: learner history is stored in a local SQLite database.
- Agent-native: normal use happens in a conversation, initially through Hermes.
- Deterministic where it matters: the agent never invents a score, mastery update, due date, or persisted fact.
- Portable content: packs are directories or archives of YAML and Markdown, not database dumps or runtime prompts.
- Runtime-independent core: adapters depend on the core; the core never imports Hermes.
- Evidence-aware: packs can require authoritative sources, claim-level traceability, and human question review.
- Inspectable: users can view their state, scoring inputs, pack provenance, and validation results.
- Small: no service tier, background queue, vector database, or hosted control plane is required.

## Intended users

- A learner preparing for a structured exam or maintaining technical knowledge.
- A subject-matter expert building and reviewing a pack conversationally.
- An educator or community maintainer sharing versioned packs through Git.
- A runtime integrator adapting the same core to an agent other than Hermes.

## Pilot subjects

- AWS Certified Solutions Architect - Professional (SAP-C02).
- United States Amateur Radio Extra class.

Both pilots are evidence-sensitive. Their packs must identify the applicable exam or question-pool version, cite authoritative material, and pass question review before a release is installable in normal study mode. The project must not reproduce proprietary exam questions or imply endorsement by AWS, the FCC, ARRL, or NCVEC.

## Authority model

In descending order of authority:

1. The installed, validated pack version defines objectives, questions, accepted answers, explanations, and evidence references.
2. The Python learning core defines scoring, scheduling, validation, and state transitions.
3. SQLite records operational learner state and immutable attempt facts.
4. The current user request supplies conversational intent.
5. Agent memory may personalize wording or recall a preference, but is never evidence of mastery, a correct answer, pack provenance, or policy compliance.

Any conflict is resolved in favor of the higher source. A model-generated explanation must be clearly presented as unverified unless it is grounded in reviewed pack content.

## MVP outcome

The MVP is successful when a user can, entirely on one local machine:

- connect Adaptive Learning Agent to Hermes;
- install and validate a pack from a directory or archive;
- create a learner profile and complete a study session;
- receive deterministic scores and reproducible scheduling updates;
- inspect progress by objective;
- conversationally draft a new pack and route each question through review;
- export an installable, reproducible pack archive with no learner data;
- use the two pilot packs as end-to-end acceptance fixtures.

## Explicit non-goals

- Web application or separate API server.
- PostgreSQL, Redis, Celery, vector database, or cloud deployment.
- Multi-user hosting, organization administration, or remote synchronization.
- Public marketplace, ratings, payments, or discovery service.
- Autonomous publication or unattended acceptance of generated questions.
- Multi-agent swarms or autonomous reviewer personas.
- Treating model memory, chat transcripts, or embeddings as authoritative learner state.
- Open-ended essay grading by an LLM in the deterministic MVP score.

