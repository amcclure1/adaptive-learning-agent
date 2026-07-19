# Future Subject Builder Architecture

Status: accepted architecture direction; implementation not authorized
Updated: 2026-07-19

## Objective

The Subject Builder is the future conversational workflow for turning a learning goal into an evidence-backed, human-approved portable subject. It coordinates research and drafting through the agent runtime while leaving deterministic validation, authoritative learner state, immutable pack installation, and activation gates outside model memory.

The architecture preserves three separations:

1. whole learning architecture versus the realization built now;
2. research/drafting versus human approval and activation;
3. optional runtime capabilities versus the runtime-independent learning core and portable packs.

## Target workflow

1. **Identify learning goal.** Capture the learner's intended outcome, constraints, prior evidence, and explicit non-goals.
2. **Identify assessment or competency target.** Resolve the current certification, exam, practical competency, or other success target and version.
3. **Discover useful capabilities.** During planning or a relevant stage transition, inspect available and trustworthy discoverable tools by abstract role; rediscover when a role is unsatisfied, a new action requires it, or an existing capability becomes unavailable.
4. **Propose capability setup.** Explain benefit, permissions, data, effects, cost, least privilege, fallback, and removal; obtain approval where required.
5. **Research authoritative learning sources.** Build a source inventory with identity, authority, currency, rights, and allowed uses.
6. **Research assessment structure and style.** Determine formats, response rules, cognitive demands, scenarios, constraints, exhibits/labs, and uncertainty.
7. **Build an assessment blueprint.** Produce a versioned, evidence-linked, human-reviewable description of assessment grammar.
8. **Build the complete curriculum architecture.** Define the complete outcome, objectives, depth, dependencies, evidence requirements, assessment mappings, and completion criteria.
9. **Show dependencies, confidence, and gaps.** Make blocking, bridge, recommended, and independent relationships visible without requiring the user to design a graph.
10. **Obtain user approval.** Approve the research baseline, blueprint, learning architecture, uncertainty, and non-claims before substantial content generation.
11. **Agree on a realization plan.** Select the smallest coherent scope, bridges, omissions, depth, and completion boundary.
12. **Build selected modules plus required bridges.** Draft only the approved realization while retaining whole-plan mappings.
13. **Validate claims and authored content.** Apply deterministic structural checks and human evidence/quality review.
14. **Obtain human approval.** Separate claim, question, and pack-release approval as applicable; the authoring agent cannot self-approve.
15. **Activate the pack.** Install only immutable content satisfying the accepted pack version's approval gates.
16. **Learn and assess.** Use deterministic core tools and SQLite learner state; conversation remains non-authoritative.
17. **Expand or revise the realization plan.** Add approved modules or respond to target revisions through versioned impacts rather than silent edits.

## Phase outputs

| Phase | Human-reviewable output | Authority boundary |
|---|---|---|
| Goal/target | Goal statement and target identity | User approves intent and current target |
| Capability discovery | Inventory and proposals | Discovery is not activation |
| Learning research | Source inventory, rights/use classifications, freshness | Sources support claims only within declared roles |
| Assessment research | Evidence hierarchy, blueprint, confidence and gaps | Blueprint is reviewed, not model memory |
| Curriculum design | Whole learning architecture and dependencies | Human approves coherent plan/version |
| Scope negotiation | Realization plan and omission/bridge impacts | User chooses within coherence constraints |
| Authoring | Claims, lessons, scenarios, rationales, citations | Draft until layered review |
| Validation/review | Diagnostics and approval records | Code checks structure; humans approve judgment/content |
| Activation/study | Immutable pack and deterministic learner operations | Pack files and SQLite are authoritative |
| Revision | Architecture impact and revised realization | No silent rewrite of packs or progress |

The exact serialization of pre-pack authoring outputs is unresolved. They must be inspectable, versioned files rather than hidden conversation state. No new pack fields, tools, or database tables are implied by this table.

## Blueprint and learning-architecture relationship

An assessment blueprint is an independent assessment-model artifact. One blueprint may support multiple learning architectures. A learning architecture may reference zero, one, or several blueprints, and non-certification learning need not reference an external exam blueprint. The learning architecture owns curriculum coverage, prerequisites, dependencies, and completion criteria; blueprint references inform assessment intent and mappings.

The learning architecture is complete in outcome coverage, domains, objectives, prerequisites, dependencies, assessment intent, completion criteria, and gap visibility—not in authored lesson prose, complete claims, complete questions, or detailed deferred content.

## Research and assessment behavior

Assessment research follows [Assessment Research and Authenticity Policy](assessment-research-policy.md). The agent should research style automatically and guide fallback when evidence is incomplete; it should not ask the learner to invent question style. Evidence authority, assessment-style usefulness, and reuse rights are classified separately.

Reusable official questions require exact provenance and rights. Study-only examples can inform structure and cognitive demand but are not copied. Unsafe material is excluded. Authored questions copy assessment grammar, not sentences.

## Curriculum and learner control

Planning follows [Curriculum Planning](curriculum-planning.md). The complete architecture is approved first, but content is progressively realized. Partial-scope requests are mapped to the complete plan; the user receives the smallest coherent recommendation, bridge options, warnings for nonblocking omissions, and a refusal only when the stated outcome cannot be met.

Each relevant prerequisite is visibly marked included, bridged, satisfied by prior learning, satisfied by evidence, satisfied by diagnostic assessment, or temporarily waived. A prior-learning assertion or waiver remains visible and may reduce confidence or qualify completion. The agent recommends verification when a blocking prerequisite is asserted rather than demonstrated. Conversation memory alone never satisfies it.

## Capability-seeking behavior

Capability behavior follows [Capability Discovery and Controlled Activation](capability-discovery.md). The agent seeks roles such as authoritative search, source snapshotting, claim verification, asset inspection, execution, and labs. Runtime-specific providers are optional implementations.

Capability records distinguish discovered, recommended, approved, configured, healthy, unavailable, and revoked. Discovery is not activation, and approval/configuration is not proof of health. Public read-only discovery can be automatic at the defined planning/stage triggers; it does not run continuously during ordinary study. Private access, credentials, mutation, and sensitive/costly work require explicit permission. Setup state and credentials remain outside packs. Declining a capability triggers a manual, local, or narrower fallback.

## Authored-content authority

For evidence-backed original questions, the agent may draft the chain from objective through claims, constraints, answers, rationales, and citations. Deterministic validators should eventually check shapes, references, version consistency, and approval completeness. They cannot decide factual truth, architectural judgment, or answer uniqueness. Qualified humans approve those conclusions.

Activation is a distinct user-controlled mutation. No approval may be inferred from a positive conversation, memory, source availability, successful validation, or earlier approval of a different digest/version.

## Revision and impact

Target or source changes first revise research and architecture. A versioned impact report identifies objectives, dependencies, lessons, questions, sources, progress interpretations, realization plans, and content gaps affected. Maintainers then decide what requires revalidation, renewed review, or a new pack. Installed content and historical attempts are not silently migrated.

## Runtime-neutrality

The orchestration experience begins in Hermes, but Subject Builder artifacts and deterministic validation must not require Hermes semantics. Capability discovery belongs to Subject Builder/runtime orchestration; the deterministic learning core does not discover MCP servers or connectors. A future runtime adapter may expose equivalent interactions. Packs contain no credentials or runtime configuration. Optional capabilities never become required for installed-pack validation, scoring, learner state, normal study, or offline study, and installed packs remain usable when those capabilities are unavailable.

## Milestone boundary

- **0.2B** separately proves official static assets and does not implement this builder.
- **0.3A** manually exercises research, blueprint, curriculum, scope, and capability proposals as reviewable artifacts.
- **0.3B** manually produces and reviews one bounded SAP-C02 realization with five original questions.
- **0.3C** introduces agent-assisted construction only after manual artifacts and approval boundaries are proven.

## Explicit non-goals for this design

No implementation, pack-format expansion, tool addition, SQLite change, Hermes workflow change, MCP setup, AWS content, diagram content, scoring, scheduling, mastery, autonomous publication, or self-approval is authorized.
