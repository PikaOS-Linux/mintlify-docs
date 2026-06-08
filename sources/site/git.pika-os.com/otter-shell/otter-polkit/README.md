# otter-polkit

A Wayland polkit authentication agent for the otter-shell desktop environment. Runs as a persistent daemon, displaying a password dialog on a layer-shell overlay when privileged actions are requested.

## Build

```bash
cd otter-polkit && zig build
```

### Build Options

```bash
# Use jemalloc as C allocator (higher baseline RSS, better fragmentation handling)
zig build -Dc_allocator=jemalloc

# Use mimalloc as C allocator
zig build -Dc_allocator=mimalloc
```

## Run

```bash
cd otter-polkit && zig build run
```

The daemon registers itself as a polkit authentication agent for the current session and waits for authentication requests. Test with:

```bash
pkexec echo hello
```

## Test

```bash
cd otter-polkit && zig build test
```

## Configuration

Config file: `~/.config/otter-shell/otter-polkit.conf` (auto-created on first run).

Fallback: `/etc/otter-shell/otter-polkit.conf`, then compiled-in defaults.

Colors inherit from `~/.config/otter-shell/theme.conf` when not explicitly set.

```
font_size = 14
title_font_size = 16
dialog_width = 420
dialog_padding = 24
border_width = 2
border_radius = 8
input_height = 36
button_height = 36
max_retries = 3
enable_fingerprint = true

# Optional color overrides (null = inherit from theme.conf)
# background_color = "#000000aa"
# dialog_background = "#181825f5"
# dialog_border_color = "#45475aff"
# text_color = "#ffffffff"
# input_background = "#1e1e2eff"
# input_border_color = "#45475aff"
# button_background = "#89b4faff"
# button_text_color = "#181825ff"
# error_color = "#f38ba8ff"

# Custom font (overrides theme font_family)
# font_path = "/usr/share/fonts/TTF/MyFont.ttf"
```

## Keybindings

| Key | Action |
|-----|--------|
| Escape | Cancel authentication |
| Enter | Submit password |
| Ctrl+U | Clear password field |
| Ctrl+W | Delete word |
| Home / End | Move cursor to start/end |
| Left / Right | Move cursor |
| Ctrl+Left / Ctrl+Right | Move cursor by word |

## Fingerprint Support

When `enable_fingerprint = true` (default) and fprintd is available with enrolled fingerprints, the dialog shows a fingerprint prompt alongside the password field. Either method can authenticate.

## Architecture

Persistent daemon with on-demand overlay surfaces:

- Registers as polkit agent via D-Bus on the system bus (`otter-desktop` polkit_agent module)
- Idles with no surfaces until an auth request arrives
- Creates full-screen dim overlay via 1x1 pixel buffer + `wp_viewport`
- Centered password dialog via `zwlr_layer_shell_v1` overlay layer with exclusive keyboard
- Communicates with `polkit-agent-helper-1` via socket (polkit 127+) or direct process spawn
- Optional fprintd integration for fingerprint authentication
- Frame callback throttled rendering (vsync-limited, no CPU spin)
- Rendering describes `otter-ui` surface nodes into bounded UI state; `otter-ui` owns command emission and rasterization through the shared CPU renderer
- Theme integration via `otter-theme`

## License

MIT License — see [LICENSE](LICENSE).
