# Evidence before completion

Use checks matched to the change. Pure documentation needs link/consistency checks; gameplay behavior needs the Editor or a build. Keep exact versions, date, project identity, scenario, actual result and evidence path. Mark unavailable checks as pending.

For a playable slice, confirm compilation, scene references, required components, input bindings and transitions. Enter Play mode and verify time/state advances across observations. Exercise the intended loop, failure, restart, pause and quit paths; read Console after the scenario. A single attractive screenshot or a Play flag is insufficient.

For a device build, record build target, configuration, Editor/package versions, command or UI path, output location and actual exit/result. Install/run the produced artifact on the named target device when possible. Test controls, orientation/safe areas, suspend/resume, performance and sound there. An Editor test does not verify a mobile or XR build. Do not equate a prepared build method, generated APK path or absence of visible errors with success.

## Starter checks

```text
python -m unittest discover -s tests -v
python scripts/validate_repo.py
pwsh -File tests/Test-PowerShell.ps1
python scripts/package_starter.py
```

Tests create temporary synthetic project structures and exercise helper behavior without Unity, Blender or PhotoCraft. The PowerShell checks parse scripts and exercise argument construction, missing binaries and occupied-port detection through test doubles; they do not launch the application. The Python PhotoCraft tests use in-memory streams, not a real credential or listener. Read [VALIDATION.md](../VALIDATION.md) for the actual delivery results and exclusions.

## Fresh-user acceptance (still requires real tools)

1. Extract into a path with spaces on another machine. Verify no active project or `.local/` credential is included.
2. Discover tool versions and obtain authorized setup. Describe a small original game; confirm constraints before designing it.
3. Create two real Unity projects, register both, switch between them, and show each retains only its own progress. Check an intentionally wrong connected Editor path is rejected before an edit.
4. Author a small Blender asset and a layered PhotoCraft sprite; export, import, inspect scale/pivots/materials/alpha, and exercise them in Play mode.
5. Save and restart PhotoCraft deliberately; verify token reuse without printing it. Check an unrelated occupied port stops a new launch.
6. Build and run on the intended device. Move the entire repo to another path and recheck state plus runtime-derived paths. Review a clean package for secrets and unwanted binaries.

The starter enables these workflows; none of these real-tool acceptance steps is implied by simulated helper tests.
