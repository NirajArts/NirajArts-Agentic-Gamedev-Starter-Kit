---
name: gameplay-feel
description: "Improve controls, movement, camera, timing and feedback through measured playable iteration."
---

# Make the core action feel right

Inputs: a running core mechanic, intended feel, target controls/device and a reproducible test scene.

1. Observe baseline behavior at normal gameplay speed. Identify the specific friction: input delay, overshoot, hard-to-read collision, camera obstruction, weak impact or unclear recovery. Capture values and reproduction steps.
2. Expose a small coherent set of tuning variables. Test movement acceleration/braking, buffering or grace windows only where appropriate to the design; avoid applying platformer conventions to unrelated mechanics.
3. Tune one category at a time: controls, motion, camera, then layered feedback. Check feedback timing against the actual state transition. Reserve shake, flashes and hit pauses for meaningful events and offer suitable reductions.
4. Compare repeated attempts on the intended input device. Include low/high frame-rate conditions, loss of focus and edge-of-level/collision cases. Ensure timing uses the correct update/time domain for physics and UI.
5. Keep the stronger variant and record why. Revisit collision or camera rules before masking structural problems with effects.

Validation: play the same scenario before/after; observe responsiveness and predictability, not only visual appeal. Test control readability and comfort with representative users when available.

Output: final tuning values, comparison evidence, accessibility choices and remaining questions. Store per-game decisions rather than changing global starter rules.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
