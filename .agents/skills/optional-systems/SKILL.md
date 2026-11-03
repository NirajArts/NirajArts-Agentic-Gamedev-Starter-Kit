---
name: optional-systems
description: "Plan and integrate explicitly requested multiplayer, XR, procedural-world or monetization systems."
---

# Optional complexity only when needed

Inputs: explicitly requested subsystem, game constraints, platform/service accounts, budget and existing architecture.

Use only the relevant branch below. These systems are not default dependencies of a new game.

- Multiplayer: settle player count, topology/authority, latency tolerance and session lifecycle. Verify current package/service docs; prototype connection, ownership, disconnect/rejoin and state synchronization before broad content work. Test with separate clients and adverse network conditions; one local instance proves little.
- XR: identify headset/runtime, interaction model, locomotion/comfort needs and rendering budget. Verify installed XR packages and input paths against the target. Test scale, reach, tracking loss, UI readability and comfort on hardware; an Editor view cannot verify headset experience.
- Procedural worlds: define deterministic seed/version, generation constraints and valid/invalid outcomes. Separate generation from presentation; test representative and adversarial seeds for reachability, bounds, content budgets and save/load reproducibility. Preserve failing seeds for regression.
- Monetization: confirm the requested purchase/ad/subscription model and platform. Research current official SDK/store requirements, costs and privacy obligations; do not make purchases, create paid services or publish configuration without authorization. Use sandbox/test modes; verify cancellation, duplicate callbacks, restore/entitlements and offline/error behavior. Keep secrets server-side where required.

Validation: write subsystem-specific acceptance scenarios and test on the real topology/device/store sandbox when available. Mark setup and runtime gaps explicitly. Do not turn a design recommendation into a claim of compliance or production readiness.

Output: scoped integration decision, compatibility/cost notes, minimal tested implementation when authorized, evidence and remaining release gates.

Shared setup: [AGENTS.md](../../../AGENTS.md). Record results with [project state](../../../docs/project-state.md).
