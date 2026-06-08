# otter-ui

Widget framework for the Otter desktop shell. Provides a bounded Surface Description frame API, vtable-based widget lifecycle/input, and concrete widget implementations for status bar components.

## Overview

otter-ui uses compile-time vtable generation to provide a unified `Widget` interface that supports:

- Required operations: `draw`, `deinit`, `setArea`, `getWidth`
- Optional handlers: `motion`, `leave`, `click`, `scroll`, `getPopupSupport`

Widgets that implement optional handlers automatically have them wired into the vtable; those that don't get `null` function pointers that the dispatcher skips.

App code describes nodes into a `UiState`. `UiFrame` handles integer layout, command emission, hit regions, overlay ordering, uniform-list visible ranges, and rasterization handoff to `otter-render`.

## Surface Description

`UiState` owns per-frame bounded arrays and the internal `DefaultCommandList`. App draw paths should keep one state value and describe a frame:

```zig
const caps = ui.ui_frame.Capacities{ .elements = 64, .hit_regions = 64, .overlays = 8 };
var state: ui.UiState(caps) = .{};

var frame = state.begin(.{
    .viewport = .{ .x = 0, .y = 0, .width = width, .height = height },
    .scale = surface.scale,
    .font = font,
});

const children = [_]ui.SurfaceNode{
    ui.SurfaceNode.label(ui.SurfaceId.namedComptime("title"), "Settings", 18, null),
    ui.SurfaceNode.button(ui.SurfaceId.namedComptime("save"), "Save"),
};
const root = ui.SurfaceNode{
    .id = ui.SurfaceId.namedComptime("root"),
    .kind = .column,
    .layout = .{ .width = .fill, .height = .fill, .gap = 8, .padding = ui.Padding.uniform(12) },
    .children = &children,
};

_ = try frame.render(&root, frame.viewport);
try frame.finish();

// Rasterization still uses otter-render's CPU command path.
render.quad_renderer.rasterize(ui.render.DefaultCommandList, &state.commands, surface, null, null, true);
```

`UiState.hitTest(point)` returns the topmost `HitRegion`. `HitRegion.data` carries caller payloads such as list indices, so apps do not need parallel hit arrays or y-coordinate math.

`FieldRegistry(Owner, specs)` centralizes name-based widget dispatch for app-owned optional widget fields. `NamedWidgetList(Owner, spec)` does the same for bounded arrays of dynamic named widgets such as `button_menu`. Containers provide comptime specs once, then use the registries for lookup, preferred width, area forwarding, hit testing, popup enumeration, lifecycle calls, damage collection, full-redraw marking, and frame dispatch. This keeps app layouts from building low-level command/draw lists or duplicating widget traversal logic.

`UniformList` provides visible range, scroll-to-selected, content height, and hit-index helpers for large fixed-row lists without heap allocation:

```zig
const list = ui.UniformList{
    .item_count = result_count,
    .item_height = row_height,
    .viewport_height = list_rect.height,
    .scroll_offset = scroll_offset,
};
const range = list.visibleRange();
```

## VTable Polymorphism Pattern

Every widget embeds a `Widget` struct and implements the required methods:

```zig
const MyWidget = struct {
    widget: Widget,
    // ... widget-specific fields

    pub fn draw(self: *MyWidget, cmds: *CmdList, clip: Rect) !void {
        // record draw commands into CommandList
    }

    pub fn deinit(self: *MyWidget) void {
        // cleanup
    }

    pub fn setArea(self: *MyWidget, area: Rect) void {
        self.widget.area = area;
    }

    pub fn getWidth(self: *MyWidget) u31 {
        return 100; // preferred width
    }

    // Optional: implement for mouse interaction
    pub fn click(self: *MyWidget, button: MouseButton) void {
        // handle click
    }
};
```

Initialize the widget by generating its vtable at comptime:

```zig
var my_widget = MyWidget{
    .widget = .{
        .vtable = Widget.generateVTable(MyWidget),
        .area = area,
    },
    // ...
};
```

## Available Widgets

| Widget | Description |
|--------|-------------|
| `Clock` | Time display with timezone-aware formatting via zeit, tooltip with date (strftime), configurable `time_format`/`date_format`, 12-hour format detection, global minute tracking for multi-output sync |
| `Battery` | Battery status via UPower D-Bus service (requires D-Bus) |
| `Brightness` | Backlight control with icon display, tooltip, and scroll-to-adjust |
| `Button` | Clickable icon button with command execution |
| `Workspaces` | Workspace indicator/switcher via otter-tag, Mango/dwl IPC, or ext-workspace, displays workspace names from protocol when available (falls back to configured symbol strings assigned left-to-right by ID), `override_names` forces configured symbols over protocol names, optional `hide_empty`, variable-width per workspace |
| `ActiveWindow` | Focused window title via foreign-toplevel protocol |
| `PowerProfiles` | Power profile selector with tooltip and dropdown menu (requires D-Bus) |
| `CpuLoad` | CPU usage percentage with threshold-based colors |
| `CpuTemp` | CPU temperature with threshold-based colors |
| `Memory` | Memory usage percentage with threshold-based colors |
| `Network` | Network activity indicator with connection-aware icons (WiFi signal bars, ethernet, VPN, disconnected), EMA-smoothed rate detection via NM Device.Statistics byte counters, rich tooltip with per-adapter info, and click menu for WiFi/VPN management via NetworkManager D-Bus |
| `Falcond` | Falcond daemon status (performance mode, profile, VCache, SCX scheduler) |
| `Volume` | Audio volume control via PipeWire with level-based speaker icons, scroll-to-adjust, custom popup with output/input device sections, per-device sliders with drag support, mute toggles, and default device selection |
| `Mpris` | Media player status via MPRIS D-Bus (requires D-Bus, album art + title/artist, click to play/pause) |
| `SystemTray` | StatusNotifierItem icon row with animated expand/collapse, XDG icon theme lookup with ARGB32 pixmap conversion to Image (unified box-filter pipeline), DBusMenu context menus, and configurable icon spacing/padding (requires D-Bus) |

## Core Components

| Component | Description |
|-----------|-------------|
| `Widget` | Base interface with vtable dispatch |
| `FieldRegistry` | Comptime registry for app-owned widget fields: lookup, hit testing, area forwarding, popup enumeration, lifecycle calls, damage collection, and frame dispatch |
| `NamedWidgetList` | Comptime registry for bounded arrays of prefixed dynamic widgets, used for config-driven/custom widget lists |
| `UiState` / `UiFrame` | Bounded Surface Description frame state: layout, hit registry, overlays, and internal command sink |
| `hitTestRect` | Shared half-open rect hit test for app input handlers that still consume explicit draw-result rectangles |
| `UniformList` | Fixed-row visible range, scroll-to-selected, content height, and hit-index helper |
| Surface component specs | Specs for button, icon button, text input with preedit/cursor, checkbox, toggle, slider, number input, select, progress, tabs, list row, form row, section header, color swatch, and color picker |
| `Container` | Layout manager for horizontal/vertical child arrangement |
| `TextBox` | Text rendering with font scaling and UTF-8 support |
| `Tooltip` | Reusable tooltip popup with configurable styling |
| `PopupMenu` | Dropdown menu with item selection, highlighting, and position-aware submenus (`open_upward` for bottom bars) |
| `HoverState` | Tracks hover timing for tooltip delays |
| `PopupSupport` | Generic interface for widgets with popup capabilities (supports `custom_popup_visible` flag for widgets with custom popup overlays) |
| `Slider` | Reusable horizontal slider component with rendering and hit-testing (used by Volume widget popup) |
| `InputBuffer` | Comptime-generic UTF-8 text input buffer with cursor (insert at cursor, backspace, forward delete, word delete, cursor movement, selection, IME preedit/commit) |
| `ScrollState` | Pure stateless scroll tracking: offset clamping, thumb rect calculation, hit-testing, content/viewport sizing |
| `icons` | Embedded MIT-licensed Tabler SVG icons for semantic built-in widgets and optional custom bar buttons via `svg_icon` |
| `drawing` | Stateless component primitives used inside frame-routed widgets and controls (panel, control, border, inputBox, wrappingInputBox, toggle, checkbox, colorSwatch, dropdown, dropdownOverlay, tabBar, scrollbar, formRow, sectionHeader, button, numberInput, progressBar, iconButton, textTruncated, wrappedText, colorPickerPopup, etc.) |
| `IconImageCache` | Comptime-generic fixed-slot icon image cache with XDG theme lookup, absolute path resolution (with extension and basename fallback), and negative caching |
| `DynamicIconImageCache` | HashMap-backed icon image cache with optional target size loading and LRU eviction, same lookup/caching behavior as `IconImageCache` (for launcher and other bounded use cases) |

## Usage

```zig
const ui = @import("otter_ui");

// Create a clock widget
var clock = ui.Clock.init(area, .{
    .text_color = ui.Color.white,
    .font = font,
});

// Use container for layout
var container = ui.Container.init(.{
    .direction = .horizontal,
    .gap = 5,
    .padding = ui.Padding.uniform(10),
});
try container.addChild(&clock.widget);
```

## Input Buffer

Generic UTF-8 text input buffer with cursor support and configurable capacity:

```zig
const ui = @import("otter_ui");

// Default 256-byte buffer
var buf: ui.DefaultInputBuffer = .{};

// Or custom capacity
var large_buf: ui.InputBuffer(1024) = .{};

buf.appendUtf8("hello");   // Insert UTF-8 text at cursor
const text = buf.text();   // Get current text slice
buf.backspace();           // Delete codepoint before cursor
buf.deleteForward();       // Delete codepoint after cursor
buf.deleteWord();          // Delete word before cursor (Ctrl+W)
buf.moveCursorLeft();      // Move cursor left one codepoint
buf.moveCursorRight();     // Move cursor right one codepoint
buf.moveCursorHome();      // Move cursor to start
buf.moveCursorEnd();       // Move cursor to end
buf.clear();               // Clear all text

// Cursor position
const pos = buf.cursor_pos;  // Byte offset into buffer

// IME support
buf.setPreedit("にほ");    // Set in-progress composition
const p = buf.preedit();   // Get preedit text slice
buf.commitText("日本");    // Insert IME-committed text at cursor (clears preedit)
buf.clearPreedit();        // Clear preedit without committing
```

## Scroll State

Pure stateless scroll tracking for scrollable content areas:

```zig
const ui = @import("otter_ui");

var scroll: ui.ScrollState = .{};

// Set content and viewport dimensions
scroll.content_height = total_content_height;
scroll.viewport_height = visible_area_height;

// Scroll by delta (returns true if offset changed)
if (scroll.scroll(delta_pixels)) {
    // Trigger redraw
}

// Check if scrollbar needed
if (scroll.needsScrollbar()) {
    const thumb = scroll.thumbRect(track_area);
    // Draw scrollbar thumb
}
```

## Benchmarks

```bash
cd /home/ferreo/otter-shell/otter-ui/benchmarks
zig build -Doptimize=ReleaseFast -Dcpu=x86_64_v3 bench
```

Benchmarks cover static tree layout, dynamic rows, settings-like forms with text inputs, component button grids, list rows, number/select/color-picker controls, hit lookup, overlay flush, and `UniformList` visible-range helpers.

## Icon Image Cache

Caches loaded icon images by name with XDG theme lookup. Caches both hits and misses (missing icons return `null` without re-scanning directories).

Two implementations:
- `IconImageCache(N)` - Fixed-slot array, zero heap overhead (for bar widgets with bounded icon sets)
- `DynamicIconImageCache` - HashMap-backed with optional target size loading and LRU eviction (for launcher). `init(allocator, target_size, max_entries)` — `target_size=0` loads at native resolution, `max_entries=0` disables eviction

```zig
const ui = @import("otter_ui");

// Fixed-slot cache (default 128 slots, for bar widgets)
var cache = ui.DefaultIconImageCache.init(allocator);
defer cache.deinit();

// Or custom slot count
var large_cache = ui.IconImageCache(256).init(allocator);

// Dynamic cache with target size and LRU eviction (for launcher)
// target_size=64 loads icons at 64px, max_entries=96 caps memory usage
var dyn_cache = ui.DynamicIconImageCache.init(allocator, 64, 96);
defer dyn_cache.deinit();

// Lookup by icon name (resolved via otter-desktop findIcon)
if (cache.getOrLoad("firefox")) |image| {
    image.drawScaled(surface, rect);
}

// Also accepts absolute paths (tries exact, then common extensions, then basename theme lookup)
if (cache.getOrLoad("/usr/share/pixmaps/app.png")) |image| {
    // ...
}

// Handles .desktop files with full icon paths that may no longer exist
// e.g. Icon=/home/user/Downloads/app/icon.png → tries path, extensions, then theme lookup for "icon"
if (cache.getOrLoad("/some/path/com.example.app")) |image| {
    // Falls back to theme lookup for "com.example.app"
}
```

## Popup Components

Tooltip and PopupMenu are reusable building blocks for widgets that need overlays:

```zig
const popup = @import("otter_ui").popup;

// Tooltip for hover information
var tooltip = popup.Tooltip{};
tooltip.style = .{
    .background_color = Color.init(30, 30, 46, 230),
    .text_color = Color.white,
};
tooltip.setText("Hover text here");
tooltip.show(anchor_point);

// Draw tooltip (typically in overlay pass)
tooltip.draw(surface, font, font_size, screen_bounds);

// PopupMenu for dropdown selection
var menu = popup.PopupMenu{};
menu.style = .{ .item_height = 28 };
menu.open_upward = true;  // for bottom-positioned bars (submenus grow upward)
_ = menu.addItem("Option 1", 0);
_ = menu.addItemSelected("Option 2", 1, true);  // selected item
menu.on_select = myCallback;
menu.callback_ctx = context;
menu.toggle(widget_area);

// HoverState for tooltip timing
var hover = popup.HoverState{};
hover.enter();  // call on mouse enter
if (hover.hasHoveredFor(popup.HoverState.default_tooltip_delay_ms)) {
    // Show tooltip after 300ms
}
hover.leave();  // call on mouse leave
```

## PopupSupport Interface

Widgets that support popups can implement `getPopupSupport()` to expose their popup components through a unified interface. This allows containers/bars to query any widget for popup support without knowing its concrete type:

```zig
const popup = @import("otter_ui").popup;

// In your widget implementation
pub fn getPopupSupport(self: *MyWidget) ?popup.PopupSupport {
    return popup.PopupSupport{
        .tooltip = &self.tooltip,      // optional, null if no tooltip
        .menu = &self.menu,            // optional, null if no menu
        .font = self.config.font,
        .font_size = self.config.font_size,
        .widget_area = self.widget.area,
        .frame_request = self.frame_request,
    };
}
```

The container can then query popup state uniformly:

```zig
// Query any widget for popup support
if (widget.getPopupSupport()) |support| {
    if (support.shouldShowTooltip()) {
        // Render tooltip using support.tooltip, support.font, etc.
    }
    if (support.isMenuOpen()) {
        // Render menu using support.menu
    }

    // Get positioning info
    const center_x = support.getCenterX();

    // Hide all popups
    support.hideAll();

    // Request redraw
    support.requestFrame();
}
```

## Running Tests

```bash
cd otter-ui
zig build test
```

## Shared Auth Surface

`auth_input.zig`, `auth_theme.zig`, and `auth_surface.zig` provide shared password/IME input state, resolved visual tokens, layout, drawing, and hit testing for lock and greeter auth panels. `otter-lock` keeps same user-facing layout while routing through this shared surface.

## Dependencies

- `otter-geo` - Geometry types (Rect, Point, Padding)
- `otter-render` - Font rendering and surface operations
- `otter-wayland` - Wayland protocol bindings
- `otter-utils` - Logging and BoundedArray
- `otter-desktop` - Icon lookup, system info, and optionally D-Bus services (UPower, MPRIS, SystemTray, PowerProfiles)
- `zeit` - Native Zig timezone-aware date/time library (replaces C time.h/locale.h)

## Third-party licenses

Otter Shell code is MIT — see [LICENSE](LICENSE). Bundled assets:

- **Tabler Icons** — MIT — `src/icons/tabler/LICENSE`

## License

MIT License — see [LICENSE](LICENSE).
