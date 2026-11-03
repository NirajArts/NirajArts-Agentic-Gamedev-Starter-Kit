---
name: game-audio
description: "Integrate licensed sound and music with sensible mixer routing, levels and runtime playback."
---

# Sound that supports play

Inputs: sound event list, mood, target hardware, existing audio architecture and source/license information.

1. Identify the role of each cue: information, impact, ambience or music. Reuse suitable licensed or user-provided sources; document rights before importing. Do not use generative music/sound services unless requested.
2. Trim/loop sources deliberately and retain originals. Match mono/stereo and spatialization to use. Inspect actual file durations, peaks and loop seams before selecting compression/load behavior.
3. Route sources to the project's mixer groups (for example effects, music, UI and ambience), with user volume/mute settings where in scope. Avoid creating parallel mixers without a reason.
4. Limit overlapping one-shots, make repeated cues varied where useful, and handle scene transitions/pause/resume without duplicate music or orphaned sources. Tune relative level and dynamics in a representative busy scene.
5. Profile memory and playback on the target platform when asset counts or streaming make this material. Choose load/compression settings from measurements rather than assigning one setting to every clip.

Validation: check no clipping, missing cue, audible loop click or double playback; verify volume/mute persistence and meaningful audio alternatives for critical information. Record untested device audio separately.

Output: configured clips/sources/mixer, asset register entries, playback evidence and unresolved licensing/device limitations.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
