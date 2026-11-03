# Work in small playable slices

Start with the user's idea, resolve material constraints, and choose the smallest loop that can prove the experience. Plan one slice with observable criteria, implement it, play it, then decide whether to refine, expand or cut it. A compile success is not a playable-game verdict.

For each selected game, keep a short `Docs/design.md` (intent, constraints, loop, rules, success/failure, controls, art direction, scope and exclusions), `Docs/asset-register.md` (rights and import contracts), and `Docs/verification.md` (reproduction steps and evidence) when those documents become relevant. Use `.game-workspace/state.json` for the current stage, history and next steps; do not copy every log into it.

Read skills on demand. Claude can read these files directly; no particular paid plugin is required. The procedural skills are shared across clients.

| Situation | Skill |
|---|---|
| Player needs, competition, evidence | [Game research](../.agents/skills/game-research/SKILL.md) |
| New idea or feasibility | [Creative ideation](../.agents/skills/game-ideation/SKILL.md) |
| Rules and playable-slice specification | [Game design](../.agents/skills/game-design/SKILL.md) |
| Unity scripts, scenes, UI and interactions | [Unity implementation](../.agents/skills/unity-implementation/SKILL.md) |
| Models, rigging and animation | [Blender assets](../.agents/skills/blender-assets/SKILL.md) |
| 2D art, pixel art, UI textures | [PhotoCraft art](../.agents/skills/photocraft-art/SKILL.md) |
| Responsiveness, camera and feedback | [Gameplay feel](../.agents/skills/gameplay-feel/SKILL.md) |
| Levels, pacing and progression | [Level progression](../.agents/skills/level-progression/SKILL.md) |
| Sound and mixing | [Game audio](../.agents/skills/game-audio/SKILL.md) |
| Importing and verifying source assets | [Asset integration](../.agents/skills/asset-integration/SKILL.md) |
| Bugs, playtesting and regression checks | [Debug and playtest](../.agents/skills/debug-playtest/SKILL.md) |
| Device performance and deliverable builds | [Performance and build](../.agents/skills/performance-build/SKILL.md) |
| Checkpoints, restore and moving machines | [Recovery and portability](../.agents/skills/recovery-portability/SKILL.md) |
| Explicit multiplayer, XR, procedural or purchase scope | [Optional systems](../.agents/skills/optional-systems/SKILL.md) |

Use tool-native inspections and version-matching official documentation. Never assume installed optional integrations. If tooling is absent, finish independent design or code inspection and state exactly which runtime verification remains blocked. Do not claim that a prepared script has been executed.
