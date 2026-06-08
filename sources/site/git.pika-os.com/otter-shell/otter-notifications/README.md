# otter-notifications

A Wayland notification daemon implementing the freedesktop.org Desktop Notifications specification (org.freedesktop.Notifications). Drop-in replacement for mako/dunst/fnott. Part of the otter-shell project.

## Features

- **Full freedesktop.org Notifications 1.2 spec** - `org.freedesktop.Notifications` D-Bus service
- **Priority system** - Low, normal, and critical urgency levels with per-level timeouts
- **Configurable position** - 6 screen positions (top/bottom combined with left/center/right)
- **Themed via otter-theme** - shared theme with otter-bar and otter-launcher
- **Icon support** - XDG icon theme lookup via otter-desktop
- **Click to dismiss** - Left click dismisses and activates the source application, right click dismisses
- **Configurable timeouts** - Per-urgency timeout control (critical defaults to persistent)
- **Notification queue** - Max visible limit with overflow queuing
- **Animation** - Smooth enter/exit transitions
- **Hot-reload** - Config and theme changes apply without restart via inotify (font family changes trigger full surface recreation)
- **Centered text** - Notifications without icons center title and body text
- **HiDPI support** - Correct scaling on high-DPI displays via wl_output.scale, wl_surface.enter, and preferred_buffer_scale

## Building

```bash
cd otter-notifications && zig build
```

### Dependencies

- Zig 0.15.2
- wayland-client
- xkbcommon
- FreeType2 (via otter-render)
- D-Bus (basu, vendored/static)

## Usage

```bash
# Start the daemon
otter-notifications

# Or build and run directly
cd otter-notifications && zig build run
```

Send notifications with any tool that speaks the freedesktop.org Notifications protocol:

```bash
# Basic notification
notify-send "Hello" "World"

# Critical urgency (persistent by default)
notify-send -u critical "Alert" "Something important"

# Low urgency (shorter timeout)
notify-send -u low "FYI" "Not urgent"

# With icon
notify-send -i firefox "Browser" "Download complete"
```

## Configuration

Config file: `~/.config/otter-shell/notifications.conf`

Falls back to `/etc/otter-shell/notifications.conf` if user config does not exist. A default config is auto-created on first run.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `position` | Position | `top_right` | Screen position for notifications |
| `max_visible` | u8 | `5` | Maximum notifications shown at once (overflow queued) |
| `gap` | u16 | `8` | Vertical gap between notifications (pixels) |
| `width` | u16 | `360` | Notification popup width (pixels) |
| `margin_top` | u16 | `8` | Margin from top screen edge (pixels) |
| `margin_right` | u16 | `8` | Margin from right screen edge (pixels) |
| `margin_bottom` | u16 | `8` | Margin from bottom screen edge (pixels) |
| `margin_left` | u16 | `8` | Margin from left screen edge (pixels) |
| `border_width` | u16 | `2` | Border width around each notification (pixels) |
| `icon_size` | u16 | `48` | Notification icon size (pixels) |
| `default_timeout` | u32 | `10000` | Normal urgency timeout in milliseconds |
| `low_timeout` | u32 | `5000` | Low urgency timeout in milliseconds |
| `critical_timeout` | u32 | `0` | Critical urgency timeout in milliseconds (0 = persistent) |
| `animation_duration` | u32 | `200` | Enter/exit animation duration in milliseconds |
| `background_color` | ?Color | null | Background color (default: theme `popup.background`) |
| `border_color` | ?Color | null | Border color (default: theme `popup.border`) |
| `title_color` | ?Color | null | Title text color (default: theme `colors.foreground`) |
| `body_color` | ?Color | null | Body text color (default: theme `colors.muted`) |
| `critical_border_color` | ?Color | null | Border color for critical notifications (default: theme `colors.critical`) |

### Position Values

```
top_left      top_center      top_right
bottom_left   bottom_center   bottom_right
```

### Example Config

```conf
# Screen position and layout
position = top_right
max_visible = 5
width = 360
gap = 8
margin_top = 8
margin_right = 8

# Timeouts (milliseconds, 0 = no auto-dismiss)
default_timeout = 10000
low_timeout = 5000
critical_timeout = 0

# Animation
animation_duration = 200

# Dimensions
border_width = 2
icon_size = 48

# Optional color overrides (hex RGBA: #RRGGBBAA)
# Omit to inherit from theme.conf
# background_color = "#181825f5"
# border_color = "#45475aff"
# title_color = "#ffffffff"
# body_color = "#a6adc8ff"
# critical_border_color = "#f38ba8ff"
```

### Colors

Colors are specified in hex RGBA format: `#RRGGBBAA`

All color fields are optional (`?Color = null`). When omitted, the value is inherited from `theme.conf`. Resolution order:

1. Explicit color in `notifications.conf` (if set)
2. Theme token from `theme.conf` (if set)
3. Compiled-in default

## Theming

Visual styling inherits from `~/.config/otter-shell/theme.conf` (fallback: `/etc/otter-shell/theme.conf`, then compiled-in defaults). Shared across all otter-shell applications.

Notification-specific theme tokens:

| Token | Default | Description |
|-------|---------|-------------|
| `fonts_font_family` | `"Inter"` | Font family (system font discovery) |
| `fonts_notification_title_size` | `15` | Title font size |
| `fonts_notification_body_size` | `14` | Body font size |

Additional theme tokens used by notifications: `popup_background`, `popup_border`, `popup_padding`, `colors_foreground`, `colors_muted`, `colors_critical`.

See [otter-theme](../otter-theme/) for the full token reference.

## Running Tests

```bash
cd otter-notifications && zig build test
```

## Architecture

```
otter-notifications/src/
  main.zig            - Wayland setup, event loop, output tracking, click-to-dismiss
  config.zig          - Config parsing and theme resolution via otter-conf
  draw.zig            - Notification popup rendering via otter-ui frame nodes (text wrapping, icons, borders)
  surface_manager.zig - Per-notification layer shell surface lifecycle, HiDPI scaling, UiState rasterize

otter-desktop/src/
  notification_service.zig - Notification types, store, and D-Bus service (shared library)
```

## Dependencies

- **otter-wayland** - Wayland connection, layer shell surfaces, SHM buffers
- **otter-render** - Font rendering, image loading, surface operations
- **otter-desktop** - D-Bus (basu), XDG icon lookup
- **otter-conf** - Config file parsing
- **otter-theme** - Shared visual theme
- **otter-geo** - Geometry types
- **otter-utils** - BoundedArray, logging

### System Libraries

- wayland-client
- xkbcommon

## License

MIT License — see [LICENSE](LICENSE).
