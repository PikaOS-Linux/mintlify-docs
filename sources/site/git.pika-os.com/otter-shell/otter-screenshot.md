# Source: https://git.pika-os.com/otter-shell/otter-screenshot

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-screenshot](https://git.pika-os.com/otter-shell/otter-screenshot)

Watch [1](https://git.pika-os.com/otter-shell/otter-screenshot/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-screenshot/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-screenshot/forks)

You've already forked otter-screenshot

[**105** Commits](https://git.pika-os.com/otter-shell/otter-screenshot/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-screenshot/branches) [**47** Tags](https://git.pika-os.com/otter-shell/otter-screenshot/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-screenshot/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-screenshot/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-screenshot/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-screenshot/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-screenshot/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-screenshot/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-screenshot/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [6658d2f656](https://git.pika-os.com/otter-shell/otter-screenshot/commit/6658d2f656bc0db45ec0e8255f2a303d141738eb) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-screenshot/commit/6658d2f656bc0db45ec0e8255f2a303d141738eb)

2026-06-08 20:23:07 +01:00

[src](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/src 'src')

[Apply simplify review and trim render deps](https://git.pika-os.com/otter-shell/otter-screenshot/commit/55461ea724ecd67089047aba5385d6a55fd3f335)

2026-06-05 20:12:54 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/.gitignore '.gitignore')

[Add otter screenshot](https://git.pika-os.com/otter-shell/otter-screenshot/commit/b28765c29e8cc50ba816ee750857fa541c2e2536)

2026-05-02 13:16:39 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/build.zig 'build.zig')

[Apply simplify review and trim render deps](https://git.pika-os.com/otter-shell/otter-screenshot/commit/55461ea724ecd67089047aba5385d6a55fd3f335)

2026-06-05 20:12:54 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-screenshot/commit/6658d2f656bc0db45ec0e8255f2a303d141738eb)

2026-06-08 20:23:07 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/README.md 'README.md')

[Commit pending otter-screenshot changes](https://git.pika-os.com/otter-shell/otter-screenshot/commit/8ce7ce82db7ec81fe89c365acfe862be0c72f2e5)

2026-06-07 00:35:14 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

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

Write the PNG to `PATH` instead of copying it to the clipboard.

`--fullscreen`

Capture all outputs immediately.

`--active`

Capture the compositor-reported active toplevel immediately. Requires `ext_foreign_toplevel_list_v1` and `ext_foreign_toplevel_image_capture_source_manager_v1`.

`--freeze`

Capture first, then show that frozen image behind the selector.

`--cursor`

Include the cursor in the captured image.

`--border`

Keep the selection border in region captures. By default the border is only a selection aid.

`--tonemap-hdr`

Apply a simple SDR tonemap before encoding. This is a best-effort fallback for HDR captures, not color-managed output.

`--help`, `-h`

Print usage.

## Clipboard

Clipboard output uses `wl-copy --type image/png`; Otter packages `wl-copy` as its native data-control implementation.

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

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-screenshot/blame/commit/6658d2f656bc0db45ec0e8255f2a303d141738eb/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-screenshot/src/branch/main/README.md) **218** KiB

Languages

Zig 100%