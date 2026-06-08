# otter-idle

Wayland idle management daemon for the Otter desktop shell. Detects user inactivity via `ext-idle-notify-v1`, executes configurable timeout/resume commands, integrates with systemd-logind for sleep events, and provides built-in DPMS control via `wlr-output-power-management-unstable-v1` with compositor IPC fallbacks.

## Architecture

Poll-based event loop monitoring four file descriptors:

- **Wayland display** -- idle notifications and output power management
- **logind system bus** -- PrepareForSleep, Lock, and Unlock signals with delay inhibitor locks
- **ScreenSaver session bus** -- `org.freedesktop.ScreenSaver` Inhibit/UnInhibit tracking from applications
- **inotify config watcher** -- hot-reload on config file changes

Up to 8 listeners can be configured, each with an independent timeout. When a listener fires, inhibitors are checked before executing the command. Resume commands only fire if the corresponding timeout command was actually executed.

### DPMS

Built-in DPMS commands (`dpms:off`, `dpms:on`, `dpms:standby`, `dpms:suspend`) are handled natively without spawning a shell. Backend selection:

1. `wlr-output-power-management-unstable-v1` protocol (preferred, wlroots compositors)
2. Compositor IPC fallback detected from `XDG_CURRENT_DESKTOP`:
   - Hyprland: `hyprctl dispatch dpms`
   - Sway: `swaymsg "output * dpms"`
   - niri: `niri msg action power-off-monitors` / `power-on-monitors`

### Inhibitor Stack

Three layers of idle inhibition are supported:

1. **Wayland-native** (`zwp_idle_inhibit_manager_v1`) -- handled by the compositor, suppresses idle notifications transparently
2. **D-Bus** (`org.freedesktop.ScreenSaver`) -- tracked by otter-idle's built-in service, apps like video players call Inhibit/UnInhibit
3. **systemd** (`loginctl inhibit`) -- checked via logind ListInhibitors for `what=idle`

## Build

```bash
cd otter-idle && zig build
```

## Run

```bash
otter-idle
```

## Test

```bash
cd otter-idle && zig build test
```

## Configuration

Config file: `~/.config/otter-shell/otter-idle.conf` (fallback: `/etc/otter-shell/otter-idle.conf`). Auto-created with sensible defaults on first run. Hot-reloadable via inotify.

```conf
# Lock command run when logind Lock signal is received
lock_cmd = pidof otter-lock || otter-lock
unlock_cmd =

# Commands run before/after system sleep
before_sleep_cmd = loginctl lock-session
after_sleep_cmd = dpms:on

# Inhibitor policy
ignore_dbus_inhibit = false
ignore_systemd_inhibit = false

# Listener 1: Lock screen after 5 minutes
listener_1_timeout = 300
listener_1_on_timeout = loginctl lock-session
listener_1_on_resume =

# Listener 2: DPMS off after 6 minutes, on when resumed
listener_2_timeout = 360
listener_2_on_timeout = dpms:off
listener_2_on_resume = dpms:on
```

### Built-in Commands

| Command | Effect |
|---------|--------|
| `dpms:off` | Turn displays off |
| `dpms:on` | Turn displays on |
| `dpms:standby` | Set displays to standby |
| `dpms:suspend` | Set displays to suspend |

Any other value is executed as a shell command via `/bin/sh -c`.

### Listeners

Up to 8 listeners (`listener_1` through `listener_8`). Each has:

- `timeout` -- Idle time in seconds before firing (0 = disabled)
- `on_timeout` -- Command to run when the user becomes idle
- `on_resume` -- Command to run when activity resumes (only fires if on_timeout executed)

## Dependencies

Shared libraries from the otter-shell monorepo: otter-utils, otter-wayland, otter-desktop, otter-conf, otter-config-types.

### System Libraries

- wayland-client
- sd-bus (vendored basu, via otter-desktop)

## License

MIT License — see [LICENSE](LICENSE).
