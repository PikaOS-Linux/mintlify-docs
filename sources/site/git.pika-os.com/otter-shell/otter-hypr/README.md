# otter-hypr

Hyprland Lua layout (`otter-float`) + native Otter layer-shell titlebar companion (`otter-hypr-titlebar`).

**Status:** v1 complete (full event loop, real IPC socket2/hyprctl paths, per-monitor overlays, shaped input, CommandList draw + text, drag, min/restore, theme watcher, etc). See design spec for details.

Provides GNOME/KDE-like freeform + snap behavior for Hyprland workspaces while keeping windows layout-managed. Titlebars are drawn as overlay layer-shell surfaces using Otter's theme and render stack. Commands are sent back to the layout via Hyprland's `hl.dsp.layout(...)` surface.

## Components

- `lua/otter_hypr_layout/` — pure Lua custom layout package. Registers `lua:otter-float`.
- `otter-hypr-titlebar` — Zig binary. Layer-shell overlays, Hyprland socket2 IPC, hit-tested titlebar buttons and drag, theme hot-reload.

## Non-Goals (v1)

- No C++ Hyprland plugin.
- No custom resize handles (use Hyprland border resize).
- No dock/taskbar for minimized windows.
- Minimize uses special workspace `special:otter-minimized`.
- True fullscreen is Hyprland-owned and hides titlebars.

## Build

```bash
cd otter-hypr
zig build
zig build test
```

## Run (titlebar companion)

```bash
cd otter-hypr
zig build run
# with debug dump
zig build run -- --dump-state
```

The titlebar binary must run under a Hyprland session (`HYPRLAND_INSTANCE_SIGNATURE` required).

## Lua Package Install

Copy the `lua/otter_hypr_layout` tree into your Hyprland Lua path, e.g.:

```bash
mkdir -p ~/.config/hypr/lua
cp -r lua/otter_hypr_layout ~/.config/hypr/lua/
```

Or after `zig build`, the installed copy lives under `zig-out/share/otter-hypr/lua/otter_hypr_layout`.

## Usage In Hyprland Config

See `examples/hyprland.lua` for a full snippet.

Minimal:

```lua
package.path = os.getenv("HOME") .. "/.config/hypr/lua/?.lua;"
  .. os.getenv("HOME") .. "/.config/hypr/lua/?/init.lua;"
  .. package.path

local otter = require("otter_hypr_layout")
otter.setup({ layout_name = "otter-float" })

hl.config({
  general = {
    layout = "lua:otter-float",
    border_size = 2,
    resize_on_border = true,
    extend_border_grab_area = 8,
  },
})

hl.bind("SUPER + SHIFT + M", hl.dsp.layout("otter:restore-last"))
```

## Config (titlebar)

`~/.config/otter-shell/otter-hypr.conf` (no auto-write/normalize in v1):

```
enabled = true
layout_name = otter-float
titlebar_height = 28
button_order_left =
button_order_right = minimize,maximize,close
font_size = 13
socket_poll_fallback_ms = 500
titlebar_exclude_class = org.gnome.Nautilus,steam
titlebar_exclude_title = Picture-in-Picture
```

Theme tokens from `otter-theme` (decorations_*) control visuals. Set `OTTER_HYPR_TITLEBAR_HEIGHT` to override both the Zig titlebar companion and Lua layout height from one source.

## Commands (via hyprctl)

```bash
hyprctl dispatch 'hl.dsp.layout("otter:dump-state")'
hyprctl dispatch 'hl.dsp.layout("otter:restore-last")'
hyprctl dispatch 'hl.dsp.layout("otter:toggle-maximize active")'
```

## Theme Tokens Used

See design spec. Uses `decorations_titlebar_*`, `decorations_button_*` etc. from existing Otter theme.

## Limitations (v1)

- Without `OTTER_HYPR_TITLEBAR_HEIGHT`, Lua package and titlebar height must be kept in sync manually.
- CSD clients may need denylist in config.
- Drag uses native Hyprland move (fallback paths exist if address-targeted relative moves are rejected by layout).
- Restore requires explicit keybind or `hyprctl`; no shelf UI yet.

## References

- Design: `docs/superpowers/specs/2026-06-04-otter-hypr-layout-design.md`
- Plan: `docs/superpowers/plans/2026-06-04-otter-hypr-layout.md`

## License

MIT License — see [LICENSE](LICENSE).
