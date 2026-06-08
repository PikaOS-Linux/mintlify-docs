# otter-pick

Color picker using the same `ext-image-copy-capture` path as `otter-screenshot`.

```bash
otter-pick                 # frozen overlay, loupe, click to copy hex
otter-pick --x 120 --y 80  # sample signed global Wayland coordinate
otter-pick --x -10 --y 80  # negative coords work for left-of-primary outputs
otter-pick --loupe --x 1 --y 2 # print a 5x5 ANSI loupe for scripted sampling
otter-pick --no-copy       # print only
otter-pick --hex '#336699' # offline conversion/test path
```

Output includes hex, RGB, and OKLCH. Clipboard output goes through the shared
Otter clipboard helper; packaged installs shadow `wl-copy` to native
`otter-copy`, with `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store` as the unavailable-Wayland fallback.

Config: `~/.config/otter-shell/otter-pick.conf`

```text
copy = true
loupe = false
```

## License

MIT License — see [LICENSE](LICENSE).
