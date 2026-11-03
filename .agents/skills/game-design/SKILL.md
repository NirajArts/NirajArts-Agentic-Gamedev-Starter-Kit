---
name: game-design
description: "Specify a game loop, rules, controls and a small implementable slice from an agreed idea."
---

# Rules that can be built and tested

Inputs: selected concept, platform/input/orientation, intended audience, scope and research/feasibility findings.

1. Write the core loop as player action -> state change -> feedback -> next decision. Specify start, win/loss, restart, pause and persistence expectations; state when a flow is out of scope.
2. Describe each mechanic's inputs, preconditions, output, timing and failure cases. Distinguish tunable values from rules. Name state transitions and ownership to avoid overlapping systems.
3. Map controls to the actual device, including touch targets or controller focus where relevant. Plan readable feedback, color-independent signals, audio controls and optional motion reduction appropriate to scope.
4. Choose one vertical slice. List the minimum scene, scripts, UI, art and audio it needs and the order that reduces risk. Keep an explicit later list so optional systems do not sneak into the slice.
5. Define acceptance scenarios in observable terms: input, initial state, expected result and recovery. Give each major uncertainty a cheap test.

Validation: no rule contradicts another; success/failure are testable; intended controls and mobile orientation were settled before layout; asset requirements fit production resources.

Output: compact Docs/design.md, slice checklist and decisions. Update it when playtesting changes the design, then record the next action in state.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
