---
name: performance-build
description: "Profile a Unity game on its target and produce, verify and document an actual playable build."
---

# Measured performance and real builds

Inputs: registered game, target device/platform, performance goals, build configuration and available SDK/modules.

1. Confirm the intended target and budgets (frame time, memory, load time, download size) from the game's needs. Discover the installed Editor/CLI build syntax and project build configuration; do not silently download missing modules.
2. Profile representative worst cases on the named target when possible. Record hardware, build type and scenario. Distinguish CPU, GPU, allocation/GC, asset memory and loading bottlenecks before choosing a fix.
3. Apply a focused improvement: e.g. visibility/LOD, batching, texture/audio settings, bounded pools or lower update frequency when the measured bottleneck supports it. Compare the same scenario and inspect visual/gameplay regressions.
4. Build with explicit scene/profile/target/output settings under the game's ignored Builds directory. Read the actual exit/result and logs; verify the output exists and matches the requested platform. Keep signing secrets local and do not invent a production signing configuration.
5. Launch/install that artifact on the intended device when available. Test startup, core loop, input/orientation/safe areas, pause/suspend/resume, audio and restart. Record artifact hash/configuration for reproducibility.

Validation: distinguish build success, launch success and gameplay acceptance. Editor-only measurements do not establish device performance. If device access is absent, report the exact pending checks and deliver the verified subset honestly.

Output: build artifact location, build/test evidence, measured budget comparison, known limitations and next device check. A script prepared for building is not itself a successful build.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
