# Shared game-development instructions

Read this at the beginning of every session. Treat the user's latest instructions as authoritative; retain answers and authorization already given. This is a generic workspace, not an implemented game.

## Session contract

1. Run `python scripts/workspace.py status` from the repo root. Read `workspace.json`, then the selected game's `.game-workspace/state.json`, its design and recent evidence. With no selection, read `WORKSPACE.md` and discuss the idea; do not guess a target.
2. Inspect the actual project, including Editor version, packages, render pipeline, scenes and local changes. Run `python scripts/workspace.py check`. Missing/mismatched identity is a stop for project edits, not permission to recreate state silently.
3. Before any Editor operation, use current Unity CLI help/status to identify the connected Editor's canonical full project path, version, process and readiness. Compare the observed path with `python scripts/workspace.py check --editor-path "<observed full path>"`. This helper compares paths; it does not connect to Unity. Use an explicit target for each tool action, rechecking after reconnects, restarts or switches. Never choose the first Editor or rely on a partial name match.
4. Select only relevant [skills](docs/workflow.md). Make a small, reviewable change; verify it in the appropriate tool and in Unity. Do not overwrite unrelated local edits. Make routine implementation choices within the agreed scope.
5. At the end of each interaction, record meaningful changes, decisions, actual checks, blockers and next steps using `workspace.py record`. Even a discussion should preserve a new decision. If nothing changed, report that without fabricating progress. With no active game, update `WORKSPACE.md`. Finish with what works, evidence and remaining limitations.

## Initial idea discussion

Before designing the game, resolve platform, 2D/3D, input/controls, scope and the intended experience. For mobile, resolve portrait/landscape then. Carry known answers forward. Ask only if the missing detail materially changes the design or target; label reasonable minor assumptions. Research depth should fit the request. Agree a playable slice and observable success criteria before expanding content.

## Tool and asset rules

- Prefer Unity CLI; inspect installed version/help before composing commands. A legacy bridge is a fallback when needed, with the same target checks. Never silently install/upgrade Editors, packages, bridges or system tools. Follow [tool setup](docs/tool-setup.md).
- Create actual Unity projects with installed Hub/CLI when requested. `UnityProjects/` is intentionally empty of projects. Never manufacture marker files to claim a valid project.
- Discover Blender separately and verify its version. Default to game-ready low-poly assets within project-specific budgets. Request authorization before installation if missing.
- Use PhotoCraft drawing/editing and Blender scripting/procedural geometry. Do not call generative image, video, music or other asset services unless explicitly requested. No paid calls by default.
- Use relative repository paths; calculate machine paths at runtime. Keep tokens in the gitignored local runtime location prescribed by [PhotoCraft setup](docs/photocraft.md); never print, log, commit or package them. Use authenticated loopback control.
- Preserve source asset files, `.meta` identities, licenses and attribution. Record actual imports and runtime evidence, not just export success.
- Before restarting/closing a tool with unsaved work, get save/restart consent if not already authorized. Never silently kill an application. Before destructive recovery, identify precisely what would be lost and get approval.

Keep shared guidance here concise. Put game-specific requirements, progress and decisions inside that game's directory. Do not transfer another game's assumptions on a switch. See [state recovery](docs/project-state.md) and [verification](docs/verification.md).
