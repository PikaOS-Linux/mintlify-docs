# Source: https://git.pika-os.com/otter-shell/otter-vox/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-vox](https://git.pika-os.com/otter-shell/otter-vox)

Watch [1](https://git.pika-os.com/otter-shell/otter-vox/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-vox/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-vox/forks)

You've already forked otter-vox

[**20** Commits](https://git.pika-os.com/otter-shell/otter-vox/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-vox/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-vox/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-vox/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-vox/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-vox/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-vox/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-vox/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-vox/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-vox/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [a11b953134](https://git.pika-os.com/otter-shell/otter-vox/commit/a11b953134ed904ee957b3307c720a21a7bb096b) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-vox/commit/a11b953134ed904ee957b3307c720a21a7bb096b)

2026-06-08 20:23:21 +01:00

[models](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/models 'models')

[Switch otter-vox to embedded Kokoro TTS](https://git.pika-os.com/otter-shell/otter-vox/commit/95ffe377dd1f4840494d8d3d498e399e50f09bcb)

2026-06-07 12:25:03 +01:00

[src](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/src 'src')

[Default voice playback on](https://git.pika-os.com/otter-shell/otter-vox/commit/dc12ace289473551281c8b0ae770b4fded7cbae2)

2026-06-07 13:47:08 +01:00

[third\_party/crispasr](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/third_party/crispasr 'third_party/crispasr')

[Switch otter-vox to embedded Kokoro TTS](https://git.pika-os.com/otter-shell/otter-vox/commit/95ffe377dd1f4840494d8d3d498e399e50f09bcb)

2026-06-07 12:25:03 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/.gitignore '.gitignore')

[Switch otter-vox to embedded Kokoro TTS](https://git.pika-os.com/otter-shell/otter-vox/commit/95ffe377dd1f4840494d8d3d498e399e50f09bcb)

2026-06-07 12:25:03 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/build.zig 'build.zig')

[Switch otter-vox to embedded Kokoro TTS](https://git.pika-os.com/otter-shell/otter-vox/commit/95ffe377dd1f4840494d8d3d498e399e50f09bcb)

2026-06-07 12:25:03 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-vox/commit/a11b953134ed904ee957b3307c720a21a7bb096b)

2026-06-08 20:23:21 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/README.md 'README.md')

[Default voice playback on](https://git.pika-os.com/otter-shell/otter-vox/commit/dc12ace289473551281c8b0ae770b4fded7cbae2)

2026-06-07 13:47:08 +01:00

[root.zig](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/root.zig 'root.zig')

[Switch otter-vox to embedded Kokoro TTS](https://git.pika-os.com/otter-shell/otter-vox/commit/95ffe377dd1f4840494d8d3d498e399e50f09bcb)

2026-06-07 12:25:03 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-vox

Pipe text into CPU Kokoro TTS using embedded GGUF model and voice assets.

```bash
printf 'Welcome to Otter Shell.' | otter-vox --no-play | pw-play -
printf 'Welcome to Otter Shell.' | otter-vox -o speech.wav
otter-vox --voice bm_lewis --play 'Welcome to Otter Shell.'
otter-vox --check-model
```

Config: `~/.config/otter-shell/otter-vox.conf`

```text
model_dir = ""
output_path = "-"
playback = true
voice = "bm_george"
cpu_threads = 4
```

Default Kokoro assets are embedded in the binary and materialized under `$XDG_RUNTIME_DIR/otter-shell/otter-vox/models/kokoro` when `models/kokoro` is not available from the current working directory. The espeak-ng phonemizer is statically linked; its generated data is embedded as `third_party/crispasr/espeak-ng/espeak-ng-data.tar` and materialized under `$XDG_RUNTIME_DIR/otter-shell/otter-vox/espeak`. Explicit `--model-dir` always wins for Kokoro model and voice files. Set `voice = "name"` in `otter-vox.conf` or pass `--voice name`; `--list-voices` prints all embedded names.

Checked-in model files:

- `models/kokoro/kokoro-82m-q8_0.gguf`
- `models/kokoro/kokoro-voice-af_alloy.gguf`
- `models/kokoro/kokoro-voice-af_aoede.gguf`
- `models/kokoro/kokoro-voice-af_bella.gguf`
- `models/kokoro/kokoro-voice-af_heart.gguf`
- `models/kokoro/kokoro-voice-af_jessica.gguf`
- `models/kokoro/kokoro-voice-af_kore.gguf`
- `models/kokoro/kokoro-voice-af_nicole.gguf`
- `models/kokoro/kokoro-voice-af_nova.gguf`
- `models/kokoro/kokoro-voice-af_river.gguf`
- `models/kokoro/kokoro-voice-af_sarah.gguf`
- `models/kokoro/kokoro-voice-af_sky.gguf`
- `models/kokoro/kokoro-voice-am_adam.gguf`
- `models/kokoro/kokoro-voice-am_echo.gguf`
- `models/kokoro/kokoro-voice-am_eric.gguf`
- `models/kokoro/kokoro-voice-am_fenrir.gguf`
- `models/kokoro/kokoro-voice-am_liam.gguf`
- `models/kokoro/kokoro-voice-am_michael.gguf`
- `models/kokoro/kokoro-voice-am_onyx.gguf`
- `models/kokoro/kokoro-voice-am_puck.gguf`
- `models/kokoro/kokoro-voice-am_santa.gguf`
- `models/kokoro/kokoro-voice-bf_alice.gguf`
- `models/kokoro/kokoro-voice-bf_emma.gguf`
- `models/kokoro/kokoro-voice-bf_isabella.gguf`
- `models/kokoro/kokoro-voice-bf_lily.gguf`
- `models/kokoro/kokoro-voice-bm_daniel.gguf`
- `models/kokoro/kokoro-voice-bm_fable.gguf`
- `models/kokoro/kokoro-voice-bm_george.gguf`
- `models/kokoro/kokoro-voice-bm_lewis.gguf`
- `models/kokoro/kokoro-voice-df_eva.gguf`
- `models/kokoro/kokoro-voice-df_victoria.gguf`
- `models/kokoro/kokoro-voice-dm_bernd.gguf`
- `models/kokoro/kokoro-voice-dm_martin.gguf`
- `models/kokoro/kokoro-voice-ef_dora.gguf`
- `models/kokoro/kokoro-voice-em_alex.gguf`
- `models/kokoro/kokoro-voice-em_santa.gguf`
- `models/kokoro/kokoro-voice-ff_siwis.gguf`
- `models/kokoro/kokoro-voice-hf_alpha.gguf`
- `models/kokoro/kokoro-voice-hf_beta.gguf`
- `models/kokoro/kokoro-voice-hm_omega.gguf`
- `models/kokoro/kokoro-voice-hm_psi.gguf`
- `models/kokoro/kokoro-voice-if_sara.gguf`
- `models/kokoro/kokoro-voice-im_nicola.gguf`
- `models/kokoro/kokoro-voice-jf_alpha.gguf`
- `models/kokoro/kokoro-voice-jf_gongitsune.gguf`
- `models/kokoro/kokoro-voice-jf_nezumi.gguf`
- `models/kokoro/kokoro-voice-jf_tebukuro.gguf`
- `models/kokoro/kokoro-voice-jm_kumo.gguf`
- `models/kokoro/kokoro-voice-pf_dora.gguf`
- `models/kokoro/kokoro-voice-pm_alex.gguf`
- `models/kokoro/kokoro-voice-pm_santa.gguf`
- `models/kokoro/kokoro-voice-zf_xiaobei.gguf`
- `models/kokoro/kokoro-voice-zf_xiaoni.gguf`
- `models/kokoro/kokoro-voice-zf_xiaoxiao.gguf`
- `models/kokoro/kokoro-voice-zf_xiaoyi.gguf`
- `models/kokoro/kokoro-voice-zm_yunjian.gguf`
- `models/kokoro/kokoro-voice-zm_yunxi.gguf`
- `models/kokoro/kokoro-voice-zm_yunxia.gguf`
- `models/kokoro/kokoro-voice-zm_yunyang.gguf`

Build:

```bash
zig build -Doptimize=ReleaseFast
```

Playback is enabled by default. Set `playback = false` or pass `--no-play` to write a WAV stream to stdout. Use `-o PATH` or `--output PATH` for file output. Use `-o speech.wav` with playback enabled to play and save.

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-vox/blame/commit/a11b953134ed904ee957b3307c720a21a7bb096b/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-vox/src/branch/main/README.md) **510** MiB

Languages

Zig 100%