# Source: https://git.pika-os.com/otter-shell/otter-cal

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-cal](https://git.pika-os.com/otter-shell/otter-cal)

Watch [1](https://git.pika-os.com/otter-shell/otter-cal/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-cal/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-cal/forks)

You've already forked otter-cal

[**19** Commits](https://git.pika-os.com/otter-shell/otter-cal/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-cal/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-cal/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-cal/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-cal/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-cal/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-cal/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-cal/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-cal/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-cal/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [e80c98863f](https://git.pika-os.com/otter-shell/otter-cal/commit/e80c98863f00a3120a1ea68c6fbd0eed0e59edd3) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-cal/commit/e80c98863f00a3120a1ea68c6fbd0eed0e59edd3)

2026-06-08 20:23:10 +01:00

[src](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/src 'src')

[Write calendar output to stdout](https://git.pika-os.com/otter-shell/otter-cal/commit/b1c063977172044d27534ab749941a55e33c3b2a)

2026-06-06 19:42:34 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-cal/commit/51c65cd808e049b60f24d6dad5aba2a0470a7559)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/build.zig 'build.zig')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-cal/commit/51c65cd808e049b60f24d6dad5aba2a0470a7559)

2026-06-06 15:14:08 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-cal/commit/e80c98863f00a3120a1ea68c6fbd0eed0e59edd3)

2026-06-08 20:23:10 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/README.md 'README.md')

[Load calendar settings from otter-conf](https://git.pika-os.com/otter-shell/otter-cal/commit/ff2c173d86549a13e0fcd7d8965b7291fab2bb02)

2026-06-06 15:45:26 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-cal

Calendar popover core. CLI prints a month grid and bounded agenda list suitable for bar clock popover integration.

```bash
otter-cal
otter-cal --month 2026-06
otter-cal --today 2026-06-05 --agenda ~/.config/otter-shell/agenda
otter-cal --next 1
```

Agenda lines use:

```text
YYYY-MM-DD text
```

The bar clock launches `clock_calendar_command` on left click. Default:

```text
clock_calendar_command = "otter-cal"
```

Config: `~/.config/otter-shell/otter-cal.conf`

```text
agenda_path = ""
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-cal/blame/commit/e80c98863f00a3120a1ea68c6fbd0eed0e59edd3/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-cal/src/branch/main/README.md) **52** KiB

Languages

Zig 100%