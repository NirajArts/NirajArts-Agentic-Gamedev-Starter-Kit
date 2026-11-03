# Delivery validation

Prepared and checked on 2026-11-02 UTC in an isolated new task workspace. No existing user project or running Editor was changed.

| Check | Result | Scope |
|---|---|---|
| Python unit tests | 32 passed | Synthetic project registration/selection, isolated game history, stale/missing/replaced identity, Editor path mismatch, traversal/nonportable paths, simulated reparse points, lock behavior, atomic-write failure, relocation, version review, authenticated protocol ordering/redaction and package exclusions |
| PowerShell checks | 9 passed | Three script parse checks, separate arguments with spaces, child environment isolation, missing binaries, simulated occupied port and dangling link, real missing-binary preflight without side effects |
| Repository validator | Passed | 42 allowlisted files, 14 skill frontmatters, 69 relative Markdown links, required structure and initial empty selection |
| Official local skill validator | 14 passed | Every SKILL.md checked with the installed skill-creator quick_validate.py |
| Content review | Passed | No game/demo assets, unrelated content, personal required drive paths or promotional material; repository license selection remains the owner's decision |
| Clean packaging test | Passed | Exact allowlist, one root folder, readable ZIP CRCs, deterministic output; synthetic .local token, PhotoCraftData, tool binary and unrelated-game data excluded; malicious runtime manifest entries rejected |

Environment: Windows, Python 3.10.6, PowerShell 7.6.5. Python tests used temporary fake Unity marker structures; those are test fixtures, not real Unity projects. Protocol tests used in-memory streams with a non-credential test string. PowerShell tests did not launch PhotoCraft, create a real credential, alter ACLs or bind a port. The ACL creation API's overload was inspected, but actual ACL application remains a runtime check.

Reproduce using the commands in [verification](docs/verification.md). The final ZIP's size and SHA256 are delivered alongside it, since embedding its own hash would change the archive. The package is built only from [package-manifest.json](package-manifest.json); generated caches are excluded.

## Official-source checks

PhotoCraft 0.17.0 executable names and wrapper layout were checked from its pinned packaging source. Authenticated loopback launch flags, token file behavior and MCP bridge arguments were checked from pinned official protocol/docs. Release metadata supplied the published archive size/hash. A partial binary-archive inspection failed because the server rejected range requests; source layout verification was used instead. Sources and extraction details are in [PhotoCraft setup](docs/photocraft.md).

Unity's official CLI/Pipeline docs and the installed unity-cli skill were consulted. The repository requires installed-help discovery rather than claiming an untested CLI version or pinning guessed project-creation/build commands. No tools were installed or upgraded.

## Not run

Real Unity project creation, Editor targeting/control, compilation, Play mode, device builds, Blender authoring/export, PhotoCraft GUI/CLI launch, token creation/reuse, Windows runtime ACL application, MCP client registration and the fresh-user end-to-end workflow were **not run**. These are acceptance checks for the first real game, listed in [verification](docs/verification.md). Helper tests do not establish application compatibility or a completed game.
