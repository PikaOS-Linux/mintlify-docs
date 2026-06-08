# Source: https://git.pika-os.com/otter-shell/otter-pick/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-pick](https://git.pika-os.com/otter-shell/otter-pick)

Watch [1](https://git.pika-os.com/otter-shell/otter-pick/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-pick/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-pick/forks)

You've already forked otter-pick

[**23** Commits](https://git.pika-os.com/otter-shell/otter-pick/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-pick/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-pick/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-pick/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-pick/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-pick/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-pick/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-pick/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-pick/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-pick/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [cb1419dec6](https://git.pika-os.com/otter-shell/otter-pick/commit/cb1419dec65a7c62bede5b0c29cd70e6ca1a9646) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-pick/commit/cb1419dec65a7c62bede5b0c29cd70e6ca1a9646)

2026-06-08 20:23:14 +01:00

[src](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/src 'src')

[Reduce picker redraw damage](https://git.pika-os.com/otter-shell/otter-pick/commit/f945c5eb12c5267ad4166e1678c766db527f3087)

2026-06-07 00:50:27 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-pick/commit/d1663f3e2b85b2f5b68e87079a7de6378f921bbb)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/build.zig 'build.zig')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-pick/commit/d1663f3e2b85b2f5b68e87079a7de6378f921bbb)

2026-06-06 15:14:08 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-pick/commit/cb1419dec65a7c62bede5b0c29cd70e6ca1a9646)

2026-06-08 20:23:14 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/README.md 'README.md')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-pick/commit/d91040c9e19c71696d5e0302aef1d85ff240cc24)

2026-06-07 02:34:41 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-pick

Color picker using the same `ext-image-copy-capture` path as `otter-screenshot`.

```bash
otter-pick                 # frozen overlay, loupe, click to copy hex
otter-pick --x 120 --y 80  # sample signed global Wayland coordinate
otter-pick --x -10 --y 80  # negative coords work for left-of-primary outputs
otter-pick --loupe --x 1 --y 2 # print a 5x5 ANSI loupe for scripted sampling
otter-pick --no-copy       # print only
otter-pick --hex '#336699' # offline conversion/test path
```

Output includes hex, RGB, and OKLCH. Clipboard output goes through the shared Otter clipboard helper; packaged installs shadow `wl-copy` to native `otter-copy`, with `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store` as the unavailable-Wayland fallback.

Config: `~/.config/otter-shell/otter-pick.conf`

```text
copy = true
loupe = false
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-pick/blame/commit/cb1419dec65a7c62bede5b0c29cd70e6ca1a9646/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-pick/src/branch/main/README.md) **79** KiB

Languages

Zig 100%