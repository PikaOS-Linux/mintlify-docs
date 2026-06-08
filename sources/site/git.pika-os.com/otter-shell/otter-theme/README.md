# otter-theme

Shared visual theme library for the Otter desktop shell. Provides semantic color tokens, spacing, popup styles, bar chrome, surface roles, density/radius tokens, dock/logout/window tokens, font tokens, and 12 bundled theme presets. Pure data structs with no I/O. Overrides via `~/.config/otter-shell/theme.conf` with hot-reload handled by consumers.

## Theme Tokens

### Colors

Semantic color palette shared across all otter-shell applications:

| Token | Default | Usage |
|-------|---------|-------|
| `background` | `#080a0fff` | App view background |
| `background_alt` | `#141720ff` | Recessed controls and secondary fills |
| `background_opaque` | `#080a0fff` | Fully opaque base for overlays |
| `foreground` | `#e6e8efff` | Primary text |
| `muted` | `#8b92a3ff` | Secondary/muted text |
| `accent` | `#5e6af2ff` | Focus, links, progress bars, active indicators |
| `active` | `#2d3578ff` | Active/selected background |
| `success` | `#76d49cff` | Battery full, healthy temp |
| `warning` | `#deb86aff` | Battery low, high CPU |
| `critical` | `#d85a68ff` | Battery critical, overheating |
| `charging` | `#78c8d0ff` | Charging/positive-action accent |
| `spacer` | `#7e8699ff` | Decorative spacer (clock colon) |

### Popup

Shared styling for popups, tooltips, and menus:

| Token | Default | Description |
|-------|---------|-------------|
| `background` | `rgba(24,24,37,245)` | Popup background |
| `text` | `#ffffffff` | Popup text |
| `border` | `rgba(69,71,90,255)` | Border color |
| `highlight` | `rgba(69,71,90,255)` | Hover highlight |
| `selected` | `rgba(137,180,250,255)` | Selected item |
| `selected_text` | `#ffffffff` | Text on selected/highlighted items |
| `disabled` | `rgba(108,112,134,255)` | Disabled text |
| `separator` | `rgba(69,71,90,200)` | Menu separator |
| `padding` | `8` | Inner padding (px) |
| `border_width` | `1` | Border width (px) |
| `item_height` | `30` | Menu item height (px) |

### Bar

| Token | Default | Description |
|-------|---------|-------------|
| `height` | `38` | Bar height (px) |
| `padding` | `8` | Bar padding (px) |
| `layout_padding` | `8` | Layout section padding (px) |
| `background` | `#0b0e14ee` | Continuous bar surface |
| `border` | `#252a35aa` | Bar outline |
| `group_background` | transparent | Optional grouped/island surface |
| `item_background` | `#161b24d8` | Widget tile background |
| `item_hover` | `#1a1f2bcc` | Widget hover background |
| `item_active` | `#2e3684ff` | Active widget/workspace background |
| `item_active_text` | `#ffffffff` | Text on active bar items |
| `separator` | `#383d4a80` | Bar separator |

### Spacing

| Token | Default | Description |
|-------|---------|-------------|
| `widget_padding` | `8` | Padding around widgets (px) |
| `widget_h_padding` | `2` | Horizontal padding between widget elements (px) |
| `icon_size` | `18` | Default icon size (px) |
| `item_spacing` | `12` | Spacing between items (px) |

### Fonts

| Token | Default | Description |
|-------|---------|-------------|
| `font_family` | `"Inter"` | Default font family for all apps |
| `tooltip_size` | `14` | Tooltip font size (px) |

### Decorations

| Token | Default | Description |
|-------|---------|-------------|
| `server_side` | `true` | Request compositor-provided decorations for xdg-toplevel windows when supported |

## Configuration

Theme values are loaded from `~/.config/otter-shell/theme.conf` (fallback: `/etc/otter-shell/theme.conf`, then compiled-in defaults). Uses flat key-value format via otter-conf with nested struct flattening:

```conf
# Semantic color palette
colors_background = "#18182566"
colors_foreground = "#ffffffff"
colors_accent = "#89b4faff"
colors_success = "#a6e3a1ff"
colors_warning = "#f9e2afff"
colors_critical = "#f38ba8ff"

# Popup styling
popup_background = "#181825f5"
popup_border = "#45475aff"
popup_padding = 6

# Bar dimensions
bar_height = 32
bar_padding = 8

# Spacing tokens
spacing_widget_padding = 8
spacing_icon_size = 18
spacing_item_spacing = 12

# Font tokens
fonts_font_family = "Inter"
fonts_tooltip_size = 14

# Surface opacity percentage. 95 gives subtle translucency.
transparency_global_alpha = 95

# Surface role tokens
surfaces_view = "#0c0f14ff"
surfaces_surface = "#0e1219ff"
surfaces_surface_alt = "#161b24ff"
surfaces_focus_ring = "#9ab4d8ff"

# Control density/radius tokens
density_control_height = 28
density_control_radius = 4
density_panel_radius = 8

# XDG toplevel decorations
decorations_server_side = true
```

## Theme Presets

12 bundled comptime theme presets in `presets.zig`:

| Preset | Description |
|--------|-------------|
| Otter Shell | Default matte continuous theme |
| Otter Shell Islands | Floating grouped bar preset |
| Catppuccin Mocha | Dark warm |
| Catppuccin Latte | Light warm |
| Catppuccin Frappe | Mid-dark warm |
| Catppuccin Macchiato | Dark warm (deeper) |
| Nord | Arctic blue |
| Gruvbox Dark | Retro dark |
| Gruvbox Light | Retro light |
| Dracula | Purple-tinted dark |
| Tokyo Night | Cool blue dark |
| One Dark | Atom-inspired dark |

```zig
const presets = @import("otter_theme").presets;

// Find a preset by name
if (presets.findPreset("Nord")) |preset| {
    const theme = preset.theme;
}

// Iterate all presets
for (presets.all_presets) |preset| {
    // preset.name, preset.theme
}
```

## Usage

```zig
const otter_theme = @import("otter_theme");
const Theme = otter_theme.Theme;

// Use defaults (Otter Shell theme)
const theme = Theme{};
const bg = theme.colors.background;
const accent = theme.colors.accent;
const icon_size = theme.spacing.icon_size;

// Widget config resolution pattern:
// config.clock.text_color orelse theme.colors.foreground
```

## Theme Loading

Shared theme loading with fallback chain, used by all otter-shell apps:

```zig
const otter_theme = @import("otter_theme");

// Load theme with full fallback: user config -> system config -> defaults
const theme = otter_theme.loadTheme(allocator);

// Load from a specific path
if (otter_theme.loadThemeFromPath(allocator, "/path/to/theme.conf")) |theme| {
    // use theme
}

// Get standard theme config path (~/.config/otter-shell/theme.conf)
var buf: [std.fs.max_path_bytes]u8 = undefined;
if (otter_theme.getThemeConfigPath(&buf)) |path| {
    // use path for inotify watcher, etc.
}
```

## Dependencies

- **otter-geo** - Geometry types
- **otter-render** - Color type
- **otter-conf** - Config parser (used by theme loader)

## Running Tests

```bash
zig build test
```

## License

MIT License — see [LICENSE](LICENSE).
