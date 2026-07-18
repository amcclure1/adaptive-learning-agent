# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use semantic versioning once releases begin.

## [Unreleased]

### Added

- Initial open-source repository governance and project context.
- Preserved initial design package covering vision, requirements, architecture, evidence, pack format, Hermes integration, SQLite, tool contracts, and testing.
- Runtime-independent Python 3.12 learning core with no runtime dependencies.
- Strict JSON-plus-Markdown pack parsing, validation, canonical digests, and controlled local installation.
- SQLite schema version 1 with the eight approved operational tables.
- Ten JSON-compatible version-0.1 tool operations for learner, pack, study, and challenge workflows.
- Synthetic `fixture-basics` pack and automated AT-01 through AT-12 core coverage.
- Minimal GitHub Actions test matrix for Python 3.12, 3.13, and 3.14.
- Thin project-local Hermes v0.18.2 adapter registering exactly ten `ala_*` tools.
- Explicitly loaded `adaptive-learning` workflow skill for the fixture study flow.
- Hermes v0.18.2 compatibility record, direct adapter coverage, restart/resume acceptance evidence, and integration handoff.

### Fixed

- Removed a redundant legacy license classifier that prevented installed-package builds with modern setuptools.
