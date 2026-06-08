# otter-tools-core

Shared pure-Zig logic for small Otter Shell tools.

No Wayland, D-Bus, PipeWire, or rendering dependencies. Keep hot-path state bounded and app UI thin.
Clipboard helpers call `wl-copy` by name; packaged installs shadow that name to Otter's native
`otter-copy`, so callers keep wl-clipboard-compatible bounds without depending on upstream
`wl-copy`.
Config schemas for the small apps live in `src/app_configs.zig`; apps and `otter-settings`
use those same structs so defaults stay in sync.

## License

MIT License — see [LICENSE](LICENSE).
