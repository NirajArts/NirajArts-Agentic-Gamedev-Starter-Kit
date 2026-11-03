---
name: blender-assets
description: "Author game-ready low-poly Blender models, rigs and animations for a selected Unity game."
---

# Blender source to game-ready export

Inputs: asset purpose, silhouette/style references, target scale, camera distance, platform budget and animation needs.

1. Discover the separate Blender install and verify its version using docs/tool-setup.md. Inspect existing source files and export conventions. Decide triangle/material/texture budgets based on the actual target; low-poly is the default, not a universal numeric budget.
2. Block the silhouette at the intended world size. Use clear collection/object names and a deliberate origin/pivot. Prefer stable procedural parameters or simple meshes; preserve the editable .blend source under the game's SourceArt directory.
3. Clean topology, normals and transforms; remove accidental duplicates/internal surfaces. Provide UVs appropriate to texture use, sensible seams and material slots that map to the chosen Unity pipeline. Avoid hidden reliance on Blender-only shader nodes.
4. If animated, define rig type and bone hierarchy, bind/weight deliberately, test extreme poses, organize named clips with explicit frame ranges, and decide root motion versus in-place motion. Do not add rigs to rigid props unnecessarily.
5. Verify export options against the installed operator schema. Export a named selection to a staging location in the game, record units/axis/scale, and keep source provenance. Use the asset-integration skill to verify the import; export success alone is insufficient.

Validation: inspect silhouette and shading at gameplay distance; check scale, pivot, UV coverage, material slots, mesh count and deformation/loop seams. Test at least one representative exported animation in Unity before producing a batch.

Output: editable source, game export, import contract and measured budget notes. No generative service is required; Blender scripting and procedural geometry are allowed.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
