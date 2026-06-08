# otter-desktop

Desktop integration library for the Otter shell. Provides XDG icon lookup, .desktop file parsing, application management, D-Bus clients, and system services.

## Features

### Applications
- **Icon Lookup**: XDG icon theme lookup with caching
- **Desktop Entry Parsing**: Full .desktop file parser with locale support
- **Application List**: Manages installed applications with deduplication
- **Hot-Reload**: inotify-based watching for .desktop file changes
- **App Launcher**: Exec field expansion and process spawning

### D-Bus Services
- **D-Bus Client**: sd-bus wrapper for IPC
- **UPower Client**: Battery monitoring via UPower D-Bus service
- **Power Profiles**: power-profiles-daemon client for power management
- **MPRIS**: Media player control and metadata tracking via MPRIS2 D-Bus
- **NetworkManager**: Network status monitoring and control (connection-aware icons, WiFi scanning, connection management) via system bus
- **SCX Loader**: SCX scheduler monitoring and control via system bus
- **Screensaver**: Screen saver inhibit/uninhibit via session bus
- **Notifications**: org.freedesktop.Notifications D-Bus service (notification types, store, and D-Bus handler for otter-notifications)

### System Services
- **Brightness Control**: Sysfs-based backlight control with connector-to-device matching for internal displays
- **System Info**: CPU, memory, disk, temperature, load, uptime via sysinfo(2), /proc/stat, /proc/meminfo, and /sys
- **Falcond**: Falcond daemon status monitoring via inotify file watching

### Authentication
- **PAM**: Password authentication via system PAM stack (lockscreen, polkit)

### Audio
- **PipeWire**: Audio device enumeration, per-device volume/mute control, default device switching via PipeWire metadata, pub/sub for state changes (native libpipewire-0.3). Volume steps use `roundToStep()` to prevent floating-point drift. Lazy proxy binding with automatic fallback on device hot-plug/removal

## Usage

### Icon Lookup

```zig
const otter_desktop = @import("otter_desktop");

// Direct lookup (caller owns returned memory)
if (otter_desktop.findIcon(allocator, "firefox")) |path| {
    defer allocator.free(path);
    // Use the icon path
}

// Cached lookups
var cache = otter_desktop.IconCache.init(allocator);
defer cache.deinit();
const icon_path = cache.lookup("firefox");
```

### Desktop Entry Parsing

```zig
const DesktopEntry = otter_desktop.applications.DesktopEntry;
const desktop_entry = otter_desktop.applications.desktop_entry;

var entry = try desktop_entry.parse(allocator, "/usr/share/applications/firefox.desktop", .{});
defer entry.deinit();

std.debug.print("Name: {s}\n", .{entry.name});
std.debug.print("Exec: {s}\n", .{entry.exec});
std.debug.print("Icon: {s}\n", .{entry.icon orelse "none"});
```

### Application List

```zig
const AppList = otter_desktop.applications.AppList;

// Without hot-reload
var apps = AppList.init(allocator);
defer apps.deinit();
try apps.scan();

// With hot-reload
var apps = try AppList.initWithWatcher(allocator);
defer apps.deinit();
try apps.scan();

// Subscribe to changes
apps.subscribe(myCallback, context);

// Poll for changes in event loop
if (apps.watcher) |*w| {
    while (w.nextEvent()) |event| {
        // Handle .desktop file changes
    }
}
```

### Launching Applications

```zig
const launcher = otter_desktop.applications.launcher;

// Auto-detects terminal emulator for Terminal=true entries
try launcher.launch(allocator, &entry);

// Or with explicit terminal config
try launcher.launchWithTerminal(allocator, &entry, .{
    .cmd = "foot",
    .exec_flag = "-e",
});

// Terminal detection checks $TERMINAL then probes PATH for known terminals:
// xdg-terminal-exec, foot, otter-term, ghostty, kitty, alacritty, wezterm, rio,
// contour, gnome-terminal, konsole, xfce4-terminal, mate-terminal, tilix, xterm
const detected = launcher.detectTerminal();
```

### D-Bus Client

```zig
const dbus = otter_desktop.dbus;

var conn = try dbus.Connection.open(allocator, .session);
defer conn.deinit();

// Get FD for poll integration
const fd = conn.getFd();

// Process messages
while (conn.process()) {}
```

### UPower (Battery Monitoring)

```zig
const UPower = otter_desktop.UPower;

var upower = try UPower.init(allocator);
defer upower.deinit();

// Start monitoring for property changes (call after struct is in final location)
upower.startMonitoring();

// Get primary battery info
if (upower.getPrimaryBattery()) |battery| {
    std.debug.print("Battery: {d}% ({s})\n", .{
        battery.getPercentage(),
        battery.state.toString(),
    });
}

// Check if on battery power
if (upower.isOnBattery()) {
    std.debug.print("Running on battery\n", .{});
}

// Subscribe to battery changes
_ = upower.subscribe(onBatteryChanged, context);

// Poll integration for event loop
const fd = upower.getFd();
// ... poll fd ...
while (upower.process()) {}
```

### Brightness Control

```zig
const Brightness = otter_desktop.Brightness;

var brightness = Brightness.init();
defer brightness.deinit();

// Open backlight for a specific display connector (recommended)
// Automatically matches connector to backlight device via sysfs symlinks
// Only works for internal displays (eDP, LVDS, DSI)
try brightness.openForConnector("eDP-1");

// Or auto-enumerate all available backlight devices
try brightness.enumerate();

// Or open a specific device by name
try brightness.openDevice("intel_backlight");

// Get/set brightness as percentage (0-100)
const level = brightness.getBrightness();
brightness.setBrightness(50);

// Adjust by delta with clamping
const new_level = brightness.adjustBrightness(-10);  // decrease by 10%

// Access individual devices
if (brightness.getPrimaryDevice()) |device| {
    std.debug.print("Device: {s}, brightness: {d}%\n", .{
        device.getName(),
        device.getBrightness(),
    });
}

// Check if connector is an internal display
if (Brightness.isInternalDisplay("eDP-1")) {
    // Has sysfs backlight support
}

// Check write capability
if (brightness.canWrite()) {
    // Can adjust brightness
}
```

### Power Profiles

```zig
const PowerProfiles = otter_desktop.PowerProfiles;

var profiles = try PowerProfiles.init(allocator);
defer profiles.deinit();

// Get current profile
if (profiles.getActiveProfile()) |active| {
    std.debug.print("Active: {s}\n", .{active});
}

// List available profiles
for (profiles.getProfiles()) |maybe_profile| {
    if (maybe_profile) |p| {
        std.debug.print("{s} (driver: {s})\n", .{p.name, p.driver});
    }
}

// Set profile
try profiles.setActiveProfile("balanced");

// Subscribe to profile changes
_ = profiles.subscribe(onProfileChanged, context);

// Poll integration for event loop
const fd = profiles.getFd();
// ... poll fd ...
while (profiles.process()) {}
```

### System Info

```zig
const SysInfo = otter_desktop.SysInfo;

var sysinfo = SysInfo.init();
defer sysinfo.deinit();

// Subscribe to state changes (pub/sub pattern)
_ = sysinfo.subscribe(onMetricsChanged, context);

// Option 1: Use poll() for throttled updates (recommended)
// Call frequently (e.g., every frame) - internally throttled to refresh_interval_ms
if (sysinfo.poll()) {
    // Refresh occurred, subscribers were notified
}

// Option 2: Force refresh (bypasses throttling)
sysinfo.refresh();

// Access cached metrics
const mem = sysinfo.memory;
std.debug.print("Memory: {d:.1} / {d:.1} GiB ({d}%)\n", .{
    mem.usedGiB(),
    mem.totalGiB(),
    mem.percent_used,
});

std.debug.print("CPU: {d}%\n", .{sysinfo.cpu_percent});

if (sysinfo.cpu_temp) |temp| {
    std.debug.print("Temperature: {d}°C\n", .{temp});
}

const disk = sysinfo.disk;
std.debug.print("Disk: {d:.1} / {d:.1} GiB ({d}%)\n", .{
    disk.usedGiB(),
    disk.totalGiB(),
    disk.percent_used,
});

std.debug.print("Load: {d:.2} {d:.2} {d:.2}\n", .{
    sysinfo.load.one,
    sysinfo.load.five,
    sysinfo.load.fifteen,
});

// Or query metrics directly (bypasses cache)
const mem_info = sysinfo.getMemoryInfo();
const disk_info = try sysinfo.getDiskInfo("/home");
```

#### CPU Temperature Sensors

SysInfo automatically detects CPU temperature sensors:

- **Intel (coretemp)**: Averages all core temperatures
- **AMD (k10temp/zenpower)**: Reads the Tctl sensor

Other sensors (network adapters, GPUs, etc.) are ignored to ensure accurate CPU temperature readings.

### MPRIS (Media Player Control)

```zig
const Mpris = otter_desktop.Mpris;

var mpris = try Mpris.init(allocator);
defer mpris.deinit();

// Start monitoring for player changes (call after struct is in final location)
mpris.startMonitoring();

// Get active player
if (mpris.getActivePlayer()) |player| {
    std.debug.print("Now playing: {s} - {s}\n", .{
        player.artist.get(),
        player.title.get(),
    });
    std.debug.print("Status: {s}\n", .{player.status.toString()});
    std.debug.print("Progress: {d}%\n", .{player.getProgress()});
}

// List all players
for (mpris.getPlayers()) |maybe_player| {
    if (maybe_player) |p| {
        std.debug.print("{s}: {s}\n", .{p.getShortName(), p.status.toString()});
    }
}

// Playback control
try mpris.playPause();
try mpris.next();
try mpris.previous();
try mpris.play();
try mpris.pause();
try mpris.stop();

// Subscribe to player changes
_ = mpris.subscribe(onPlayerChanged, context);

// Poll integration for event loop
const fd = mpris.getFd();
// ... poll fd ...
while (mpris.process()) {}
```

### SCX Loader (Scheduler Control)

```zig
const ScxLoader = otter_desktop.ScxLoader;
const ScxScheduler = otter_desktop.ScxScheduler;
const ScxMode = otter_desktop.ScxMode;

var scx = try ScxLoader.init(allocator);
defer scx.deinit();

// Start monitoring for property changes (call after struct is in final location)
scx.startMonitoring();

// Get current scheduler
if (scx.getCurrentScheduler()) |sched| {
    std.debug.print("Scheduler: {s}\n", .{sched.toScxName()});
}

// Get current mode
const mode = scx.getSchedulerMode();
std.debug.print("Mode: {d}\n", .{mode.toInt()});

// List supported schedulers
for (scx.getSupportedSchedulers()) |sched| {
    std.debug.print("  - {s}\n", .{sched.toScxName()});
}

// Switch scheduler
try scx.switchScheduler(.bpfland, .gaming);

// Stop scheduler
try scx.stopScheduler();

// Subscribe to scheduler changes
_ = scx.subscribe(onSchedulerChanged, context);

// Poll integration for event loop
const fd = scx.getFd();
// ... poll fd ...
while (scx.process()) {}
```

### Screensaver (Inhibit Control)

```zig
const Screensaver = otter_desktop.Screensaver;

var screensaver = try Screensaver.init(allocator);
defer screensaver.deinit();  // auto-uninhibits if needed

// Inhibit screensaver
const cookie = try screensaver.inhibit("my-app", "Playing video");

// Check status
if (screensaver.isInhibited()) {
    std.debug.print("Screensaver inhibited\n", .{});
}

// Uninhibit screensaver
try screensaver.uninhibit();
```

### NetworkManager (Network Status & Control)

```zig
const NetworkManager = otter_desktop.NetworkManager;

var nm = try NetworkManager.init(allocator);
defer nm.deinit();

// Start monitoring for state changes (call after struct is in final location)
nm.startMonitoring();

// Check connectivity
if (nm.isConnected()) {
    std.debug.print("Connected\n", .{});
}

// Active connections (WiFi, Ethernet, VPN)
for (nm.getConnections()) |maybe_conn| {
    if (maybe_conn) |conn| {
        std.debug.print("{s} ({s})", .{conn.getName(), conn.getIfaceName()});
        if (conn.device_type == .wifi) {
            std.debug.print(" WiFi {d}%", .{conn.wifi_strength});
        }
        if (conn.ip_address_len > 0) {
            std.debug.print(" {s}", .{conn.getIpAddress()});
        }
        std.debug.print("\n", .{});
    }
}

// WiFi scanning and network listing
nm.requestWifiScan();
nm.refreshWifiNetworks();
for (nm.getWifiNetworks()) |maybe_net| {
    if (maybe_net) |net| {
        std.debug.print("{s} {d}% {s}\n", .{
            net.getSsid(), net.strength, if (net.secured) "secured" else "open",
        });
    }
}

// Connection management
nm.activateConnection(conn_path, device_path, ap_path);
nm.deactivateConnection(active_conn_path);
nm.setWirelessEnabled(true);

// Byte counters from Device.Statistics (for rate calculation)
std.debug.print("RX: {d} TX: {d}\n", .{nm.total_rx_bytes, nm.total_tx_bytes});

// Subscribe to state changes
_ = nm.subscribe(onNmChanged, context);

// Poll integration for event loop
const fd = nm.getFd();
// ... poll fd ...
while (nm.process()) {}
```

### Falcond (Daemon Status)

```zig
const Falcond = otter_desktop.Falcond;

var falcond = try Falcond.init(allocator, null);  // null = default path
defer falcond.deinit();

// Poll integration (optional - file may not exist)
if (falcond.getFd()) |fd| {
    // ... poll fd ...
    _ = falcond.process();
}

// Get status
const status = falcond.getStatus();

// Check performance mode
if (status.isPerformanceActive()) {
    std.debug.print("Performance mode active\n", .{});
}

// Check active profile
if (status.hasActiveProfile()) {
    std.debug.print("Active profile: {s}\n", .{status.active_profile.get()});
}

// Check SCX scheduler
if (status.hasScxScheduler()) {
    std.debug.print("SCX scheduler: {s}\n", .{status.current_scx.get()});
}

// List available schedulers
for (status.getAvailableSchedulers()) |sched| {
    std.debug.print("  - {s}\n", .{sched.get()});
}

// Subscribe to status changes
_ = falcond.subscribe(onStatusChanged, context);
```

### PipeWire (Audio Control)

```zig
const PipeWire = otter_desktop.PipeWire;

var pw = try PipeWire.init(allocator);
defer pw.deinit();

// Start monitoring for device changes (call after struct is in final location)
pw.startMonitoring();

// Get default sink (speakers/headphones)
if (pw.getDefaultSink()) |sink| {
    std.debug.print("Output: {s}\n", .{sink.description.get()});
    std.debug.print("Volume: {d}%\n", .{sink.getVolumePercent()});
    std.debug.print("Muted: {any}\n", .{sink.muted});
}

// Get default source (microphone)
if (pw.getDefaultSource()) |source| {
    std.debug.print("Input: {s}\n", .{source.description.get()});
}

// List all devices
for (pw.getSinks()) |maybe_sink| {
    if (maybe_sink) |s| {
        std.debug.print("Sink: {s} ({d}%)\n", .{s.name.get(), s.getVolumePercent()});
    }
}

// Volume control (default sink)
try pw.setSinkVolume(0.5);        // Set to 50%
try pw.increaseSinkVolume(0.05);  // Increase by 5%
try pw.decreaseSinkVolume(0.05);  // Decrease by 5%
try pw.toggleSinkMute();          // Toggle mute
try pw.setSinkMute(true);         // Mute

// Per-device control (by node ID)
try pw.setNodeVolume(node_id, 0.75);  // Set any device to 75%
try pw.setNodeMute(node_id, true);    // Mute any device
try pw.toggleNodeMute(node_id);       // Toggle mute on any device

// Default device switching (via PipeWire metadata)
try pw.setDefaultSink(node_id);       // Set default output device
try pw.setDefaultSource(node_id);     // Set default input device

// Subscribe to device changes
_ = pw.subscribe(onDeviceChanged, context);

// Poll integration for event loop
if (pw.getFd()) |fd| {
    // ... poll fd ...
    _ = pw.process();
}
```

## Build Options

PipeWire and D-Bus (basu/sd-bus) are optional compile-time dependencies. Both default to enabled.

| Option | Default | Effect when disabled |
|---|---|---|
| `-Denable_dbus=false` | `true` | Removes D-Bus client, UPower, PowerProfiles, MPRIS, SystemTray, NetworkManager, SCX Loader, Screensaver |
| `-Denable_pipewire=false` | `true` | Removes PipeWire audio device control |
| `-Denable_pam=false` | `false` | Removes PAM authentication module |

```bash
# Build without D-Bus support
zig build -Denable_dbus=false

# Build without PipeWire
zig build -Denable_pipewire=false

# Minimal build (pure Zig modules only)
zig build -Denable_dbus=false -Denable_pipewire=false
```

When a feature is disabled, its types are exported as `void`. Consumers can check
`desktop.has_dbus` / `desktop.has_pipewire` / `desktop.has_pam` at comptime to conditionally compile.

## Icon Search Order

The icon lookup scans actual directories on disk rather than using hardcoded size/context lists. There are no bounded limits on the number of themes or subdirectories scanned.

1. **Preferred themes** (priority order): Single-pass scan of actual subdirectories (1-2 levels deep) within each theme, checking all extensions per subdir (SVG first for vector preference, then `.png/.jpg/.jpeg`). Uses dir-relative `faccessat` syscalls against open directory handles for minimal kernel overhead.
2. **All other themes**: Iterates remaining theme directories found on disk that aren't in the preferred list. Same single-pass scanning approach.
3. **Pixmaps fallback**: `{name}.{svg,png,jpg,jpeg}` in pixmaps directories.
4. **Desktop file fallback** (two-pass):
   - **Pass 1 (exact match)**: Looks for `{app_id}.desktop` by name in each application directory.
   - **Pass 2 (directory scan)**: Iterates all `.desktop` files in each directory and matches their `Icon=` field against the app_id. This handles AppImages and other apps where the `.desktop` filename differs from the icon name (e.g., `appimagekit_<hash>-<name>.desktop`).
   - Icon resolution from `.desktop` files tries theme lookup first, then absolute path with extension fallback (`.svg/.png/.jpg/.jpeg`).

SVG is preferred over raster formats within each subdirectory. Candidate filenames are pre-built once per theme and full return paths are only constructed on hit. Directory scanning discovers icons in any theme layout (size/context, context/size, or flat) without hardcoding paths.

### Icon base directories (searched in order)

| Path | Source |
|------|--------|
| `$XDG_DATA_HOME/icons/` | User icons |
| `~/.local/share/flatpak/exports/share/icons/` | User flatpak |
| `/usr/share/icons/` | System |
| `/usr/local/share/icons/` | System (local) |
| `/var/lib/flatpak/exports/share/icons/` | System flatpak |

Pixmaps: `/usr/share/pixmaps/`, `/usr/local/share/pixmaps/`, `~/.local/share/flatpak/exports/share/pixmaps/`, `/var/lib/flatpak/exports/share/pixmaps/`

### Desktop file directories (searched in order)

| Path | Source |
|------|--------|
| `$XDG_DATA_HOME/applications/` | User apps (AppImages install here) |
| `~/.local/share/flatpak/exports/share/applications/` | User flatpak |
| `/usr/share/applications/` | System |
| `/usr/local/share/applications/` | System (local) |
| `/var/lib/flatpak/exports/share/applications/` | System flatpak |

## Preferred Icon Themes

Themes checked first, in priority order:

- steam, Papirus-Colors-Dark, Papirus-Dark, Papirus-Colors, Papirus, Papirus-Light
- breeze-dark, breeze
- Adwaita, hicolor

## Benchmarks

```bash
cd otter-desktop/benchmarks

# Run all benchmarks
zig build bench

# Individual benchmarks
zig build bench-icon-lookup   # Icon lookup (direct + cached + per-icon breakdown)
zig build bench-scan          # Application directory scanning
zig build bench-parse         # .desktop file parsing
zig build bench-sysinfo       # System info collection

# Generate test data for parse benchmark
zig build gen-testdata
```

## Running Tests

```bash
cd otter-desktop
zig build test

# Tests without D-Bus
zig build test -Denable_dbus=false

# Tests without PipeWire
zig build test -Denable_pipewire=false
```

## Display Manager APIs

`otter-desktop` exposes reusable display-manager primitives for `otter-greeter`:

- `pam_session.zig` wraps stateful PAM conversations and session lifecycle.
- `session_catalog.zig` scans Wayland `.desktop` session files and maps `DesktopNames` to XDG session variables.
- `session_launcher.zig` builds user/session environment without synthesizing logind-owned variables.
- `accounts_service.zig` loads AccountsService users with passwd fallback.
- `logind_seats.zig` provides logind seat records and watch hooks.
- `power_actions.zig` routes shutdown, reboot, and suspend requests through logind policy.

## Dependencies

### Build Dependencies
- **otter-utils** - Shared inotify wrapper for directory watching

### Vendored/Static Libraries
- **basu** (sd-bus) - D-Bus client library, statically linked. Required when D-Bus support is enabled (default)
  - Location: `vendor/basu/`
  - License: LGPL-2.1+
  - Source: https://github.com/emersion/basu

- **PipeWire** - Audio control library, statically linked. Required when PipeWire support is enabled (default)
  - License: MIT
  - Source: https://github.com/allyourcodebase/pipewire (Zig package)
  - Upstream: https://pipewire.org/

## Runtime Services

- **UPower** - Required for battery monitoring (optional)
- **power-profiles-daemon** or **tuned-ppd** - Required for power profile management (optional)
- **PipeWire** - Required for audio control (optional)
- **Falcond** - Required for falcond status monitoring (optional)
- **NetworkManager** - Required for network status monitoring and WiFi/VPN management (optional)
- **scx_loader** - Required for SCX scheduler control (optional)
- **MPRIS-compatible media player** - Required for media player control (optional)
- **PAM** (`libpam-dev`) - Required for lockscreen authentication (optional)

## License

MIT License — see [LICENSE](LICENSE). Third-party licenses for vendored code are listed under **Vendored / third-party** above.
