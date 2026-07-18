# Proposed SQLite Schema

Status: proposed schema version 1  
Design baseline: 2026-07-18

## Scope

SQLite stores operational learner state, installation receipts, idempotency results, and audit facts. Pack YAML/Markdown remains canonical for content, answer keys, sources, and reviews. The schema intentionally does not store Hermes sessions, model memory, OAuth credentials, embeddings, or a content marketplace.

IDs are application-generated UUID strings. Times are RFC 3339 UTC text. Fixed-point scores use integer millionths. JSON columns contain canonical JSON text validated by the application; SQLite JSON functions are not required.

## Connection rules

Every connection enables foreign keys and a busy timeout. Normal local operation should evaluate WAL mode, but the data directory should not default to a cloud-synchronized folder. Mutations use `BEGIN IMMEDIATE` and commit the attempt, progress projections, idempotency result, and audit event in one transaction. Backups use `sqlite3.Connection.backup` or the SQLite online-backup API.

## DDL

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO schema_meta (key, value) VALUES ('schema_version', '1');

CREATE TABLE learners (
    learner_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) BETWEEN 1 AND 120),
    timezone TEXT NOT NULL DEFAULT 'UTC',
    locale TEXT NOT NULL DEFAULT 'en-US',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    archived_at TEXT
);

CREATE TABLE installed_packs (
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    pack_digest TEXT NOT NULL CHECK (length(pack_digest) = 64),
    format_version TEXT NOT NULL,
    title TEXT NOT NULL,
    install_path TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('installed', 'unavailable', 'quarantined')),
    evidence_mode TEXT NOT NULL CHECK (evidence_mode IN ('none', 'recommended', 'required')),
    installed_at TEXT NOT NULL,
    last_verified_at TEXT NOT NULL,
    PRIMARY KEY (pack_id, pack_version),
    UNIQUE (pack_id, pack_version, pack_digest),
    UNIQUE (pack_digest)
);

CREATE TABLE authoring_projects (
    draft_id TEXT PRIMARY KEY,
    pack_id TEXT NOT NULL,
    proposed_version TEXT NOT NULL,
    draft_path TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('draft', 'review', 'release_ready', 'closed')),
    current_digest TEXT,
    validation_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE study_sessions (
    session_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    pack_digest TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'abandoned')),
    selection_rule_version TEXT NOT NULL,
    scoring_rule_version TEXT NOT NULL,
    mastery_rule_version TEXT NOT NULL,
    scheduling_rule_version TEXT NOT NULL,
    seed TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    last_activity_at TEXT NOT NULL,
    UNIQUE (session_id, learner_id, pack_id, pack_version),
    FOREIGN KEY (pack_id, pack_version, pack_digest)
        REFERENCES installed_packs(pack_id, pack_version, pack_digest),
    CHECK ((status = 'active' AND ended_at IS NULL) OR
           (status IN ('completed', 'abandoned') AND ended_at IS NOT NULL))
);

CREATE TABLE presentations (
    presentation_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES study_sessions(session_id),
    ordinal INTEGER NOT NULL CHECK (ordinal > 0),
    question_id TEXT NOT NULL,
    question_digest TEXT NOT NULL CHECK (length(question_digest) = 64),
    selection_reason_json TEXT NOT NULL,
    presented_at TEXT NOT NULL,
    answered_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('presented', 'answered', 'skipped', 'invalidated')),
    UNIQUE (session_id, ordinal),
    UNIQUE (presentation_id, session_id),
    UNIQUE (presentation_id, session_id, question_id, question_digest),
    CHECK ((status = 'answered' AND answered_at IS NOT NULL) OR
           (status <> 'answered' AND answered_at IS NULL))
);

CREATE TABLE attempts (
    attempt_id TEXT PRIMARY KEY,
    presentation_id TEXT NOT NULL UNIQUE,
    session_id TEXT NOT NULL,
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    question_id TEXT NOT NULL,
    question_digest TEXT NOT NULL CHECK (length(question_digest) = 64),
    submitted_response_json TEXT NOT NULL,
    normalized_response_json TEXT NOT NULL,
    score_micros INTEGER NOT NULL CHECK (score_micros BETWEEN 0 AND 1000000),
    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),
    confidence INTEGER CHECK (confidence BETWEEN 1 AND 5),
    scoring_rule_version TEXT NOT NULL,
    mastery_rule_version TEXT NOT NULL,
    scheduling_rule_version TEXT NOT NULL,
    answered_at TEXT NOT NULL,
    duration_ms INTEGER CHECK (duration_ms IS NULL OR duration_ms >= 0),
    FOREIGN KEY (presentation_id, session_id, question_id, question_digest)
        REFERENCES presentations(presentation_id, session_id, question_id, question_digest),
    FOREIGN KEY (session_id, learner_id, pack_id, pack_version)
        REFERENCES study_sessions(session_id, learner_id, pack_id, pack_version),
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version),
    CHECK ((score_micros = 1000000 AND is_correct = 1) OR
           (score_micros < 1000000 AND is_correct = 0))
);

CREATE TABLE attempt_objectives (
    attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id) ON DELETE CASCADE,
    objective_id TEXT NOT NULL,
    weight_micros INTEGER NOT NULL CHECK (weight_micros BETWEEN 1 AND 1000000),
    mastery_before_micros INTEGER NOT NULL CHECK (mastery_before_micros BETWEEN 0 AND 1000000),
    mastery_after_micros INTEGER NOT NULL CHECK (mastery_after_micros BETWEEN 0 AND 1000000),
    PRIMARY KEY (attempt_id, objective_id)
);

CREATE TABLE objective_progress (
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    objective_id TEXT NOT NULL,
    mastery_micros INTEGER NOT NULL CHECK (mastery_micros BETWEEN 0 AND 1000000),
    evidence_count INTEGER NOT NULL CHECK (evidence_count >= 0),
    weighted_score_total_micros INTEGER NOT NULL CHECK (weighted_score_total_micros >= 0),
    weighted_opportunity_total_micros INTEGER NOT NULL CHECK (weighted_opportunity_total_micros >= 0),
    last_attempt_id TEXT REFERENCES attempts(attempt_id),
    last_practiced_at TEXT,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, pack_id, pack_version, objective_id),
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version)
);

CREATE TABLE item_progress (
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    question_id TEXT NOT NULL,
    question_digest TEXT NOT NULL CHECK (length(question_digest) = 64),
    leitner_box INTEGER NOT NULL CHECK (leitner_box BETWEEN 0 AND 5),
    exposure_count INTEGER NOT NULL CHECK (exposure_count >= 0),
    correct_count INTEGER NOT NULL CHECK (correct_count BETWEEN 0 AND exposure_count),
    last_score_micros INTEGER CHECK (last_score_micros BETWEEN 0 AND 1000000),
    last_confidence INTEGER CHECK (last_confidence BETWEEN 1 AND 5),
    last_attempt_id TEXT REFERENCES attempts(attempt_id),
    last_seen_at TEXT,
    due_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, pack_id, pack_version, question_id),
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version)
);

CREATE TABLE idempotency_results (
    scope TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    request_sha256 TEXT NOT NULL CHECK (length(request_sha256) = 64),
    response_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT,
    PRIMARY KEY (scope, idempotency_key)
);

CREATE TABLE audit_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    learner_id TEXT REFERENCES learners(learner_id),
    session_id TEXT REFERENCES study_sessions(session_id),
    details_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_sessions_learner_status
    ON study_sessions (learner_id, status, last_activity_at);
CREATE INDEX idx_presentations_session_status
    ON presentations (session_id, status, ordinal);
CREATE INDEX idx_attempts_learner_pack_time
    ON attempts (learner_id, pack_id, pack_version, answered_at);
CREATE INDEX idx_objective_progress_priority
    ON objective_progress (learner_id, pack_id, pack_version, mastery_micros);
CREATE INDEX idx_item_progress_due
    ON item_progress (learner_id, pack_id, pack_version, due_at);
CREATE INDEX idx_audit_entity
    ON audit_events (entity_type, entity_id, occurred_at);
```

## Transaction invariants

- `study.next` inserts one `presentations` row and advances no learner progress.
- `study.submit` verifies one outstanding presentation, inserts one attempt, inserts its objective deltas, upserts objective/item progress, marks the presentation answered, stores the idempotent response, and appends an audit event in one transaction.
- A duplicate `(scope, idempotency_key)` with the same request hash returns `response_json`; a different request hash returns `IDEMPOTENCY_CONFLICT`.
- Installed pack rows are not deleted while referenced. A pack can become `unavailable`, but history remains.
- Pack content is never cascaded through learner history because it is not stored as relational content.
- Derived progress is a projection. A repair command may rebuild it from ordered attempts and must compare the result before replacement.

## Migration and backup

- A migration checks `schema_meta.schema_version`, creates a SQLite-safe backup, runs once in an exclusive transaction, verifies foreign keys and integrity, then updates the version.
- Downgrade is not automatic. A user restores the pre-migration backup with the earlier application version.
- Backup metadata records application version, schema version, timestamp, and SHA-256 outside the database.
- Restore stages into a new file, runs `PRAGMA integrity_check` and `PRAGMA foreign_key_check`, then atomically swaps files while the application is closed.

## Deliberate omissions

- No users, passwords, roles, tenants, or remote sessions.
- No pack question/answer tables; pack files remain canonical.
- No vector or full-text index in MVP.
- No chat transcript or agent memory tables.
- No evidence approval table; release reviews travel with the pack. `authoring_projects` is only local workflow metadata.
