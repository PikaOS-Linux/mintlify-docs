# Source: https://git.pika-os.com/otter-shell/otter-rec/src

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-rec](https://git.pika-os.com/otter-shell/otter-rec)

Watch [1](https://git.pika-os.com/otter-shell/otter-rec/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-rec/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-rec/forks)

You've already forked otter-rec

[**30** Commits](https://git.pika-os.com/otter-shell/otter-rec/commits/branch/main) [**1** Branch](https://git.pika-os.com/otter-shell/otter-rec/branches) [**8** Tags](https://git.pika-os.com/otter-shell/otter-rec/tags)

**main**

 [Go to file](https://git.pika-os.com/otter-shell/otter-rec/find/branch/main) Add File

[New File](https://git.pika-os.com/otter-shell/otter-rec/_new/main/) [Upload File](https://git.pika-os.com/otter-shell/otter-rec/_upload/main/) [Apply Patch](https://git.pika-os.com/otter-shell/otter-rec/_diffpatch/main/)

Code

Clone

HTTPS Tea CLI

[Open with VS Code]() [Open with VSCodium]() [Open with Intellij IDEA]()

[Download ZIP](https://git.pika-os.com/otter-shell/otter-rec/archive/main.zip) [Download TAR.GZ](https://git.pika-os.com/otter-shell/otter-rec/archive/main.tar.gz) [Download BUNDLE](https://git.pika-os.com/otter-shell/otter-rec/archive/main.bundle)

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [ae6b839fdc](https://git.pika-os.com/otter-shell/otter-rec/commit/ae6b839fdccb2730d93629a83448ee722240b10c) [build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-rec/commit/ae6b839fdccb2730d93629a83448ee722240b10c)

2026-06-08 20:23:13 +01:00

[src](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/src 'src')

[Make recorder command toggle recording](https://git.pika-os.com/otter-shell/otter-rec/commit/e1347e5394fce67efac2cb915dd05608eb3324d7)

2026-06-07 13:57:39 +01:00

[.gitignore](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/.gitignore '.gitignore')

[Initial implementation](https://git.pika-os.com/otter-shell/otter-rec/commit/16c7d946d474d2533baa1b960cced97e11bc1b3e)

2026-06-06 15:14:08 +01:00

[build.zig](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/build.zig 'build.zig')

[Add native KMS CUDA recorder path](https://git.pika-os.com/otter-shell/otter-rec/commit/981f03f6f213b8431b1d1a104065941df3a15923)

2026-06-06 17:47:12 +01:00

[build.zig.zon](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/build.zig.zon 'build.zig.zon')

[build: restore local path deps after v0.11.14 tagging](https://git.pika-os.com/otter-shell/otter-rec/commit/ae6b839fdccb2730d93629a83448ee722240b10c)

2026-06-08 20:23:13 +01:00

[README.md](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/README.md 'README.md')

[Make recorder command toggle recording](https://git.pika-os.com/otter-shell/otter-rec/commit/e1347e5394fce67efac2cb915dd05608eb3324d7)

2026-06-07 13:57:39 +01:00

#### 

**[README.md](https://git.pika-os.com/#readme)**

# otter-rec

Wayland screen recorder with native KMS/EGL/CUDA NVENC path, portal stream opener, and in-process libav encoder.

```bash
otter-rec
otter-rec
otter-rec --dry-run --source screen --output out.mp4
otter-rec --portal --source screen --output out.mp4
otter-rec --region X,Y,W,H
otter-rec --region X,Y,W,H --hevc
otter-rec --region select --output region.mp4
otter-rec --window active --output window.mp4
```

`otter-rec` probes `/sys/class/drm` for GPU vendor and queries system libavcodec directly through Zig translate-c bindings. It does not shell out to `ffmpeg`. NVIDIA uses NVENC first, Intel uses Quick Sync/QSV first, and AMD uses VAAPI first. Within the selected vendor family, H.264 is preferred unless `--hevc` or `--av1` is set.

Hardware encoders come from distro FFmpeg packages. Install FFmpeg/libavcodec development packages built with the needed backends (`av1_nvenc`, `hevc_nvenc`, `h264_nvenc`, `av1_qsv`, `hevc_qsv`, `h264_qsv`, `av1_vaapi`, `hevc_vaapi`, `h264_vaapi`) and `pkg-config` metadata for `libavcodec`, `libavformat`, `libavutil`, and `libswscale`. The native NVIDIA fullscreen path also links system `egl`, `glesv2`, `libdrm`, and CUDA Driver API (`cuda`) libraries. It does not use CUDA runtime and does not vendor FFmpeg.

Running `otter-rec` starts the default region recording. Running `otter-rec` again stops the active recording. Default output is `~/Videos/YYYY-MM-DD-HH-MM-SS.mp4`; set `output` or pass `--output` to override it. Dry-run prints the selected capture input, encoder, mode, and output. Capture input prefers non-PipeWire Wayland paths in Wayland sessions. Single-output fullscreen NVENC recording uses the KMS helper to export primary planes as DMA-BUF, imports them through EGL, crops through GL texture coordinates when recording a region, copies through CUDA/GL interop into FFmpeg CUDA frames, and encodes in-process. The `wlr-screencopy` raw path remains the non-NVENC single-output region fallback. The `ext-image-copy-capture` path remains the fallback and is still used for window capture. `--portal` forces xdg-desktop-portal selection before recording through Otter's native capture/encoder path. Portal detection checks Wayland, runtime PipeWire and session bus sockets, then verifies `org.freedesktop.portal.ScreenCast.version`.

`--region X,Y,W,H` records the requested global logical rectangle. `--region select` opens the same frozen Wayland selection overlay used by screenshot/product-shot and records the selected bounds. `--window active`, `--window N`, or `--window QUERY` records a compositor-reported foreign toplevel through `ext_foreign_toplevel_image_capture_source_manager_v1`.

`otter-rec-kms-server SOCKET CARD` is the privileged KMS helper used for direct GPU fullscreen recording. If no helper is already running and the helper binary does not have `cap_sys_admin+ep`, `otter-rec` first runs `pkexec setcap cap_sys_admin+ep <helper>` so later launches run the helper directly. If the permission repair fails, it falls back to launching the helper through `pkexec`. The helper opens the DRM card, exports active primary/cursor planes as DMA-BUF fds, and returns bounded metadata over a Unix socket.

Only Wayland capture paths are used. `--portal` opens an xdg-desktop-portal ScreenCast session, then records through Otter's in-process capture/encoder path. `--window` requests portal window sources.

Config: `~/.config/otter-shell/otter-rec.conf`

```text
output = ""
source = ""
mode = "region"
codec = "h264"
force_portal = false
fps = 30
seconds = 0
bitrate = 12000000
```

Empty `output` writes to `~/Videos/YYYY-MM-DD-HH-MM-SS.mp4`. `mode` accepts `fullscreen`, `region`, or `window`. `codec` accepts `h264`, `hevc`, or `av1`.

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-rec/blame/commit/ae6b839fdccb2730d93629a83448ee722240b10c/) [Copy Permalink]()

Description

No description provided

[Readme](https://git.pika-os.com/otter-shell/otter-rec/src/branch/main/README.md) **98** KiB

Languages

Zig 80.3%

C 19.7%