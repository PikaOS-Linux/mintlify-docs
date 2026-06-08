# Source: https://git.pika-os.com/otter-shell/otter-shot/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-shot](https://git.pika-os.com/otter-shell/otter-shot)

Watch [1](https://git.pika-os.com/otter-shell/otter-shot/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-shot/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-shot/forks)

You've already forked otter-shot

[**70** Commits](https://git.pika-os.com/otter-shell/otter-shot/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-shot/branches) [**26** Tags](https://git.pika-os.com/otter-shell/otter-shot/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-shot/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-shot/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-shot/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-shot/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-shot/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-shot/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-shot/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [70c71347c0](https://git.pika-os.com/otter-shell/otter-shot/commit/70c71347c0dabf2318426556c7fce50feced709a) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-shot/commit/70c71347c0dabf2318426556c7fce50feced709a)

2026-06-08 20:23:09 +01:00

[data](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/data 'data')

[Add otter-shot desktop assets](https://git.pika-os.com/otter-shell/otter-shot/commit/f7a9dc3009ef000a0b88b34da48e7d94523d1dd0)

2026-05-21 18:17:35 +01:00

[src](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/src 'src')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-shot/commit/f43afe285c61b5c8e97a09ff5f1c09aa659e7389)

2026-06-07 02:34:41 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/.gitignore '.gitignore')

[initial release](https://git.pika-os.com/otter-shell/otter-shot/commit/d4fb047604a135a725ec10166a96121c04378823)

2026-05-21 17:48:25 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/build.zig 'build.zig')

[Add otter-shot desktop assets](https://git.pika-os.com/otter-shell/otter-shot/commit/f7a9dc3009ef000a0b88b34da48e7d94523d1dd0)

2026-05-21 18:17:35 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-shot/commit/70c71347c0dabf2318426556c7fce50feced709a)

2026-06-08 20:23:09 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/README.md 'README.md')

[Add otter-shot desktop assets](https://git.pika-os.com/otter-shell/otter-shot/commit/f7a9dc3009ef000a0b88b34da48e7d94523d1dd0)

2026-05-21 18:17:35 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

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

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-shot/blame/commit/70c71347c0dabf2318426556c7fce50feced709a/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-shot/src/branch/main/README.md) **1.6** MiB

Languages

Zig 100%