# otter-settings

A graphical configuration editor and theme browser for Otter Shell, written in Zig.

## Features

- Tab-based UI for editing all Otter Shell application configs (bar, launcher, notifications, wallpaper, OSD, Jade, logout, polkit, lock, idle, dock, terminal, theme-gen, recorder, voice)
- Voice tab with voice selection and a playback test box for `otter-vox`
- Theme browser with live preview of all 12 built-in presets
- Search field on config pages with key, label, value, and section matching
- Runtime-only collapsed advanced sections for noisy config groups; search still scans advanced fields
- Section-grouped form fields with type-aware controls (toggles, color swatches, dropdowns, number steppers, text inputs)
- Layout editor with drag-and-drop chip UI for widget arrangement
- Custom button creation and deletion for otter-bar
- Clipboard paste support (Ctrl+V) in all text inputs via Wayland data device protocol
- Hot-reload: saved changes are picked up by running apps via inotify
- Config preservation: saves directly from ConfigDoc, preserving comments, field order, and custom fields

## Architecture

| File | Purpose |
|------|---------|
| `main.zig` | Entry point, Wayland setup, event loop |
| `app.zig` | Settings struct, lifecycle (init/deinit, config load/save, tab switching) |
| `input_handlers.zig` | Pointer/keyboard callbacks, field click handling, edit key dispatch |
| `draw.zig` | DrawContext struct, DrawResult, Surface Description frame orchestration, anchored overlays |
| `draw_form.zig` | Config form rendering, shared row/text-input components, field controls, row height calculation |
| `draw_chips.zig` | Layout/array chip rendering, measurement, drag indicators |
| `draw_sidebar.zig` | Sidebar tabs, toolbar (Apply/Reset buttons) |
| `draw_helpers.zig` | Color parsing (delegates to otter-render Color.parseHex) |
| `editor.zig` | ConfigDoc (parsed config with comments), field type detection, layout helpers |
| `tabs.zig` | Tab definitions, section prefix mapping, field-to-section routing |
| `config.zig` | Config directory resolution, path helpers |
| `theme_browser.zig` | Theme preset browser struct, state management, re-exports sub-modules |
| `theme_draw.zig` | Theme browser/editor rendering with UniformList/UniformGrid visible ranges |
| `theme_fields.zig` | Theme field introspection metadata (sections, field kinds, offsets) |
| `layout_helpers.zig` | Widget layout utilities for drag-and-drop chip management |
| `display_names.zig` | Human-readable field name formatting |

## Dependencies

### Required
- Zig 0.16.0
- wayland-client
- FreeType2
- xkbcommon

### Otter Shell Libraries
- otter-wayland (Wayland connection, keyboard, clipboard)
- otter-render (font rendering, command list, shaped text path)
- otter-ui (Surface Description frame API, shared controls, overlays, scroll state, input buffer)
- otter-conf (config parser/serializer)
- otter-config-types (typed config struct definitions)
- otter-theme (theme presets and definitions)
- otter-geo (geometry types)
- otter-utils (logging)

## Build

```bash
zig build        # build only
zig build run    # build and run
zig build test   # run tests
```

## Configuration

Reads and writes configs in `~/.config/otter-shell/`:
- `otter-bar.conf`, `otter-launcher.conf`, `notifications.conf`, `otter-wallpaper.conf`, `otter-osd.conf`, `otter-jade.conf`, `otter-logout.conf`, `otter-polkit.conf`, `otter-lock.conf`, `otter-idle.conf`, `otter-dock.conf`, `otter-term.conf`, `otter-theme-gen.conf`, `otter-rec.conf`, `otter-vox.conf`
- `theme.conf` for shared visual theme

Falls back to `/etc/otter-shell/` for system-wide defaults.

## Desktop Integration

The install step places:
- `data/applications/otter-settings.desktop`
- `data/icons/hicolor/*/apps/otter-settings.png`
- `data/icons/otter-settings-source.png`

## License

MIT License — see [LICENSE](LICENSE).
