# Otter Shell documentation

Mintlify documentation for Otter Shell. The site covers end-user setup, packaged applications, configuration, the otr developer libraries, and LuaJIT extensions.

## Source of truth

- `docs.json` defines navigation and site settings.
- MDX pages contain YAML frontmatter and Mintlify components.
- The shell workspace is `/home/ferreo/otter-shell`; each package has its own repository.
- `sources/` contains imported reference snapshots, not current API contracts or published guide pages. Preserve their historical provenance; verify current claims against package source and manifests instead.
- Read `AGENTS.md` for terminology, package boundaries, and writing conventions.

Otter Shell v0.13.0 uses otr 0.2.0 and LuaJIT extensions. Some native dependencies and separate products use Zig and have their own build instructions.

## Local preview

The Mintlify CLI requires Node.js 18 or newer. Install the CLI, then run it from this repository:

```bash
bun add --global mint
mint dev --telemetry=false
```

The preview normally opens at `http://localhost:3000`.

## Verification

```bash
mint --telemetry=false validate
mint --telemetry=false broken-links --check-anchors --check-redirects
git diff --check
```

Check that every published MDX page has a navigation entry, all local links and anchors resolve, and code examples match the current native or Lua API. Link validation does not establish that external sites are reachable or that an example behaves correctly at runtime.

Use `pikman` for end-user package installation examples. Check metapackage membership against `otter-zenith/debian/control`; do not imply that Otter Shell supplies a default compositor or that every advertised portal method is implemented.

## Publishing

Review changes locally before pushing. The connected Mintlify deployment can publish pushes to the default branch, so a push can change the production site. Publishing documentation does not release shell binaries or change Zenith package pins.
