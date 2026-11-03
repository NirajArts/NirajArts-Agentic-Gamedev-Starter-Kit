---
name: asset-integration
description: "Import Blender and PhotoCraft assets into Unity and verify geometry, rigs, materials, sprites and collisions."
---

# Verify the complete asset path

Inputs: source/export files, provenance, per-game style contract, target scale/pivot and rendering/animation requirements.

1. Inspect source metadata and export settings before importing. Record editable source and exported file paths, author/license, dimensions/units, pivot, material/texture mapping and any rig/clip contract in the asset register.
2. Import into the intended game's Assets subtree, preserving existing .meta files and references on reimport. Keep editable source outside Assets when automatic import would introduce unwanted tool dependencies.
3. For 3D, compare against a known Unity scale reference. Check axis/orientation, pivots, normals, UVs, material slots and texture color-space intent. Verify collision shape and layer behavior separately from render mesh.
4. For rigs, inspect avatar mapping, bone transforms, clip ranges, looping and root motion; play transitions on the actual character. For 2D, check alpha edges, pixels-per-unit, filtering, compression, slice rectangles/pivots, borders and animation order.
5. Make a prefab or reusable presentation with explicit references. Inspect in the actual lighting/camera/UI context and at target display scale. Reimport once to ensure settings/references persist.

Validation: compare source intent and actual Unity output; test a representative collision and animation, or sprite/UI layout as applicable. Flag incompatible shader effects rather than silently replacing the style.

Output: integrated reusable assets, documented import settings/provenance, before/after evidence and any remaining art or runtime defects.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
