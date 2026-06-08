# Source: https://git.pika-os.com/otter-shell/otter-emoji/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-emoji](https://git.pika-os.com/otter-shell/otter-emoji)

Watch [1](https://git.pika-os.com/otter-shell/otter-emoji/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-emoji/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-emoji/forks)

You've already forked otter-emoji

[**21** Commits](https://git.pika-os.com/otter-shell/otter-emoji/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-emoji/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-emoji/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-emoji/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-emoji/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-emoji/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-emoji/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-emoji/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-emoji/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-emoji/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [a9df9098f2](https://git.pika-os.com/otter-shell/otter-emoji/commit/a9df9098f2034457af396e835147e32998ce9d4e) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-emoji/commit/a9df9098f2034457af396e835147e32998ce9d4e)

2026-06-08 20:23:16 +01:00

[src](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/src 'src')

[Write emoji results to stdout](https://git.pika-os.com/otter-shell/otter-emoji/commit/f57924e06ea951443af207c9e97c927f296747f6)

2026-06-06 19:42:34 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-emoji/commit/07a88b9a3cce7d6fe8ce56c600603caa3676a78b)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/build.zig 'build.zig')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-emoji/commit/07a88b9a3cce7d6fe8ce56c600603caa3676a78b)

2026-06-06 15:14:08 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-emoji/commit/a9df9098f2034457af396e835147e32998ce9d4e)

2026-06-08 20:23:16 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/README.md 'README.md')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-emoji/commit/74540d46b6197de04590f07a53bc3594e2f1764a)

2026-06-07 02:34:41 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-emoji

Searchable emoji picker core. CLI prints matching glyph/name rows or a compact grid for launcher integration.

Emoji data comes from Unicode 17.0.0 `emoji-test.txt` and includes all fully-qualified emoji sequences.

```bash
otter-emoji heart
otter-emoji --grid weather
otter-emoji --limit 8 smile
otter-emoji --copy rocket
```

`--copy` copies the first match through the shared Otter clipboard helper. Packaged installs shadow `wl-copy` to native `otter-copy`; `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store` is used only when the Wayland clipboard path is unavailable.

Config: `~/.config/otter-shell/otter-emoji.conf`

```text
grid = false
copy = false
limit = 32
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-emoji/blame/commit/a9df9098f2034457af396e835147e32998ce9d4e/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-emoji/src/branch/main/README.md) **51** KiB

Languages

Zig 100%