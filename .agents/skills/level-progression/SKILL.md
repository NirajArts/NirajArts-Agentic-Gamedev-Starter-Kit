---
name: level-progression
description: "Design and iterate playable levels, challenge pacing and progression for an established game loop."
---

# Teach, test and combine mechanics

Inputs: verified core mechanics, audience skill assumptions, session length, content budget and current progression rules.

1. Map a learning sequence: safe introduction, focused practice, variation and combination. Establish what each segment teaches and how the player learns from failure.
2. Greybox spaces and paths using scale/movement/camera metrics measured from the real controller. Define spawn/checkpoint/retry locations and critical sightlines before decorative art.
3. Build challenges with clear cause/effect and distinguish optional mastery from mandatory difficulty. Inspect shortcut, softlock, out-of-bounds and inaccessible objective cases.
4. If progression has resources/unlocks, specify earn/spend rules and expected pacing with transparent assumptions. Simulate representative paths; do not let rewards require a system the slice does not implement.
5. Playtest route comprehension, retries, completion time and challenge spikes. Adjust geometry/rules from observations; add art only once the structure works.

Validation: complete from a fresh state, retry after failure, resume at checkpoints and verify progression persistence where implemented. Check required content can be reached without hidden knowledge.

Output: playable greybox/content changes, pacing/progression table where useful, observed playtest findings and prioritized revisions.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
