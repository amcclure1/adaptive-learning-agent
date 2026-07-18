# Project Context

Status: durable project context
Updated: 2026-07-18

## Problem

People can have productive learning conversations with an agent, but conversation alone is a poor system of record. Model output varies, memory can be summarized or lost, and unreviewed generated material can look authoritative. Adaptive Learning Agent aims to combine an agent's conversational strengths with deterministic assessment, durable local state, portable content, and explicit evidence controls.

## Agent-native vision

The agent harness is the application rather than a chat feature added to a conventional learning product. A learner asks questions, studies, reviews progress, and creates subjects through conversation. Behind that conversation, narrow Python tools perform operations that need reproducibility or authority.

Hermes is the first supported agent runtime. It provides the initial conversational surface, model-provider integration, and tool invocation. The learning core, data model, tool contract, and subject-pack format must remain independent of Hermes so another runtime can adopt them without rewriting learning behavior.

## Why a lightweight custom kernel

The MVP needs a small set of capabilities: deterministic scoring and scheduling, local SQLite persistence, pack validation, structured authoring, evidence review, and runtime adapters. These capabilities can be built as a focused Python kernel with clear boundaries and few dependencies.

A complete learning platform would bring assumptions about web delivery, hosted users, services, content models, and operations that are outside the MVP. Lumen, OpenTutor, and similar projects may later be studied for reusable patterns or narrowly compatible components, but they are not dependencies and do not define this project's architecture. The project will add infrastructure only after a measured need.

## Deterministic tools

Python tools will own:

- answer normalization and scoring;
- mastery and progress projections;
- question selection and review scheduling;
- transactional learner-state changes;
- pack validation, installation, export, and canonical digests;
- evidence-policy and review-gate enforcement.

Agent conversation and memory may personalize wording. They are not authoritative for scores, correct answers, learner state, provenance, or content activation.

## Subject packs

Portable subject packs use human-readable YAML, JSON, and Markdown with static assets where needed. A pack can define objectives, questions, deterministic answers, explanations, sources, claims, review attestations, and applicability dates. Packs are versioned, inspectable in Git, safe to validate before installation, and separate from learner data.

Users should be able to draft a subject conversationally. Agent-generated content remains a draft until a human performs the required review and explicitly activates or exports it. Evidence-sensitive packs can require authoritative source classes, precise locators, currency metadata, and question challenges.

## Pilot use cases

### AWS SAP-C02

The AWS Certified Solutions Architect – Professional pilot tests complex scenario questions, a weighted exam blueprint, fast-changing vendor documentation, and strict originality requirements. Generated material must not be described as real or recalled exam content.

### US Amateur Radio Extra

The Amateur Extra pilot tests regulatory sources, effective dates, an official question-pool context, deterministic technical questions, and jurisdiction-specific evidence. Pack metadata must distinguish FCC rules from explanatory secondary material.

Neither pilot pack currently contains functional learning content.

## Open-source objective

The project is intended to be open source from its first durable repository. Original engine, adapter, schema, and skill code uses Apache License 2.0. Pack maintainers remain responsible for compatible licensing, attribution, trademarks, and source-use constraints for pack content.

## Current implementation status

Version 0.1.0 is a completed runtime and architecture proof: the deterministic runtime-independent core, synthetic fixture, eight-table SQLite schema, ten-operation contract, thin project-local Hermes adapter, and fixture workflow skill are implemented. Hermes v0.18.2 Windows CLI/profile behavior is verified. The fixture is not a real learning pack. Pilot packs, subject building, evidence workflows, scheduling, mastery, exam simulation, and other deferred features remain unimplemented and require separate authorization. Format 0.2 and the Amateur Extra E1A pilot are proposals unless accepted by review.
