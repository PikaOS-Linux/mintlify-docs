# otter-utils

Stack-allocated utilities for the Otter desktop shell. Provides bounded arrays, path handling, and zero-allocation logging.

## Components

### BoundedArray

A drop-in replacement for the removed `std.BoundedArray` in Zig 0.15+. Provides a fixed-capacity array with dynamic length.

```zig
const utils = @import("otter_utils");

var arr = utils.BoundedArray(u8, 256){};
try arr.append(42);
try arr.appendSlice("hello");

const slice = arr.constSlice();
```

### FilePath

Stack-allocated file path with builder operations, using `fs.max_path_bytes` as the buffer size.

```zig
const FilePath = @import("otter_utils").FilePath;

// Create from string
const path = try FilePath.from("/home/user/docs");

// Create from segments
const path2 = try FilePath.fromMany(&.{ "home", "user", "docs" });

// Append segments incrementally
var builder = try FilePath.from("/home");
try builder.appendSegment("user");
try builder.appendSegment("docs");
const s = builder.slice(); // [:0]const u8

// Pop segments
_ = builder.pop(); // returns "docs"
```

### Logging

Zero-allocation logging with scoped loggers and performance counters.

```zig
const log = @import("otter_utils").log;

// Scoped logger
const mylog = log.Scoped("my-component");
mylog.info("starting up", .{});
mylog.debug("value: {}", .{42});
mylog.err("something failed", .{});

// Performance counter
var counter = log.Counter{};
counter.inc();
counter.add(5);
const total = counter.reset();

// Timer
var timer = log.Timer{};
timer.begin();
// ... do work ...
const elapsed_ms = timer.elapsedMs();

// Periodic reporter
var reporter = log.Reporter("perf", 30).init();
if (reporter.shouldReport()) |elapsed| {
    // report metrics
}
```

### Inotify

Generic inotify wrapper for file/directory watching. Used by otter-conf for config hot-reload and otter-desktop for application list changes.

```zig
const inotify = @import("otter_utils").inotify;

var watcher = try inotify.Watcher.init(allocator);
defer watcher.deinit();

// Watch a file for changes
_ = try watcher.addWatch("/path/to/file", inotify.Watcher.Mask.file_changes);

// Watch a directory for changes
_ = try watcher.addWatch("/path/to/dir", inotify.Watcher.Mask.dir_changes);

// In event loop, poll watcher.getFd() then:
while (watcher.nextEvent()) |event| {
    if (event.isModified()) {
        // File was modified
    }
    if (event.isCreated()) {
        // File was created (directory watching)
    }
}
```

Event helper methods:
- `isModified()` - File was written and closed
- `isDeleted()` - File was deleted
- `isCreated()` - File was created
- `isMoved()` - File was moved/renamed
- `isIgnored()` - Watch was removed

## Running Tests

```bash
cd otter-utils
zig build test
```

## Dependencies

None. This is a pure Zig library with no external dependencies.

## License

MIT License — see [LICENSE](LICENSE).
