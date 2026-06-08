# otter-shot

Native Wayland product-shot composer for Otter Shell.

## Features

- Capture focused window, selected window from the live toplevel list, all screens, or a dragged selection.
- Use predefined gradients, a portal-selected wallpaper, or the current `otter-wallpaper` state file as background.
- Adjust padding, corner radius, shadow, border color, and synthetic chrome.
- Export framed PNG to file or clipboard through `wl-copy --type image/png`.

## Requirements

The compositor must expose `ext_image_copy_capture_v1` for capture. Screen and selection capture require output capture source support. Window capture requires foreign toplevel capture source support plus `ext_foreign_toplevel_list_v1`.

## Usage

```bash
zig build run
```

The right inspector owns source, expandable window list, background, frame, options, size, and export controls. Source buttons capture immediately when the required capture path is available; capturable window rows select and capture that window. If the compositor only exposes WLR toplevel metadata without the capture protocol, those rows are shown as metadata-only instead of pretending capture will work. Scroll the inspector when controls exceed the visible height. Click the wallpaper field to open the xdg-desktop-portal file picker. Export PNG opens the portal save picker before writing.

## Desktop integration

The install step places the binary in `bin`, the desktop entry in `share/applications`, and icons in `share/icons/hicolor`.

Desktop assets:

- `data/applications/otter-shot.desktop`
- `data/icons/hicolor/*/apps/otter-shot.png`
- `data/icons/otter-shot-source.png`

## License

MIT License — see [LICENSE](LICENSE).
