# Source: https://git.pika-os.com/otter-shell/otter-timer

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-timer](https://git.pika-os.com/otter-shell/otter-timer)

Watch [1](https://git.pika-os.com/otter-shell/otter-timer/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-timer/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-timer/forks)

You've already forked otter-timer

[**21** Commits](https://git.pika-os.com/otter-shell/otter-timer/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-timer/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-timer/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-timer/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-timer/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-timer/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-timer/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-timer/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-timer/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-timer/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [27f66aae09](https://git.pika-os.com/otter-shell/otter-timer/commit/27f66aae09051798e95e57b90a75bf6cec453da0) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-timer/commit/27f66aae09051798e95e57b90a75bf6cec453da0)

2026-06-08 20:23:17 +01:00

[src](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/src 'src')

[Run timer completion commands](https://git.pika-os.com/otter-shell/otter-timer/commit/b539fd3c1f9fc0a7a8a1ca1f00547691f74fc86d)

2026-06-07 13:32:55 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-timer/commit/b908ada5273648d1d9a49fd2642c5875cb437c62)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/build.zig 'build.zig')

[Resolve timer OSD from Otter install](https://git.pika-os.com/otter-shell/otter-timer/commit/074a3fc19088155d34f6c566e5fa409fd343cf62)

2026-06-06 20:18:40 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-timer/commit/27f66aae09051798e95e57b90a75bf6cec453da0)

2026-06-08 20:23:17 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/README.md 'README.md')

[Run timer completion commands](https://git.pika-os.com/otter-shell/otter-timer/commit/b539fd3c1f9fc0a7a8a1ca1f00547691f74fc86d)

2026-06-07 13:32:55 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-timer

`otter-timer 5m` waits for countdown completion and emits a desktop ping.

```bash
otter-timer 5m
otter-timer --message "Tea" 3m
otter-timer --command 'playerctl pause' 30m
otter-timer --dry-run 30s
otter-timer --no-notify 1h
```

Durations support `s`, `m`, `h`, and `d` segments such as `1h30m`. Completion sends `otter-osd message` when available and still prints `timer done`. If `command` is set, it runs after the timer completes.

Config: `~/.config/otter-shell/otter-timer.conf`

```text
default_duration = ""
message = "Timer done"
command = ""
notify = true
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-timer/blame/commit/27f66aae09051798e95e57b90a75bf6cec453da0/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/README.md) **55** KiB

Languages

Zig 100%