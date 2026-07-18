# Runtime-Independent Core Implementation 0.1 Handoff

Date: 2026-07-18
Status: Core implementation complete; Hermes integration not implemented

## Implemented modules

- `pack_model.py`: immutable objective, option, question, and pack records.
- `pack_validation.py`: strict format-0.1 parsing, unknown-field rejection, cross-reference checks, UTF-8 handling, and confined lesson paths.
- `pack_digest.py`: NFC normalization, canonical JSON, normalized Markdown, pack SHA-256, and question SHA-256.
- `schema.py`: schema version 1 and exactly the eight accepted tables.
- `storage.py`: normalized local paths, schema initialization, foreign keys on every connection, and explicit read/write transaction boundaries.
- `time_and_ids.py`: injectable opaque IDs and monotonically ordered RFC 3339 UTC timestamps.
- `application_service.py`: deterministic pack, learner, session, scoring, progress, challenge, retry, and restart operations.
- `tool_contract.py`: strict contract-0.1 request dispatch and JSON-compatible success/error envelopes.
- `errors.py`: public-safe typed errors.

The core imports no Hermes, MCP, model-provider, or network package.

## Database schema

Schema version `1` creates exactly:

1. `schema_meta`
2. `learners`
3. `installed_packs`
4. `study_sessions`
5. `presentations`
6. `attempts`
7. `objective_progress`
8. `question_challenges`

Foreign keys are enabled for every connection. Mutations use `BEGIN IMMEDIATE`. There is no generic idempotency table, audit table, scheduling state, event stream, or backup metadata. The application service exposes no attempt update or delete operation.

## Fixture pack

The manually authored synthetic fixture is in `packs/fixture-basics/`:

- `pack.json`
- `lesson.md`

It contains exactly two objectives, one lesson, three single-response questions, two multiple-response questions, and explanations for every answer. It contains no certification, AWS, Amateur Radio, or copied course content.

## Tool operations

All ten runtime-neutral operations are implemented:

- `system.health`
- `learner.initialize`
- `pack.validate`
- `pack.install`
- `study.start`
- `study.next`
- `study.submit`
- `study.status`
- `study.finish`
- `question.challenge`

Mutations use operation-specific uniqueness and payload comparison. Exact submission retries reconstruct the original progress snapshot from immutable attempts and their monotonically persisted submission timestamps; no result cache was added.

## Test results

Command run:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

Result on 2026-07-18 with Python 3.14.3: **25 tests passed**. Python 3.12 was not installed in the working environment, so the declared minimum was reviewed for compatible syntax but not separately executed here.

The suite covers AT-01 through AT-12 and the requested additional cases: lesson traversal, unknown fields, pack-version conflict, changed question digest, one-option multiple response, challenged completion, a new session after completion, JSON serialization, and absence of runtime/network provider imports. Tests use temporary directories and never write to the repository's `user-data/` directory.

Coverage percentage was not measured because no coverage dependency was installed or added.

## Manual core exercise

From the repository root, set the source path and run this example. It uses a temporary user-data directory and leaves no learner state in the repository.

```powershell
$env:PYTHONPATH='src'
@'
from pathlib import Path
from tempfile import TemporaryDirectory
from adaptive_learning.application_service import ApplicationService
from adaptive_learning.tool_contract import ToolContract

with TemporaryDirectory() as data:
    tools = ToolContract(ApplicationService(data))
    pack = tools.invoke("pack.install", {"source_path": str(Path("packs/fixture-basics").resolve())})["result"]
    learner = tools.invoke("learner.initialize", {"display_name": "Alex"})["result"]
    session = tools.invoke("study.start", {
        "learner_id": learner["learner_id"],
        "pack_id": pack["pack_id"],
        "pack_version": pack["pack_version"],
    })["result"]
    question = tools.invoke("study.next", {"session_id": session["session_id"]})
    print(question)
'@ | python -
```

## Deviations and clarifications

- The governing document was clarified before implementation: completed sessions do not block a new session; an unanswered challenged presentation is resolved for finish; an empty multiple-response selection is invalid while one valid option is scoreable.
- The task explicitly excluded Hermes work, so the governing definition of done now distinguishes core completion from later runtime compatibility.
- No standalone CLI was added. The runtime-neutral boundary is the Python `ToolContract`, which is sufficient for the requested core and tests.

No accepted ADR was altered.

## Unresolved issues

- The Hermes plugin and workflow skill are not implemented.
- Hermes v0.18.2 installation, discovery, enablement, restart, and contract conformance remain unverified.
- The package has not been published or released.
- All features listed as deferred in `docs/mvp-vertical-slice.md` remain unimplemented.

## Scope confirmation

No Hermes code, functional skill, MCP adapter, pilot pack, YAML/ZIP support, authoring workflow, evidence workflow, mastery/scheduler, LLM/network call, UI, API server, extra database table, or generic idempotency/audit framework was implemented.
