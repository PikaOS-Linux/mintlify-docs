# Source: https://git.pika-os.com/otter-shell/otter-calc

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-calc](https://git.pika-os.com/otter-shell/otter-calc)

Watch [1](https://git.pika-os.com/otter-shell/otter-calc/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-calc/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-calc/forks)

You've already forked otter-calc

[**21** Commits](https://git.pika-os.com/otter-shell/otter-calc/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-calc/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-calc/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-calc/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-calc/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-calc/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-calc/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-calc/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-calc/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-calc/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [731ce9087e](https://git.pika-os.com/otter-shell/otter-calc/commit/731ce9087e164efe34c621e99c7eedad5b898e19) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-calc/commit/731ce9087e164efe34c621e99c7eedad5b898e19)

2026-06-08 20:23:11 +01:00

[src](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/src 'src')

[Write calculator result to stdout](https://git.pika-os.com/otter-shell/otter-calc/commit/0a3b27f39c024f3699f22fe5603748d669c9589d)

2026-06-06 19:42:34 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-calc/commit/338b7cd9e53922990b19db1514439480e7bbe97e)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/build.zig 'build.zig')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-calc/commit/338b7cd9e53922990b19db1514439480e7bbe97e)

2026-06-06 15:14:08 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-calc/commit/731ce9087e164efe34c621e99c7eedad5b898e19)

2026-06-08 20:23:11 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/README.md 'README.md')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-calc/commit/d290122cbe82de4442244c7ba377afbe5dea64b3)

2026-06-07 02:34:41 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-calc

Quick calculator overlay core. CLI evaluates an expression, prints the result, or copies it for overlay/launcher use.

```bash
otter-calc '2 + 3 * 4'
otter-calc 2 + 3 '* 4'
otter-calc --copy '(2 + 3) * 4'
```

`--copy` uses the shared Otter clipboard helper. Packaged installs shadow `wl-copy` to native `otter-copy`; `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store` is used only when the Wayland clipboard path is unavailable.

Config: `~/.config/otter-shell/otter-calc.conf`

```text
copy_result = false
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-calc/blame/commit/731ce9087e164efe34c621e99c7eedad5b898e19/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-calc/src/branch/main/README.md) **50** KiB

Languages

Zig 100%