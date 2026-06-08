# Source: https://git.pika-os.com/otter-shell/otter-weather/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-weather](https://git.pika-os.com/otter-shell/otter-weather)

Watch [1](https://git.pika-os.com/otter-shell/otter-weather/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-weather/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-weather/forks)

You've already forked otter-weather

[**23** Commits](https://git.pika-os.com/otter-shell/otter-weather/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-weather/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-weather/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-weather/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-weather/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-weather/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-weather/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-weather/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-weather/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-weather/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [1019621c46](https://git.pika-os.com/otter-shell/otter-weather/commit/1019621c468712e84f78a1cd02d97ad27cc71114) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-weather/commit/1019621c468712e84f78a1cd02d97ad27cc71114)

2026-06-08 20:23:19 +01:00

[src](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/src 'src')

[Reload weather daemon config promptly](https://git.pika-os.com/otter-shell/otter-weather/commit/3c87e8cc3618f96c27380a336dde2611c8330866)

2026-06-07 13:26:20 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-weather/commit/cc0ab90090a489c87f0c9e63002ba97775a24480)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/build.zig 'build.zig')

[Commit pending otter-weather changes](https://git.pika-os.com/otter-shell/otter-weather/commit/418e19b71fdc16b4bbb85abad1e961730d9a20a2)

2026-06-07 00:35:24 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-weather/commit/1019621c468712e84f78a1cd02d97ad27cc71114)

2026-06-08 20:23:19 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/README.md 'README.md')

[chore: commit pending updates](https://git.pika-os.com/otter-shell/otter-weather/commit/1aaa65a22c09c791a4bf11fcb1981965294aa6e2)

2026-06-07 02:34:41 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-weather

Open-Meteo weather fetcher for the bar widget and 7-day popup.

```bash
otter-weather
otter-weather 40.7128 -74.0060
otter-weather --dry-run 51.5072 -0.1276
otter-weather --write-cache
otter-weather --watch 900 --write-cache
otter-weather --cache
otter-weather --layer
```

Default location is London. The CLI fetches current conditions plus seven daily rows with Zig's std HTTP client and a 128 KiB response cap. `--dry-run` prints the generated Open-Meteo URL. `--write-cache` refreshes the bounded cache read by the `otter-bar` weather widget; `--watch SECONDS` keeps refreshing that cache; `--cache` prints an existing cache without HTTP. `--layer` opens the cached forecast in a small layer-shell popup and exits when clicked.

Config: `~/.config/otter-shell/otter-weather.conf`

```text
latitude = 51.5072
longitude = -0.1276
# Optional; empty uses $XDG_CACHE_HOME/otter-shell/weather-cache
cache_path = ""
write_cache = false
watch_seconds = 0
```

`--watch` mode reloads this config file between refreshes.

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-weather/blame/commit/1019621c468712e84f78a1cd02d97ad27cc71114/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-weather/src/branch/main/README.md) **80** KiB

Languages

Zig 100%