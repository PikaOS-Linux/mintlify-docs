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

Playback is enabled by default. Set `playback = false` or pass `--no-play` to
write a WAV stream to stdout. Use `-o PATH` or `--output PATH` for file output.
Use `-o speech.wav` with playback enabled to play and save.

## Third-party licenses

Otter Shell code is MIT — see [LICENSE](LICENSE). Vendored TTS stack:

- **crispasr** — see `third_party/crispasr/LICENSE` and `third_party/crispasr/ggml/LICENSE`
- **espeak-ng** — embedded phonemizer data under `third_party/crispasr/espeak-ng/`

## License

MIT License — see [LICENSE](LICENSE).
