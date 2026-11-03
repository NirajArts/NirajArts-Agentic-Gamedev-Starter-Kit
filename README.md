# NirajArts Game Development Starter

A reusable workspace for developing your own Unity games with Claude or Codex. It includes agent instructions, focused skills, project tracking and tool helpers. It starts with no game and no Unity project.

## Set up

1. Extract this folder somewhere you own. Open **this folder** in your coding agent.
2. Have Unity Hub, a licensed Unity Editor and the modules for your target platform available. Prefer the Unity CLI for automation. Install Blender separately when you need 3D art. Helpers require Python 3.10+; the PhotoCraft launcher requires PowerShell 7 on Windows. See [tool setup](docs/tool-setup.md).
3. Have the agent read [AGENTS.md](AGENTS.md). Claude also enters through [CLAUDE.md](CLAUDE.md); both use the same skills. Run `python scripts/workspace.py status` to check the initial state.
4. Describe your idea. The agent settles the essential constraints first, creates a real project through your installed Unity tools when requested, and registers it under `UnityProjects/`. Each game has its own progress and decisions.

### PhotoCraft fallback (Windows x64)

If either the GUI or CLI is missing, manually download the [official PhotoCraft 0.17.0 portable ZIP](https://github.com/storytold/photocraft/releases/download/v0.17.0/photocraft-0.17.0-windows-x64-portable.zip). Extract it, then move the **contents** of `photocraft-0.17.0-windows-x64-portable/` into `tools/photocraft/` under this repo root. Keep `portable.txt` and all upstream notices. The final executable paths must be:

```text
tools/photocraft/photocraft.exe
tools/photocraft/photocraft-cli.exe
```

After reviewing [PhotoCraft setup](docs/photocraft.md), use `pwsh -File scripts/Start-PhotoCraft.ps1 -AllowTokenCreation` for the first launch. PhotoCraft writes its credential to `.local/photocraft-control.token` inside this repo, so your local agent can read it without printing it. The starter contains no credential. Keep `.local/` private and out of shared ZIPs.

## Start with your own prompt

> Read AGENTS.md and check the workspace state. Help me create [my game idea] for [platform], in [2D/3D], with [controls]. For mobile use [portrait/landscape]. My intended scope is [small prototype / other], and my art direction is [style]. Use the information I've already provided; ask only about missing essentials. Plan a small playable slice, then build and verify it. Use Blender and PhotoCraft as needed. Do not use generative asset services unless I request them.

For an existing game, say which `UnityProjects/<folder>` to continue. To switch manually: `python scripts/workspace.py select UnityProjects/YourGame`.

[Workflow and skills](docs/workflow.md) · [Project state](docs/project-state.md) · [Verification](docs/verification.md) · [Compatibility](docs/compatibility.md) · [Validation results](VALIDATION.md) · [Distribution license decision](LICENSE-DECISION.md)
