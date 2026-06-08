# otter-launcher

Wayland application launcher for the Otter desktop shell. Displays a centered overlay with a search box and scrollable application list. Similar to fuzzel/rofi/wofi but built on the otter-shell library stack.

## Features

- **Layer shell overlay** - Appears on the focused output via `zwlr_layer_shell_v1`
- **Keyboard input** - xkbcommon-based text input with key repeat
- **IME support** - Japanese, Chinese, Korean, and compose-key input via `zwp_text_input_v3` with inline preedit display
- **Application search** - Case-insensitive filtering by name, ID, and keywords
- **Launcher extensions** - `=EXPR`/`calc EXPR` copies calculator results; `:QUERY`/`emoji QUERY` copies emoji
- **Icon display** - SVG and raster icon rendering via XDG icon theme lookup
- **Mouse support** - Hover selection, click to launch, scroll, right-click to close
- **Terminal detection** - Auto-detects terminal emulator for `Terminal=true` entries
- **HiDPI support** - Correct scaling on high-DPI displays
- **Dim overlay** - Full-screen semi-transparent backdrop using `wp_viewporter` (1x1 pixel buffer, ~4 bytes)
- **Configurable** - Colors, sizes, fonts, and layout via config file
- **Single instance** - Socket-based enforcement prevents duplicate overlays; new invocation closes existing launcher
- **One-shot process** - Starts, shows launcher, exits after launch or Escape

## Usage

```bash
# Build and run
zig build run

# Or install and run directly
zig build
./zig-out/bin/otter-launcher
```

Launcher extensions appear above application matches:

```text
=2+3*4       # Enter copies the calculated result through otter-calc
calc 2+3*4   # same calculator extension
:pushpin     # Enter copies the first matching emoji through Otter clipboard
emoji heart  # searchable emoji extension
clip         # clipboard history rows from otter-clip.conf history_path
clip query   # searchable clipboard history extension
```

Bind to a key in your compositor config, e.g. for Hyprland:
```
bind = $mainMod, D, exec, otter-launcher
```

## Configuration

Config file: `~/.config/otter-shell/otter-launcher.conf`

A default config is created automatically on first run.

```conf
# Launcher size as percentage of screen
width_percent = 30
height_percent = 35

# Dimensions
border_width = 2
icon_size = 32
item_height = 48
input_height = 40
font_size = 16

# Font (empty = use theme fonts_font_family, then system fallback font)
font_path = ""

# Placeholder text shown when search is empty
placeholder_text = " Search applications..."

# Optional color overrides (null = inherit from theme.conf)
# background_color = "#1e1e2eee"
# input_background_color = "#313244ff"
# input_text_color = "#cdd6f4ff"
# border_color = "#89b4faff"
# selected_name_color = "#ffffffff"        # text on highlighted item (default: theme popup.selected_text)
# selected_description_color = "#ffffffff" # description on highlighted item (default: theme popup.selected_text)

# overlay_color always has a concrete default
overlay_color = "#1b1b1b99"
```

Colors resolve through the theme system: most color fields are `?Color = null` and inherit from `theme.conf` via `resolve(raw, theme) → ResolvedConfig`. Padding and item_padding come exclusively from the theme (`popup.padding` and `spacing.widget_padding`).

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Escape | Close launcher |
| Enter | Launch selected application |
| Up / Down | Move selection |
| Tab / Shift+Tab | Next / previous |
| Page Up / Page Down | Scroll by page |
| Home / End | Jump to first / last |
| Ctrl+U | Clear search |
| Ctrl+W | Delete last word |
| Backspace | Delete character |

During IME composition (preedit active), Escape and Enter are suppressed to allow the IME to handle candidate selection/cancellation. Navigation keys (Up/Down/Tab) still work during composition.

## Terminal Detection

For desktop entries with `Terminal=true`, the launcher auto-detects an available terminal:

1. `$TERMINAL` environment variable (checked first)
2. Probes known terminals in `$PATH`: `xdg-terminal-exec`, `foot`, `otter-term`, `ghostty`, `kitty`, `alacritty`, `wezterm`, `rio`, `contour`, `gnome-terminal`, `konsole`, `xfce4-terminal`, `mate-terminal`, `tilix`, `xterm`

Each terminal uses its correct exec flag (`-e`, `--`, `start --`, etc.).

## Architecture

```
main.zig      - Wayland setup, event loop, input handling, overlay, IME integration, UiState rasterize
config.zig    - Config parsing via otter-conf
input.zig     - Text buffer and key-to-action mapping (IME-aware)
app_cache.zig - Application list with sorted entries and icon resolution
draw.zig      - Surface Description frame (panel stack, TextInputSpec, UniformList result rows)
extensions.zig - Fixed-buffer calculator and emoji launcher extension results
```

Rendering uses `otter-ui` Surface Description: `draw.zig` describes nodes into `LauncherUiState`, then `main.zig` asks the state to rasterize through the shared CPU renderer. Hit-testing uses `UiState.hitTest()` payloads instead of app-local row y-coordinate math.

The overlay uses `wp_viewporter` when available to render a full-screen dim backdrop with a single 1x1 pixel SHM buffer (~4 bytes). Falls back to a full-size buffer at scale 1 on compositors without viewporter support.

## Running Tests

```bash
zig build test
```

## Dependencies

- **otter-wayland** - Wayland connection, layer shell, seat/keyboard, SHM buffers
- **otter-render** - Font rendering, image loading, surface operations
- **otter-desktop** - Application list, desktop entry parsing, icon lookup, launcher
- **otter-conf** - Config file parsing
- **otter-theme** - Shared visual theme (colors resolve from theme when not overridden)
- **otter-ui** - Surface Description frame API, TextInputSpec, UniformList, InputBuffer, DynamicIconImageCache
- **otter-tools-core** - Shared calculator and emoji search logic
- **otter-geo** - Geometry types
- **otter-utils** - BoundedArray, logging

### System Libraries
- wayland-client
- xkbcommon

### Not Linked
- No D-Bus (basu/systemd) dependency
- No PipeWire dependency

## License

MIT License — see [LICENSE](LICENSE).
