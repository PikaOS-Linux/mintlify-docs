# otter-screenshot

`otter-screenshot` is a Wayland screenshot tool for Otter Shell. It captures a selected region by default, copies the result as `image/png`, and can also save directly to a file.

The tool is built for compositors that expose `ext_image_copy_capture_v1` output capture. It does not use X11 screenshot APIs, grim, or external capture tools.

## Usage

Run without arguments to select a region:

```bash
otter-screenshot
```

Drag with the left mouse button to choose an area. Press `Esc` or `Ctrl+C` before selecting to close without taking a screenshot. The screenshot is copied to the clipboard. The cursor is hidden from the capture unless `--cursor` is set.

Save a selected region to a file:

```bash
otter-screenshot --output screenshot.png
```

Capture every output without opening the selector:

```bash
otter-screenshot --fullscreen --output screenshot.png
```

Capture the current active toplevel without opening the selector:

```bash
otter-screenshot --active --output active.png
```

Freeze the screen before selecting a region:

```bash
otter-screenshot --freeze --output region.png
```

Freezing is useful when the thing you want to capture would disappear while you are dragging a selection.

## Options

`--output PATH`, `-o PATH`
: Write the PNG to `PATH` instead of copying it to the clipboard.

`--fullscreen`
: Capture all outputs immediately.

`--active`
: Capture the compositor-reported active toplevel immediately. Requires `ext_foreign_toplevel_list_v1` and `ext_foreign_toplevel_image_capture_source_manager_v1`.

`--freeze`
: Capture first, then show that frozen image behind the selector.

`--cursor`
: Include the cursor in the captured image.

`--border`
: Keep the selection border in region captures. By default the border is only a selection aid.

`--tonemap-hdr`
: Apply a simple SDR tonemap before encoding. This is a best-effort fallback for HDR captures, not color-managed output.

`--help`, `-h`
: Print usage.

## Clipboard

Clipboard output uses `wl-copy --type image/png`; Otter packages `wl-copy` as its native
data-control implementation.

File output does not need clipboard access.

## Building

From this component directory:

```bash
zig build
zig build test
```

Run from source with:

```bash
zig build run -- --output screenshot.png
```

Use Zig 0.16.0. The build links against `wayland-client` and the local `otter-render` and `otter-wayland` packages.

## Notes

The compositor must support image-copy capture for outputs. If it does not, `otter-screenshot` exits with an error instead of falling back to another capture path. Active-window capture additionally requires foreign-toplevel image capture support.

Multi-output screenshots are composed into one image using the compositor's output layout where available. If layout positions are not reported distinctly, outputs are placed side by side.

## License

MIT License — see [LICENSE](LICENSE).
