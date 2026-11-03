# Discover tools before changing anything

The starter does not download, install, activate, upgrade or register system tools. Python helpers use only the standard library. The state helper works with Python 3.10+; Windows helpers require PowerShell 7. Open a terminal at the repository root.

```powershell
Get-Command python, pwsh, unity, blender -ErrorAction SilentlyContinue
python --version
pwsh --version
```

If `blender` is not on PATH, inspect existing installs (Windows installed-app locations, macOS Applications, Linux package locations) or ask for the executable. Test the discovered executable with `--version`. Do not infer a missing installation from a PATH miss. Configure executable paths locally, not in committed scripts. For installation, explain the [official Blender download](https://www.blender.org/download/) and obtain authorization before making system changes. A fresh machine also needs its own Unity account/license and target SDKs/modules; do not share credentials or assume another machine's license applies.

## Unity CLI

Use the [official CLI guide](https://docs.unity.com/en-us/unity-cli) and [command reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference). Check installed help before each new command family:

```text
unity --version
unity --help
unity editors --help
unity projects create --help
unity templates --help
unity status --help
unity command --help
unity pipeline --help
```

Prefer an installed stable Editor appropriate to the target and selected packages. Pin its exact version per game; do not upgrade an existing project merely because a newer Editor exists. Request setup changes only when needed. CLI command syntax may differ between releases, so this starter does not ship a guessed project-creation wrapper. Use Hub if CLI creation is unavailable.

When creating a requested game, select a real installed template, resolve its render pipeline, set its destination to a direct child of `UnityProjects/`, then initialize it with that Editor. Verify `Assets/`, `Packages/manifest.json`, and `ProjectSettings/` exist; save settings so `productGUID` is present. Register it with the state helper. Do not write those files by hand to satisfy registration.

Live CLI control needs the [Unity Pipeline package](https://docs.unity.com/en-us/unity-cli/unity-pipeline/unity-pipeline-package). Verify compatibility and authorization before adding it to that particular project. Inspect `unity status --format json`; require successful output, a ready instance, exact canonical target path and the intended Editor version. The state helper's `--editor-path` takes the path you just observed, not a path inferred from the active state. Explicitly target each subsequent command and inspect the result. Discover commands from the connected Editor rather than inventing command names. If installed help supports caller/skill metadata, identify the invoking workflow.

For a legacy bridge fallback, verify the installed bridge's own schema and target identity. Do not change clients' global MCP settings merely to make this repository work. Any local MCP registration must use runtime-expanded absolute executable/credential paths; stale paths after moving a repository must be regenerated.

## Connection failures

Differentiate no instance, wrong target, package missing, still importing, compilation/Safe Mode, unsupported version and sandbox access. Read available logs without launching another Editor or killing an existing one. If a restart is required, protect unsaved work and obtain save/restart consent. Recheck instance identity after recovery. A failed connection alone does not prove the Editor is closed.

PhotoCraft setup, launch, credentials and bridge mode are in [its guide](photocraft.md). Keep per-machine executable overrides in your terminal or gitignored `.local/` files. Do not store personal absolute paths in shared game state.
