# otter-config-types

Shared configuration struct definitions for all Otter Shell applications.

## Purpose

Provides the typed config structs that `otter-conf` parses into and serializes from. Each application has its own config module defining the fields, defaults, and types used in its `.conf` file.

## Modules

| Module | Application | Key Types |
|--------|-------------|-----------|
| `bar.zig` | otter-bar | `Config`, `LayoutConfig`, `ClockConfig`, `WorkspacesConfig`, `BatteryConfig`, `ButtonConfig`, etc. |
| `launcher.zig` | otter-launcher | Launcher appearance and behavior settings |
| `notifications.zig` | otter-notifications | Notification daemon display settings |
| `wallpaper.zig` | otter-wallpaper | Wallpaper mode and path settings |
| `osd.zig` | otter-osd | On-screen display appearance settings |
| `jade.zig` | otter-jade | Layer-shell animated pet settings |
| `logout.zig` | otter-logout | Power menu overlay settings |
| `polkit.zig` | otter-polkit | Polkit auth agent dialog settings |
| `lock.zig` | otter-lock | Session lockscreen settings (colors, layout, PAM, focus output) |

## Usage

```zig
const config_types = @import("otter_config_types");
const BarConfig = config_types.bar.Config;
const ButtonConfig = config_types.bar.ButtonConfig;
```

Config structs follow otter-conf conventions:
- All fields must have defaults
- Nested structs are flattened with underscore prefixes (`clock_time_format` -> `config.clock.time_format`)
- Optional color fields (`?Color = null`) for theme-mapped values
- Enum fields for constrained choices (e.g., `Position { top, bottom }`)

## Dependencies

- otter-geo (Rect, Size types)
- otter-render (Color type)

## Build

```bash
zig build
```

## License

MIT License — see [LICENSE](LICENSE).
