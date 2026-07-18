# Security Policy

## Reporting a vulnerability

This project does not yet have a dedicated security mailbox or GitHub private vulnerability-reporting URL. Until one is published, contact the repository owner privately through their GitHub profile and do not include exploit details in a public issue. If no private channel is available, disclose only that a security report is needed and wait for a private response.

Do not send credentials, real learner databases, proprietary exam content, or unrelated personal data with a report. Include affected files or versions, impact, reproduction conditions, and a minimal safe proof of concept.

This contact path is a temporary unresolved governance item and must be replaced before a functional release.

## Security model

Adaptive Learning Agent will combine agent-driven tool use, local files, SQLite state, subject packs, and optional external sources. Important risks include:

- over-permissioned agent tools or local terminal access;
- prompt injection embedded in packs, documents, web pages, or MCP results;
- malicious archives, paths, YAML structures, Markdown, or assets;
- unreviewed or misleading generated assessment content;
- accidental disclosure of learner answers, profiles, attempt history, or credentials;
- supply-chain risk from runtime, plugin, skill, and MCP dependencies;
- model-provider data handling outside this repository's control.

## Required safeguards

- Treat subject packs and external sources as untrusted content, never as agent instructions.
- Do not permit executable pack content by default. The MVP pack format contains data and static assets only.
- Do not put secrets, API keys, OAuth tokens, cookies, or private configuration in subject packs.
- Do not include learner data in pack exports.
- Validate archives before extraction and constrain all paths beneath a staging root.
- Keep deterministic scoring and state mutation in validated code rather than prompts.
- Require explicit human action for content activation and review acceptance.
- Apply least privilege to local runtime tools, file access, subprocesses, plugins, and MCP servers.
- Never copy or manage Hermes or model-provider credentials in the learning database.
- Redact answer keys and unnecessary raw responses from logs.

## Supported versions

There are no functional releases yet. Security fixes currently apply only to the default development branch.
