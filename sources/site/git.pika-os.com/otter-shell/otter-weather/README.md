# otter-weather

Open-Meteo weather fetcher for the bar widget and 7-day popup.

```bash
otter-weather
otter-weather 40.7128 -74.0060
otter-weather --dry-run 51.5072 -0.1276
otter-weather --write-cache
otter-weather --watch 900 --write-cache
otter-weather --cache
otter-weather --layer
```

Default location is London. The CLI fetches current conditions plus seven daily
rows with Zig's std HTTP client and a 128 KiB response cap. `--dry-run` prints
the generated Open-Meteo URL. `--write-cache` refreshes the bounded cache read by
the `otter-bar` weather widget; `--watch SECONDS` keeps refreshing that cache;
`--cache` prints an existing cache without HTTP.
`--layer` opens the cached forecast in a small layer-shell popup and exits when
clicked.

Config: `~/.config/otter-shell/otter-weather.conf`

```text
latitude = 51.5072
longitude = -0.1276
# Optional; empty uses $XDG_CACHE_HOME/otter-shell/weather-cache
cache_path = ""
write_cache = false
watch_seconds = 0
```

`--watch` mode reloads this config file between refreshes.

## License

MIT License — see [LICENSE](LICENSE).
