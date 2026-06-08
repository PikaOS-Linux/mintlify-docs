# otter-lock

A Wayland session lockscreen for the otter-shell desktop environment. Uses the `ext-session-lock-v1` protocol to securely lock the session across all outputs.

## Build

```bash
cd otter-lock && zig build
```

### Build Options

```bash
# Use jemalloc as C allocator (higher baseline RSS, better fragmentation handling)
zig build -Dc_allocator=jemalloc

# Use mimalloc as C allocator
zig build -Dc_allocator=mimalloc

# Disable PAM (authentication will be unavailable)
zig build -Denable_pam=false

# Disable D-Bus (fprintd fingerprint support unavailable)
zig build -Denable_dbus=false
```

## Run

```bash
cd otter-lock && zig build run
```

## Test

```bash
cd otter-lock && zig build test
```

## Configuration

Config file: `~/.config/otter-shell/otter-lock.conf` (auto-created on first run).

Fallback: `/etc/otter-shell/otter-lock.conf`, then compiled-in defaults.

Colors inherit from `~/.config/otter-shell/theme.conf` when not explicitly set.

```
blur_radius = 9
clock_font_size = 72
date_font_size = 18
font_size = 14
dialog_width = 360
dialog_padding = 32
input_height = 44
button_height = 44
avatar_size = 96
enable_fingerprint = true
show_clock = true
show_avatar = true
pam_service = "otter-lock"
screensaver_image = "/usr/share/otter-shell/lock/otter-shell.png"
screensaver_fps = 60
screensaver_speed = 2
screensaver_image_min_size = 64
screensaver_image_max_size = 256

# Force the full UI (password dialog) onto a specific output by name.
# Empty string (default) follows keyboard/pointer focus.
# focus_output = "DP-1"

# Optional color overrides (null = inherit from theme.conf)
# overlay_color = "#00000078"
# dialog_background = "#181825c8"
# text_color = "#ffffffff"
# muted_color = "#6c7086ff"
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
| Enter | Submit password |
| Backspace | Delete character before cursor |
| Delete | Delete character after cursor |
| Home / End | Move cursor to start/end |
| Left / Right | Move cursor |
| Ctrl+Left / Ctrl+Right | Move cursor by word |
| Ctrl+U | Clear password field |
| Ctrl+W | Delete word |

## Multi-monitor

Each output gets a lock surface. The full UI (password dialog, avatar, clock) is displayed on the focused output; other outputs show a minimal view (wallpaper + clock).

Focus follows keyboard and pointer input by default. Set `focus_output` to pin the dialog to a specific output name (e.g. `DP-1`, `HDMI-A-1`).

## Fingerprint Support

When `enable_fingerprint = true` (default) and fprintd is available with enrolled fingerprints, the dialog shows a fingerprint prompt alongside the password field. Either method can authenticate.

## Wallpaper Integration

Reads `/tmp/{uid}/otter-wallpaper-state` to display the same wallpaper as `otter-wallpaper` on each output. Falls back to the theme overlay color if no wallpaper state is available.

## Screensaver Mode

The install step packages `data/screensaver/otter-shell.png` to `/usr/share/otter-shell/lock/otter-shell.png`. This transparent PNG is the compiled-in default for `screensaver_image`.

## Architecture

Session lock application using `ext-session-lock-v1`:

- Locks via `ext_session_lock_manager_v1.lock()` to securely capture all outputs
- 1x1 viewporter placeholder for near-instant first commit (required by protocol)
- Full renderer created lazily after the compositor accepts the lock
- Frame callback throttled rendering (vsync-limited, no CPU spin)
- PAM authentication with deferred execution (authenticating state is displayed before blocking on PAM)
- Per-output `LockSurface` with independent `DoubleShmPool` renderers
- Rendering describes `otter-ui` surface nodes into bounded UI state; `otter-ui` owns command emission and rasterization through the shared CPU renderer
- Avatar loaded from `~/.face` (deferred until first frame is on screen)
- Theme integration via `otter-theme`

## License

MIT License — see [LICENSE](LICENSE).
