# otter-note

Sticky markdown notes with a Super+N-ready layer-shell surface.

```bash
otter-note add "ship release"
otter-note new
otter-note --pin top-right new
otter-note list
otter-note clear
otter-note --path /tmp/notes.md add test note
```

Default storage is `$XDG_DATA_HOME/otter-shell/notes.md` or
`$HOME/.local/share/otter-shell/notes.md`. The sticky surface edits markdown
directly when edit mode is enabled, saves on exit or Ctrl+S, and toggles rendered
markdown preview with Ctrl+M. In view mode only the header buttons accept input,
so the note body does not block apps underneath it. The install step provides
`otter-note.desktop`, so the launcher indexes it as a normal application.

Config: `~/.config/otter-shell/otter-note.conf`

```text
notes_path = ""
```

## License

MIT License — see [LICENSE](LICENSE).
