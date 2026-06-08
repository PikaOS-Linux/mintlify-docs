# otter-transcribe

Hotkey-controlled transcription daemon for Otter Shell.

`otter-transcribe` runs as daemon, records microphone PCM directly through PipeWire, transcribes through statically linked `mudler/parakeet.cpp`, then emits text to focused input, stdout, or clipboard. While recording, it shows a bottom-center layer-shell indicator driven by live PCM levels.

## Build

```bash
cd otter-transcribe
zig build
```

`zig build` compiles vendored `mudler/parakeet.cpp`, GGML, OpenMP (`libgomp.a`), and the C++ runtime into `otter-transcribe`. The layer-shell UI uses the system Wayland/font stack.

```bash
zig-out/bin/otter-transcribe
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

`focused` requires compositor support for virtual keyboard injection. ASCII output uses physical evdev keycodes for better Chromium/Electron compatibility. Use `clipboard` or `stdout` if virtual keyboard injection is blocked.
In streaming mode, `clipboard` receives each finalized chunk as it arrives; set `stream = false` when you want one final clipboard value for the whole utterance.
The realtime model's EOU/EOB event resets the internal Parakeet stream so long capture sessions continue producing text after each utterance boundary.
Model memory is released after each recording finishes.

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

## Third-party licenses

Otter Shell code is MIT — see [LICENSE](LICENSE). Vendored transcription stack:

- **mudler/parakeet.cpp** and **GGML** — vendored under `third_party/`; see bundled `LICENSE` files

## License

MIT License — see [LICENSE](LICENSE).
