# Hermes Integration

Status: proposed for review  
Documentation inspected: 2026-07-18  
Latest verified Hermes release: v0.18.2 (released 2026-07-07)

## Accepted version 0.1 boundary

[ADR 0007](decisions/0007-hermes-plugin-skill-boundary.md) and [`mvp-vertical-slice.md`](mvp-vertical-slice.md) define the accepted split. The plugin registers and delegates the ten deterministic tools; the optional skill provides conversational workflow only. Neither owns scoring, selection, persistence, pack interpretation, provider configuration, or authentication.

Hermes v0.18.2 is the first compatibility-test target, not a current compatibility claim. Plugin discovery, enablement, tool registration, skill loading, and CLI/Desktop restart behavior remain explicitly unverified until exercised against that tagged release.

## Verified Hermes baseline

The following behavior was verified against official NousResearch Hermes Agent documentation on the `main` branch and the official release page:

- The official installer supports Linux, macOS, WSL2, native Windows, and Termux. It provisions a Hermes-managed environment and may install Python, Node.js, ripgrep, and ffmpeg. The CLI-only install supports `--skip-browser`. See [Installation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md).
- The latest release visible during review was [Hermes Agent v0.18.2](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2). Documentation on `main` may be ahead of that release.
- Skills are on-demand documents, use progressive disclosure, and primarily live in `~/.hermes/skills/`. Hermes can modify or delete locally writable skills. See [Skills System](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).
- Built-in tools are grouped into selectable toolsets. The local terminal backend is the default, and terminal/file tools include command execution and file manipulation. See [Tools & Toolsets](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tools.md).
- Custom tools for a user, team, or project are expected to use a plugin rather than modifying Hermes core. A plugin supplies `plugin.yaml` and Python registration code; `ctx.register_tool()` registers a schema and handler. General plugins are opt-in. See [Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md) and [Build a Hermes Plugin](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/build-a-hermes-plugin.md).
- Hermes supports local stdio and remote HTTP MCP servers, discovers their tools, and supports per-server tool filtering. Standard installs include MCP support. See [MCP](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md).
- `hermes model` configures providers and authentication outside a chat; `/model` switches only among already configured providers/models inside a session. See [AI Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md).
- The OpenAI Codex provider uses a device-code flow, stores Hermes-managed credentials under `~/.hermes/auth.json`, and may import existing Codex CLI credentials from `~/.codex/auth.json`. Hermes says the Codex CLI is not required. Reauthentication is `hermes auth add openai-codex` or `hermes model` then OpenAI Codex. See [AI Providers: Codex note](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md#nous-portal).

## Installation interpretation

The project's “Hermes, Python, Git, and small Python dependencies” requirement is interpreted as the Adaptive Learning Agent's direct footprint. A literal machine-level limit cannot be guaranteed because the official Hermes installer documents additional managed dependencies such as Node.js, ripgrep, and ffmpeg. Adaptive Learning Agent will not add a server, database service, JavaScript application, browser dependency, or model SDK.

Accepted version-0.1 project dependencies:

- Python 3.12 or newer, matching this repository's package metadata;
- no runtime third-party packages; version-0.1 packs use standard-library JSON and Markdown;
- no SQLite package, because `sqlite3` is in the standard library;
- development-only test tooling, not required for normal use.

No packages or Hermes configuration are changed by these design artifacts.

## Recommended MVP integration

### 1. Thin plugin

Ship a Hermes adapter plugin named `adaptive-learning` that:

- registers only the ten version-0.1 tools in `docs/mvp-vertical-slice.md`;
- groups them in an `adaptive_learning` toolset;
- converts Hermes arguments to the common request envelope;
- invokes the in-process application service;
- returns the common response envelope unchanged;
- never reads Hermes memory or provider credentials;
- never contains scoring, SQL, scheduling, or pack-policy logic.

The plugin depends inward on the installable core package. The core has no Hermes dependency. A conformance test runs the same request corpus through direct service calls, the JSON CLI, and the plugin handlers.

### 2. Workflow skill

Ship an optional `adaptive-learning` skill containing conversational guidance:

- select a learner and pack before study;
- call `study.next` rather than inventing a question;
- never reveal answer fields before submission;
- retry `study.submit` with the same selections and confidence after an uncertain response;
- quote the tool's score and reviewed rationale faithfully;
- do not imply that deferred authoring or review workflows are available;
- treat memory as preference context only.

The skill is convenience, not authority. If it is missing or changed, tool behavior and stored state remain correct.

### 3. Runtime-neutral fallback

Exercise the same contract through direct application-service calls for debugging and tests. A one-shot JSON CLI is a reasonable later adapter but is not required by the version-0.1 proof. Normal Hermes use should call registered plugin tools directly so schemas, permissions, and structured results are visible.

## Why not MCP for the MVP

Hermes MCP support is capable, but an MCP adapter would introduce a subprocess lifecycle and protocol dependency solely to call local Python. The in-process plugin is smaller and is Hermes' documented route for custom local tools. The runtime-neutral contract preserves a future stdio MCP adapter without moving core logic.

MCP remains appropriate later if multiple agent applications need live discovery of the same local service. It must remain an adapter, not the architecture's core.

## Provider and OAuth boundary

Adaptive Learning Agent is provider-agnostic. Hermes owns model choice, Codex OAuth, refresh, and provider configuration. The plugin:

- never opens OAuth flows;
- never imports `~/.codex/auth.json` or `~/.hermes/auth.json`;
- never stores access or refresh tokens in SQLite;
- never assumes the conversation uses a particular model;
- works with local or remote providers configured in Hermes;
- treats provider failure as a presentation interruption, not a reason to alter committed learning state.

Codex OAuth is therefore an installation option for Hermes, not an Adaptive Learning Agent feature or dependency.

## Tool exposure and modes

Only the ten accepted learner/pack tools are registered in version 0.1. The broader mode separation below is deferred:

- Learner-safe: pack list, learner select/status, study start/next/submit/status.
- Pack administration: validate, install, export.
- Authoring: create draft, add/update content, add sources, request status.
- Human review: record review outcome and release validation.

A future plugin may register the broader schemas with explicit authorization/mode controls. Version 0.1 must not register the deferred administration, authoring, or review operations.

## Conversation rules

1. Never generate a study question when a pack question is expected.
2. Never score from natural-language judgment; always call `study.submit`.
3. Do not pass answer keys into conversation before submission.
4. After submission, state the exact binary correctness returned by the tool.
5. Ground explanations in the returned fixture rationale.
6. Label any supplemental model explanation as unverified and do not persist it as pack content.
7. On duplicate, timeout, or provider retry, repeat the same operation-specific payload so the core can return the existing result.
8. On a typed conflict, read current session state rather than guessing.

## Installation sketch for later implementation

The intended reviewed flow is:

1. Install Hermes using an official method.
2. Install Adaptive Learning Agent into the Python environment visible to Hermes.
3. Let Hermes discover the packaged plugin entry point or install a local plugin wrapper.
4. Explicitly enable the `adaptive-learning` plugin/toolset.
5. Install the optional workflow skill.
6. Run a diagnostic tool call against a temporary learner and bundled fixture pack.

**Not yet verified:** the exact commands for installing a local editable project into every Hermes distribution method, the project plugin discovery precedence for v0.18.2, whether a packaged entry point can bundle/activate the skill without copying it, and the precise restart behavior on Desktop versus CLI. These must be tested against the target Hermes release before implementation documentation is finalized. No speculative commands are prescribed here.

## Version compatibility

- Record the tested Hermes version range in adapter metadata.
- Use only public plugin registration APIs documented by Hermes.
- Keep tool names namespaced to avoid collisions.
- Treat documentation from `main` as provisional when a behavior is not demonstrated in the latest tagged release.
- Fail with a clear adapter-compatibility error when registration APIs are unavailable; direct JSON/CLI functionality must continue to work.

## Operational privacy

Hermes documents that conversations, memory, and skills are stored locally under its home directory, but model calls still go to the configured provider. Adaptive Learning Agent should disclose that learner data in SQLite is local while conversational text sent through Hermes follows the user's provider and Hermes settings. Users should avoid putting secrets or unnecessary personal information in answers or pack content.
