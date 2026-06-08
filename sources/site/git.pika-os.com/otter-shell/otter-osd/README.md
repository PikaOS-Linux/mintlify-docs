# otter-osd

On-screen display (OSD) overlay daemon for the Otter desktop shell. Shows transient volume, brightness, and lock key indicators as Wayland layer shell overlays.

## Architecture

Single binary with two modes:

- **Daemon mode** (no args): Connects to Wayland, initializes PipeWire eagerly at startup, creates a UNIX datagram socket, and polls for commands. Surfaces are created lazily on first command and destroyed after timeout for zero idle RAM. PipeWire stays alive for the daemon lifetime to avoid RSS growth from repeated init/teardown cycles. Rendering describes `otter-ui` surface nodes into a bounded `OsdUiState`; `otter-ui` owns command emission and rasterization through the shared CPU renderer.
- **Client mode** (with args): Parses the command, sends a datagram to the daemon socket, and exits immediately.

## Build

```bash
cd otter-osd && zig build
```

## Run

Start the daemon:

```bash
otter-osd
```

Send commands from scripts or keybindings:

```bash
otter-osd volume-up 5
otter-osd volume-down 10
otter-osd volume-mute-toggle
otter-osd brightness-up 5
otter-osd brightness-down 5
otter-osd caps-lock
otter-osd num-lock
otter-osd scroll-lock
```

## Socket Protocol

Communication uses AF_UNIX SOCK_DGRAM at `$XDG_RUNTIME_DIR/otter-shell/osd-{WAYLAND_DISPLAY}.sock`.

Datagrams are plain text:

```
command-name[ step]\n
```

Commands: `volume-up`, `volume-down`, `volume-mute-toggle`, `brightness-up`, `brightness-down`, `caps-lock`, `num-lock`, `scroll-lock`.

The optional step value (default 5) applies to volume and brightness up/down commands.

Lock key commands (`caps-lock`, `num-lock`, `scroll-lock`) use toggle-based state tracking. The daemon toggles its internal state on each command and periodically syncs against `/sys/class/leds/` (every 60 seconds) to correct drift. This avoids race conditions where sysfs LED values may not yet reflect the new state when the command arrives, and works on Wayland compositors that do not update sysfs LEDs.

## Configuration

Config file: `~/.config/otter-shell/otter-osd.conf` (fallback: `/etc/otter-shell/otter-osd.conf`). Auto-created on first run. Hot-reloadable via inotify — recreates the visible surface on reload (position/width/height/margins are baked at surface creation).

```
timeout = 1500
position = bottom_center
width = 340
height = 60
margin_bottom = 60
margin_top = 60
icon_size = 28
border_width = 2
bar_height = 14
font_size = 15
animation_duration = 150
# background_color = "#181825f5"
# border_color = "#45475aff"
# bar_color = "#89b4faff"
# bar_background_color = "#31324466"
# text_color = "#ffffffff"
# mute_color = "#f9e2afff"
```

Color fields are optional -- omit to inherit from `theme.conf`.

## Tests

```bash
cd otter-osd && zig build test
```

## Dependencies

Shared libraries from the otter-shell monorepo: otter-geo, otter-utils, otter-render, otter-wayland, otter-desktop, otter-conf, otter-theme.

### System Libraries
- wayland-client

### Audio Control
- PipeWire (statically linked via otter-desktop) for native volume/mute control

## License

MIT License — see [LICENSE](LICENSE).
