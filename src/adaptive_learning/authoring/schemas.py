"""Closed, hand-written standard-library schemas for authored-content records."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any
from urllib.parse import urlsplit

from adaptive_learning.errors import LearningError

from .canonical import SHA256_RE, artifact_digest, markdown_digest, portable_relative_path


ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
COMMON = {
    "schema_version", "artifact_id", "artifact_type", "revision", "status", "created_at",
    "modified_at", "author", "supersedes", "canonical_digest",
}
PROJECT_V1_FIELDS = {
    "project_id", "title", "pilot_scope", "workspace_contract_version",
    "default_target_pack_format", "allowed_target_pack_formats", "text_only_default",
    "artifact_indexes", "private_material_policy",
}
PROJECT_V2_FIELDS = PROJECT_V1_FIELDS | {"workspace_commit"}
SCHEMAS: dict[str, tuple[str, set[str]]] = {
    "project": ("ala.authoring.project.v2", PROJECT_V2_FIELDS),
    "source": ("ala.authoring.source.v1", {
        "source_id", "title", "publisher", "canonical_url", "source_category", "authority_tier",
        "rights_reuse", "intended_uses", "retrieved_on", "published_or_updated_on",
        "source_revision", "retained_snapshot", "freshness_policy", "review_state",
        "access_limitations", "prohibited_disposition",
    }),
    "claim": ("ala.authoring.claim.v1", {
        "claim_id", "statement", "category", "source_references", "applicability", "scope",
        "region_sensitivity", "account_configuration_sensitivity", "time_sensitivity",
        "freshness_horizon", "derived_from", "decision_criterion", "validation_state",
        "human_review_state", "invalidation_state",
    }),
    "lesson": ("ala.authoring.lesson.v1", {
        "lesson_id", "objective_ids", "prerequisite_bridge_ids", "claim_references",
        "markdown_path", "markdown_sha256", "learner_citations", "intended_depth",
        "validation_state", "content_review_state",
    }),
    "question_spec": ("ala.authoring.question-spec.v1", {
        "specification_id", "target_objective_id", "supporting_objective_ids",
        "intended_cognitive_operation", "assessment_blueprint_references", "response_design",
        "scenario_theme", "material_requirements", "material_constraints",
        "compared_services_or_patterns", "expected_keyed_answer_properties",
        "planned_distractor_categories", "evidence_requirements", "intended_difficulty",
        "ambiguity_risks", "originality_notes", "validation_state", "design_review_state",
    }),
    "question": ("ala.authoring.question.v1", {
        "question_id", "specification_reference", "question_type", "required_selection_count",
        "stem", "options", "keyed_option_ids", "learner_explanation", "option_rationales",
        "requirement_option_matrix", "supporting_claim_references", "objective_references",
        "blueprint_references", "source_citation_projection", "originality_review_state",
        "content_review_state", "answer_uniqueness_state", "validation_state",
    }),
    "approval": ("ala.authoring.approval.v1", {
        "approval_id", "approval_type", "record_kind", "target", "dependency_digests",
        "prerequisite_decisions", "decision", "reviewer", "scope", "findings", "conditions",
        "decided_at", "supersedes_decision_id", "revokes_decision_id",
    }),
    "review": ("ala.authoring.review.v1", {
        "review_id", "review_type", "record_kind", "target", "dependency_digests",
        "prerequisite_decisions", "decision", "reviewer", "scope", "findings", "conditions",
        "decided_at", "supersedes_decision_id", "revokes_decision_id",
    }),
    "validation_report": ("ala.authoring.validation-report.v1", {
        "validation_id", "validator_name", "validator_version", "rule_set_id", "rule_set_version",
        "executed_at", "workspace_commit", "checked_artifacts", "findings", "result",
        "human_approval_implication", "output_digest",
    }),
    "release_candidate": ("ala.authoring.release-candidate.v1", {
        "candidate_id", "compiler_version", "project", "selection_digest", "source_workspace_commit",
        "compiled_pack", "compiler_input_digest", "compiler_output_digest", "compilation_timestamp",
    }),
    "release_evidence": ("ala.release-evidence/1", {
        "phase", "project", "compiler_version", "source_workspace_commit", "assessment_blueprint",
        "learning_architecture", "realization_plan", "source_records", "approved_claims", "lessons",
        "question_specifications", "approved_final_questions", "approval_records",
        "validation_reports", "compiled_pack", "compilation_timestamp", "compiler_input_digest",
        "compiler_output_digest", "candidate_manifest", "release_review_approval", "exclusions",
    }),
    "ai_verification_run": ("ala.authoring.ai-verification-run.v1", {
        "verification_id", "protocol_version", "target_project_id", "target_workspace_commit",
        "verifier", "model", "research_date", "target_artifacts", "architecture_references",
        "verification_scope", "deterministic_validation_report", "independently_accessed_sources",
        "finding_references", "artifact_dispositions", "summary_counts", "unresolved_questions",
        "completion_status", "human_approval_implication",
    }),
    "verification_finding": ("ala.authoring.verification-finding.v1", {
        "finding_id", "verification_id", "target", "disputed_field", "disputed_language",
        "category", "severity", "supporting_source", "explanation", "required_action",
        "suggested_revision", "affected_dependencies", "confidence", "blocking", "finding_status",
    }),
    "finding_resolution": ("ala.authoring.finding-resolution.v1", {
        "resolution_id", "finding", "old_artifact", "new_artifact", "author_response",
        "change_summary", "response_disposition", "supporting_source_changes", "resolved_at",
    }),
}

ARTIFACT_TYPES = frozenset(SCHEMAS)
LIFECYCLE = {"draft", "review_ready", "active", "stale", "superseded", "invalidated", "rejected", "immutable"}
SOURCE_CATEGORIES = {
    "certification_blueprint", "exam_guide", "service_documentation", "architecture_guidance",
    "security_guidance", "service_faq", "announcement", "pricing", "quota", "rights_policy",
    "licensed_open_reference", "descriptive_reference", "prohibited_material",
}
AUTHORITY_TIERS = {"tier_1_official", "tier_2_licensed_open", "tier_3_descriptive", "excluded"}
RIGHTS_REUSE = {"public_domain", "licensed_reuse", "reference_only", "analysis_only", "style_evidence_only", "unresolved", "prohibited"}
INTENDED_USES = {"factual_support", "architecture_guidance", "assessment_scope", "assessment_grammar", "learner_citation", "rights_basis"}
CLAIM_CATEGORIES = {"documented_fact", "service_limitation", "derived_recommendation", "scenario_assumption", "cost_tradeoff", "operational_tradeoff"}
APPROVAL_TYPES = {"source_approval", "claim_approval", "question_content_approval", "answer_uniqueness_approval", "pack_release_approval"}
REVIEW_TYPES = {"lesson_content_review", "question_originality_review", "question_spec_design_review", "impact_review", "material_need_review"}
DECISIONS = {"approved", "changes_requested", "rejected", "revoked"}
VERIFICATION_CATEGORIES = {
    "factual_error", "missing_qualification", "overbroad_assertion", "outdated_behavior",
    "source_mismatch", "weak_locator", "unsupported_recommendation", "insufficient_premises",
    "internal_contradiction", "taxonomy_or_classification_error", "scope_drift",
    "freshness_concern", "rights_concern", "unable_to_verify",
}
VERIFICATION_SEVERITIES = {"critical", "high", "medium", "low", "informational"}
VERIFICATION_DISPOSITIONS = {
    "verified", "verified_with_nonblocking_note", "revision_required", "blocked", "unable_to_verify",
}


def fail(message: str, *, field: str = "$") -> None:
    raise LearningError("AUTHORING_SCHEMA_INVALID", message, details={"field": field})


def _object(value: Any, field: str, required: set[str], optional: set[str] = frozenset()) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object.", field=field)
    unknown = set(value) - required - optional
    missing = required - set(value)
    if unknown:
        fail(f"{field} has unknown fields: {', '.join(sorted(unknown))}.", field=field)
    if missing:
        fail(f"{field} is missing fields: {', '.join(sorted(missing))}.", field=field)
    return value


def _text(value: Any, field: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        fail(f"{field} must be non-empty trimmed text.", field=field)
    return value


def _id(value: Any, field: str) -> str:
    text = _text(value, field)
    if not ID_RE.fullmatch(text):
        fail(f"{field} must use the stable lowercase artifact-ID grammar.", field=field)
    return text


def _timestamp(value: Any, field: str) -> str:
    text = _text(value, field)
    if not UTC_RE.fullmatch(text):
        fail(f"{field} must be an RFC 3339 UTC whole-second timestamp.", field=field)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{field} is not a valid timestamp.", field=field)
    return text


def _date(value: Any, field: str, *, nullable: bool = False) -> str | None:
    text = _text(value, field, nullable=nullable)
    if text is None:
        return None
    try:
        date.fromisoformat(text)
    except ValueError:
        fail(f"{field} must be an ISO calendar date.", field=field)
    return text


def _string_list(value: Any, field: str, *, sorted_unique: bool = False, allowed: set[str] | None = None) -> list[str]:
    if not isinstance(value, list):
        fail(f"{field} must be an array.", field=field)
    result = [_text(item, f"{field}[{index}]") for index, item in enumerate(value)]
    if len(set(result)) != len(result):
        fail(f"{field} must not contain duplicates.", field=field)
    if sorted_unique and result != sorted(result):
        fail(f"{field} must be sorted.", field=field)
    if allowed is not None and not set(result) <= allowed:
        fail(f"{field} contains an unsupported value.", field=field)
    return result


def validate_reference(value: Any, field: str = "reference", *, expected_type: str | None = None) -> dict[str, Any]:
    record = _object(value, field, {"artifact_id", "artifact_type", "revision", "canonical_digest"})
    _id(record["artifact_id"], f"{field}.artifact_id")
    if record["artifact_type"] not in ARTIFACT_TYPES:
        fail(f"{field}.artifact_type is unsupported.", field=f"{field}.artifact_type")
    if expected_type is not None and record["artifact_type"] != expected_type:
        fail(f"{field}.artifact_type must be {expected_type}.", field=f"{field}.artifact_type")
    if not isinstance(record["revision"], int) or isinstance(record["revision"], bool) or record["revision"] < 1:
        fail(f"{field}.revision must be a positive integer.", field=f"{field}.revision")
    if not isinstance(record["canonical_digest"], str) or not SHA256_RE.fullmatch(record["canonical_digest"]):
        fail(f"{field}.canonical_digest must be lowercase SHA-256.", field=f"{field}.canonical_digest")
    return record


def _validate_common(record: dict[str, Any], artifact_type: str) -> None:
    schema, fields = SCHEMAS[artifact_type]
    if artifact_type == "project" and record.get("schema_version") == "ala.authoring.project.v1":
        schema, fields = "ala.authoring.project.v1", PROJECT_V1_FIELDS
    _object(record, artifact_type, COMMON | fields)
    if record["schema_version"] != schema or record["artifact_type"] != artifact_type:
        fail(f"{artifact_type} schema or artifact type does not match.")
    _id(record["artifact_id"], "artifact_id")
    if not isinstance(record["revision"], int) or isinstance(record["revision"], bool) or record["revision"] < 1:
        fail("revision must be a positive integer.", field="revision")
    if record["status"] not in LIFECYCLE:
        fail("status is unsupported.", field="status")
    _timestamp(record["created_at"], "created_at")
    _timestamp(record["modified_at"], "modified_at")
    author = _object(record["author"], "author", {"identity", "identity_type", "role"})
    _text(author["identity"], "author.identity")
    if author["identity_type"] not in {"human", "model", "service", "imported"}:
        fail("author.identity_type is unsupported.", field="author.identity_type")
    _text(author["role"], "author.role")
    if record["supersedes"] is not None:
        validate_reference(record["supersedes"], "supersedes", expected_type=artifact_type)
    if not isinstance(record["canonical_digest"], str) or not SHA256_RE.fullmatch(record["canonical_digest"]):
        fail("canonical_digest must be lowercase SHA-256.", field="canonical_digest")


def validate_record(record: dict[str, Any], *, markdown: str | None = None, verify_digest: bool = True) -> dict[str, Any]:
    if not isinstance(record, dict):
        fail("A record must be an object.")
    artifact_type = record.get("artifact_type")
    if artifact_type not in ARTIFACT_TYPES:
        fail("artifact_type is unsupported.", field="artifact_type")
    _validate_common(record, artifact_type)
    identity_field = {
        "project": "project_id", "source": "source_id", "claim": "claim_id", "lesson": "lesson_id",
        "question_spec": "specification_id", "question": "question_id", "approval": "approval_id",
        "review": "review_id", "validation_report": "validation_id", "release_candidate": "candidate_id",
        "ai_verification_run": "verification_id", "verification_finding": "finding_id",
        "finding_resolution": "resolution_id",
    }.get(artifact_type)
    if identity_field and record[identity_field] != record["artifact_id"]:
        fail(f"{identity_field} must equal artifact_id.", field=identity_field)
    validator = globals().get(f"_validate_{artifact_type}")
    if validator is not None:
        validator(record, markdown)
    if verify_digest:
        expected = artifact_digest(record, markdown_path=record.get("markdown_path"), markdown=markdown)
        if record["canonical_digest"] != expected:
            fail("canonical_digest does not match the canonical record bytes.", field="canonical_digest")
        if artifact_type == "validation_report" and record["output_digest"] != expected:
            fail("output_digest does not match the validation-report digest.", field="output_digest")
    return record


def _validate_project(record: dict[str, Any], _: str | None) -> None:
    _text(record["title"], "title")
    scope_fields = {
        "assessment_blueprint", "learning_architecture", "realization_plan", "objective_ids",
        "lesson_count", "question_count", "response_mix",
    }
    if record["schema_version"] == "ala.authoring.project.v2":
        scope_fields.add("claim_count_range")
        if not isinstance(record["workspace_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["workspace_commit"]):
            fail("workspace_commit must be a full lowercase Git commit.", field="workspace_commit")
    _object(record["pilot_scope"], "pilot_scope", scope_fields)
    for field in ("assessment_blueprint", "learning_architecture", "realization_plan"):
        _object(record["pilot_scope"][field], f"pilot_scope.{field}", {"version", "path", "canonical_digest"})
        _text(record["pilot_scope"][field]["version"], f"pilot_scope.{field}.version")
        portable_relative_path(record["pilot_scope"][field]["path"])
        if not isinstance(record["pilot_scope"][field]["canonical_digest"], str) or not SHA256_RE.fullmatch(record["pilot_scope"][field]["canonical_digest"]):
            fail(f"pilot_scope.{field}.canonical_digest must be lowercase SHA-256.")
    _string_list(record["pilot_scope"]["objective_ids"], "pilot_scope.objective_ids", sorted_unique=True)
    for field in ("lesson_count", "question_count"):
        if not isinstance(record["pilot_scope"][field], int) or record["pilot_scope"][field] < 0:
            fail(f"pilot_scope.{field} must be a non-negative integer.")
    if "claim_count_range" in record["pilot_scope"]:
        claim_range = _object(record["pilot_scope"]["claim_count_range"], "pilot_scope.claim_count_range", {"minimum", "maximum"})
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in claim_range.values()):
            fail("pilot_scope.claim_count_range values must be non-negative integers.")
        if claim_range["minimum"] > claim_range["maximum"]:
            fail("pilot_scope.claim_count_range minimum cannot exceed maximum.")
    mix = _object(record["pilot_scope"]["response_mix"], "pilot_scope.response_mix", {"single_response", "multiple_response"})
    if any(not isinstance(value, int) or value < 0 for value in mix.values()):
        fail("response_mix values must be non-negative integers.")
    if record["default_target_pack_format"] != "0.2" or record["allowed_target_pack_formats"] != ["0.2", "0.3"] or record["text_only_default"] is not True:
        fail("Project pack-format defaults must match the accepted 0.3B contract.")
    if not isinstance(record["artifact_indexes"], dict) or not record["artifact_indexes"]:
        fail("artifact_indexes must be a non-empty object.")
    for path in record["artifact_indexes"].values():
        portable_relative_path(path)
    if record["private_material_policy"] != "prohibited":
        fail("private_material_policy must be prohibited.")


def _validate_source(record: dict[str, Any], _: str | None) -> None:
    for field in ("title", "publisher"):
        _text(record[field], field)
    url = _text(record["canonical_url"], "canonical_url")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        fail("canonical_url must be a public HTTPS URL without credentials.", field="canonical_url")
    if record["source_category"] not in SOURCE_CATEGORIES:
        fail("source_category is unsupported.", field="source_category")
    if record["authority_tier"] not in AUTHORITY_TIERS or record["rights_reuse"] not in RIGHTS_REUSE:
        fail("Source authority or rights vocabulary is unsupported.")
    _string_list(record["intended_uses"], "intended_uses", sorted_unique=True, allowed=INTENDED_USES)
    _date(record["retrieved_on"], "retrieved_on")
    _date(record["published_or_updated_on"], "published_or_updated_on", nullable=True)
    _text(record["source_revision"], "source_revision", nullable=True)
    snapshot = _object(record["retained_snapshot"], "retained_snapshot", {"retained", "content_sha256", "repository_path"})
    if not isinstance(snapshot["retained"], bool):
        fail("retained_snapshot.retained must be boolean.")
    if snapshot["retained"]:
        if not isinstance(snapshot["content_sha256"], str) or not SHA256_RE.fullmatch(snapshot["content_sha256"]):
            fail("A retained snapshot requires a lowercase SHA-256 digest.")
        portable_relative_path(snapshot["repository_path"])
    elif snapshot["content_sha256"] is not None or snapshot["repository_path"] is not None:
        fail("Unretained snapshots cannot declare bytes or a path.")
    freshness = _object(record["freshness_policy"], "freshness_policy", {"mode", "max_age_days", "recheck_triggers", "last_checked_on"})
    if freshness["mode"] not in {"max_age_days", "event_triggered", "both"}:
        fail("freshness_policy.mode is unsupported.")
    if freshness["max_age_days"] is not None and (not isinstance(freshness["max_age_days"], int) or freshness["max_age_days"] < 1):
        fail("freshness_policy.max_age_days must be a positive integer or null.")
    if freshness["mode"] in {"max_age_days", "both"} and freshness["max_age_days"] is None:
        fail("A max-age freshness mode requires max_age_days.")
    _string_list(freshness["recheck_triggers"], "freshness_policy.recheck_triggers", sorted_unique=True)
    _date(freshness["last_checked_on"], "freshness_policy.last_checked_on")
    _state(record["review_state"], "review_state", "approval")
    _text(record["access_limitations"], "access_limitations", nullable=True)
    prohibited = record["source_category"] == "prohibited_material" or record["authority_tier"] == "excluded" or record["rights_reuse"] == "prohibited"
    if prohibited:
        disposition = _object(record["prohibited_disposition"], "prohibited_disposition", {"reason", "content_retained", "downstream_use"})
        _text(disposition["reason"], "prohibited_disposition.reason")
        if disposition["content_retained"] is not False or disposition["downstream_use"] != "none":
            fail("Prohibited sources must retain no content and permit no downstream use.")
    elif record["prohibited_disposition"] is not None:
        fail("prohibited_disposition is only valid for prohibited or excluded sources.")


def _state(value: Any, field: str, reference_key: str) -> None:
    state = _object(value, field, {"status", reference_key})
    if state["status"] not in {"not_run", "pending", "passed", "failed", "approved", "changes_requested", "rejected", "invalidated"}:
        fail(f"{field}.status is unsupported.")
    if state[reference_key] is not None:
        validate_reference(state[reference_key], f"{field}.{reference_key}")


def _validate_claim(record: dict[str, Any], _: str | None) -> None:
    _text(record["statement"], "statement")
    if record["category"] not in CLAIM_CATEGORIES:
        fail("category is unsupported.", field="category")
    refs = record["source_references"]
    if not isinstance(refs, list) or not refs:
        fail("source_references must be non-empty.")
    for index, value in enumerate(refs):
        item = _object(value, f"source_references[{index}]", {"source_id", "revision", "canonical_digest", "locator", "supported_proposition"})
        _id(item["source_id"], f"source_references[{index}].source_id")
        _text(item["locator"], f"source_references[{index}].locator")
        _text(item["supported_proposition"], f"source_references[{index}].supported_proposition")
        if not isinstance(item["revision"], int) or item["revision"] < 1 or not SHA256_RE.fullmatch(item["canonical_digest"]):
            fail("Source references require a positive revision and digest.")
    _object(record["applicability"], "applicability", {"conditions", "exclusions", "decision_context"})
    for field in ("conditions", "exclusions", "decision_context"):
        _string_list(record["applicability"][field], f"applicability.{field}")
    _object(record["scope"], "scope", {"services", "architecture_patterns", "account_boundaries", "objective_ids"})
    for field in record["scope"]:
        _string_list(record["scope"][field], f"scope.{field}", sorted_unique=True)
    region = _object(record["region_sensitivity"], "region_sensitivity", {"level", "regions", "partitions"})
    if region["level"] not in {"none", "possible", "explicit"}:
        fail("region_sensitivity.level is unsupported.")
    _string_list(region["regions"], "region_sensitivity.regions", sorted_unique=True)
    _string_list(region["partitions"], "region_sensitivity.partitions", sorted_unique=True)
    account = _object(record["account_configuration_sensitivity"], "account_configuration_sensitivity", {"level", "required_states", "forbidden_states"})
    if account["level"] not in {"none", "possible", "explicit"}:
        fail("account_configuration_sensitivity.level is unsupported.")
    _string_list(account["required_states"], "account_configuration_sensitivity.required_states", sorted_unique=True)
    _string_list(account["forbidden_states"], "account_configuration_sensitivity.forbidden_states", sorted_unique=True)
    time = _object(record["time_sensitivity"], "time_sensitivity", {"level"})
    if time["level"] not in {"stable", "review_on_change", "short_horizon"}:
        fail("time_sensitivity.level is unsupported.")
    horizon = _object(record["freshness_horizon"], "freshness_horizon", {"valid_through", "rule", "last_checked_on"})
    _date(horizon["valid_through"], "freshness_horizon.valid_through", nullable=True)
    _text(horizon["rule"], "freshness_horizon.rule", nullable=True)
    _date(horizon["last_checked_on"], "freshness_horizon.last_checked_on")
    if horizon["valid_through"] is None and horizon["rule"] is None:
        fail("freshness_horizon requires a date or rule.")
    if not isinstance(record["derived_from"], list):
        fail("derived_from must be an array.")
    for index, item in enumerate(record["derived_from"]):
        validate_reference(item, f"derived_from[{index}]", expected_type="claim")
    if record["category"] == "derived_recommendation" and (not record["derived_from"] or not record["decision_criterion"]):
        fail("Derived recommendations require premise claims and a decision criterion.")
    if record["category"] != "derived_recommendation" and record["decision_criterion"] is not None:
        fail("decision_criterion is only valid for a derived recommendation.")
    _state(record["validation_state"], "validation_state", "report")
    _state(record["human_review_state"], "human_review_state", "approval")
    invalidation = _object(record["invalidation_state"], "invalidation_state", {"status", "reason", "event"})
    if invalidation["status"] not in {"current", "stale", "invalidated", "superseded"}:
        fail("invalidation_state.status is unsupported.")


def _validate_lesson(record: dict[str, Any], markdown: str | None) -> None:
    if markdown is None:
        fail("Lesson validation requires Markdown bytes.")
    for field in ("objective_ids", "prerequisite_bridge_ids"):
        _string_list(record[field], field, sorted_unique=True)
    if not isinstance(record["claim_references"], list):
        fail("claim_references must be an array.")
    for index, item in enumerate(record["claim_references"]):
        validate_reference(item, f"claim_references[{index}]", expected_type="claim")
    portable_relative_path(record["markdown_path"])
    if record["markdown_sha256"] != markdown_digest(markdown):
        fail("markdown_sha256 does not match normalized Markdown.")
    if not isinstance(record["learner_citations"], list):
        fail("learner_citations must be an array.")
    for index, item in enumerate(record["learner_citations"]):
        citation = _object(item, f"learner_citations[{index}]", {"source_id", "revision", "canonical_digest", "locator"})
        _id(citation["source_id"], f"learner_citations[{index}].source_id")
        _text(citation["locator"], f"learner_citations[{index}].locator")
    if record["intended_depth"] not in {"foundation", "applied", "professional"}:
        fail("intended_depth is unsupported.")
    _state(record["validation_state"], "validation_state", "report")
    _state(record["content_review_state"], "content_review_state", "review")


def _validate_question_spec(record: dict[str, Any], _: str | None) -> None:
    _text(record["target_objective_id"], "target_objective_id")
    _string_list(record["supporting_objective_ids"], "supporting_objective_ids", sorted_unique=True)
    if record["intended_cognitive_operation"] not in {"identify", "interpret", "apply", "analyze", "evaluate", "design"}:
        fail("intended_cognitive_operation is unsupported.")
    if not isinstance(record["assessment_blueprint_references"], list) or not record["assessment_blueprint_references"]:
        fail("assessment_blueprint_references must be non-empty.")
    for index, item in enumerate(record["assessment_blueprint_references"]):
        ref = _object(item, f"assessment_blueprint_references[{index}]", {"blueprint_id", "version", "canonical_digest", "matched_features"})
        _text(ref["blueprint_id"], f"assessment_blueprint_references[{index}].blueprint_id")
        if not SHA256_RE.fullmatch(ref["canonical_digest"]):
            fail("Blueprint references require a digest.")
        _string_list(ref["matched_features"], f"assessment_blueprint_references[{index}].matched_features")
    response = _object(record["response_design"], "response_design", {"question_type", "required_selection_count"})
    _response_rule(response["question_type"], response["required_selection_count"], None)
    _text(record["scenario_theme"], "scenario_theme")
    for field in ("material_requirements", "material_constraints"):
        if not isinstance(record[field], list):
            fail(f"{field} must be an array.")
        for index, item in enumerate(record[field]):
            _object(item, f"{field}[{index}]", {"requirement_id", "description"})
            _id(item["requirement_id"], f"{field}[{index}].requirement_id")
            _text(item["description"], f"{field}[{index}].description")
    for field in ("compared_services_or_patterns", "expected_keyed_answer_properties", "planned_distractor_categories", "evidence_requirements", "ambiguity_risks", "originality_notes"):
        _string_list(record[field], field, sorted_unique=field == "compared_services_or_patterns")
    if record["intended_difficulty"] not in {"medium", "medium_high", "high"}:
        fail("intended_difficulty is unsupported.")
    _state(record["validation_state"], "validation_state", "report")
    _state(record["design_review_state"], "design_review_state", "review")


def _response_rule(question_type: Any, count: Any, key_count: int | None) -> None:
    if question_type not in {"single_response", "multiple_response"} or not isinstance(count, int) or isinstance(count, bool) or count < 1:
        fail("Question type or required selection count is invalid.")
    if question_type == "single_response" and count != 1:
        fail("Single-response questions require selection count 1.")
    if key_count is not None and count != key_count:
        fail("Key count must equal required selection count.")


def _validate_question(record: dict[str, Any], _: str | None) -> None:
    validate_reference(record["specification_reference"], "specification_reference", expected_type="question_spec")
    _response_rule(record["question_type"], record["required_selection_count"], len(record["keyed_option_ids"]) if isinstance(record["keyed_option_ids"], list) else None)
    _text(record["stem"], "stem")
    if not isinstance(record["options"], list) or len(record["options"]) < 2:
        fail("options must contain at least two options.")
    option_ids: list[str] = []
    for index, item in enumerate(record["options"]):
        option = _object(item, f"options[{index}]", {"option_id", "text"})
        option_ids.append(_id(option["option_id"], f"options[{index}].option_id"))
        _text(option["text"], f"options[{index}].text")
    if len(set(option_ids)) != len(option_ids):
        fail("Option IDs must be unique.")
    keys = _string_list(record["keyed_option_ids"], "keyed_option_ids")
    if any(key not in option_ids for key in keys) or keys != [item for item in option_ids if item in keys]:
        fail("keyed_option_ids must resolve in option declaration order.")
    _text(record["learner_explanation"], "learner_explanation")
    if not isinstance(record["option_rationales"], list):
        fail("option_rationales must be an array.")
    rationale_ids: list[str] = []
    for index, item in enumerate(record["option_rationales"]):
        rationale = _object(item, f"option_rationales[{index}]", {"option_id", "is_keyed", "category", "requirement_ids", "claim_references", "rationale"})
        rationale_ids.append(_id(rationale["option_id"], f"option_rationales[{index}].option_id"))
        if not isinstance(rationale["is_keyed"], bool):
            fail("option rationale is_keyed must be boolean.")
        _text(rationale["category"], f"option_rationales[{index}].category")
        _string_list(rationale["requirement_ids"], f"option_rationales[{index}].requirement_ids")
        if not isinstance(rationale["claim_references"], list):
            fail("Rationale claim_references must be an array.")
        for ref_index, ref in enumerate(rationale["claim_references"]):
            validate_reference(ref, f"option_rationales[{index}].claim_references[{ref_index}]", expected_type="claim")
        _text(rationale["rationale"], f"option_rationales[{index}].rationale")
        if rationale["is_keyed"] != (rationale["option_id"] in keys):
            fail("Rationale keyed state must match keyed_option_ids.")
    if rationale_ids != option_ids:
        fail("Exactly one ordered option rationale is required per option.")
    if not isinstance(record["requirement_option_matrix"], list) or not record["requirement_option_matrix"]:
        fail("requirement_option_matrix must be non-empty.")
    for index, row in enumerate(record["requirement_option_matrix"]):
        matrix = _object(row, f"requirement_option_matrix[{index}]", {"requirement_id", "cells"})
        _id(matrix["requirement_id"], f"requirement_option_matrix[{index}].requirement_id")
        if not isinstance(matrix["cells"], list):
            fail("Matrix cells must be an array.")
        cells = []
        results: dict[str, str] = {}
        for cell_index, item in enumerate(matrix["cells"]):
            cell = _object(item, f"requirement_option_matrix[{index}].cells[{cell_index}]", {"option_id", "result"})
            cells.append(cell["option_id"])
            if cell["result"] not in {"satisfies", "fails", "not_applicable"}:
                fail("Matrix result is unsupported.")
            results[cell["option_id"]] = cell["result"]
        if cells != option_ids:
            fail("Every matrix row must cover every option in declaration order.")
        if any(results[key] != "satisfies" for key in keys):
            fail("Every keyed option must satisfy every material requirement.")
    for option_id in option_ids:
        if option_id not in keys and not any(next(cell["result"] for cell in row["cells"] if cell["option_id"] == option_id) == "fails" for row in record["requirement_option_matrix"]):
            fail("Every distractor must fail at least one material requirement.")
    for index, ref in enumerate(record["supporting_claim_references"]):
        validate_reference(ref, f"supporting_claim_references[{index}]", expected_type="claim")
    objectives = _object(record["objective_references"], "objective_references", {"primary", "supporting"})
    _text(objectives["primary"], "objective_references.primary")
    _string_list(objectives["supporting"], "objective_references.supporting", sorted_unique=True)
    if not isinstance(record["blueprint_references"], list) or not isinstance(record["source_citation_projection"], list):
        fail("Blueprint and citation projections must be arrays.")
    for index, item in enumerate(record["blueprint_references"]):
        blueprint = _object(item, f"blueprint_references[{index}]", {"blueprint_id", "version", "canonical_digest"})
        _text(blueprint["blueprint_id"], f"blueprint_references[{index}].blueprint_id")
        _text(blueprint["version"], f"blueprint_references[{index}].version")
        if not isinstance(blueprint["canonical_digest"], str) or not SHA256_RE.fullmatch(blueprint["canonical_digest"]):
            fail("Blueprint references require lowercase SHA-256 digests.")
    for index, item in enumerate(record["source_citation_projection"]):
        citation = _object(item, f"source_citation_projection[{index}]", {"source_id", "revision", "canonical_digest", "locator"})
        _id(citation["source_id"], f"source_citation_projection[{index}].source_id")
        if not isinstance(citation["revision"], int) or citation["revision"] < 1 or not isinstance(citation["canonical_digest"], str) or not SHA256_RE.fullmatch(citation["canonical_digest"]):
            fail("Citation projections require a positive revision and lowercase SHA-256 digest.")
        _text(citation["locator"], f"source_citation_projection[{index}].locator")
    for field, key in (("originality_review_state", "review"), ("content_review_state", "approval"), ("answer_uniqueness_state", "approval"), ("validation_state", "report")):
        _state(record[field], field, key)


def _validate_approval(record: dict[str, Any], _: str | None) -> None:
    if record["approval_type"] not in APPROVAL_TYPES:
        fail("approval_type is unsupported.")
    _validate_decision(record)


def _validate_review(record: dict[str, Any], _: str | None) -> None:
    if record["review_type"] not in REVIEW_TYPES:
        fail("review_type is unsupported.")
    _validate_decision(record)


def _validate_decision(record: dict[str, Any]) -> None:
    if record["record_kind"] not in {"decision", "supersession", "revocation"} or record["decision"] not in DECISIONS:
        fail("Decision kind or decision is unsupported.")
    validate_reference(record["target"], "target")
    digests = _string_list(record["dependency_digests"], "dependency_digests", sorted_unique=True)
    if any(not SHA256_RE.fullmatch(item) for item in digests):
        fail("dependency_digests must contain lowercase SHA-256 values.")
    if not isinstance(record["prerequisite_decisions"], list):
        fail("prerequisite_decisions must be an array.")
    for index, item in enumerate(record["prerequisite_decisions"]):
        validate_reference(item, f"prerequisite_decisions[{index}]")
    reviewer = _object(record["reviewer"], "reviewer", {"identity", "role", "qualification_summary", "conflict_of_interest"})
    for field in reviewer:
        _text(reviewer[field], f"reviewer.{field}")
    for field in ("scope", "conditions"):
        _string_list(record[field], field)
    if not isinstance(record["findings"], list):
        fail("findings must be an array.")
    for index, item in enumerate(record["findings"]):
        finding = _object(item, f"findings[{index}]", {"visibility", "text"})
        if finding["visibility"] not in {"public", "release_evidence", "private_local_reference"}:
            fail("Finding visibility is unsupported.")
        _text(finding["text"], f"findings[{index}].text")
    _timestamp(record["decided_at"], "decided_at")
    for field in ("supersedes_decision_id", "revokes_decision_id"):
        if record[field] is not None:
            _id(record[field], field)
    if record["record_kind"] == "revocation" and (record["decision"] != "revoked" or record["revokes_decision_id"] is None):
        fail("Revocation records require decision revoked and a prior decision ID.")
    if record["record_kind"] != "revocation" and record["decision"] == "revoked":
        fail("Only revocation records may use decision revoked.")


def _validate_validation_report(record: dict[str, Any], _: str | None) -> None:
    for field in ("validator_name", "validator_version", "rule_set_id", "rule_set_version"):
        _text(record[field], field)
    _timestamp(record["executed_at"], "executed_at")
    if not isinstance(record["workspace_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["workspace_commit"]):
        fail("workspace_commit must be a full lowercase Git commit.")
    if not isinstance(record["checked_artifacts"], list):
        fail("checked_artifacts must be an array.")
    for index, item in enumerate(record["checked_artifacts"]):
        validate_reference(item, f"checked_artifacts[{index}]")
    if not isinstance(record["findings"], list):
        fail("findings must be an array.")
    for index, item in enumerate(record["findings"]):
        finding = _object(item, f"findings[{index}]", {"code", "severity", "blocking", "artifact", "field", "message"})
        if finding["severity"] not in {"error", "warning", "information"} or not isinstance(finding["blocking"], bool):
            fail("Finding severity or blocking state is invalid.")
    if record["result"] not in {"passed", "failed"} or record["human_approval_implication"] != "none":
        fail("Validation report result or authority declaration is invalid.")


def _compiled_pack(value: Any, field: str = "compiled_pack") -> dict[str, Any]:
    record = _object(value, field, {"pack_id", "version", "target_format", "relative_output_path", "digest"})
    _text(record["pack_id"], f"{field}.pack_id")
    _text(record["version"], f"{field}.version")
    if record["target_format"] not in {"0.2", "0.3"}:
        fail(f"{field}.target_format is unsupported.")
    portable_relative_path(record["relative_output_path"])
    if not isinstance(record["digest"], str) or not SHA256_RE.fullmatch(record["digest"]):
        fail(f"{field}.digest must be lowercase SHA-256.")
    return record


def _validate_release_candidate(record: dict[str, Any], _: str | None) -> None:
    _text(record["compiler_version"], "compiler_version")
    validate_reference(record["project"], "project", expected_type="project")
    for field in ("selection_digest", "compiler_input_digest", "compiler_output_digest"):
        if not isinstance(record[field], str) or not SHA256_RE.fullmatch(record[field]):
            fail(f"{field} must be lowercase SHA-256.")
    if not isinstance(record["source_workspace_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["source_workspace_commit"]):
        fail("source_workspace_commit must be a full lowercase Git commit.")
    _compiled_pack(record["compiled_pack"])
    _timestamp(record["compilation_timestamp"], "compilation_timestamp")


def _validate_release_evidence(record: dict[str, Any], _: str | None) -> None:
    if record["phase"] not in {"candidate", "final"}:
        fail("Release evidence phase is invalid.")
    if record["phase"] == "candidate" and (record["candidate_manifest"] is not None or record["release_review_approval"] is not None):
        fail("Candidate evidence cannot include final approval references.")
    if record["phase"] == "final":
        validate_reference(record["candidate_manifest"], "candidate_manifest", expected_type="release_evidence")
        validate_reference(record["release_review_approval"], "release_review_approval", expected_type="approval")
    validate_reference(record["project"], "project", expected_type="project")
    _text(record["compiler_version"], "compiler_version")
    if not isinstance(record["source_workspace_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["source_workspace_commit"]):
        fail("source_workspace_commit must be a full lowercase Git commit.")
    for field in ("assessment_blueprint", "learning_architecture", "realization_plan"):
        design = _object(record[field], field, {"version", "path", "canonical_digest"})
        _text(design["version"], f"{field}.version")
        portable_relative_path(design["path"])
        if not isinstance(design["canonical_digest"], str) or not SHA256_RE.fullmatch(design["canonical_digest"]):
            fail(f"{field}.canonical_digest must be lowercase SHA-256.")
    for field, expected_type in (
        ("source_records", "source"), ("approved_claims", "claim"), ("lessons", "lesson"),
        ("question_specifications", "question_spec"), ("approved_final_questions", "question"),
        ("validation_reports", "validation_report"),
    ):
        if not isinstance(record[field], list):
            fail(f"{field} must be an array.")
        for index, item in enumerate(record[field]):
            validate_reference(item, f"{field}[{index}]", expected_type=expected_type)
    if not isinstance(record["approval_records"], list):
        fail("approval_records must be an array.")
    for index, item in enumerate(record["approval_records"]):
        validate_reference(item, f"approval_records[{index}]")
        if item["artifact_type"] not in {"approval", "review"}:
            fail("approval_records may contain only approval or review references.")
    _compiled_pack(record["compiled_pack"])
    _timestamp(record["compilation_timestamp"], "compilation_timestamp")
    for field in ("compiler_input_digest", "compiler_output_digest"):
        if not isinstance(record[field], str) or not SHA256_RE.fullmatch(record[field]):
            fail(f"{field} must be lowercase SHA-256.")
    _string_list(record["exclusions"], "exclusions")


def _validate_ai_verification_run(record: dict[str, Any], _: str | None) -> None:
    _text(record["protocol_version"], "protocol_version")
    _id(record["target_project_id"], "target_project_id")
    if not isinstance(record["target_workspace_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["target_workspace_commit"]):
        fail("target_workspace_commit must be a full lowercase Git commit.", field="target_workspace_commit")
    verifier = _object(record["verifier"], "verifier", {"identity", "identity_type", "role", "invocation_id"})
    _text(verifier["identity"], "verifier.identity")
    if verifier["identity_type"] not in {"model", "service"}:
        fail("The independent verifier must be a model or service identity.", field="verifier.identity_type")
    if verifier["role"] != "independent_ai_verifier":
        fail("verifier.role must be independent_ai_verifier.", field="verifier.role")
    _text(verifier["invocation_id"], "verifier.invocation_id")
    model = _object(record["model"], "model", {"provider", "model_id", "configuration", "reproducibility_notes"})
    _text(model["provider"], "model.provider", nullable=True)
    _text(model["model_id"], "model.model_id", nullable=True)
    if not isinstance(model["configuration"], dict):
        fail("model.configuration must be an object.", field="model.configuration")
    _text(model["reproducibility_notes"], "model.reproducibility_notes", nullable=True)
    _date(record["research_date"], "research_date")
    if not isinstance(record["target_artifacts"], list) or not record["target_artifacts"]:
        fail("target_artifacts must be a non-empty array.", field="target_artifacts")
    for index, item in enumerate(record["target_artifacts"]):
        validate_reference(item, f"target_artifacts[{index}]")
    if not isinstance(record["architecture_references"], list) or not record["architecture_references"]:
        fail("architecture_references must be non-empty.", field="architecture_references")
    for index, item in enumerate(record["architecture_references"]):
        ref = _object(item, f"architecture_references[{index}]", {"artifact_id", "version", "path", "canonical_digest"})
        _text(ref["artifact_id"], f"architecture_references[{index}].artifact_id")
        _text(ref["version"], f"architecture_references[{index}].version")
        portable_relative_path(ref["path"])
        if not isinstance(ref["canonical_digest"], str) or not SHA256_RE.fullmatch(ref["canonical_digest"]):
            fail("Architecture-reference digest must be lowercase SHA-256.")
    _string_list(record["verification_scope"], "verification_scope", sorted_unique=True)
    validate_reference(record["deterministic_validation_report"], "deterministic_validation_report", expected_type="validation_report")
    if not isinstance(record["independently_accessed_sources"], list):
        fail("independently_accessed_sources must be an array.")
    for index, item in enumerate(record["independently_accessed_sources"]):
        source = _object(item, f"independently_accessed_sources[{index}]", {"source_id", "title", "publisher", "canonical_url", "accessed_on", "locators"})
        _id(source["source_id"], f"independently_accessed_sources[{index}].source_id")
        _text(source["title"], f"independently_accessed_sources[{index}].title")
        _text(source["publisher"], f"independently_accessed_sources[{index}].publisher")
        parsed = urlsplit(_text(source["canonical_url"], f"independently_accessed_sources[{index}].canonical_url"))
        if parsed.scheme != "https" or not parsed.netloc:
            fail("Consulted sources require public HTTPS URLs.")
        _date(source["accessed_on"], f"independently_accessed_sources[{index}].accessed_on")
        _string_list(source["locators"], f"independently_accessed_sources[{index}].locators")
    for index, item in enumerate(record["finding_references"]):
        validate_reference(item, f"finding_references[{index}]", expected_type="verification_finding")
    if not isinstance(record["artifact_dispositions"], list):
        fail("artifact_dispositions must be an array.")
    for index, item in enumerate(record["artifact_dispositions"]):
        disposition = _object(item, f"artifact_dispositions[{index}]", {"target", "disposition", "finding_ids", "notes"})
        validate_reference(disposition["target"], f"artifact_dispositions[{index}].target")
        if disposition["disposition"] not in VERIFICATION_DISPOSITIONS:
            fail("Artifact disposition is unsupported.")
        _string_list(disposition["finding_ids"], f"artifact_dispositions[{index}].finding_ids", sorted_unique=True)
        _text(disposition["notes"], f"artifact_dispositions[{index}].notes", nullable=True)
    counts = _object(record["summary_counts"], "summary_counts", {"total_artifacts", "total_findings", "blocking_findings", "by_disposition", "by_severity"})
    for field in ("total_artifacts", "total_findings", "blocking_findings"):
        if not isinstance(counts[field], int) or isinstance(counts[field], bool) or counts[field] < 0:
            fail(f"summary_counts.{field} must be a non-negative integer.")
    for field, keys in (("by_disposition", VERIFICATION_DISPOSITIONS), ("by_severity", VERIFICATION_SEVERITIES)):
        values = _object(counts[field], f"summary_counts.{field}", keys)
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values.values()):
            fail(f"summary_counts.{field} values must be non-negative integers.")
    _string_list(record["unresolved_questions"], "unresolved_questions")
    if record["completion_status"] not in {"in_progress", "completed", "failed"}:
        fail("completion_status is unsupported.")
    if record["human_approval_implication"] != "none":
        fail("AI verification never implies human approval.")


def _validate_verification_finding(record: dict[str, Any], _: str | None) -> None:
    _id(record["verification_id"], "verification_id")
    validate_reference(record["target"], "target")
    _text(record["disputed_field"], "disputed_field")
    _text(record["disputed_language"], "disputed_language", nullable=True)
    if record["category"] not in VERIFICATION_CATEGORIES or record["severity"] not in VERIFICATION_SEVERITIES:
        fail("Finding category or severity is unsupported.")
    source = _object(record["supporting_source"], "supporting_source", {"title", "publisher", "canonical_url", "accessed_on", "locator"})
    _text(source["title"], "supporting_source.title")
    _text(source["publisher"], "supporting_source.publisher")
    parsed = urlsplit(_text(source["canonical_url"], "supporting_source.canonical_url"))
    if parsed.scheme != "https" or not parsed.netloc:
        fail("supporting_source.canonical_url must be public HTTPS.")
    _date(source["accessed_on"], "supporting_source.accessed_on")
    _text(source["locator"], "supporting_source.locator")
    _text(record["explanation"], "explanation")
    _text(record["required_action"], "required_action")
    _text(record["suggested_revision"], "suggested_revision", nullable=True)
    for index, item in enumerate(record["affected_dependencies"]):
        validate_reference(item, f"affected_dependencies[{index}]")
    if record["confidence"] not in {"high", "medium", "low"}:
        fail("confidence is unsupported.")
    if not isinstance(record["blocking"], bool):
        fail("blocking must be boolean.")
    if record["finding_status"] not in {"open", "resolved", "disputed", "withdrawn"}:
        fail("finding_status is unsupported.")


def _validate_finding_resolution(record: dict[str, Any], _: str | None) -> None:
    validate_reference(record["finding"], "finding", expected_type="verification_finding")
    validate_reference(record["old_artifact"], "old_artifact")
    validate_reference(record["new_artifact"], "new_artifact")
    if record["old_artifact"]["artifact_id"] != record["new_artifact"]["artifact_id"] or record["old_artifact"]["artifact_type"] != record["new_artifact"]["artifact_type"]:
        fail("A finding resolution must preserve stable artifact identity.")
    _text(record["author_response"], "author_response")
    _text(record["change_summary"], "change_summary")
    if record["response_disposition"] not in {"accepted", "modified", "disputed"}:
        fail("response_disposition is unsupported.")
    if record["response_disposition"] != "disputed" and record["old_artifact"]["canonical_digest"] == record["new_artifact"]["canonical_digest"]:
        fail("Accepted or modified resolutions require a changed artifact digest.")
    _string_list(record["supporting_source_changes"], "supporting_source_changes")
    _timestamp(record["resolved_at"], "resolved_at")


def seal_record(record: dict[str, Any], *, markdown: str | None = None) -> dict[str, Any]:
    sealed = dict(record)
    if sealed.get("artifact_type") == "lesson" and markdown is not None:
        sealed["markdown_sha256"] = markdown_digest(markdown)
    sealed["canonical_digest"] = "0" * 64
    sealed["canonical_digest"] = artifact_digest(sealed, markdown_path=sealed.get("markdown_path"), markdown=markdown)
    if sealed.get("artifact_type") == "validation_report":
        sealed["output_digest"] = sealed["canonical_digest"]
    validate_record(sealed, markdown=markdown)
    return sealed
