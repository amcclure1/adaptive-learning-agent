from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from adaptive_learning.authoring.operations import AuthoringOperations
from adaptive_learning.authoring.workspace import reference


TIMESTAMP = "2030-01-01T00:00:00Z"
REVIEW_TIMESTAMP = "2030-01-02T00:00:00Z"
COMMIT = "0" * 40
DESIGN_DIGESTS = {"blueprint": "1" * 64, "architecture": "2" * 64, "realization": "3" * 64}


def author(identity: str, role: str = "synthetic_author") -> dict[str, str]:
    return {"identity": identity, "identity_type": "human", "role": role}


def reviewer(identity: str, role: str) -> dict[str, str]:
    return {
        "identity": identity,
        "role": role,
        "qualification_summary": "Synthetic test qualification",
        "conflict_of_interest": "none_declared",
    }


def common(artifact_id: str, artifact_type: str, schema_version: str, identity: str) -> dict[str, Any]:
    return {
        "schema_version": schema_version,
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "revision": 1,
        "status": "draft",
        "created_at": TIMESTAMP,
        "modified_at": TIMESTAMP,
        "author": author(identity),
        "supersedes": None,
        "canonical_digest": "0" * 64,
    }


def project_request(project_id: str = "synthetic-authoring") -> dict[str, Any]:
    return {
        "project_id": project_id,
        "title": "Synthetic authoring infrastructure test",
        "created_at": TIMESTAMP,
        "author": author("project-author", "project_owner"),
        "pilot_scope": {
            "assessment_blueprint": {"version": "test-1", "path": "docs/blueprint.md", "canonical_digest": DESIGN_DIGESTS["blueprint"]},
            "learning_architecture": {"version": "test-1", "path": "docs/architecture.md", "canonical_digest": DESIGN_DIGESTS["architecture"]},
            "realization_plan": {"version": "test-1", "path": "docs/realization.md", "canonical_digest": DESIGN_DIGESTS["realization"]},
            "objective_ids": ["obj-one"],
            "lesson_count": 1,
            "question_count": 1,
            "response_mix": {"single_response": 1, "multiple_response": 0},
        },
    }


def source_record(source_id: str, *, category: str = "service_documentation", author_id: str = "source-author") -> dict[str, Any]:
    return {
        **common(source_id, "source", "ala.authoring.source.v1", author_id),
        "source_id": source_id,
        "title": f"Synthetic source {source_id}",
        "publisher": "Synthetic Publisher",
        "canonical_url": f"https://example.invalid/{source_id}",
        "source_category": category,
        "authority_tier": "tier_1_official",
        "rights_reuse": "reference_only",
        "intended_uses": ["factual_support", "learner_citation"],
        "retrieved_on": "2030-01-01",
        "published_or_updated_on": "2030-01-01",
        "source_revision": "test-revision-1",
        "retained_snapshot": {"retained": False, "content_sha256": None, "repository_path": None},
        "freshness_policy": {"mode": "event_triggered", "max_age_days": None, "recheck_triggers": ["provider_revision"], "last_checked_on": "2030-01-01"},
        "review_state": {"status": "pending", "approval": None},
        "access_limitations": None,
        "prohibited_disposition": None,
    }


def claim_record(source: dict[str, Any], *, claim_id: str = "clm-synthetic", author_id: str = "claim-author") -> dict[str, Any]:
    return {
        **common(claim_id, "claim", "ala.authoring.claim.v1", author_id),
        "claim_id": claim_id,
        "statement": "A synthetic component has the documented test behavior.",
        "category": "documented_fact",
        "source_references": [{
            "source_id": source["artifact_id"], "revision": source["revision"],
            "canonical_digest": source["canonical_digest"], "locator": "section synthetic-1",
            "supported_proposition": "The bounded synthetic behavior.",
        }],
        "applicability": {"conditions": [], "exclusions": [], "decision_context": []},
        "scope": {"services": ["synthetic-component"], "architecture_patterns": [], "account_boundaries": [], "objective_ids": ["obj-one"]},
        "region_sensitivity": {"level": "none", "regions": [], "partitions": []},
        "account_configuration_sensitivity": {"level": "none", "required_states": [], "forbidden_states": []},
        "time_sensitivity": {"level": "review_on_change"},
        "freshness_horizon": {"valid_through": "2031-01-01", "rule": None, "last_checked_on": "2030-01-01"},
        "derived_from": [],
        "decision_criterion": None,
        "validation_state": {"status": "not_run", "report": None},
        "human_review_state": {"status": "pending", "approval": None},
        "invalidation_state": {"status": "current", "reason": None, "event": None},
    }


def lesson_record(claim: dict[str, Any], source: dict[str, Any], *, author_id: str = "lesson-author") -> tuple[dict[str, Any], str]:
    markdown = "# Synthetic lesson\r\n\r\nThis synthetic statement supports the test objective.\r\n"
    return ({
        **common("les-synthetic", "lesson", "ala.authoring.lesson.v1", author_id),
        "lesson_id": "les-synthetic",
        "objective_ids": ["obj-one"],
        "prerequisite_bridge_ids": [],
        "claim_references": [reference(claim)],
        "markdown_path": "lesson.md",
        "markdown_sha256": "0" * 64,
        "learner_citations": [{
            "source_id": source["artifact_id"], "revision": source["revision"],
            "canonical_digest": source["canonical_digest"], "locator": "section synthetic-1",
        }],
        "intended_depth": "applied",
        "validation_state": {"status": "not_run", "report": None},
        "content_review_state": {"status": "pending", "review": None},
    }, markdown)


def specification_record(*, author_id: str = "spec-author") -> dict[str, Any]:
    return {
        **common("qspec-synthetic", "question_spec", "ala.authoring.question-spec.v1", author_id),
        "specification_id": "qspec-synthetic",
        "target_objective_id": "obj-one",
        "supporting_objective_ids": [],
        "intended_cognitive_operation": "apply",
        "assessment_blueprint_references": [{"blueprint_id": "blueprint-synthetic", "version": "test-1", "canonical_digest": DESIGN_DIGESTS["blueprint"], "matched_features": ["scenario_reasoning"]}],
        "response_design": {"question_type": "single_response", "required_selection_count": 1},
        "scenario_theme": "Choose a synthetic component using explicit requirements.",
        "material_requirements": [{"requirement_id": "req-one", "description": "Meet the synthetic requirement."}],
        "material_constraints": [],
        "compared_services_or_patterns": ["pattern-one", "pattern-two"],
        "expected_keyed_answer_properties": ["meets the stated requirement"],
        "planned_distractor_categories": ["requirement_violation"],
        "evidence_requirements": ["documented_fact"],
        "intended_difficulty": "medium",
        "ambiguity_risks": [],
        "originality_notes": ["synthetic independent construction"],
        "validation_state": {"status": "not_run", "report": None},
        "design_review_state": {"status": "pending", "review": None},
    }


def question_record(spec: dict[str, Any], claim: dict[str, Any], source: dict[str, Any], *, author_id: str = "question-author") -> dict[str, Any]:
    return {
        **common("q-synthetic", "question", "ala.authoring.question.v1", author_id),
        "question_id": "q-synthetic",
        "specification_reference": reference(spec),
        "question_type": "single_response",
        "required_selection_count": 1,
        "stem": "A synthetic scenario requires behavior X. Which option meets the requirement?",
        "options": [{"option_id": "a", "text": "Use synthetic pattern one."}, {"option_id": "b", "text": "Use synthetic pattern two."}],
        "keyed_option_ids": ["a"],
        "learner_explanation": "Pattern one meets the requirement; pattern two does not.",
        "option_rationales": [
            {"option_id": "a", "is_keyed": True, "category": "key_support", "requirement_ids": ["req-one"], "claim_references": [reference(claim)], "rationale": "It satisfies the synthetic requirement."},
            {"option_id": "b", "is_keyed": False, "category": "requirement_violation", "requirement_ids": ["req-one"], "claim_references": [reference(claim)], "rationale": "It fails the synthetic requirement."},
        ],
        "requirement_option_matrix": [{"requirement_id": "req-one", "cells": [{"option_id": "a", "result": "satisfies"}, {"option_id": "b", "result": "fails"}]}],
        "supporting_claim_references": [reference(claim)],
        "objective_references": {"primary": "obj-one", "supporting": []},
        "blueprint_references": [{"blueprint_id": "blueprint-synthetic", "version": "test-1", "canonical_digest": DESIGN_DIGESTS["blueprint"]}],
        "source_citation_projection": [{"source_id": source["artifact_id"], "revision": source["revision"], "canonical_digest": source["canonical_digest"], "locator": "section synthetic-1"}],
        "originality_review_state": {"status": "pending", "review": None},
        "content_review_state": {"status": "pending", "approval": None},
        "answer_uniqueness_state": {"status": "pending", "approval": None},
        "validation_state": {"status": "not_run", "report": None},
    }


def draft_and_freeze(ops: AuthoringOperations, project_id: str, record: dict[str, Any], markdown: str | None = None) -> dict[str, Any]:
    draft = ops.add_or_update_draft({"project_id": project_id, "record": record, "expected_prior_digest": None, "markdown": markdown})["artifact"]
    return ops.freeze_draft({
        "project_id": project_id, "artifact_type": record["artifact_type"], "artifact_id": record["artifact_id"],
        "expected_draft_digest": draft["canonical_digest"], "modified_at": REVIEW_TIMESTAMP,
    })["artifact"]


def decide(ops: AuthoringOperations, project_id: str, decision_id: str, decision_type: str, target: dict[str, Any], reviewer_id: str, dependencies: list[str] | None = None, prerequisites: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return ops.create_decision({
        "project_id": project_id,
        "decision_id": decision_id,
        "decision_type": decision_type,
        "target": reference(target),
        "dependency_digests": dependencies or [],
        "prerequisite_decisions": prerequisites or [],
        "decision": "approved",
        "reviewer": reviewer(reviewer_id, decision_type),
        "scope": ["synthetic_test_scope"],
        "findings": [],
        "conditions": [],
        "decided_at": REVIEW_TIMESTAMP,
        "record_kind": "decision",
        "supersedes_decision_id": None,
        "revokes_decision_id": None,
    })["decision"]


def build_approved_workspace(root: Path) -> dict[str, Any]:
    ops = AuthoringOperations(root / "authoring")
    project_id = "synthetic-authoring"
    initialized = ops.initialize_project(project_request(project_id))
    project = initialized["project"]
    source_pool = draft_and_freeze(ops, project_id, source_record("src-pool", category="certification_blueprint"))
    source_errata = draft_and_freeze(ops, project_id, source_record("src-errata", category="announcement", author_id="errata-author"))
    source_pool_approval = decide(ops, project_id, "apr-source-pool", "source_approval", source_pool, "source-reviewer")
    source_errata_approval = decide(ops, project_id, "apr-source-errata", "source_approval", source_errata, "source-reviewer")
    claim = draft_and_freeze(ops, project_id, claim_record(source_pool))
    claim_approval = decide(ops, project_id, "apr-claim", "claim_approval", claim, "claim-reviewer", [source_pool["canonical_digest"]], [reference(source_pool_approval)])
    lesson_draft, markdown = lesson_record(claim, source_pool)
    lesson = draft_and_freeze(ops, project_id, lesson_draft, markdown)
    lesson_review = decide(ops, project_id, "rev-lesson", "lesson_content_review", lesson, "lesson-reviewer", [claim["canonical_digest"]], [reference(claim_approval)])
    spec = draft_and_freeze(ops, project_id, specification_record())
    spec_review = decide(ops, project_id, "rev-spec", "question_spec_design_review", spec, "spec-reviewer")
    question = draft_and_freeze(ops, project_id, question_record(spec, claim, source_pool))
    originality = decide(ops, project_id, "rev-originality", "question_originality_review", question, "originality-reviewer")
    content = decide(ops, project_id, "apr-content", "question_content_approval", question, "content-reviewer", [claim["canonical_digest"], spec["canonical_digest"], originality["canonical_digest"]], [reference(claim_approval), reference(spec_review), reference(originality)])
    uniqueness = decide(ops, project_id, "apr-uniqueness", "answer_uniqueness_approval", question, "uniqueness-reviewer", [content["canonical_digest"], question["canonical_digest"]], [reference(content)])
    report = ops.validate_project({
        "project_id": project_id, "as_of": "2030-01-03", "workspace_commit": COMMIT,
        "validation_id": "val-workspace", "executed_at": "2030-01-03T00:00:00Z", "persist": True,
    })
    if report["result"] != "passed":
        raise AssertionError(report["findings"])
    approvals = [source_pool_approval, source_errata_approval, claim_approval, content, uniqueness]
    reviews = [lesson_review, spec_review, originality]
    selection = {
        "schema_version": "ala.authoring.selection.v1",
        "selection_id": "selection-synthetic",
        "project": reference(project),
        "assessment_blueprint": project["pilot_scope"]["assessment_blueprint"],
        "learning_architecture": project["pilot_scope"]["learning_architecture"],
        "realization_plan": project["pilot_scope"]["realization_plan"],
        "source_references": [reference(source_pool), reference(source_errata)],
        "claim_references": [reference(claim)],
        "lesson_references": [reference(lesson)],
        "question_specification_references": [reference(spec)],
        "question_references": [reference(question)],
        "approval_references": [reference(item) for item in approvals],
        "review_references": [reference(item) for item in reviews],
        "validation_report_references": [reference(report)],
        "source_projections": [
            {"source_reference": reference(source_pool), "pack_source_id": "source-pool", "pack_source_type": "official_question_pool", "rights_id": "reference-rights"},
            {"source_reference": reference(source_errata), "pack_source_id": "source-errata", "pack_source_type": "official_errata", "rights_id": "reference-rights"},
        ],
        "lesson_projections": [{"lesson_reference": reference(lesson), "title": "Synthetic lesson", "path": "lessons/synthetic.md", "rights_id": "original-rights"}],
        "question_projections": [{"question_reference": reference(question), "tags": ["synthetic"], "question_rights_id": "original-rights", "explanation_rights_id": "original-rights"}],
        "pack": {
            "pack_id": "synthetic-authored-pack", "version": "0.3b-test", "title": "Synthetic authored pack",
            "language": "en-US", "tags": ["synthetic"],
            "objectives": [{"id": "obj-one", "title": "Synthetic objective"}],
            "assessment_pool": {
                "id": "synthetic-assessment", "title": "Synthetic assessment", "publisher": "Synthetic Publisher",
                "effective_from": "2030-01-01", "effective_through": "2030-12-31",
                "source_id": "source-pool", "errata_revision": "test-revision-1",
                "errata_source_id": "source-errata", "withdrawn_official_question_ids": [],
            },
            "rights": [
                {"id": "original-rights", "scope": "original_lessons_questions_explanations", "status": "licensed", "license_expression": "CC-BY-4.0", "copyright_holder": "Synthetic contributors"},
                {"id": "reference-rights", "scope": "external_references", "status": "reference_only"},
            ],
            "notice_markdown": "Synthetic test data only.\n",
        },
        "target_pack_format": "0.2",
        "compilation_timestamp": "2030-01-04T00:00:00Z",
        "source_workspace_commit": COMMIT,
        "requires_structured_option_teaching": False,
    }
    ops.store_selection({"project_id": project_id, "selection": selection})
    return {
        "ops": ops, "project_id": project_id, "workspace": root / "authoring" / project_id,
        "project": project, "sources": [source_pool, source_errata], "claim": claim, "lesson": lesson,
        "spec": spec, "question": question, "approvals": approvals, "reviews": reviews,
        "report": report, "selection": selection,
    }
