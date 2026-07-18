"""SQLite schema version 1 for the version-0.1 core."""

SCHEMA_VERSION = "1"
APPROVED_TABLES = frozenset(
    {
        "schema_meta",
        "learners",
        "installed_packs",
        "study_sessions",
        "presentations",
        "attempts",
        "objective_progress",
        "question_challenges",
    }
)

SCHEMA_SQL = """
BEGIN IMMEDIATE;

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS learners (
    learner_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) > 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS installed_packs (
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    pack_digest TEXT NOT NULL CHECK (length(pack_digest) = 64),
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    install_path TEXT NOT NULL CHECK (length(trim(install_path)) > 0),
    installed_at TEXT NOT NULL,
    PRIMARY KEY (pack_id, pack_version)
);

CREATE TABLE IF NOT EXISTS study_sessions (
    session_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'completed')),
    started_at TEXT NOT NULL,
    finished_at TEXT,
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version)
);

CREATE UNIQUE INDEX IF NOT EXISTS one_active_session_per_learner
ON study_sessions(learner_id) WHERE status = 'active';

CREATE TABLE IF NOT EXISTS presentations (
    presentation_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES study_sessions(session_id),
    ordinal INTEGER NOT NULL CHECK (ordinal > 0),
    question_id TEXT NOT NULL,
    question_digest TEXT NOT NULL CHECK (length(question_digest) = 64),
    status TEXT NOT NULL CHECK (status IN ('presented', 'answered', 'challenged')),
    presented_at TEXT NOT NULL,
    UNIQUE (session_id, ordinal),
    UNIQUE (session_id, question_id)
);

CREATE TABLE IF NOT EXISTS attempts (
    attempt_id TEXT PRIMARY KEY,
    presentation_id TEXT NOT NULL UNIQUE REFERENCES presentations(presentation_id),
    selected_option_ids_json TEXT NOT NULL CHECK (json_valid(selected_option_ids_json)),
    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),
    confidence INTEGER NOT NULL CHECK (confidence BETWEEN 1 AND 5),
    submitted_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS objective_progress (
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    objective_id TEXT NOT NULL,
    attempts_count INTEGER NOT NULL CHECK (attempts_count >= 0),
    correct_count INTEGER NOT NULL CHECK (correct_count BETWEEN 0 AND attempts_count),
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, pack_id, pack_version, objective_id),
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version)
);

CREATE TABLE IF NOT EXISTS question_challenges (
    challenge_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL REFERENCES learners(learner_id),
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    question_id TEXT NOT NULL,
    presentation_id TEXT NOT NULL REFERENCES presentations(presentation_id),
    reason TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    challenged_at TEXT NOT NULL,
    UNIQUE (learner_id, pack_id, pack_version, question_id),
    FOREIGN KEY (pack_id, pack_version)
        REFERENCES installed_packs(pack_id, pack_version)
);

INSERT INTO schema_meta(key, value) VALUES ('schema_version', '1')
ON CONFLICT(key) DO NOTHING;

COMMIT;
"""
