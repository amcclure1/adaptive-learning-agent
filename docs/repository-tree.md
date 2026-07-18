# Proposed Repository Tree

Status: proposed for review  
No implementation files in this tree have been created.

```text
adaptive-learning-agent/
├── README.md
├── LICENSE
├── pyproject.toml
├── CHANGELOG.md
├── SECURITY.md
├── CONTRIBUTING.md
├── docs/
│   ├── vision.md
│   ├── mvp-requirements.md
│   ├── architecture.md
│   ├── evidence-policy.md
│   ├── pack-format.md
│   ├── hermes-integration.md
│   ├── repository-tree.md
│   ├── sqlite-schema.md
│   ├── tool-contract.md
│   ├── test-plan.md
│   └── decisions/
│       └── 0001-lightweight-local-first.md
├── src/
│   └── adaptive_learning_agent/
│       ├── __init__.py
│       ├── domain/
│       │   ├── models.py
│       │   ├── scoring.py
│       │   ├── mastery.py
│       │   ├── scheduling.py
│       │   ├── selection.py
│       │   └── evidence.py
│       ├── application/
│       │   ├── learners.py
│       │   ├── study.py
│       │   ├── authoring.py
│       │   ├── packs.py
│       │   └── reporting.py
│       ├── pack_format/
│       │   ├── reader.py
│       │   ├── validator.py
│       │   ├── canonical.py
│       │   ├── archive.py
│       │   └── versions.py
│       ├── persistence/
│       │   ├── database.py
│       │   ├── repositories.py
│       │   ├── backup.py
│       │   └── migrations/
│       │       └── 0001_initial.sql
│       ├── contracts/
│       │   ├── dispatcher.py
│       │   ├── schemas.py
│       │   └── errors.py
│       └── cli.py
├── integrations/
│   └── hermes/
│       ├── plugin.yaml
│       ├── __init__.py
│       ├── schemas.py
│       └── skill/
│           └── SKILL.md
├── schemas/
│   ├── pack-v1.schema.json
│   ├── objectives-v1.schema.json
│   ├── questions-v1.schema.json
│   ├── sources-v1.schema.json
│   ├── claims-v1.schema.json
│   ├── reviews-v1.schema.json
│   └── tools-v1.schema.json
├── packs/
│   ├── aws-sap-c02/
│   │   └── README.md
│   └── us-amateur-extra/
│       └── README.md
├── examples/
│   └── minimal-pack/
├── tests/
│   ├── unit/
│   │   ├── test_scoring.py
│   │   ├── test_mastery.py
│   │   ├── test_scheduling.py
│   │   ├── test_selection.py
│   │   ├── test_evidence.py
│   │   └── test_canonicalization.py
│   ├── integration/
│   │   ├── test_database.py
│   │   ├── test_pack_lifecycle.py
│   │   ├── test_authoring_lifecycle.py
│   │   ├── test_json_contract.py
│   │   └── test_hermes_adapter.py
│   ├── e2e/
│   │   ├── test_study_journey.py
│   │   └── test_pilot_packs.py
│   └── fixtures/
│       ├── packs-valid/
│       ├── packs-invalid/
│       ├── packs-hostile/
│       └── contract-cases/
└── scripts/
    ├── validate_pack.py
    └── verify_reproducible_export.py
```

## Boundary rules

- `domain/` imports only the standard library and other domain modules.
- `application/` imports domain interfaces, never Hermes.
- `persistence/` and `pack_format/` implement infrastructure used by application services.
- `integrations/hermes/` imports the public contract/application boundary only.
- `schemas/` are distribution artifacts shared by validators and adapters; they contain no runtime-specific fields.
- `packs/` contains portable content only. Pilot content must pass the same public validator as third-party packs.
- `scripts/` are maintainer conveniences, not required daemons or alternative business logic.

## Packaging intent

One small Python distribution should contain the core, JSON CLI, format schemas, migration SQL, and Hermes adapter metadata. The YAML parser is the only expected direct runtime dependency beyond Hermes and Python. Test and formatting tools remain development extras. Exact Hermes plugin entry-point packaging is deferred until the unverified install behavior in `docs/hermes-integration.md` is tested.

