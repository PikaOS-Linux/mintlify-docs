# otter-clip

Clipboard manager with bounded Wayland data-control monitoring and native copy/paste CLIs.
`otter-copy` and `otter-paste` use Wayland data-control directly. The package also owns
and shadows the `wl-copy` and `wl-paste` names, so existing app calls resolve to
Otter's native implementation.

```bash
otter-clip daemon          # monitor clipboard selection changes
otter-clip popup           # open Super+V launcher-backed history popup
otter-clip popup query     # open popup with search prefilled
otter-clip list            # print stored history
otter-clip search query    # filter history
otter-clip add some text   # manually append text
otter-clip clear           # clear history
otter-clip pin 0           # pin entry
otter-clip unpin 0
otter-clip select 0        # copy a history entry
otter-copy text            # copy argv text
printf text | otter-copy   # copy stdin
png-tool | otter-copy --type image/png
otter-paste [-n]
wl-copy text               # packaging shadows this name to otter-copy
wl-paste [-n]              # packaging shadows this name to otter-paste
otter-clip --file /tmp/history list
otter-copy --file /tmp/store text
otter-paste --file /tmp/store
```

History defaults to `$XDG_CACHE_HOME/otter-shell/otter-clip-history` (legacy `/tmp/otter-clip-history` is still read when configured) and is capped in memory.
`popup` opens `otter-launcher --query "clip ..."`; launcher rows call back into
`otter-clip select INDEX` so Enter copies the selected history item. Text offers
and common image MIME types are accepted; images are stored as bounded blob files
with MIME/path metadata so the launcher can show thumbnails. Clipboard monitor
skips password/secret MIME hints before reading data. Wayland data-control does
not expose the source app id for copied data, so app-id password-manager
filtering is enforced only when a source id is available to the caller.

Config: `~/.config/otter-shell/otter-clip.conf`

```text
# Optional; empty uses $XDG_CACHE_HOME/otter-shell/otter-clip-history
history_path = ""
```

## License

MIT License — see [LICENSE](LICENSE).
