# SAP-C02 0.3B Authoring Schemas

Status: Accepted contract; generic closed-schema validator implemented; project schema v2 adds initialization provenance and claim-envelope fields

Contract version: `ala-authoring-0.3b.1`

## Scope

This document fixes the file-record contract for the future `aws-sap-c02-org-04-pilot` authoring workspace. It defines shapes and placeholder examples only. It does not create a source record, claim, lesson, question, approval, validation report, pack, or learner content.

JSON objects are closed: an implementation rejects unknown fields unless a later accepted schema version explicitly adds them. Every cross-reference binds identity, revision, and canonical digest; an ID alone is insufficient for approval or compilation.

## Common artifact envelope

Every structured artifact contains:

| Field | Rule |
|---|---|
| `schema_version` | Exact schema identifier such as `ala.authoring.claim.v1` |
| `artifact_id` | Stable lowercase ID independent of filename where practical |
| `artifact_type` | One controlled value listed below |
| `revision` | Positive integer; starts at 1 and increases for immutable revisions |
| `status` | Type-specific lifecycle value; never treated as approval by itself |
| `created_at` | RFC 3339 UTC at whole-second precision: `YYYY-MM-DDTHH:MM:SSZ` |
| `modified_at` | Same form; equals `created_at` for a new immutable revision |
| `author` | Bounded author identity object when authorship applies |
| `supersedes` | `null` or exact prior artifact reference |
| `canonical_digest` | Lowercase SHA-256 calculated by the rules below |

Controlled `artifact_type` values are `project`, `source`, `claim`, `lesson`, `question_spec`, `question`, `review`, `approval`, `validation_report`, `release_candidate`, and `release_evidence`.

IDs use `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`, are unique within the project, and are never reassigned to a different conceptual artifact. Recommended prefixes are `src-`, `clm-`, `les-`, `qspec-`, `q-`, `rev-`, `apr-`, `val-`, `cand-`, and `evidence-`. Filenames may change without changing identity.

The author object is:

```json
{
  "identity": "<human, service, or model identity>",
  "identity_type": "human",
  "role": "<bounded author role>"
}
```

`identity_type` is one of `human`, `model`, `service`, or `imported`. Contact details, credentials, model secrets, and private personnel data are forbidden.

An artifact reference is always:

```json
{
  "artifact_id": "<stable-id>",
  "artifact_type": "claim",
  "revision": 1,
  "canonical_digest": "<64 lowercase hex characters>"
}
```

## Drafts, revisions, and status

- An editable draft may remain at revision `1` while being atomically replaced. Every write supplies `expected_prior_digest`; a mismatch fails with no write.
- Creating an immutable revision freezes its JSON and any bound Markdown. Later work creates revision `n + 1` with `supersedes` pointing to the prior revision.
- An approved target is immutable. Changed bytes either create a new immutable revision or update an unapproved draft and invalidate every decision targeting the prior digest.
- No operation may silently retarget an approval, validation selection, or release manifest to new bytes.
- Historical revisions and decisions remain in Git even after supersession, rejection, invalidation, or revocation.

Common lifecycle `status` values are `draft`, `review_ready`, `active`, `stale`, `superseded`, `invalidated`, and `rejected`. `approved` is not a general lifecycle value; approval is derived from immutable approval records.

## Canonicalization and digests

### JSON

1. Input is UTF-8 without BOM and valid JSON.
2. Every string and object key is Unicode NFC normalized.
3. Line endings in string values are normalized to LF where multiline text is permitted.
4. Objects are serialized with keys sorted by Unicode code point after NFC normalization.
5. Array order is preserved. Schemas identify set-like arrays and require their declared deterministic sort order.
6. Serialization uses no insignificant whitespace: separators are `,` and `:` and non-ASCII characters are emitted directly.
7. Only integers are accepted as JSON numbers. Decimal quantities use normalized decimal strings. NaN, infinity, negative zero, and implementation-dependent floats are forbidden.
8. Timestamps use exact UTC whole-second form. Dates use `YYYY-MM-DD`.
9. Paths use NFC-normalized relative POSIX form with `/`; absolute paths, `..`, `.`, empty segments, backslashes, and platform-specific drive syntax are rejected.
10. `canonical_digest` is omitted from its own digest input.

The digest is SHA-256 over length-framed bytes:

```text
frame("adaptive-learning-authoring")
|| frame("<artifact-type>")
|| frame("<schema-version>")
|| frame(canonical-json-without-canonical_digest)
```

`frame(x)` is an unsigned eight-byte big-endian byte length followed by the exact UTF-8 or binary bytes. Artifact type and schema version provide domain separation. A validator rejects a declared digest that does not match.

### Markdown-bound lessons

Lesson Markdown is UTF-8 without BOM, NFC normalized, converted to LF, and normalized to exactly one trailing LF. Its path is normalized as above. The lesson `canonical_digest` uses:

```text
frame("adaptive-learning-authoring")
|| frame("lesson")
|| frame("ala.authoring.lesson.v1")
|| frame(canonical-lesson-json-without-canonical_digest)
|| frame(normalized-markdown-path)
|| frame(normalized-markdown-bytes)
```

The lesson record also declares `markdown_sha256`, calculated over the normalized Markdown bytes alone. Changing prose, path, metadata, claim mapping, or citations changes the lesson canonical digest.

## Project schema

New workspaces use `ala.authoring.project.v2`; the validator continues to accept historical `ala.authoring.project.v1` records. Version 2 contains the common envelope plus:

- `project_id`, equal to `artifact_id`;
- `title`;
- `workspace_commit`, the full Git commit used as the clean initialization baseline (validation reports bind later exact workspace commits; this field is not a self-referential assertion that the project file is contained in its own digest-named commit);
- `pilot_scope` with architecture, blueprint, realization, objective, intended claim-count range, future lesson count, future question count, and response-mix references;
- `workspace_contract_version`;
- `default_target_pack_format`, exactly `0.2` for this pilot;
- `allowed_target_pack_formats`, exactly `['0.2', '0.3']` in that order;
- `text_only_default`, `true`;
- `artifact_indexes`, workspace-relative paths to generated indexes;
- `private_material_policy`, declaring prohibited workspace material.

The project file is an editable administrative draft until a later authorized task freezes its first revision. It never carries credentials or approval decisions. Project v1 lacks `workspace_commit` and `claim_count_range`; no historical v1 bytes are rewritten.

## Source schema

`ala.authoring.source.v1` adds these required fields:

| Field | Rule |
|---|---|
| `source_id` | Equals `artifact_id` |
| `title`, `publisher` | Non-empty exact identity strings |
| `canonical_url` | Public HTTPS URL; no embedded credentials |
| `source_category` | Controlled value below |
| `authority_tier` | Controlled value below |
| `rights_reuse` | Controlled value below |
| `intended_uses` | Sorted unique controlled values |
| `retrieved_on` | Required date |
| `published_or_updated_on` | Date or `null` |
| `source_revision` | Provider revision/version string or `null` |
| `retained_snapshot` | Conditional object below |
| `freshness_policy` | Explicit recheck rule below |
| `review_state` | Derived decision summary plus approval reference or `pending` |
| `access_limitations` | Non-sensitive notes or `null` |
| `prohibited_disposition` | Conditional object or `null` |

`source_category` is one of `certification_blueprint`, `exam_guide`, `service_documentation`, `architecture_guidance`, `security_guidance`, `service_faq`, `announcement`, `pricing`, `quota`, `rights_policy`, `licensed_open_reference`, `descriptive_reference`, or `prohibited_material`.

`authority_tier` is one of `tier_1_official`, `tier_2_licensed_open`, `tier_3_descriptive`, or `excluded`.

`rights_reuse` is one of `public_domain`, `licensed_reuse`, `reference_only`, `analysis_only`, `style_evidence_only`, `unresolved`, or `prohibited`.

`intended_uses` values are `factual_support`, `architecture_guidance`, `assessment_scope`, `assessment_grammar`, `learner_citation`, and `rights_basis`.

`retained_snapshot` contains `retained`, `content_sha256`, and `repository_path`. When `retained` is false, the other fields are `null`. Licensed source copies, temporary downloads, and source text not authorized for Git must never receive a repository path.

`freshness_policy` contains `mode` (`max_age_days`, `event_triggered`, or `both`), optional positive `max_age_days`, sorted unique `recheck_triggers`, and `last_checked_on`.

If `authority_tier` is `excluded` or `rights_reuse` is `prohibited`, `prohibited_disposition` is required with `reason`, `content_retained: false`, and `downstream_use: "none"`. Copied exam-question text must not be retained merely for style comparison.

Illustrative shape only:

```json
{
  "schema_version": "ala.authoring.source.v1",
  "artifact_id": "src-example",
  "artifact_type": "source",
  "revision": 1,
  "status": "draft",
  "created_at": "2030-01-01T00:00:00Z",
  "modified_at": "2030-01-01T00:00:00Z",
  "author": {"identity": "example-author", "identity_type": "human", "role": "source_researcher"},
  "supersedes": null,
  "source_id": "src-example",
  "title": "<exact public source title>",
  "publisher": "<publisher>",
  "canonical_url": "https://example.invalid/official-source",
  "source_category": "service_documentation",
  "authority_tier": "tier_1_official",
  "rights_reuse": "reference_only",
  "intended_uses": ["factual_support", "learner_citation"],
  "retrieved_on": "2030-01-01",
  "published_or_updated_on": null,
  "source_revision": null,
  "retained_snapshot": {"retained": false, "content_sha256": null, "repository_path": null},
  "freshness_policy": {"mode": "event_triggered", "max_age_days": null, "recheck_triggers": ["provider_revision"], "last_checked_on": "2030-01-01"},
  "review_state": {"status": "pending", "approval": null},
  "access_limitations": null,
  "prohibited_disposition": null,
  "canonical_digest": "<computed>"
}
```

## Claim schema

`ala.authoring.claim.v1` adds:

- `claim_id`, equal to `artifact_id`;
- `statement`, exactly one atomic assertion;
- `category`, one of `documented_fact`, `service_limitation`, `derived_recommendation`, `scenario_assumption`, `cost_tradeoff`, or `operational_tradeoff`;
- `source_references`, non-empty ordered references containing source identity/revision/digest, precise locator, and `supported_proposition`;
- `applicability`, containing explicit `conditions`, `exclusions`, and `decision_context` arrays;
- `scope`, containing sorted unique `services`, `architecture_patterns`, `account_boundaries`, and `objective_ids`;
- `region_sensitivity`, with level `none`, `possible`, or `explicit` and sorted Regions/partitions;
- `account_configuration_sensitivity`, with level `none`, `possible`, or `explicit` and sorted required/forbidden states;
- `time_sensitivity`, with level `stable`, `review_on_change`, or `short_horizon`;
- `freshness_horizon`, containing an explicit `valid_through` date or a rule plus last-check date;
- `derived_from`, sorted claim references, empty unless derived;
- `decision_criterion`, required only for `derived_recommendation`;
- `validation_state` and `human_review_state`, both derived references rather than self-approval;
- `invalidation_state`, one of `current`, `stale`, `invalidated`, or `superseded`, with reason/event reference when non-current.

A derived recommendation requires at least one approved premise claim, an acyclic dependency graph, explicit decision criterion, and applicability. One claim never bundles independently disputable assertions.

```json
{
  "schema_version": "ala.authoring.claim.v1",
  "artifact_id": "clm-example",
  "artifact_type": "claim",
  "revision": 1,
  "status": "draft",
  "created_at": "2030-01-01T00:00:00Z",
  "modified_at": "2030-01-01T00:00:00Z",
  "author": {"identity": "example-drafter", "identity_type": "model", "role": "claim_drafter"},
  "supersedes": null,
  "claim_id": "clm-example",
  "statement": "<one independently reviewable placeholder assertion>",
  "category": "documented_fact",
  "source_references": [{"source_id": "src-example", "revision": 1, "canonical_digest": "<source-digest>", "locator": "<precise locator>", "supported_proposition": "<bounded proposition>"}],
  "applicability": {"conditions": [], "exclusions": [], "decision_context": []},
  "scope": {"services": [], "architecture_patterns": [], "account_boundaries": [], "objective_ids": ["SAP-ORG-04"]},
  "region_sensitivity": {"level": "none", "regions": [], "partitions": []},
  "account_configuration_sensitivity": {"level": "none", "required_states": [], "forbidden_states": []},
  "time_sensitivity": {"level": "review_on_change"},
  "freshness_horizon": {"valid_through": "2030-01-31", "rule": null, "last_checked_on": "2030-01-01"},
  "derived_from": [],
  "decision_criterion": null,
  "validation_state": {"status": "not_run", "report": null},
  "human_review_state": {"status": "pending", "approval": null},
  "invalidation_state": {"status": "current", "reason": null, "event": null},
  "canonical_digest": "<computed>"
}
```

## Lesson schema

`ala.authoring.lesson.v1` adds:

- `lesson_id`, equal to `artifact_id`;
- sorted unique `objective_ids` and `prerequisite_bridge_ids`;
- ordered `claim_references`, each binding ID/revision/digest;
- `markdown_path`, relative to the lesson revision directory;
- `markdown_sha256`;
- ordered `learner_citations` with source reference and learner-safe locator;
- `intended_depth`, one of `foundation`, `applied`, or `professional`;
- `validation_state` and immutable `content_review_state`;
- `canonical_digest`, bound to JSON and exact normalized Markdown.

Every material factual or derived statement in Markdown must map to an approved claim. The compiler rejects unsupported prose; lesson review remains human judgment.

```json
{
  "schema_version": "ala.authoring.lesson.v1",
  "artifact_id": "les-example",
  "artifact_type": "lesson",
  "revision": 1,
  "status": "draft",
  "created_at": "2030-01-01T00:00:00Z",
  "modified_at": "2030-01-01T00:00:00Z",
  "author": {"identity": "example-drafter", "identity_type": "model", "role": "lesson_drafter"},
  "supersedes": null,
  "lesson_id": "les-example",
  "objective_ids": ["SAP-ORG-04"],
  "prerequisite_bridge_ids": ["SAP-FND-01"],
  "claim_references": [{"artifact_id": "clm-example", "artifact_type": "claim", "revision": 1, "canonical_digest": "<claim-digest>"}],
  "markdown_path": "lesson.md",
  "markdown_sha256": "<computed-markdown-digest>",
  "learner_citations": [{"source_id": "src-example", "revision": 1, "canonical_digest": "<source-digest>", "locator": "<learner-safe locator>"}],
  "intended_depth": "professional",
  "validation_state": {"status": "not_run", "report": null},
  "content_review_state": {"status": "pending", "review": null},
  "canonical_digest": "<computed>"
}
```

## Question-specification schema

`ala.authoring.question-spec.v1` contains no final learner-ready wording, options, keys, or explanations. It adds:

- `specification_id`, equal to `artifact_id`;
- `target_objective_id` and sorted `supporting_objective_ids`;
- `intended_cognitive_operation`;
- ordered `assessment_blueprint_references` with identity/version/digest and matched features;
- `response_design` with question type and required selection count;
- `scenario_theme` as an abstract design description;
- ordered `material_requirements` and `material_constraints` using stable requirement IDs;
- sorted `compared_services_or_patterns`;
- ordered `expected_keyed_answer_properties`, never option text or key IDs;
- ordered `planned_distractor_categories`;
- ordered `evidence_requirements`;
- `intended_difficulty`;
- ordered `ambiguity_risks` and `originality_notes`;
- `validation_state` and `design_review_state`.

`intended_cognitive_operation` is one of `identify`, `interpret`, `apply`, `analyze`, `evaluate`, or `design`. `intended_difficulty` is one of `medium`, `medium_high`, or `high`. `planned_distractor_categories` values are `partial_solution`, `wrong_scope`, `wrong_control_plane`, `requirement_violation`, `operational_tradeoff_mismatch`, `over_engineered`, `under_scoped`, or `plausible_but_nonprioritized`. A later incompatible vocabulary requires a schema-version change.

For the fixed pilot, the set contains exactly five specs, three single-response and two multiple-response/select-two. A schema validator rejects `stem`, `options`, `keyed_option_ids`, and learner explanation fields in a specification.

```json
{
  "schema_version": "ala.authoring.question-spec.v1",
  "artifact_id": "qspec-example",
  "artifact_type": "question_spec",
  "revision": 1,
  "status": "draft",
  "created_at": "2030-01-01T00:00:00Z",
  "modified_at": "2030-01-01T00:00:00Z",
  "author": {"identity": "example-designer", "identity_type": "human", "role": "assessment_designer"},
  "supersedes": null,
  "specification_id": "qspec-example",
  "target_objective_id": "SAP-ORG-04",
  "supporting_objective_ids": [],
  "intended_cognitive_operation": "evaluate",
  "assessment_blueprint_references": [{"blueprint_id": "sap-c02-blueprint", "version": "<accepted-version>", "canonical_digest": "<blueprint-digest>", "matched_features": ["scenario_reasoning"]}],
  "response_design": {"question_type": "single_response", "required_selection_count": 1},
  "scenario_theme": "<abstract non-learner-ready theme>",
  "material_requirements": [{"requirement_id": "req-1", "description": "<abstract requirement>"}],
  "material_constraints": [],
  "compared_services_or_patterns": [],
  "expected_keyed_answer_properties": ["<property, not answer text>"],
  "planned_distractor_categories": ["partial_solution"],
  "evidence_requirements": ["<claim category requirement>"],
  "intended_difficulty": "medium_high",
  "ambiguity_risks": [],
  "originality_notes": ["independent construction required"],
  "validation_state": {"status": "not_run", "report": null},
  "design_review_state": {"status": "pending", "review": null},
  "canonical_digest": "<computed>"
}
```

## Final-question schema

`ala.authoring.question.v1` adds:

- `question_id`, equal to `artifact_id`;
- exact `specification_reference`;
- `question_type`, `single_response` or `multiple_response`;
- `required_selection_count`, positive integer;
- `stem`, original learner-ready text;
- ordered `options` with stable option IDs and original text;
- sorted `keyed_option_ids` in option-declaration order;
- `learner_explanation`, including optional concise learner-safe discussion of major alternatives;
- exactly one internal `option_rationale` per option, including keyed options, with requirement/claim links and `is_keyed`;
- ordered `requirement_option_matrix` rows whose cells cover every option;
- ordered `supporting_claim_references`;
- primary/supporting objective references and blueprint references;
- ordered `source_citation_projection` for learner-safe compilation;
- `originality_review_state`, `content_review_state`, and `answer_uniqueness_state`, each derived from exact immutable records;
- `validation_state` and `canonical_digest`.

For `single_response`, required selection count and key count are 1. For `multiple_response`, the stem must state the selection count, the key count must equal it, every keyed selection is required, and scoring remains the existing exact-set/all-or-nothing behavior. No partial credit is introduced.

Illustrative placeholders only:

```json
{
  "schema_version": "ala.authoring.question.v1",
  "artifact_id": "q-example",
  "artifact_type": "question",
  "revision": 1,
  "status": "draft",
  "created_at": "2030-01-01T00:00:00Z",
  "modified_at": "2030-01-01T00:00:00Z",
  "author": {"identity": "example-drafter", "identity_type": "model", "role": "question_drafter"},
  "supersedes": null,
  "question_id": "q-example",
  "specification_reference": {"artifact_id": "qspec-example", "artifact_type": "question_spec", "revision": 1, "canonical_digest": "<spec-digest>"},
  "question_type": "single_response",
  "required_selection_count": 1,
  "stem": "<original placeholder stem>",
  "options": [{"option_id": "A", "text": "<original placeholder option A>"}, {"option_id": "B", "text": "<original placeholder option B>"}],
  "keyed_option_ids": ["A"],
  "learner_explanation": "<learner-safe placeholder explanation>",
  "option_rationales": [{"option_id": "A", "is_keyed": true, "category": "key_support", "requirement_ids": ["req-1"], "claim_references": [], "rationale": "<internal placeholder rationale>"}, {"option_id": "B", "is_keyed": false, "category": "partial_solution", "requirement_ids": ["req-1"], "claim_references": [], "rationale": "<internal placeholder rationale>"}],
  "requirement_option_matrix": [{"requirement_id": "req-1", "cells": [{"option_id": "A", "result": "satisfies"}, {"option_id": "B", "result": "fails"}]}],
  "supporting_claim_references": [],
  "objective_references": {"primary": "SAP-ORG-04", "supporting": []},
  "blueprint_references": [],
  "source_citation_projection": [],
  "originality_review_state": {"status": "pending", "review": null},
  "content_review_state": {"status": "pending", "approval": null},
  "answer_uniqueness_state": {"status": "pending", "approval": null},
  "validation_state": {"status": "not_run", "report": null},
  "canonical_digest": "<computed>"
}
```

The example is structural and deliberately contains no AWS scenario, fact, option, key meaning, or teaching content.

## Approval and review schemas

The five authority-bearing approvals use `ala.authoring.approval.v1`. Immutable lesson-content, originality, and design reviews use `ala.authoring.review.v1`. Both use the common envelope and the reviewer/conflict fields fixed in [the approval model](sap-c02-0.3b-approval-model.md).

Approval types are exactly `source_approval`, `claim_approval`, `question_content_approval`, `answer_uniqueness_approval`, and `pack_release_approval`. Decisions are `approved`, `changes_requested`, `rejected`, and `revoked`; `revoked` is valid only for a revocation record targeting a prior approval.

Every decision record contains:

- `approval_id` or `review_id`;
- `record_kind`: `decision`, `supersession`, or `revocation`;
- exact target artifact reference;
- sorted dependency artifact digests and prerequisite decision references;
- decision;
- reviewer identity, role, qualification summary, and conflict declaration;
- ordered scope and findings;
- ordered conditions, empty for unconditional approval;
- visibility for each finding: `public`, `release_evidence`, or `private_local_reference`;
- exact UTC timestamp;
- optional `supersedes_decision_id` or `revokes_decision_id`.

Private findings themselves are not stored in Git; a public record may contain only a non-sensitive local reference and its digest when policy permits. An original approval never changes its supersession field after creation. Current/superseded/revoked status is derived from later immutable records.

```json
{
  "schema_version": "ala.authoring.approval.v1",
  "artifact_id": "apr-example",
  "artifact_type": "approval",
  "revision": 1,
  "status": "active",
  "created_at": "2030-01-02T00:00:00Z",
  "modified_at": "2030-01-02T00:00:00Z",
  "author": {"identity": "reviewer-example", "identity_type": "human", "role": "claim_reviewer"},
  "supersedes": null,
  "approval_id": "apr-example",
  "approval_type": "claim_approval",
  "record_kind": "decision",
  "target": {"artifact_id": "clm-example", "artifact_type": "claim", "revision": 1, "canonical_digest": "<claim-digest>"},
  "dependency_digests": [],
  "prerequisite_decisions": [],
  "decision": "approved",
  "reviewer": {"identity": "reviewer-example", "role": "aws_factual_reviewer", "qualification_summary": "<bounded public summary>", "conflict_of_interest": "none_declared"},
  "scope": ["factual_accuracy", "applicability"],
  "findings": [],
  "conditions": [],
  "decided_at": "2030-01-02T00:00:00Z",
  "supersedes_decision_id": null,
  "revokes_decision_id": null,
  "canonical_digest": "<computed>"
}
```

## Validation-report schema

`ala.authoring.validation-report.v1` is generated, carries no human authority, and contains:

- `validation_id`;
- `validator_name` and semantic `validator_version`;
- `rule_set_id` and version;
- `executed_at` UTC timestamp;
- `workspace_commit` full Git commit;
- sorted checked artifact references;
- ordered findings with finding ID, rule ID/version, severity (`error`, `warning`, `information`), `blocking`, field/path, related artifacts, message, and bounded remediation;
- `result`, `passed` or `failed`;
- `output_digest`, the canonical report digest duplicated for tool ergonomics and required to equal `canonical_digest`. Both digest fields are excluded while calculating the validation-report digest, avoiding a self-reference.

Reports under `validations/current/` may be regenerated and replaced with expected-prior-digest checking. Once selected for compilation, release evidence binds the exact report ID, workspace commit, and digest used. Replacement never changes historical release evidence and never implies approval.

## Release schemas

Release-candidate and release-evidence schemas are normative in [the release-evidence contract](sap-c02-0.3b-release-evidence.md). They reuse these artifact references and canonicalization rules.

## Schema evolution

Schema identifiers are exact. An implementation must not accept unknown versions or fields. A backward-incompatible record change requires a new schema identifier and documented migration/compatibility decision. Schema migration cannot rewrite immutable approvals or historical evidence in place.
