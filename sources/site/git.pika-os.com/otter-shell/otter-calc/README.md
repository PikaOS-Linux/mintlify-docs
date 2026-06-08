# otter-calc

Quick calculator overlay core. CLI evaluates an expression, prints the result, or
copies it for overlay/launcher use.

```bash
otter-calc '2 + 3 * 4'
otter-calc 2 + 3 '* 4'
otter-calc --copy '(2 + 3) * 4'
```

`--copy` uses the shared Otter clipboard helper. Packaged installs shadow
`wl-copy` to native `otter-copy`; `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store` is used only when the
Wayland clipboard path is unavailable.

Config: `~/.config/otter-shell/otter-calc.conf`

```text
copy_result = false
```

## License

MIT License — see [LICENSE](LICENSE).
