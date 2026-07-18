# ChatGPT Review Bundle

Prepared: 2026-07-18

## 1. Repository identity

- Final local repository name: `adaptive-learning-agent`
- Default branch: `main`
- Visibility target: public
- Description: `A lightweight, local-first, agent-native adaptive learning system with portable subject packs and evidence-aware assessment.`
- Remote URL: not created; GitHub CLI is not installed, so authentication and name availability could not be checked safely.

After installing GitHub CLI, the user can run:

```powershell
gh auth login
gh repo create adaptive-learning-agent --public --description "A lightweight, local-first, agent-native adaptive learning system with portable subject packs and evidence-aware assessment." --source . --remote origin --push
```

If GitHub reports that the name is unavailable in the authenticated account, choose the smallest reasonable variation, substitute it in the second command, and record the final name/URL in `docs/current-status.md`.

## 2. Commit snapshot

Repository content summarized before adding this review bundle:

```text
98ec8c13996b39ad1262b3c0778295fd003155f6
```

This file is necessarily added by a later handoff commit, so it cannot contain the hash of the commit that contains itself. Use `git rev-parse HEAD` for the post-bundle commit. The final task response records that resulting hash.

## 3. Repository tree

```text
adaptive-learning-agent/
├── .editorconfig
├── .gitattributes
├── .gitignore
├── AGENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── pyproject.toml
├── docs/
│   ├── architecture.md
│   ├── current-status.md
│   ├── evidence-policy.md
│   ├── hermes-integration.md
│   ├── mvp-requirements.md
│   ├── pack-format.md
│   ├── product-principles.md
│   ├── project-context.md
│   ├── repository-tree.md
│   ├── sqlite-schema.md
│   ├── test-plan.md
│   ├── tool-contract.md
│   ├── vision.md
│   ├── decisions/0001..0006
│   └── handoffs/
├── packs/{template,aws-sap-c02,us-amateur-extra}/
├── schemas/
├── skills/{adaptive-learning,subject-builder,content-reviewer}/
├── src/adaptive_learning/__init__.py
├── tests/
└── user-data/.gitignore
```

## 4. Original design documents

All 11 original documents are preserved:

1. `docs/vision.md`
2. `docs/mvp-requirements.md`
3. `docs/architecture.md`
4. `docs/evidence-policy.md`
5. `docs/pack-format.md`
6. `docs/hermes-integration.md`
7. `docs/decisions/0001-lightweight-local-first.md`
8. `docs/repository-tree.md`
9. `docs/sqlite-schema.md`
10. `docs/tool-contract.md`
11. `docs/test-plan.md`

The only directional edit to an original document during repository establishment was changing ADR 0001 from Proposed to Accepted and aligning its alternatives heading with the repository ADR template. Its substantive design was preserved.

## 5. Architecture summary

Accepted direction:

- The agent harness is the application.
- Hermes is first, but the core is runtime-independent.
- Deterministic Python owns scoring, selection, scheduling, validation, and state mutation.
- SQLite owns local operational learner state.
- YAML/JSON/Markdown files own portable pack content.
- Agent memory is non-authoritative.
- Human action controls content activation.
- No heavy learning platform or service infrastructure is an MVP dependency.

Still proposed: exact module layout, scoring/mastery/scheduling formulas, archive canonicalization, full schema DDL, and concrete adapter packaging.

## 6. SQLite proposal

The proposed schema includes learner profiles, installed-pack receipts, authoring projects, pinned study sessions, committed question presentations, immutable attempts, objective deltas, objective/item progress projections, idempotency results, audit events, and schema metadata. A submit operation is proposed as one atomic transaction. Pack content stays in files, and progress can be rebuilt from attempts.

## 7. Tool-contract proposal

The proposed `ala.tools.v1` contract uses common JSON request/success/error envelopes, stable error codes, and idempotency keys for mutations. Proposed tools cover system/learner management, SQLite-safe backup/restore, pack validation/install/export, draft authoring and explicit human review, and study start/next/submit/status/finish. `study.next` hides answer keys; `study.submit` derives scores and explanations from the pinned pack and deterministic rules.

## 8. Hermes integration summary

Use a thin, opt-in Hermes plugin that registers namespaced tools and delegates to the runtime-neutral core. An optional skill provides workflow guidance only. Hermes owns provider selection and Codex OAuth; Adaptive Learning Agent must never read or store those credentials. MCP is deferred as an optional future adapter.

Official Hermes documentation was inspected for installation, skills, MCP, local tools/plugins, providers, and Codex OAuth. Exact project plugin installation/discovery/restart behavior remains unverified and must be tested against a selected tagged Hermes release.

## 9. Accepted ADRs

- ADR 0001: Lightweight, Local-First Architecture.
- ADR 0002: Agent Harness as the Application.
- ADR 0003: Hermes First, Runtime-Independent Core.
- ADR 0004: SQLite for Operational Learner State.
- ADR 0005: File-Based Portable Subject Packs.
- ADR 0006: No Heavy Learning-Platform Dependency for the MVP.

## 10. Proposed ADRs

No uncertain choice was turned into a Proposed ADR during establishment. Detailed algorithms and contracts remain explicitly proposed in their design documents. After review, accepted or disputed portions should be captured in focused ADRs rather than promoting entire design documents wholesale.

## 11. Unresolved decisions

- GitHub owner, remote URL, name availability, and permanent security contact.
- Final project/package name.
- YAML parser selection.
- Exact scoring, mastery, scheduling, and selection rules.
- Pack schema/canonicalization/signing and pack-content licensing.
- SQLite DDL, migrations, data paths, and concurrency settings.
- Final JSON tool schemas and human-confirmation enforcement.
- Hermes supported versions, plugin distribution, profile behavior, and optional MCP adapter.
- Reviewer identity beyond local attestation.

## 12. Dependencies present

- Required Python: 3.12 or newer.
- Runtime dependencies: none.
- Build backend: `setuptools.build_meta`, with `setuptools>=77` as the isolated build requirement.
- Development dependencies: none declared.
- No framework, agent SDK, database service/client, vector library, UI dependency, or YAML parser is present.

## 13. Validation performed

- Parsed `pyproject.toml` with Python `tomllib`.
- Imported `adaptive_learning` from `src` and verified version `0.0.0`.
- Checked all Markdown code fences and repository-relative links.
- Ran a focused secret-pattern scan; no credential-like material was found.
- Validated the proposed SQL DDL against in-memory standard-library SQLite; schema creation and foreign-key checks passed.
- Checked staged file lists and `git diff --cached --check` for each new commit. Existing original Markdown hard-break whitespace was preserved intentionally.
- Confirmed the 11 original documents remain present.
- Confirmed no runtime dependencies or learning-engine modules were added.

## 14. Failures and incomplete steps

- GitHub repository creation and push were not completed because `gh` is not installed.
- Repository-name availability was not checked because no authenticated GitHub account was available through `gh`.
- External web links were reviewed where practical but not exhaustively crawled.
- No YAML files exist yet, so there was no YAML syntax to validate.
- Hermes integration behavior was documented but not executed or configured.

## 15. Recommended next Codex task

Run a design-review task only: compare product principles against the proposed requirements, pack/evidence formats, SQLite schema, and tool contract; record accepted decisions and requested revisions; update `docs/current-status.md`. Do not implement the engine in that task.

## 16. Implementation confirmation

No learning engine, database migration, pack validator, runtime adapter, functional skill, schema, or pilot question was implemented. `src/adaptive_learning/__init__.py` is a behavior-free package boundary containing only documentation and version metadata.
