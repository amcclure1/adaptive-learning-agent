# Hermes v0.18.2 Compatibility

Date: 2026-07-18  
Status: verified on the local Windows installation

## Version and installation

The official [Hermes Agent v0.18.2 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2) is tag `v2026.7.7.2`, released 2026-07-07. The tagged checkout resolves to commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`; its `pyproject.toml` declares package version `0.18.2` and Python `>=3.11,<3.14`.

No `hermes`, `uv`, or discoverable OpenClaw command/configuration was present before this task. OpenClaw was not installed, altered, or removed. Hermes was installed from the pinned PyPI release into a uv-managed Python 3.13 tool environment:

```powershell
uv tool install --python 3.13 'hermes-agent==0.18.2'
```

Locally verified output:

- Hermes Agent `v0.18.2 (2026.7.7.2)`
- CPython `3.13.14`
- OpenAI SDK `2.24.0`
- install root `C:\Users\amccl\AppData\Roaming\uv\tools\hermes-agent`

This method is isolated from the system Python. It installs Hermes' own package dependencies inside the tool environment.

## Profiles

The tagged [profile documentation](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/user-guide/profiles.md) states that profiles isolate configuration, provider state, sessions, memory, skills, and related runtime data. It also states that `terminal.home_mode: profile` gives terminal subprocesses a profile-local `HOME` while exposing the original path separately as `HERMES_REAL_HOME`; profile isolation is not a filesystem sandbox.

The installed CLI exposes `profile list`, `use`, `create`, `delete`, `describe`, `show`, `alias`, `rename`, `export`, `import`, `install`, `update`, and `info`. The dedicated profile was created without cloning another profile, without an alias, and without bundled skills:

```powershell
hermes profile create adaptive-learning-dev --no-alias --no-skills
hermes -p adaptive-learning-dev config set terminal.cwd 'C:\Users\amccl\OneDrive\Documents\AIFounderForge\adaptive-learning-agent'
hermes -p adaptive-learning-dev config set terminal.home_mode profile
```

Verified profile path: `C:\Users\amccl\AppData\Local\hermes\profiles\adaptive-learning-dev`.

## Project plugin discovery

The tagged [plugin documentation](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/user-guide/features/plugins.md) and tagged source agree on these points:

- Project plugins are scanned only from `./.hermes/plugins/` relative to the process working directory.
- Project scanning is off unless `HERMES_ENABLE_PROJECT_PLUGINS=1` (or another supported truthy value) is set for that process.
- General/project plugins are also opt-in through the profile's `plugins.enabled` list; `plugins.disabled` wins.
- A plugin contains `plugin.yaml` and `__init__.py`, and `register(ctx)` calls the public `ctx.register_tool(...)` API.
- Project plugins take precedence over user and bundled plugins on a key collision.

Local verification loaded `.hermes/plugins/adaptive-learning`, registered exactly ten `ala_*` tools through the v0.18.2 registry, and reported no loader error. The launch-time environment variable is intentionally scoped to commands run from this trusted repository; it is not stored globally.

Observed tagged-release management limitation: `hermes plugins enable adaptive-learning`, even with project scanning enabled, reported the project plugin as not installed or bundled. Also, `hermes config set plugins.enabled '["adaptive-learning"]'` stored a scalar string rather than a YAML sequence. The isolated profile therefore contains an explicit YAML list:

```yaml
plugins:
  enabled:
    - adaptive-learning
```

This profile edit is required in addition to the per-process environment gate. It affects only `adaptive-learning-dev` and does not globally trust project plugins.

## Skill discovery

The tagged [skills documentation](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/user-guide/features/skills.md) describes profile skills and progressive loading. Tagged source scans the profile skills directory and configured `skills.external_dirs`; it does not automatically scan a repository `skills/` directory.

v0.18.2 provides `ctx.register_skill(name, path)`. A plugin skill is namespaced, read-only, absent from the ordinary flat skill index, and available only through an explicit qualified load. The project plugin registers `skills/adaptive-learning/SKILL.md` as `adaptive-learning:adaptive-learning`. Local verification found that exact qualified skill and preloaded it successfully with:

```powershell
--skills adaptive-learning:adaptive-learning
```

## Codex OAuth and model

The tagged [provider documentation](https://github.com/NousResearch/hermes-agent/blob/v2026.7.7.2/website/docs/integrations/providers.md) states that OpenAI Codex uses a device-code flow and that Hermes stores provider authentication in its own auth store; an existing Codex CLI login may be imported, but the Codex CLI is not required. The installed CLI and tagged source use the canonical provider identifier `openai-codex`:

```powershell
hermes -p adaptive-learning-dev auth add openai-codex
hermes -p adaptive-learning-dev config set model.provider openai-codex
hermes -p adaptive-learning-dev config set model.default gpt-5.5
```

Observed documentation difference: one tagged prose reference uses `codex-oauth`, while the tagged CLI help/source and successful local flow require `openai-codex`. The executable behavior is authoritative for this compatibility record.

Non-sensitive verification only:

- Provider: `openai-codex`
- Model: `gpt-5.5`
- Auth: logged in through device code, stored at the isolated profile's `auth.json`
- Health/chat: a real request succeeded and the model called `ala_system_health`

Adaptive Learning Agent never opened, copied, parsed, logged, or committed the auth store or `.env`. Token values were not inspected. Provider text is still sent to OpenAI under Hermes/provider behavior; only learner operational state remains in local SQLite.

## Trust and filesystem boundary

The plugin computes the repository root from its own project-local location and imports only the public runtime-neutral application/contract modules from `src/`. It can access:

- its own repository source and `skills/adaptive-learning/SKILL.md`;
- pack source paths supplied only to `ala_pack_validate` or `ala_pack_install`, subject to core checks;
- fixed learner data under `<HERMES_HOME>/adaptive-learning/user-data`.

For this profile that learner-data path is `C:\Users\amccl\AppData\Local\hermes\profiles\adaptive-learning-dev\adaptive-learning\user-data`. No tool accepts a database or user-data path. The adapter does not access provider credentials, SQLite internals, or pack contents directly.

To disable the project plugin, omit/unset `HERMES_ENABLE_PROJECT_PLUGINS`. For defense in depth, also remove `adaptive-learning` from this profile's `plugins.enabled` list.

## Verified launch

Run from the trusted repository root:

```powershell
$env:HERMES_ENABLE_PROJECT_PLUGINS='1'
& "$env:USERPROFILE\.local\bin\hermes.exe" -p adaptive-learning-dev --skills adaptive-learning:adaptive-learning
Remove-Item Env:HERMES_ENABLE_PROJECT_PLUGINS
```

Project-plugin discovery depends on the current directory despite `terminal.cwd`; launch from the repository root.

## Assumptions and unverified surfaces

- Verified: Windows CLI one-shot and resume behavior, actual plugin registry, qualified skill preload, profile-local state, Codex request, and full process restart.
- Officially documented but not separately exercised: profile export/import, aliases, gateway operation, Desktop behavior, other platforms, and other providers.
- Not claimed: compatibility with Hermes versions other than 0.18.2, hostile same-account process isolation, or project-plugin discovery when launched outside the repository root.
- Current `main` documentation may be ahead of the tag. This record uses tagged source/docs wherever behavior matters.
