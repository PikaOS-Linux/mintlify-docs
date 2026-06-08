# otter-wayland

Wayland client library for the Otter desktop shell. Provides connection management, input handling, SHM buffer management, and protocol handlers for common Wayland extensions.

## Wayland Protocols

- **wl_compositor** - Surface creation and management
- **wl_seat** - Input device handling (pointer, keyboard)
- **wl_shm** - Shared memory buffer management
- **wl_output** - Monitor/output detection
- **zwlr_layer_shell_v1** - Layer shell for positioning surfaces (panels, overlays)
- **ext_workspace_manager_v1** - Workspace tracking and switching
- **zwlr_foreign_toplevel_manager_v1** - Active window tracking
- **wp_cursor_shape_manager_v1** - Cursor shape management
- **wp_viewporter** - Buffer scaling (allows small buffers to fill large surfaces)
- **wl_data_device_manager** / **wl_data_device** - Clipboard paste and drag-and-drop support via data offers
- **zwp_text_input_manager_v3** / **zwp_text_input_v3** - IME (Input Method Editor) support for CJK and compose-key input
- **ext_session_lock_manager_v1** / **ext_session_lock_v1** - Session lock (lockscreen) protocol

## Usage

### Connection Management

```zig
const otter_wayland = @import("otter_wayland");

var conn: otter_wayland.Connection = .{};
conn.callbacks = .{
    .on_output_added = onOutputAdded,
    .on_seat_added = onSeatAdded,
    .context = &my_app_state,
};
try conn.init();
defer conn.deinit();

// Event loop
while (conn.running) {
    try conn.dispatch();
}
```

### Workspace Management (ext-workspace-v1)

```zig
var workspace_manager: otter_wayland.ExtWorkspaceManager = .{};

// Subscribe to state changes
_ = workspace_manager.subscribe(onWorkspaceChange, context);

// Get current state
const state = workspace_manager.getState();
for (state.workspaces.constSlice()) |ws_id| {
    // Get workspace name from protocol (compositor-provided)
    if (workspace_manager.getWorkspaceName(ws_id)) |name| {
        // Use the protocol name (e.g. "1", "web", "code")
    }
}

// Switch workspace
workspace_manager.setWorkspace(2);
```

### Foreign Toplevel (Active Window Tracking)

```zig
var toplevel_manager: otter_wayland.ForeignToplevelManager = .{};

// Subscribe to state changes
_ = toplevel_manager.subscribe(onToplevelChange, context);

// Get active window info
const state = toplevel_manager.getActiveState();
const title = state.title.constSlice();
const app_id = state.app_id.constSlice();
```

### Input Handling

```zig
var seat_state: otter_wayland.SeatState = .{};
seat_state.setCallbacks(.{
    .on_enter = onPointerEnter,
    .on_motion = onPointerMotion,
    .on_button = onPointerButton,
    .on_scroll = onPointerScroll,
    .on_scroll_end = onScrollEnd,  // fires on axis_stop (touchpad/smooth scroll)
    .context = &my_app_state,
});

// Set cursor shape
seat_state.setCursorShape(.pointer);

// Raw signed pointer coordinates (updated on every motion event, before clamping)
// Useful for detecting pointer outside surface bounds (negative = off-surface)
const px = seat_state.pointer_x;  // i32, surface-local
const py = seat_state.pointer_y;  // i32, surface-local
```

### Keyboard Input (xkbcommon)

```zig
const otter_wayland = @import("otter_wayland");

var keyboard = try otter_wayland.Keyboard.init();
defer keyboard.deinit();

keyboard.setCallbacks(.{
    .on_key = onKey,
    .on_enter = onKeyboardEnter,  // receives ?*wl.Surface for focus tracking
    .on_leave = onKeyboardLeave,
    .context = &my_app_state,
});

// Set keyboard in seat state for automatic wl_keyboard handling
seat_state.keyboard = &keyboard;

// Key repeat via timerfd - add to poll loop
if (keyboard.getRepeatFd()) |fd| {
    // ... poll fd ...
    keyboard.handleRepeat();  // Call when fd is readable
}

fn onKey(keysym: u32, utf8: []const u8, state: otter_wayland.KeyState, mods: otter_wayland.keyboard.Modifiers, ctx: ?*anyopaque) void {
    if (state != .pressed) return;
    // Handle keysym, utf8 text, and modifier state
}
```

### Text Input / IME (zwp_text_input_v3)

```zig
const otter_wayland = @import("otter_wayland");

// Create text input from connection's manager and seat
var text_input = otter_wayland.TextInput.init(
    conn.text_input_manager,
    conn.seat,
);
defer text_input.deinit();

text_input.setCallbacks(.{
    .on_commit = onImeCommit,    // Final committed text from IME
    .on_preedit = onImePreedit,  // In-progress composition string
    .context = &my_app_state,
});

// Enable on keyboard focus (call commit() after each state change)
text_input.enable(wl_surface);
text_input.commit();

// Position IME candidate window near cursor
text_input.setCursorRectangle(cursor_x, cursor_y, 1, input_height);
text_input.commit();

// Disable on blur
text_input.disable();
text_input.commit();

// Check composition state
if (text_input.isComposing()) {
    // Suppress direct key handling — IME owns the input
}
const preedit_text = text_input.getPreedit();  // Current composition string

fn onImeCommit(text: []const u8, ctx: ?*anyopaque) void {
    // Append committed text to input buffer
}

fn onImePreedit(text: ?[]const u8, cursor_begin: i32, cursor_end: i32, ctx: ?*anyopaque) void {
    // Update preedit display (null = composition ended)
}
```

### Clipboard (Paste)

```zig
const otter_wayland = @import("otter_wayland");

var clipboard: otter_wayland.Clipboard = .{};

// Initialize after display, seat, and data_device_manager are bound
if (conn.data_device_manager) |ddm| {
    clipboard.init(conn.display, ddm, seat);
}
defer clipboard.deinit();

// Read clipboard text (e.g., on Ctrl+V)
var paste_buf: [4096]u8 = undefined;
if (clipboard.getText(conn.display, &paste_buf)) |text| {
    // text is a slice of paste_buf containing the clipboard content
}

// Optional: receive text or file URI drops
clipboard.setDropCallback(onDrop, &my_app_state);
```

### SHM Buffer Pool

```zig
var pool = try otter_wayland.BufferPool(2).init(width, height);
defer pool.deinit();

// Acquire buffer for rendering
if (pool.acquire()) |buffer| {
    // Draw to buffer.data
    // ...
    pool.release(buffer);
}
```

### Wayland SHM Pool (with wl_buffer management)

For Wayland surfaces that need proper wl_buffer integration with automatic release handling. Two variants are provided:

- **`DoubleShmPool`** - Double-buffered for interactive surfaces that need continuous rendering (bars, launchers)
- **`SingleShmPool`** - Single-buffered for static content that rarely changes (wallpapers). Supports `forceReleaseAll()` for immediate buffer reuse on static content redraws

```zig
const otter_wayland = @import("otter_wayland");

// Double-buffered pool for interactive surfaces
self.shm_pool = try otter_wayland.DoubleShmPool.init(.{
    .wl_shm = wl_shm,
    .width = 800,
    .height = 600,
    .scale = 2,         // HiDPI scale factor (1 = no scaling)
    .name = "my-surface",
});
// IMPORTANT: Call bindListeners after the struct is in its final memory location
self.shm_pool.?.bindListeners();

// Single-buffered pool for static content (halves memory usage)
self.pool = try otter_wayland.SingleShmPool.init(.{
    .wl_shm = wl_shm,
    .width = 1920,
    .height = 1080,
    .scale = 1,
});
self.pool.?.bindListeners();

// Acquire buffer for rendering (same API for both pool types)
if (self.shm_pool.?.acquire()) |acquired| {
    var surface = RenderSurface.fromPixelsScaledWithStride(
        acquired.pixels,
        self.shm_pool.?.physicalWidth(),
        self.shm_pool.?.physicalHeight(),
        acquired.stride_pixels,
        scale,
    );
    surface.clear(Color.black);
    surface.fillRectLogical(.{ .x = 10, .y = 10, .width = 100, .height = 50 }, Color.red);

    wl_surface.attach(acquired.wl_buffer, 0, 0);
    wl_surface.damageBuffer(0, 0, self.shm_pool.?.physicalWidth(), self.shm_pool.?.physicalHeight());
    wl_surface.commit();
    // Buffer automatically released via wl_buffer.release event
}

// Resize with new scale when needed (all buffers must be free)
try self.shm_pool.?.resizeWithScale(wl_shm, new_width, new_height, new_scale);
```

`WaylandShmPool` uses 256-byte aligned row stride and page-aligned buffer slots inside the memfd. This keeps `wl_shm` buffers eligible for compositors that can import shm-backed memfds through `udmabuf`/dmabuf. Callers must use `acquired.stride_pixels` when wrapping `acquired.pixels` in an `otter_render.Surface`; the visible width can be smaller than the memory stride.

### Layer Shell Popup

Generic overlay popup surface for tooltips, menus, and transient UI:

```zig
const otter_wayland = @import("otter_wayland");

var popup = otter_wayland.LayerPopup.init(.{
    .wl_shm = wl_shm,
    .compositor = compositor,
    .layer_shell = layer_shell,
    .output = output,        // optional, null for default
    .bar_at_bottom = false,  // true to anchor popups from bottom edge
});
defer popup.deinit();

// Show popup at position with HiDPI scale
try popup.showWithScale(
    .menu,           // popup type
    100,             // x position (logical)
    32,              // y position (logical)
    200,             // width (logical)
    150,             // height (logical)
    scale,           // HiDPI scale factor from output
    drawCallback,    // fn(*RenderSurface, Point, ?*anyopaque) void
    context,         // passed to callback
);

// Or show centered on an x position
try popup.showCentered(
    .tooltip,
    center_x,
    y,
    width,
    height,
    screen_width,
    scale,           // HiDPI scale factor
    drawCallback,
    context,
);

// Hide (marks for deferred destruction)
popup.hide();

// Call after Wayland dispatch to actually destroy
popup.processPendingHide();

// Query state
if (popup.isActiveAndConfigured()) {
    // Popup is ready for interaction
}
```

### XDG Toplevel Window

Reusable wrapper for xdg_surface + xdg_toplevel lifecycle with configure event handling and HiDPI scale tracking:

```zig
const otter_wayland = @import("otter_wayland");

var toplevel = otter_wayland.XdgToplevel.init(&conn, .{
    .on_configure = onConfigure,
    .on_close = onClose,
    .context = &my_state,
});
toplevel.bindListeners();  // After struct is at stable address

toplevel.setTitle("My Window");
toplevel.setAppId("com.example.myapp");

fn onConfigure(width: u31, height: u31, state: otter_wayland.XdgToplevelState, ctx: ?*anyopaque) void {
    // width/height of 0 = client decides dimensions
    if (state.activated) { /* window focused */ }
}
```

### Hyprland IPC (Alternative Workspace Provider)

```zig
const hyprland = otter_wayland.protocols.hyprland;

if (hyprland.available()) {
    var manager: hyprland.HyprlandManager = .{};
    manager.initState();

    const state = manager.getState();
    // Process workspaces...

    // Handle events
    manager.processEvent("workspace", "2");
}
```

## Running Tests

```bash
zig build test
```

## Dependencies

- wayland-client (system library)
- xkbcommon (system library)
- otter_geo
- otter_render
- otter_utils

## License

MIT License — see [LICENSE](LICENSE).
