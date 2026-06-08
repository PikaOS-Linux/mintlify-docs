# Source: https://git.pika-os.com/otter-shell/otter-transcribe

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-transcribe](https://git.pika-os.com/otter-shell/otter-transcribe)

Watch [1](https://git.pika-os.com/otter-shell/otter-transcribe/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-transcribe/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-transcribe/forks)

You've already forked otter-transcribe

[**21** Commits](https://git.pika-os.com/otter-shell/otter-transcribe/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-transcribe/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-transcribe/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-transcribe/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-transcribe/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-transcribe/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-transcribe/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-transcribe/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-transcribe/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-transcribe/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [25ba37100d](https://git.pika-os.com/otter-shell/otter-transcribe/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-transcribe/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5)

2026-06-08 20:23:20 +01:00

[scripts](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/scripts 'scripts')

[Add otter-transcribe](https://git.pika-os.com/otter-shell/otter-transcribe/commit/7b25bfa7980df9129964dde1232fffc6e2f0dd89)

2026-06-06 17:26:09 +01:00

[src](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/src 'src')

[Load transcribe model only while recording](https://git.pika-os.com/otter-shell/otter-transcribe/commit/b10eee37a0c6911599df762f0b023808df84eac3)

2026-06-08 00:18:02 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/.gitignore '.gitignore')

[Add otter-transcribe](https://git.pika-os.com/otter-shell/otter-transcribe/commit/7b25bfa7980df9129964dde1232fffc6e2f0dd89)

2026-06-06 17:26:09 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/build.zig 'build.zig')

[Use direct PipeWire capture](https://git.pika-os.com/otter-shell/otter-transcribe/commit/c0a6586e07ff5caf044b2dfadf467cee6c2e50eb)

2026-06-06 18:27:48 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-transcribe/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5)

2026-06-08 20:23:20 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/README.md 'README.md')

[Load transcribe model only while recording](https://git.pika-os.com/otter-shell/otter-transcribe/commit/b10eee37a0c6911599df762f0b023808df84eac3)

2026-06-08 00:18:02 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-transcribe

Hotkey-controlled transcription daemon for Otter Shell.

`otter-transcribe` runs as daemon, records microphone PCM directly through PipeWire, transcribes through statically linked `mudler/parakeet.cpp`, then emits text to focused input, stdout, or clipboard. While recording, it shows a bottom-center layer-shell indicator driven by live PCM levels.

## Build

```bash
cd /home/ferreo/otter-shell/otter-transcribe
zig build
```

`zig build` compiles vendored `mudler/parakeet.cpp`, GGML, OpenMP (`libgomp.a`), and the C++ runtime into `otter-transcribe`. The layer-shell UI uses the system Wayland/font stack.

```bash
/home/ferreo/otter-shell/otter-transcribe/zig-out/bin/otter-transcribe
```

Model is embedded into `otter-transcribe`. Default build embeds `realtime_eou_120m-v1-f16.gguf`; use `-Dembedded_model=q8_0` to build with `realtime_eou_120m-v1-q8_0.gguf` for testing. The daemon does not materialize or load the embedded model while idle. On first `start`/`toggle`, it writes the embedded model to `$XDG_RUNTIME_DIR/otter-transcribe-realtime_eou_120m-v1-f16.gguf` only when missing or stale, because the Parakeet C API takes a GGUF file path.

```bash
zig build -Dembedded_model=q8_0
```

Run daemon:

```bash
zig build run
```

Runtime behavior is configured in `~/.config/otter-shell/otter-transcribe.conf`, not daemon flags. The daemon watches that file and `theme.conf` with inotify and hot-reloads changes.

## CLI

```bash
zig build ctl -- start
zig build ctl -- stop
zig build ctl -- toggle
zig build ctl -- status
```

Install names:

```bash
zig build install
otter-transcribe
otter-transcribectl toggle
```

## Hotkeys

Toggle capture:

```bash
otter-transcribectl toggle
```

Hold-to-capture:

```bash
otter-transcribectl start
otter-transcribectl stop
```

Bind those commands in compositor config. Wayland clients cannot reliably grab global hotkeys themselves.

## Output Modes

- `focused`: type transcript into current focused input with built-in Wayland virtual keyboard injection
- `clipboard`: copy transcript through `wl-copy`
- `stdout`: print transcript from daemon process

`focused` requires compositor support for virtual keyboard injection. ASCII output uses physical evdev keycodes for better Chromium/Electron compatibility. Use `clipboard` or `stdout` if virtual keyboard injection is blocked. In streaming mode, `clipboard` receives each finalized chunk as it arrives; set `stream = false` when you want one final clipboard value for the whole utterance. The realtime model's EOU/EOB event resets the internal Parakeet stream so long capture sessions continue producing text after each utterance boundary. Model memory is released after each recording finishes.

## Config

Edit in `otter-settings` under the `Transcribe` tab, or edit the file directly:

```conf
output = focused
stream = true
show_indicator = true
sample_rate = 16000
target = "@DEFAULT_SOURCE@"
max_seconds = 300
width = 120
height = 48
margin_bottom = 36
graph_height = 28
graph_bars = 24
```

Defaults:

- model: embedded `realtime_eou_120m-v1-f16.gguf` by default, `-Dembedded_model=q8_0` for q8 test builds
- output: `focused`
- streaming: enabled
- indicator: enabled
- PipeWire target: `@DEFAULT_SOURCE@`
- sample rate: `16000`
- max recording: `300` seconds

When `max_seconds` is reached, the daemon finalizes the current recording and stays alive for later commands.

`background_color`, `border_color`, `graph_color`, `graph_peak_color`, and `text_color` inherit from `otter-theme` when unset.

Only `--model PATH` remains as daemon flag for testing an alternate GGUF:

```bash
otter-transcribe --model /path/to/model.gguf
```

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-transcribe/blame/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/README.md) **395** MiB

Languages

Zig 99.3%

Shell 0.7%