---
name: photocraft-art
description: "Create or edit layered 2D artwork, pixel art and UI textures in PhotoCraft for a Unity game."
---

# Purposeful 2D art in PhotoCraft

Inputs: asset role, style/palette, dimensions, pixels-per-unit or UI scaling, transparency, slicing and target import settings.

1. Use docs/photocraft.md to verify local binaries, authenticated GUI and correct workspace roots. Inspect the actual active document and save status before editing; do not take an occupied port as proof of the right session.
2. Set canvas size, palette and layer organization for the intended use. For pixel art, work on a consistent pixel grid and inspect at integer zoom; for UI, reserve meaningful stretch borders and test readability at final display size.
3. Draw/edit with discovered operations, named layers and non-destructive structure where practical. Keep editable source beside the game's SourceArt. Do not invoke generative asset services without the user's explicit request.
4. Export only the needed region/frames with intentional alpha, dimensions, padding and filenames. For sheets, specify cell layout, pivot, animation order and frame timing. Avoid packing before import requirements are understood.
5. Reopen the export and inspect transparent edges, halos, alignment and visual consistency. Use asset-integration to set sprite/UI import behavior and verify the result in its actual scene.

Validation: exported dimensions/alpha match the contract; no accidental opaque background or clipped pixels; pixel-art filtering and UI scaling are checked in Unity. Confirm source save and export both exist.

Output: layered source, exported asset/sheet, import/slicing notes and evidence. On uncertain tool timeouts inspect state before retrying; preserve unsaved work before restart.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
