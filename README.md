# Marcle Codex Plugins

This directory is a local Codex plugin marketplace.

Codex CLI expects the marketplace manifest at:

```text
.agents/plugins/marketplace.json
```

## Install on a device

1. Add this marketplace root in Codex:

```powershell
codex plugin marketplace add D:\00_Projects_WSY\AI\Codex_Projects\marcle_skills_plugins
```

2. Install the plugin from this marketplace:

```powershell
codex plugin add image-gen-openai-hk@marcle-codex-plugins
```

3. Configure the API key on that device using one of these options:

```powershell
$env:OPENAI_HK_IMAGE_KEY="your_key_here"
```

or create one of these files:

```text
D:\00_Projects_WSY\AI\Codex_Projects\marcle_skills_plugins\plugins\image-gen-openai-hk\.env
<home>\.image-gen-openai-hk.env
```

with:

```text
openai-hk_image_key=your_key_here
```

Do not commit or share the real `.env` file.


## Maintained skills

`skills/` is the canonical source for these locally installed Codex skills:

- `marcle-goal-excution`: staged Planner / design Reviewer / Coder / implementation Reviewer execution. The spelling is intentional.
- `marcle-doc-governance`: document ownership, impact gate and generic task/review records; replaces `doc-system-governance`.
- `weekly-repo-report`: one weekly-report entry, including Skill-platform work when supported by evidence.

Install the goal and doc skills together: they use sibling references. On this Windows workstation their directories under `%USERPROFILE%\.codex\skills` are junctions to this repository's matching `skills` directories, so edits have one source. Move aside an existing physical installation before creating a junction; never merge nested skill folders. Skill discovery may require a new Codex session. The old doc repository is a retained historical source, not an active maintenance location.

The existing doc governance explicit-only invocation policy is preserved. The new goal skill uses normal discovery but does not start execution for analysis/planning requests. Existing `marcle-plan-review` remains explicit-only and is not automatically invoked by the goal skill. Plugin marketplace registration is separate from local skill installation.
