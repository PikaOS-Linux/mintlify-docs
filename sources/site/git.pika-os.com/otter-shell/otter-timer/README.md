# otter-timer

`otter-timer 5m` waits for countdown completion and emits a desktop ping.

```bash
otter-timer 5m
otter-timer --message "Tea" 3m
otter-timer --command 'playerctl pause' 30m
otter-timer --dry-run 30s
otter-timer --no-notify 1h
```

Durations support `s`, `m`, `h`, and `d` segments such as `1h30m`.
Completion sends `otter-osd message` when available and still prints `timer done`.
If `command` is set, it runs after the timer completes.

Config: `~/.config/otter-shell/otter-timer.conf`

```text
default_duration = ""
message = "Timer done"
command = ""
notify = true
```

## License

MIT License — see [LICENSE](LICENSE).
