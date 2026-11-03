# Project identity and progress

`workspace.json` holds a nullable relative `active_project` and its `active_id`. Each registered real game has `.game-workspace/state.json`: schema version, relative path, random workspace ID, Unity `productGUID`, captured Editor version, phase, timestamp and progress entries. It is versionable project documentation, not a Unity asset. The helper never creates a Unity project or touches a running Editor.

```text
python scripts/workspace.py status
python scripts/workspace.py register UnityProjects/YourGame
python scripts/workspace.py select UnityProjects/YourGame
python scripts/workspace.py check
python scripts/workspace.py check --editor-path "<full path observed from the connected Editor>"
python scripts/workspace.py record --phase prototype --done "Implemented the agreed interaction" --evidence "Docs/verification.md" --next "Test the failure and restart flow"
python scripts/workspace.py record --decision "Use landscape touch controls" --blocker "Device test pending"
python scripts/workspace.py clear
```

Use real names in place of examples. Paths are portable forward-slash paths with one game directory directly below `UnityProjects/`. The helper rejects absolute paths, traversal, reserved Windows names, reparse points/symlinks inside the repository and missing project markers. Registration checks structure and parses identifiers; it does not prove Unity can compile or run the game. Source-only fake projects are used solely in tests.

Registration leaves the active selection unchanged. Selection checks a registered project's identity, then updates only the root selection. `clear` deselects without deleting progress. `status` reports no selection successfully; `check` fails when none is selected. `record` requires an active, valid identity and at least one nonblank entry. Repeat flags to add several items. Valid phases are `idea`, `design`, `prototype`, `production`, `verification`, `blocked`, `complete`.

After each interaction, write meaningful progress. Evidence must say whether it is inspection, simulated, Editor or device evidence. A phase label is descriptive; `complete` is not proof that a build was verified. Record unresolved issues even if another part of the task is complete.

## Prevent stale state

Removing/replacing a project without its marker, changing its `productGUID`, or selecting an unregistered path causes checks to fail. Changing Editor version requires review and `refresh-version` only after the intended upgrade is confirmed. This records a decision and updates the recorded version; it never upgrades Unity. Read old decisions before continuing.

Moving the **whole starter** preserves relative paths and identity. Renaming a game folder or forking a registered game requires deliberate migration: deselect, back up its `.game-workspace/` record, inspect its identity and new intent, then archive that record outside the new game's active metadata and register the new path. Do not delete old records silently. A new fork gets its own workspace ID and fresh progress; carry only explicitly relevant decisions. Whole-directory copies retaining every identity are indistinguishable from an intentional portable move, so declare forks rather than assuming the helper detects them.

Writes use atomic replacement and a short exclusive lock. Concurrent edits should be serialized. If `.workspace.lock` remains after a crashed helper, ensure no helper is running, inspect its recorded PID, and remove only that lock. Do not automatically clear a lock based on elapsed time. If registration succeeded but selection did not, simply select again. If JSON is malformed, preserve it for recovery and restore a known checkpoint; do not reset history to make checks pass.
