# AWS SAP-C02 0.3B Design Acceptance

Status: accepted documentation baseline; implementation and authored content remain unauthorized
Acceptance date: 2026-07-18

## Decision

The 0.3B authored-content architecture and implementation contract are accepted. ADRs 0017–0020 are Accepted. This closes the documentation design gate only; it creates no AWS source record, claim, lesson, question, pack, tool, core behavior, SQLite change, Hermes/MCP change, AWS-account action, release, or tag.

## Accepted contract

- The Git-versioned workspace is fixed at `authoring/aws-sap-c02-org-04/` with separate source, claim, lesson, question-specification, final-question, validation, approval, and release areas.
- SQLite remains learner-state only. Drafts, internal reviews, and authoring evidence do not ship in installed packs.
- Stable record IDs are independent of filenames. Exact schema version, artifact type, revision, canonical digest, timestamps, author/provenance, supersession, and status are recorded.
- JSON and lesson Markdown canonicalization is deterministic, UTF-8/NFC/LF based, path portable, array-order preserving, and domain-separated by artifact type.
- Source, claim, lesson, question-specification, final-question, approval/review, validation-report, release-candidate, and release-evidence records have closed versioned schemas.
- Source, claim, question-content, answer-uniqueness, and pack-release approvals are distinct immutable human decisions. Validation never grants approval. Historical decisions are preserved and never retargeted to changed bytes.
- Artifact authors cannot approve their artifacts. A material question author/re-writer cannot approve answer uniqueness. Final release review confirms all prerequisites.
- The exact invalidation matrix is fail-closed. Any learner-facing byte or release dependency change invalidates pack-release approval.
- Compilation accepts a closed project/selection, verifies exact dependencies, produces deterministic output, projects only approved learner-facing fields, and emits external release evidence. It never installs, activates, publishes, commits, tags, or releases.
- Existing pack format 0.2 is the default projection. Unchanged format 0.3 is allowed only after the material-static-PNG gate passes. The first pilot creates no format 0.4.
- The existing explanation field may contain concise learner-safe discussion of major wrong alternatives. If adequate teaching requires structured per-option output, implementation stops and proposes explicit format 0.4 instead of overloading fields.
- Multiple-response selection count is explicit, keyed count matches it, every correct selection is required, and existing exact-set/no-partial-credit behavior remains unchanged.
- `SAP-ORG-04` remains text-only by default. A diagram must be objective-material, validity-relevant, non-decorative, authoritative, rights-cleared, accessible, non-leaking, and representable by the existing format-0.3 PNG process.
- Proposed authoring operations have closed ID/path/request boundaries, no shell or unrestricted filesystem/network, and remain separate from the ten learner-study operations.

## Normative documents

- [ADRs 0017–0020](../decisions/0017-authored-content-workspace-release-projection.md)
- [Authored-content model](../aws/sap-c02-0.3b-authored-content-model.md)
- [Authoring schemas](../aws/sap-c02-0.3b-schemas.md)
- [Approval and invalidation model](../aws/sap-c02-0.3b-approval-model.md)
- [Authoring workspace](../aws/sap-c02-0.3b-authoring-workspace.md)
- [Validation plan](../aws/sap-c02-0.3b-validation-plan.md)
- [Human-review plan](../aws/sap-c02-0.3b-human-review-plan.md)
- [Compiler contract](../aws/sap-c02-0.3b-compiler-contract.md)
- [Release-evidence contract](../aws/sap-c02-0.3b-release-evidence.md)
- [Final design handoff](aws-sap-c02-0.3b-final-design.md)

## Deliberately unresolved implementation details

These choices may be made only in a separately authorized implementation task and must remain within the accepted contracts:

- Python package/module and CLI wiring for the future authoring operations;
- whether closed schemas are enforced through hand-written standard-library validation, generated JSON Schema artifacts, or a small dependency;
- atomic-write/locking mechanics and error-message presentation on supported platforms;
- the concrete compiler build-identity source and reproducibility harness;
- reviewer assignments, identities, qualifications, and review scheduling;
- authorized source-retrieval procedure and any separately managed non-Git research cache;
- exact pilot pack version and separately authorized installation/release workflow.

No unresolved item permits schema weakening, approval inference, author self-approval, new pack fields, format 0.4, authoring SQLite tables, or automatic publication.

## Next gate

A later task may implement the empty workspace machinery, schemas, validators, and compiler contract without authoring AWS content only if explicitly authorized. A different later task may create pilot content and conduct human reviews. Compilation, installation, activation, and release each remain explicit gates and are not implied by this acceptance.
