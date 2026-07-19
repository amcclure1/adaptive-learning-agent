# SAP-C02 0.3B Release-Evidence Contract

Status: accepted contract; generic candidate/final evidence generation implemented; no AWS manifest or pack created

This document fixes the evidence that connects an authored-content workspace to a compiled learner-facing candidate. It is governed by ADRs 0017–0020, uses the canonicalization rules in [the schema contract](sap-c02-0.3b-schemas.md), and is produced only through [the compiler contract](sap-c02-0.3b-compiler-contract.md).

## Location and publication boundary

Release evidence is committed under `authoring/<project-id>/release/evidence/`. It is publishable audit evidence but is not installed in the learner pack. It contains stable reviewer identities and qualification summaries only where necessary; contact details, credentials, private notes, licensed source copies, and internal personnel information are prohibited.

## Two-phase evidence model

A pack-release approval cannot be included in the evidence it reviews without creating a digest cycle. The contract therefore has two immutable phases:

1. `authoring.release.compile_candidate` produces the candidate pack and a candidate manifest. The candidate manifest binds every compiler input, validation result, projected output, and the candidate pack digest; its `release_review_approval` is `null`.
2. A human reviews the exact candidate and candidate manifest, then creates an immutable pack-release approval targeting both digests.
3. `authoring.release.finalize_evidence` verifies that approval and creates a final manifest that binds the unchanged candidate manifest, candidate pack digest, and pack-release approval digest.

Neither manifest is edited in place. Finalization does not recompile, install, activate, publish, commit, tag, or release anything.

## Manifest schema

Both manifests use `schema_version: "ala.release-evidence/1"`, the common identity envelope, and these fields:

| Field | Rule |
| --- | --- |
| `phase` | `candidate` or `final` |
| `project` | Exact project ID, revision, and digest |
| `compiler_version` | Exact compiler contract/implementation version |
| `source_workspace_commit` | Full Git commit ID; the tree must be clean at compilation |
| `assessment_blueprint` | Version, path, and canonical file digest |
| `learning_architecture` | Version, path, and canonical file digest |
| `realization_plan` | Version, path, and canonical file digest |
| `source_records` | Sorted references to exact source IDs, revisions, and digests |
| `approved_claims` | Sorted references to exact approved claim revisions/digests |
| `lessons` | Sorted references to exact lesson record/content digests |
| `question_specifications` | Sorted references to exact specification revisions/digests |
| `approved_final_questions` | Sorted references to exact question revisions/digests |
| `approval_records` | Sorted references to all authority-bearing approval and required review-record digests |
| `validation_reports` | Sorted report IDs/digests, validator versions, and source workspace commit |
| `compiled_pack` | Pack ID, version, target format, relative output path, and compiled digest |
| `compilation_timestamp` | Explicit UTC timestamp supplied to the compiler; not ambient clock input |
| `compiler_input_digest` | Digest of the closed, ordered compiler-input manifest |
| `compiler_output_digest` | Digest of the emitted candidate byte set, including path and length framing |
| `candidate_manifest` | `null` in candidate phase; exact ID/revision/digest in final phase |
| `release_review_approval` | `null` in candidate phase; exact pack-release approval ID/revision/digest in final phase |
| `exclusions` | Fixed declaration of authoring-only classes omitted from the installed pack |

Collections are ordered by artifact type, artifact ID, revision, then digest. They are sets for eligibility purposes: duplicates are invalid. Paths are workspace-relative POSIX paths. Every referenced digest is recomputed before emission.

The final manifest's `compiled_pack`, compiler input/output digests, and source workspace commit must exactly equal the candidate manifest. Any difference requires a new compilation, candidate manifest, human release review, and final manifest.

## Compiler input and output digests

The compiler input digest uses the schema contract's domain-separated JSON digest with artifact type `compiler_input_manifest`. It binds the compile request, project, fixed design documents, every selected record and approval digest, every selected validation-report digest, compiler version, target format, output identity, and explicit timestamp.

The compiler output digest uses domain marker `ala-authored-content\0compiler_output\0v1`. For each emitted relative path sorted by UTF-8 byte order, it frames the path byte length, path bytes, content byte length, and content bytes. The compiled-pack digest remains the target pack format's existing required digest; the two values have different purposes and both are recorded.

## Illustrative candidate manifest

This example demonstrates shape only. Placeholder IDs and empty selection arrays are not a valid pilot release.

```json
{
  "schema_version": "ala.release-evidence/1",
  "artifact_id": "release-evidence-example-candidate",
  "artifact_type": "release_evidence",
  "revision": 1,
  "status": "immutable",
  "created_at": "2000-01-01T00:00:00Z",
  "modified_at": "2000-01-01T00:00:00Z",
  "author": {"identity": "reviewer-example", "display_name": "Example"},
  "supersedes": null,
  "canonical_digest": "<64 lowercase hex characters>",
  "phase": "candidate",
  "project": {"artifact_id": "project-example", "revision": 1, "digest": "<project digest>"},
  "compiler_version": "ala-authoring-compiler-v1",
  "source_workspace_commit": "0000000000000000000000000000000000000000",
  "assessment_blueprint": {"version": "example", "path": "docs/example.md", "digest": "<blueprint digest>"},
  "learning_architecture": {"version": "example", "path": "docs/example.md", "digest": "<architecture digest>"},
  "realization_plan": {"version": "example", "path": "docs/example.md", "digest": "<realization digest>"},
  "source_records": [],
  "approved_claims": [],
  "lessons": [],
  "question_specifications": [],
  "approved_final_questions": [],
  "approval_records": [],
  "validation_reports": [],
  "compiled_pack": {"pack_id": "pack-example", "version": "0.0.0-example", "target_format": "0.2", "relative_output_path": "release/candidates/example", "digest": "<pack digest>"},
  "compilation_timestamp": "2000-01-01T00:00:00Z",
  "compiler_input_digest": "<compiler input digest>",
  "compiler_output_digest": "<compiler output digest>",
  "candidate_manifest": null,
  "release_review_approval": null,
  "exclusions": ["claims", "internal_locators", "requirement_option_matrices", "internal_rationales", "originality_findings", "uniqueness_findings", "conflict_declarations", "private_notes", "reviewer_details"]
}
```

## Release eligibility

Candidate evidence is not approval and cannot be treated as a releasable result. Final evidence is eligible only when the pack-release approval is current, was made after all prerequisite approvals and reports, targets the exact candidate and manifest digests, and passes author/reviewer conflict rules. Historical manifests and approvals remain preserved after invalidation.
