# otter-logout

A Wayland power menu overlay for the otter-shell desktop environment. Provides quick access to lock, logout, suspend, reboot, and shutdown actions.

## Build

```bash
cd otter-logout && zig build
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
cd otter-logout && zig build run
```

## Test

```bash
cd otter-logout && zig build test
```

## Configuration

Config file: `~/.config/otter-shell/otter-logout.conf` (auto-created on first run).

Fallback: `/etc/otter-shell/otter-logout.conf`, then compiled-in defaults.

Colors inherit from `~/.config/otter-shell/theme.conf` when not explicitly set.

```
icon_size = 64
button_size = 120
button_spacing = 24
border_width = 2
font_size = 14
overlay_color = "#000000aa"

# Optional color overrides (null = inherit from theme.conf)
# background_color = "#181825f5"
# border_color = "#89b4faff"
# button_color = "#45475aff"
# hover_color = "#89b4faff"
# text_color = "#ffffffff"
# icon_color = "#ffffffff"

# Button configuration (label, XDG icon name, shell command)
lock_label = "Lock"
lock_icon = "system-lock-screen"
lock_exec = "loginctl lock-session"

logout_label = "Logout"
logout_icon = "system-log-out"
logout_exec = "loginctl terminate-session self"

sleep_label = "Suspend"
sleep_icon = "system-suspend"
sleep_exec = "systemctl suspend"

reboot_label = "Reboot"
reboot_icon = "system-reboot"
reboot_exec = "systemctl reboot"

shutdown_label = "Shutdown"
shutdown_icon = "system-shutdown"
shutdown_exec = "systemctl poweroff"
```

## Keybindings

| Key | Action |
|-----|--------|
| Escape | Close |
| 1-5 | Execute button directly |
| Left / Shift+Tab | Navigate left |
| Right / Tab | Navigate right |
| Enter | Execute selected button |
| Click outside | Close |
| Right-click | Close |

## Architecture

One-shot overlay application following the same pattern as `otter-launcher`:

- Full-screen dim overlay via 1x1 pixel buffer + `wp_viewport`
- Centered button panel via `zwlr_layer_shell_v1` overlay layer
- Exclusive keyboard interactivity
- Icons loaded via XDG icon theme lookup (`otter-desktop`)
- Theme integration via `otter-theme`
- Rendering describes `otter-ui` surface nodes into bounded UI state; `otter-ui` owns command emission and rasterization through the shared CPU renderer

## License

MIT License — see [LICENSE](LICENSE).
