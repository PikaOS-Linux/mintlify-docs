# otter-bar

A Wayland status bar for the Otter desktop shell, written in Zig.

## Features

- Workspace indicator/switcher (otter-tag, Mango/dwl IPC, ext-workspace; displays workspace names from protocol when available)
- Active window title display with icon (foreign_toplevel protocol)
- Clock widget with timezone-aware formatting via zeit, tooltip with date display, configurable `time_format`/`date_format`, synchronized across all outputs
- Battery status via UPower D-Bus service (auto-hides when no battery present)
- Brightness control from /sys/class/backlight/ (auto-detected per display, internal displays only)
- Power profiles control (power-profiles-daemon/tuned-ppd)
- System monitoring widgets (CPU usage, CPU temperature, memory, network activity with NetworkManager integration)
- Volume control via PipeWire (icon with level indicators, scroll-to-adjust, popup with per-device sliders, mute toggles, default device selection)
- Media player status via MPRIS D-Bus (shows album art + track info, click to play/pause)
- System tray (StatusNotifierItem) with animated expand/collapse, XDG icon theme lookup, context menus via DBusMenu
- Configurable button widgets with icon and command support (built-in menu/power + user-defined custom buttons)
- Shared theme system with hot-reload (colors, spacing, bar dimensions via `theme.conf`)
- Hot-reload configuration without restart
- Configurable bar position (top or bottom of screen)
- Transparent background support
- HiDPI support with per-output scaling via preferred_buffer_scale

## Dependencies

### Required
- Zig 0.16.0
- wayland-client
- FreeType2
- xkbcommon
- Compositor with zwlr_layer_shell_v1 support (wlroots-based compositors)

### Optional (enabled by default)
- **basu/sd-bus** - D-Bus IPC for UPower, power-profiles-daemon, MPRIS, SystemTray
- **libpipewire-0.3** - PipeWire audio control

## Building

```bash
zig build
```

### Build Options

```bash
# Disable D-Bus support (removes battery, power profiles, MPRIS, system tray widgets)
zig build -Denable_dbus=false

# Disable PipeWire support
zig build -Denable_pipewire=false

# Use jemalloc as C allocator (higher baseline RSS, better fragmentation handling)
zig build -Dc_allocator=jemalloc

# Use mimalloc as C allocator
zig build -Dc_allocator=mimalloc

# Minimal build
zig build -Denable_dbus=false -Denable_pipewire=false
```

## Running

```bash
zig build run
```

Or after building:
```bash
./zig-out/bin/otter-bar
```

## Rendering

Each output owns one bounded `BarUiState`. Bar chrome, widget groups, widgets, tooltips, and menus describe `otter-ui` Surface Description nodes; `UiState` owns command emission and rasterization. The output damage tracker is unchanged and still gates partial redraw/rasterization.

## Testing

```bash
zig build test
```

## Theme

Visual styling is controlled by `~/.config/otter-shell/theme.conf` (fallback: `/etc/otter-shell/theme.conf`, then compiled-in defaults). A default theme file is auto-created on first run. Changes hot-reload without restart.

The theme provides semantic color tokens, spacing, bar dimensions, popup styles, and font sizes shared across all otter-shell applications. See [otter-theme](../otter-theme/) for the full token reference.

All widget color fields in `otter-bar.conf` are optional. When omitted (`null`), the theme default is used:

```
# Config resolution order:
# 1. Per-widget color in otter-bar.conf (if set)
# 2. Theme token from theme.conf (if set)
# 3. Compiled-in default
```

## Configuration

Configuration file location: `~/.config/otter-shell/otter-bar.conf`

Falls back to `/etc/otter-shell/otter-bar.conf` if user config does not exist. A default config is auto-created on first run.

### Format

Flat key-value format with `key = value` syntax. Color fields are optional — omit them to inherit from the theme.

```
# Comments start with hash

# General (all optional, fall back to theme)
# Font loading priority: font_path > theme fonts_font_family > system fallback font
general_height = 32
general_position = top  # top or bottom
general_font_path = ""
general_background_color = "#18182566"
general_foreground_color = "#FFFFFFFF"
general_padding = 8

# Widget layout (comma-separated widget names)
layout_left = "button_menu,workspaces,mpris"
layout_center = "active_window"
layout_right = "system_tray,cpu_load,cpu_temp,memory,network,volume,brightness,battery,power_profiles,falcond,clock"
layout_padding = 8

# Clock settings
clock_enabled = true
clock_text_color = "#FFFFFFFF"
clock_spacer_color = "#7dcfffFF"
clock_background_color = "#18182566"
clock_time_format = "%H:%M"
clock_date_format = "%A, %B %d %Y"

# Workspaces settings
workspaces_enabled = true
# Symbols assigned left-to-right by workspace ID (supports strings of any length)
workspaces_symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
# Examples: Roman numerals, named workspaces, Nerd Font icons
# workspaces_symbols = ["I", "II", "III", "IV", "V"]
# workspaces_symbols = ["Home", "Web", "Code", "Chat", "Media"]
# Use configured symbols instead of compositor-provided workspace names
workspaces_override_names = false
# Hide known empty workspaces; active workspace remains visible
workspaces_hide_empty = false
# workspaces_font_size = 24      # null = 3/4 of bar height
workspaces_text_color = "#565f89FF"
workspaces_background_color = "#18182566"
workspaces_active_text_color = "#FFFFFFFF"
workspaces_active_background_color = "#7aa2f7FF"
workspaces_spacing = 2

# Battery settings (auto-detected via UPower, hidden if no battery)
battery_enabled = true
battery_full_color = "#a6e3a1FF"
battery_charging_color = "#89dcebFF"
battery_normal_color = "#cdd6f4FF"
battery_warning_color = "#f9e2afFF"
battery_critical_color = "#f38ba8FF"
battery_background_color = "#18182566"
battery_warning_level = 30
battery_critical_level = 15

# Brightness settings (auto-detected per display, only shows on internal displays like eDP/LVDS)
brightness_enabled = true
brightness_color = "#e0af68FF"
brightness_background_color = "#18182566"

# Active window settings
active_window_enabled = true
active_window_text_color = "#FFFFFFFF"
active_window_background_color = "#18182566"
active_window_max_width = 600
active_window_show_icon = true

# Button: menu (font_icon takes priority over icon_path)
button_menu_enabled = true
button_menu_icon_path = ""
button_menu_font_icon = "󰹯"
button_menu_icon_color = "#FFFFFFFF"
button_menu_command = "otter-launcher"
button_menu_background_color = "#18182566"
button_menu_padding = 8

# Button: power (font_icon takes priority over icon_path)
button_power_enabled = false
button_power_icon_path = ""
button_power_font_icon = "⏻"
button_power_icon_color = "#FFFFFFFF"
button_power_command = ""
button_power_background_color = "#18182566"
button_power_padding = 3

# Custom button: appears in layouts as button_firefox
button_0_name = "firefox"
button_0_enabled = true
button_0_font_icon = "F"
button_0_command = "firefox"
button_0_padding = 8

# Power profiles settings (font icons, no SVG paths needed)
power_profiles_enabled = true
power_profiles_icon_power_saver = "󱠅"
power_profiles_icon_balanced = "󰄯"
power_profiles_icon_performance = "󰈐"
power_profiles_background_color = "#18182566"

# CPU Load settings
cpu_load_enabled = true
cpu_load_icon = "󰻠"
cpu_load_color = "#89b4faFF"
cpu_load_warning_color = "#f9e2afFF"
cpu_load_critical_color = "#f38ba8FF"
cpu_load_background_color = "#18182566"
cpu_load_warning_threshold = 70
cpu_load_critical_threshold = 90

# CPU Temperature settings
cpu_temp_enabled = true
cpu_temp_icon = "󰔏"
cpu_temp_color = "#a6e3a1FF"
cpu_temp_warning_color = "#f9e2afFF"
cpu_temp_critical_color = "#f38ba8FF"
cpu_temp_background_color = "#18182566"
cpu_temp_warning_temp = 70
cpu_temp_critical_temp = 85

# Memory settings
memory_enabled = true
memory_icon = "󰍛"
memory_color = "#cba6f7FF"
memory_warning_color = "#f9e2afFF"
memory_critical_color = "#f38ba8FF"
memory_background_color = "#18182566"
memory_warning_threshold = 70
memory_critical_threshold = 90

# Network settings
network_enabled = true
network_icon_idle = "󰈀"
network_icon_download = "󰇚"
network_icon_upload = "󰕒"
network_icon_ethernet = "󰈀"
network_icon_wifi_off = "󰤮"
network_icon_wifi_1 = "󰤟"
network_icon_wifi_2 = "󰤢"
network_icon_wifi_3 = "󰤥"
network_icon_wifi_4 = "󰤨"
network_icon_vpn = "󰖂"
network_icon_disconnected = "󰪎"
network_color = "#94e2d5FF"
network_download_color = "#89b4faFF"
network_upload_color = "#f9e2afFF"
network_background_color = "#18182566"
network_click_command = "nm-connection-editor"
network_smoothing_alpha = 40
network_activity_threshold = 10240

# Volume settings (requires PipeWire)
volume_enabled = true
volume_icon_muted = "󰖁"
volume_icon_low = "󰕿"
volume_icon_medium = "󰖀"
volume_icon_high = "󰕾"
volume_color = "#FFFFFFFF"
volume_muted_color = "#f9e2afFF"
volume_background_color = "#18182566"
volume_scroll_step = 5

# Falcond settings (requires falcond daemon)
falcond_enabled = true
falcond_icon_active = "󱠇"
falcond_icon_inactive = "󰻂"
falcond_active_color = "#a6e3a1FF"
falcond_inactive_color = "#6c7086FF"
falcond_background_color = "#18182566"

# MPRIS settings (media player control via D-Bus)
mpris_enabled = true
mpris_icon_playing = "󰐊"
mpris_icon_paused = "󰏤"
mpris_icon_stopped = "󰓛"
mpris_icon_previous = "󰒮"
mpris_icon_next = "󰒭"
mpris_text_color = "#FFFFFFFF"
mpris_background_color = "#18182566"
mpris_progress_color = "#89b4faFF"
mpris_progress_bg_color = "#31324466"
mpris_popup_bg_color = "#1e1e2eEE"
mpris_max_title_width = 300

# System Tray settings (StatusNotifierItem icons via D-Bus)
system_tray_enabled = true
system_tray_icon_size = 18
system_tray_spacing = 12
system_tray_background_color = "#18182566"
system_tray_animation_duration = 750
system_tray_padding = 8
```

### Colors

Colors are specified in hex RGBA format: `#RRGGBBAA`

All color fields are optional. Omit a color to use the theme default from `theme.conf`.

### Available Widgets

- `button_menu` - Launcher button
- `button_power` - Power button
- `button_<name>` - Custom buttons (create via otter-settings or add indexed `button_N_name`, `button_N_enabled`, `button_N_font_icon`, `button_N_command` fields to config)
- `workspaces` - Workspace indicator
- `active_window` - Focused window title
- `cpu_load` - CPU usage percentage with threshold colors
- `cpu_temp` - CPU temperature with threshold colors
- `memory` - Memory usage percentage with threshold colors
- `network` - Network activity indicator with NetworkManager D-Bus integration (connection-aware icons: WiFi signal bars, ethernet, VPN, disconnected; EMA-smoothed activity detection via Device.Statistics byte counters; click menu for WiFi/VPN management)
- `volume` - Audio volume control (requires PipeWire, speaker icon with level-based icons, scroll to adjust volume, middle-click to mute, click for popup with per-device sliders/mute/default selection for outputs and inputs)
- `brightness` - Backlight control for internal displays (scroll to adjust, auto-hidden on external monitors)
- `battery` - Battery status (requires D-Bus)
- `power_profiles` - Power profile selector (requires D-Bus, power-profiles-daemon or tuned-ppd)
- `falcond` - Falcond daemon status (performance mode, profile, VCache status, SCX scheduler)
- `mpris` - Media player status (requires D-Bus, auto-hides when no player, shows album art when available, click to play/pause)
- `system_tray` - StatusNotifierItem icon row (requires D-Bus, click toggle to expand/collapse, left-click activates, right-click context menu via DBusMenu, middle-click secondary activate)
- `clock` - Current time with timezone-aware formatting via zeit, date tooltip on hover, configurable `time_format`/`date_format`, synchronized across all outputs

### Hot Reload

Both `otter-bar.conf` and `theme.conf` are watched via inotify. Changes are detected and applied without restart. Font path changes require a restart.

On startup, otter-bar normalizes the config file (adds missing defaults, strips unknown fields). Custom buttons use indexed dynamic fields (`button_N_*`). Legacy `button_<name>_*` custom button fields are migrated to the indexed form.

## Architecture

otter-bar describes widgets through `otter-ui` frame state and shared widget registries. `otter-ui` owns command emission, popup frame rendering, hit registration, and rasterization through the shared CPU renderer with damage-rect culling.

otter-bar is the main application in the Otter Shell monorepo. It uses the following components as libraries:

- otter-conf - Configuration parsing
- otter-theme - Shared visual theme (colors, spacing, popup styles)
- otter-ui - Widget framework
- otter-wayland - Wayland client library
- otter-render - Font rendering and graphics
- otter-desktop - Desktop integration (icons, D-Bus services, system info)
- otter-geo - Geometry types
- otter-utils - Utilities and logging

## Acknowledgements

otter-bar was originally inspired by [walrus-bar](https://codeberg.org/Elijah-Immer/walrus-bar). Early development drew on many of the same Zig + Wayland patterns and approaches. The codebase has since been substantially rewritten with integer-only color math, fixed-point transforms, data-driven design patterns, and a different architecture, but we appreciate walrus-bar for providing a foundation to learn from.

## License

MIT License — see [LICENSE](LICENSE).
