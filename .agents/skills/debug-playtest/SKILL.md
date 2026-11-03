---
name: debug-playtest
description: "Reproduce gameplay bugs and verify fixes with targeted tests and actual playthrough evidence."
---

# Find the cause and prove the fix

Inputs: expected/actual behavior, reproduction steps, project version, recent changes and available logs.

1. Verify project/Editor identity first. Reproduce from a known start state, noting input, time, scene, device and frequency. Preserve relevant logs and save data without exposing secrets.
2. Separate compile/import/configuration issues from runtime logic, physics, input and presentation. Reduce to the smallest failing scenario and inspect the actual component values/references.
3. Form a specific hypothesis and add focused instrumentation or a minimal regression test. Change the cause rather than stacking speculative fixes. Keep diagnostic output bounded and remove noisy probes after diagnosis.
4. Run the original failing scenario and nearby edge cases. Use EditMode tests for isolated logic, PlayMode tests for lifecycle/scene interactions, and device checks for platform behavior when appropriate. Do not write tests that simply restate implementation.
5. Play the affected loop, including failure/retry, pause and reload if relevant. Read Console afterward and verify gameplay actually advanced. Report failures and unavailable checks as such.

Validation: a previously failing scenario now meets the expected result; meaningful regressions are checked once after the final change; no new unexplained errors appear.

Output: root cause with evidence, fix, actual test results and remaining defects ranked by player impact. Update the game's verification notes and state.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
