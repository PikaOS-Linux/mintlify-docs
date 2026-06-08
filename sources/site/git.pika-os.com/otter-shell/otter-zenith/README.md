# otter-zenith

Debian packaging meta-repository for Otter Shell. Clones tagged releases of each independent component and assembles a distributable source tree.

This directory is not an application runtime. Individual apps and libraries live in their own git repositories under the `otter-shell/` monorepo workspace.

## Usage

```bash
./main.sh
```

The script reads `pika-build-config.sh`, clones each component at the configured release tag, and prepares `otter-shell-<version>/` for packaging.

## Components packaged

See `main.sh` for the current component list and release version pin.

## License

MIT License — see [LICENSE.md](LICENSE.md).
