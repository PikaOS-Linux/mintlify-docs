# Source: https://git.pika-os.com/otter-shell/otter-note

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-note](https://git.pika-os.com/otter-shell/otter-note)

Watch [1](https://git.pika-os.com/otter-shell/otter-note/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-note/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-note/forks)

You've already forked otter-note

[**33** Commits](https://git.pika-os.com/otter-shell/otter-note/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-note/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-note/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-note/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-note/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-note/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-note/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-note/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-note/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-note/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [3d5d48dc27](https://git.pika-os.com/otter-shell/otter-note/commit/3d5d48dc279fb3935db464c9bb6fc07892222c07) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-note/commit/3d5d48dc279fb3935db464c9bb6fc07892222c07)

2026-06-08 20:23:18 +01:00

[data/applications](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/data/applications 'data/applications')

[Commit pending otter-note changes](https://git.pika-os.com/otter-shell/otter-note/commit/9ef88866092eade0dc0bfc9ccfb333e168bfecf4)

2026-06-07 00:35:14 +01:00

[src](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/src 'src')

[Handle newline key fallback in note editor](https://git.pika-os.com/otter-shell/otter-note/commit/a7fdd7d6213cf00c0ce0c8c4ca15a1352906ec3d)

2026-06-07 14:59:45 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-note/commit/0b75a085b26ec3c115480d55093b05019bfe33c2)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/build.zig 'build.zig')

[Commit pending otter-note changes](https://git.pika-os.com/otter-shell/otter-note/commit/9ef88866092eade0dc0bfc9ccfb333e168bfecf4)

2026-06-07 00:35:14 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-note/commit/3d5d48dc279fb3935db464c9bb6fc07892222c07)

2026-06-08 20:23:18 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/README.md 'README.md')

[Make note popup passive by default](https://git.pika-os.com/otter-shell/otter-note/commit/a9eac08e89db0e3ca9b933a177278f6a1ace8467)

2026-06-07 14:13:29 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-note

Sticky markdown notes with a Super+N-ready layer-shell surface.

```bash
otter-note add "ship release"
otter-note new
otter-note --pin top-right new
otter-note list
otter-note clear
otter-note --path /tmp/notes.md add test note
```

Default storage is `$XDG_DATA_HOME/otter-shell/notes.md` or `$HOME/.local/share/otter-shell/notes.md`. The sticky surface edits markdown directly when edit mode is enabled, saves on exit or Ctrl+S, and toggles rendered markdown preview with Ctrl+M. In view mode only the header buttons accept input, so the note body does not block apps underneath it. The install step provides `otter-note.desktop`, so the launcher indexes it as a normal application.

Config: `~/.config/otter-shell/otter-note.conf`

```text
notes_path = ""
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-note/blame/commit/3d5d48dc279fb3935db464c9bb6fc07892222c07/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-note/src/branch/main/README.md) **177** KiB

Languages

Zig 100%