# otter-rec

Wayland screen recorder with native KMS/EGL/CUDA NVENC path, portal stream
opener, and in-process libav encoder.

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

`otter-rec` probes `/sys/class/drm` for GPU vendor and queries system libavcodec
directly through Zig translate-c bindings. It does not shell out to `ffmpeg`.
NVIDIA uses NVENC first, Intel uses Quick Sync/QSV first, and AMD uses VAAPI first.
Within the selected vendor family, H.264 is preferred unless `--hevc` or `--av1`
is set.

Hardware encoders come from distro FFmpeg packages. Install FFmpeg/libavcodec
development packages built with the needed backends (`av1_nvenc`, `hevc_nvenc`,
`h264_nvenc`, `av1_qsv`, `hevc_qsv`, `h264_qsv`, `av1_vaapi`, `hevc_vaapi`,
`h264_vaapi`) and `pkg-config` metadata for `libavcodec`, `libavformat`,
`libavutil`, and `libswscale`. The native NVIDIA fullscreen path also links
system `egl`, `glesv2`, `libdrm`, and CUDA Driver API (`cuda`) libraries. It does
not use CUDA runtime and does not vendor FFmpeg.

Running `otter-rec` starts the default region recording. Running `otter-rec`
again stops the active recording. Default output is
`~/Videos/YYYY-MM-DD-HH-MM-SS.mp4`; set `output` or pass `--output` to override
it. Dry-run prints the selected capture input, encoder, mode, and output. Capture
input prefers non-PipeWire Wayland paths in Wayland sessions. Single-output fullscreen
NVENC recording uses the KMS helper to export primary planes as DMA-BUF, imports
them through EGL, crops through GL texture coordinates when recording a region,
copies through CUDA/GL interop into FFmpeg CUDA frames, and encodes in-process.
The `wlr-screencopy` raw path remains the non-NVENC single-output region
fallback. The `ext-image-copy-capture` path remains the fallback and is still
used for window capture.
`--portal` forces xdg-desktop-portal selection before recording through Otter's
native capture/encoder path. Portal detection checks
Wayland, runtime PipeWire and session bus sockets, then verifies
`org.freedesktop.portal.ScreenCast.version`.

`--region X,Y,W,H` records the requested global logical rectangle. `--region select`
opens the same frozen Wayland selection overlay used by screenshot/product-shot and
records the selected bounds. `--window active`, `--window N`, or `--window QUERY`
records a compositor-reported foreign toplevel through
`ext_foreign_toplevel_image_capture_source_manager_v1`.

`otter-rec-kms-server SOCKET CARD` is the privileged KMS helper used for direct
GPU fullscreen recording. If no helper is already running and the helper binary
does not have `cap_sys_admin+ep`, `otter-rec` first runs
`pkexec setcap cap_sys_admin+ep <helper>` so later launches run the helper
directly. If the permission repair fails, it falls back to launching the helper
through `pkexec`. The helper opens the DRM card, exports active primary/cursor
planes as DMA-BUF fds, and returns bounded metadata over a Unix socket.

Only Wayland capture paths are used. `--portal` opens an xdg-desktop-portal
ScreenCast session, then records through Otter's in-process capture/encoder path.
`--window` requests portal window sources.

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

Empty `output` writes to `~/Videos/YYYY-MM-DD-HH-MM-SS.mp4`. `mode` accepts
`fullscreen`, `region`, or `window`. `codec` accepts `h264`, `hevc`, or `av1`.

## License

MIT License — see [LICENSE](LICENSE).
