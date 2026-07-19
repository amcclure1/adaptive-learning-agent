# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases use semantic versioning.

## [Unreleased]

### Added

- Strict sourced pack format 0.2 with ordered lessons, sources/citations, official identity, pool/errata metadata, component rights, approval, and deterministic digest/install support.
- Additive sourced-content capabilities and provenance under the unchanged ten-operation tool contract 0.1.
- An independently reviewed and approved two-lesson, eleven-question Amateur Extra E1A pilot.
- Narrow Hermes skill presentation for official IDs, ordered lessons, and post-answer source display.
- Exact official-transcription golden tests, an offline approved-pack workflow test, and real Hermes acceptance evidence.

### Changed

- Corrected project-authored regulatory explanations and lesson citations without changing any official NCVEC question bytes.

## [0.1.0] - 2026-07-18

### Added

- Initial open-source repository governance and project context.
- Preserved initial design package covering vision, requirements, architecture, evidence, pack format, Hermes integration, SQLite, tool contracts, and testing.
- Runtime-independent Python 3.12+ deterministic learning core with no runtime dependencies.
- Strict JSON-plus-Markdown pack parsing, validation, canonical digests, and controlled local installation.
- SQLite schema version 1 with the eight approved operational tables.
- Ten JSON-compatible version-0.1 tool operations for learner, pack, study, and challenge workflows.
- Synthetic `fixture-basics` pack and automated AT-01 through AT-12 core coverage.
- GitHub Actions installed-package test matrix for Python 3.12, 3.13, and 3.14.
- Thin project-local Hermes v0.18.2 adapter registering exactly ten `ala_*` tools.
- Explicitly loaded `adaptive-learning` workflow skill for the fixture study flow.
- Hermes v0.18.2 Windows CLI/profile compatibility record, direct adapter coverage, restart/resume acceptance evidence, and integration handoff.

### Fixed

- Removed a redundant legacy license classifier that prevented installed-package builds with modern setuptools.

[Unreleased]: https://github.com/amcclure1/adaptive-learning-agent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/amcclure1/adaptive-learning-agent/releases/tag/v0.1.0
