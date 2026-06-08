# otter-emoji

Searchable emoji picker core. CLI prints matching glyph/name rows or a compact
grid for launcher integration.

Emoji data comes from Unicode 17.0.0 `emoji-test.txt` and includes all
fully-qualified emoji sequences.

```bash
otter-emoji heart
otter-emoji --grid weather
otter-emoji --limit 8 smile
otter-emoji --copy rocket
```

`--copy` copies the first match through the shared Otter clipboard helper.
Packaged installs shadow `wl-copy` to native `otter-copy`; `$XDG_RUNTIME_DIR/otter-shell/otter-clip-store`
is used only when the Wayland clipboard path is unavailable.

Config: `~/.config/otter-shell/otter-emoji.conf`

```text
grid = false
copy = false
limit = 32
```

## License

MIT License — see [LICENSE](LICENSE).
