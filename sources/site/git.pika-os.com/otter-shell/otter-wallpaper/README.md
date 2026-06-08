# otter-wallpaper

Wayland wallpaper daemon for the Otter desktop shell. Renders wallpapers on the background layer using `zwlr_layer_shell_v1` with single-buffered SHM pools for minimal memory usage.

## Features

- Per-display wallpaper configuration via display overrides
- Folder rotation with configurable interval (sequential or random order)
- HiDPI scaling support (preferred buffer scale)
- Optional blurred overview surface for Niri
- Hot-reloadable config and theme files via inotify (preserves current wallpaper on reload, dynamically creates/destroys overview surfaces)
- Shared image lists across outputs with the same wallpaper path
- Images decoded, drawn to SHM buffer, and freed immediately to minimize steady-state RAM

## Build

```bash
zig build
zig build run
zig build test
```

Requires `wayland-client` system library.

## Configuration

Config file: `~/.config/otter-shell/otter-wallpaper.conf` (auto-created on first run)

```
path = /usr/share/wallpapers/pika/
rotation_interval = 300
rotation_order = random
scale_mode = cover
overview_enabled = false
overview_blur_radius = 20

# Per-display overrides (display_0 through display_7)
# display_0_name = DP-1
# display_0_path = /home/user/wallpapers/ultrawide/
```

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `path` | string | `/usr/share/wallpapers/pika/` | File or directory path |
| `rotation_interval` | u32 | `300` | Seconds between rotations (0 = disabled) |
| `rotation_order` | enum | `random` | `sequential` or `random` |
| `scale_mode` | enum | `cover` | `cover` (fill+crop) or `fit` (letterbox) |
| `same_on_all_displays` | bool | `true` | Show same wallpaper on all displays (overrides still independent) |
| `overview_enabled` | bool | `false` | Blurred overview surface for Niri |
| `overview_blur_radius` | u16 | `9` | Blur strength for overview |
| `background_color` | Color | theme | Letterbox fill color (`#RRGGBBAA`) |

Theme file: `~/.config/otter-shell/theme.conf` (shared with other otter- apps)

## Niri Overview

When `overview_enabled = true`, otter-wallpaper creates a second blurred layer surface per output with the namespace `otter-wallpaper-overview`. To use it as the Niri overview backdrop, add this layer rule to your Niri config:

```kdl
layer-rule {
    match namespace="^otter-wallpaper-overview$"
    place-within-backdrop true
}
```

## Lockscreen Integration

otter-wallpaper writes the current wallpaper path for each output to `/tmp/{uid}/otter-wallpaper-state` whenever a wallpaper changes (initial draw, rotation, config reload, output add/remove). It removes this state file on normal exit and catchable shutdown signals (`SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`). The file format is one `output_name=path` pair per line:

```
DP-1=/usr/share/wallpapers/pika/mountain.jpg
HDMI-A-1=/usr/share/wallpapers/pika/mountain.jpg
```

A lockscreen application can read this file to display the same wallpaper as the desktop background behind its lock UI. The file is updated atomically on every wallpaper change.

## Architecture

```
src/
  main.zig     # App struct, event loop, timerfd rotation, hot-reload
  config.zig   # Config/ResolvedConfig, theme integration, default file creation
  output.zig   # Per-output state, layer shell surfaces, SHM pools, image drawing
  folder.zig   # Directory scanning, image enumeration, rotation logic
```

## Dependencies

`otter-conf`, `otter-theme`, `otter-wayland`, `otter-render`, `otter-geo`, `otter-utils`

## License

MIT License — see [LICENSE](LICENSE).
