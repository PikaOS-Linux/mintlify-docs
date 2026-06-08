# otter-cal

Calendar popover core. CLI prints a month grid and bounded agenda list suitable
for bar clock popover integration.

```bash
otter-cal
otter-cal --month 2026-06
otter-cal --today 2026-06-05 --agenda ~/.config/otter-shell/agenda
otter-cal --next 1
```

Agenda lines use:

```text
YYYY-MM-DD text
```

The bar clock launches `clock_calendar_command` on left click. Default:

```text
clock_calendar_command = "otter-cal"
```

Config: `~/.config/otter-shell/otter-cal.conf`

```text
agenda_path = ""
```

## License

MIT License — see [LICENSE](LICENSE).
