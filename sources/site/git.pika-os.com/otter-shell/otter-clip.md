# Source: https://git.pika-os.com/otter-shell/otter-clip

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-clip](https://git.pika-os.com/otter-shell/otter-clip)

Watch [1](https://git.pika-os.com/otter-shell/otter-clip/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-clip/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-clip/forks)

You've already forked otter-clip

[**31** Commits](https://git.pika-os.com/otter-shell/otter-clip/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-clip/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-clip/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-clip/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-clip/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-clip/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-clip/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-clip/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-clip/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-clip/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [f78922f9b4](https://git.pika-os.com/otter-shell/otter-clip/commit/f78922f9b475384bd6793a65a1b04a83bb0422d0) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-clip/commit/f78922f9b475384bd6793a65a1b04a83bb0422d0)

2026-06-08 20:23:12 +01:00

[src](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/src 'src')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-clip/commit/89ddc50aff179477807a7fbb23ed8f6b6e92fe13)

2026-06-07 02:34:41 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-clip/commit/ee18a08acf8bebf3fda5c0d5486c558587245b49)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/build.zig 'build.zig')

[Launch local Otter launcher from popup](https://git.pika-os.com/otter-shell/otter-clip/commit/1e7caa633e28da4968184ecc0db668fefba5eff2)

2026-06-06 19:50:50 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-clip/commit/f78922f9b475384bd6793a65a1b04a83bb0422d0)

2026-06-08 20:23:12 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/README.md 'README.md')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-clip/commit/89ddc50aff179477807a7fbb23ed8f6b6e92fe13)

2026-06-07 02:34:41 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-clip

Clipboard manager with bounded Wayland data-control monitoring and native copy/paste CLIs. `otter-copy` and `otter-paste` use Wayland data-control directly. The package also owns and shadows the `wl-copy` and `wl-paste` names, so existing app calls resolve to Otter's native implementation.

```bash
otter-clip daemon          # monitor clipboard selection changes
otter-clip popup           # open Super+V launcher-backed history popup
otter-clip popup query     # open popup with search prefilled
otter-clip list            # print stored history
otter-clip search query    # filter history
otter-clip add some text   # manually append text
otter-clip clear           # clear history
otter-clip pin 0           # pin entry
otter-clip unpin 0
otter-clip select 0        # copy a history entry
otter-copy text            # copy argv text
printf text | otter-copy   # copy stdin
png-tool | otter-copy --type image/png
otter-paste [-n]
wl-copy text               # packaging shadows this name to otter-copy
wl-paste [-n]              # packaging shadows this name to otter-paste
otter-clip --file /tmp/history list
otter-copy --file /tmp/store text
otter-paste --file /tmp/store
```

History defaults to `$XDG_CACHE_HOME/otter-shell/otter-clip-history` (legacy `/tmp/otter-clip-history` is still read when configured) and is capped in memory. `popup` opens `otter-launcher --query "clip ..."`; launcher rows call back into `otter-clip select INDEX` so Enter copies the selected history item. Text offers and common image MIME types are accepted; images are stored as bounded blob files with MIME/path metadata so the launcher can show thumbnails. Clipboard monitor skips password/secret MIME hints before reading data. Wayland data-control does not expose the source app id for copied data, so app-id password-manager filtering is enforced only when a source id is available to the caller.

Config: `~/.config/otter-shell/otter-clip.conf`

```text
# Optional; empty uses $XDG_CACHE_HOME/otter-shell/otter-clip-history
history_path = ""
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-clip/blame/commit/f78922f9b475384bd6793a65a1b04a83bb0422d0/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-clip/src/branch/main/README.md) **164** KiB

Languages

Zig 100%