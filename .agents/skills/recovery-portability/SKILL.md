---
name: recovery-portability
description: "Create recoverable checkpoints and move or restore game work without losing state or assets."
---

# Protect work and resume accurately

Inputs: current working changes, selected project identity, intended checkpoint/recovery operation and known-good evidence.

1. Inspect local edits and unsaved tool documents. Save intended work deliberately; do not force-close applications. Record a compact checkpoint: project identity, tool/package versions, current behavior, evidence and next steps.
2. Use the existing version-control workflow or a reviewed local backup. Include source, Assets with .meta files, Packages, ProjectSettings and per-game state; exclude caches, builds, credentials and machine paths. Do not initialize a remote or publish without request.
3. Before recovery, distinguish code, scene, package, asset and state failures. Preserve the current failing files/logs. Propose the smallest restore and identify data that would be lost before destructive actions.
4. After restoration, verify project markers, identity and selected Editor, import/compile, then replay the affected scenario. Do not reset workspace state merely to suppress a mismatch.
5. For portability, move the whole workspace, re-discover local tools, reconfigure any local absolute MCP paths and recreate private credentials only with authorization. Use docs/project-state.md for deliberate forks/renames.

Validation: restore from a checkpoint in a separate location when warranted; check no asset/meta pairing loss, absent dependencies or secret inclusion. A copied folder alone does not prove a successful restore.

Output: checkpoint/restore evidence, explicit data-loss assessment where relevant, current working state and next steps. Update progress even when a recovery remains blocked.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
