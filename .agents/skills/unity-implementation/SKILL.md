---
name: unity-implementation
description: "Implement Unity gameplay, scenes and UI in a selected project with verified Editor targeting."
---

# Implement and inspect in Unity

Inputs: registered active project, a small design slice, installed Editor/package versions and acceptance scenarios.

1. Follow the AGENTS.md identity checks and docs/tool-setup.md. Inspect existing architecture, render pipeline, input package and local edits. Discover the actual connected Editor command schema before use.
2. Split the slice into one observable behavior at a time. Prefer small components with clear lifecycle/ownership, serialized tuning and explicit references. Keep simulation logic separable when it makes meaningful tests possible; do not add frameworks just to demonstrate architecture.
3. Use Editor APIs or verified live tools for scene/prefab changes, save deliberately, then read hierarchy/components/references back. Do not blindly fabricate Unity YAML or regenerate .meta files. Prevent duplicate objects when rerunning authoring scripts.
4. For UI, inspect whether the game uses UI Toolkit or uGUI before choosing. Keep its layout/input model consistent, verify required assets and bindings, test actual screen sizes and safe areas, and avoid fixed pixel assumptions that break the agreed orientation.
5. Compile and exercise the behavior. Observe advancing gameplay and inspect Console. Test initialization, disabling/re-enabling, scene reload and failure/restart cases affected by the change. Resolve missing references before adding polish.

Validation: compare actual behavior with acceptance scenarios; distinguish code inspection, compilation, Play mode and device checks. Check serialized references survive save/reload.

Output: working source/scene changes, relevant evidence in Docs/verification.md and updated state. If tool access blocks execution, finish independent inspection and name the exact unverified behavior.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
