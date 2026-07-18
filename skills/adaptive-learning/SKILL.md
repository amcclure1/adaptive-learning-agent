---
name: adaptive-learning
description: Run the deterministic fixture study workflow through the Adaptive Learning Agent tools.
version: 0.1.0
license: Apache-2.0
---

# Adaptive Learning

Use the `ala_*` tools as the only authority for learner identity, installed packs, session state, question content, scoring, feedback, progress, and quarantine. Never use conversation or Hermes memory as learner state.

## Workflow

1. Call `ala_system_health`.
2. Call `ala_learner_initialize` with the learner's provided display name. If none was provided, ask for it first. Treat a returned existing learner as authoritative.
3. Call `ala_study_status` with the returned learner ID.
4. If an active session exists, resume it. Otherwise, use the installed `fixture-basics` pack. If it is absent, call `ala_pack_validate` and then `ala_pack_install` with `source_path` set to `packs/fixture-basics`. Ask the learner before starting a pack when their choice is not already clear.
5. Call `ala_study_start` with the persisted learner and exact pack identifiers. Introduce the returned lesson without adding claims to it.
6. Call `ala_study_next`. Present its prompt and options exactly; never invent, alter, answer, or infer an answer key.
7. Ask the learner for option ID choice(s) and confidence from 1 through 5, then end the turn. Do not submit until both are explicit in response to the currently displayed presentation; never consume an answer supplied before that presentation.
8. Call `ala_study_submit` with the exact session and presentation IDs. Present `is_correct`, the returned correct option IDs, explanation, and objective progress as deterministic tool feedback without rewriting their meaning.
9. Offer to continue, finish, or challenge the current question. For a challenge, collect the learner's reason and call `ala_question_challenge` using the exact presentation ID.
10. Continue with `ala_study_next`. Call `ala_study_finish` only after status/tool results establish that no eligible unanswered question remains.

On a fresh conversation, always repeat health, learner initialization, and status before resuming. Preserve IDs only from current tool results. If a tool returns an error, report it faithfully and do not fabricate recovery state.

Never claim mastery, certification readiness, or subject readiness. Do not read SQLite or pack files, calculate correctness, generate questions, create subjects, modify pack content, or replace tool feedback.
