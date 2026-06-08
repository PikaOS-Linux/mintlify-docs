# Source: https://git.pika-os.com/otter-shell/otter-term/src/branch/main/README.md

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-term](https://git.pika-os.com/otter-shell/otter-term)

Watch [1](https://git.pika-os.com/otter-shell/otter-term/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-term/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-term/forks)

You've already forked otter-term

**Files**

**main**

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [ff80a31576](https://git.pika-os.com/otter-shell/otter-term/commit/ff80a315763555a36b7819410fa4fa16c85eb5fe) [Embed IoskeleyMono terminal font](https://git.pika-os.com/otter-shell/otter-term/commit/ff80a315763555a36b7819410fa4fa16c85eb5fe)

2026-05-31 23:21:10 +01:00

#### 

5.7 KiB

[Raw](https://git.pika-os.com/otter-shell/otter-term/raw/branch/main/README.md) [Permalink](https://git.pika-os.com/otter-shell/otter-term/src/commit/c754c2e16a8123222718a164949cd69f39b45a87/README.md) [Blame](https://git.pika-os.com/otter-shell/otter-term/blame/branch/main/README.md) [History](https://git.pika-os.com/otter-shell/otter-term/commits/branch/main/README.md)

# otter-term

`otter-term` is the Otter Shell terminal emulator. It uses `libghostty-vt` for terminal emulation and the Otter libraries for the Wayland window, PTY handling, input, rendering, configuration, theme integration, clipboard, and desktop metadata.

## Features

- Wayland xdg-toplevel terminal window
- PTY-backed shell session with resize support
- `libghostty-vt` parsing, render-state snapshots, key encoding, mouse encoding, dirty tracking, colors, cursor state, BEL callbacks, XTWINOPS size reports, and OSC title updates
- CPU-rendered terminal grid using `otter-render`
- DPI-aware font sizing and padding
- Configurable font, palette, padding, shell, scrollback, URL handling, and copy/paste keybinds via `otter-conf`
- Text selection with word/line multi-click, drag autoscroll, primary selection, scrollback, clipboard copy, and clipboard paste
- Themed tab strip for multiple terminal tabs, with close buttons hidden when only one tab remains
- Horizontal and vertical split panes inside a tab; splits are independently focused, resized, and closed without appearing as tabs
- Right-click context menu for copy, paste, copy URL/path/last command output, new tab, split pane, close tab/split, clear, clear scrollback, and reset
- Shell integration hooks for OSC 7 current-directory tracking and OSC 133 command status/output capture
- Mouse reporting for terminal applications
- Clickable `http://`, `https://`, and `www.` URLs
- IME support through `zwp_text_input_v3`, including committed text, preedit text, and candidate-window positioning at the terminal cursor
- Desktop integration assets: `.desktop` file and hicolor PNG icons

## Build

```bash
zig build
zig build test
zig build run
zig build profile
```

Install into a prefix with:

```bash
zig build install -p <prefix>
```

The install step places the binary in `bin`, the desktop entry in `share/applications`, and icons in `share/icons/hicolor`.

## Profiling

Run repeatable terminal hot-path scenarios with:

```bash
zig build profile
```

Local baseline captured on 2026-05-22 after the shell-capture and PTY drain optimizations:

| Scenario | Total ms | ns/iter |
| --- | --- | --- |
| idle | 1.017 | 101 |
| yes | 60.502 | 236337 |
| cat-large-log | 66.153 | 8269140 |
| chunked-cat-16k | 280.021 | 70005316 |
| chunked-cat-64k | 276.437 | 69109139 |
| render-visible-grid-after-cat | 188.537 | 1571139 |
| shell-capture-large-output | 0.976 | 30507 |
| mouse-hover | 6.359 | 317 |
| kitty-image | 14.366 | 47886 |
| powerline-prompt | 9.339 | 466 |

## Requirements

Build-time and runtime dependencies:

- Zig 0.16.0
- `libghostty-vt`
- `ghostty/vt.h`
- Wayland client libraries
- xkbcommon
- FreeType through `otter-render`

## Usage

Run with the configured default shell:

```bash
otter-term
```

Start in a specific directory:

```bash
otter-term /path/to/project
otter-term --cwd /path/to/project
otter-term --working-directory /path/to/project
```

Run a command instead of the configured shell:

```bash
otter-term -e htop
otter-term --execute sh -lc "htop"
otter-term -- nano file.txt
```

Run the built-in PTY/VT smoke test:

```bash
otter-term --self-test
```

## Configuration

Configuration is loaded from `~/.config/otter-shell/otter-term.conf`, then from `/etc/otter-shell/otter-term.conf`, then from compiled defaults. User configs are normalized on startup so missing defaults are added and stale unknown keys are removed.

`otter-settings` exposes the same schema in the Terminal tab.

Common keys:

```conf
general_shell = ""
general_term = "xterm-256color"
general_width = 900
general_height = 560
general_scrollback_rows = 10000

font_family = "IoskeleyMono Nerd Font"
font_path = ""
font_fallback_path = "/usr/share/fonts/otter-shell/IoskeleyMonoNerdFont-Regular.ttf"
font_size = 14
font_dpi_aware = true
font_scale_percent = 100
font_cell_height = 0
font_baseline_offset = 0

padding_x = 4
padding_y = 4

keybinds_copy = "ctrl+shift+c"
keybinds_paste = "ctrl+shift+v"

url_enabled = true
url_underline = true
url_highlight_on_hover = true
url_open_command = "xdg-open"

scroll_fixed_per_row = 10
scroll_rows_per_notch = 3

shell_capture_output = false

bell_enabled = true
bell_command = "paplay /usr/share/sounds/freedesktop/stereo/bell.oga"
bell_visual = false
```

An empty `general_shell` uses `$SHELL`, falling back to `/bin/sh`. `general_term` controls the `TERM` value advertised to child processes. The default is `xterm-256color` for SSH compatibility; set it to `xterm-ghostty` only when target hosts and applications have that terminfo entry. The startup working directory is intentionally a launch argument, not a config value. New tabs and split panes start in the shell integration current directory when the shell reports OSC 7; otherwise they start in the default shell directory. `shell_capture_output` enables OSC 133 command-output capture for the context menu's "Copy Last Output" action. It is disabled by default so large command output stays off the hot PTY path. BEL output is rate-limited before spawning the configured command; the default bell uses a fixed `paplay` argv path.

The color palette is configured with `colors_*` keys. Defaults provide a complete 16-color terminal palette plus foreground, background, cursor, selection, and URL colors. User config changes are watched at runtime; saving `otter-term.conf` reloads the config, reapplies terminal colors, reloads the font, resizes the grid if needed, and forces a full redraw.

## Desktop Integration

The source tree includes:

- `data/applications/otter-term.desktop`
- `data/icons/hicolor/*/apps/otter-term.png`
- `data/icons/otter-term-source.png`

The installed desktop entry uses:

- Name: `Otter Terminal`
- Exec: `otter-term`
- Icon: `otter-term`
- Categories: `System;TerminalEmulator;`

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-term/blame/commit/c754c2e16a8123222718a164949cd69f39b45a87/README.md) [Copy Permalink]()