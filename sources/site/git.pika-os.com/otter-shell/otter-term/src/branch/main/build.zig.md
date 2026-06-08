# Source: https://git.pika-os.com/otter-shell/otter-term/src/branch/main/build.zig

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-term](https://git.pika-os.com/otter-shell/otter-term)

Watch [1](https://git.pika-os.com/otter-shell/otter-term/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-term/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-term/forks)

You've already forked otter-term

**Files**

**main**

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [a08263cad6](https://git.pika-os.com/otter-shell/otter-term/commit/a08263cad68e05225a2ea239fbb02cf83ba88ce5) [Render terminal chrome with otter UI](https://git.pika-os.com/otter-shell/otter-term/commit/a08263cad68e05225a2ea239fbb02cf83ba88ce5)

2026-06-04 01:40:09 +01:00

#### 

137 lines

4.9 KiB

Zig

[Raw](https://git.pika-os.com/otter-shell/otter-term/raw/branch/main/build.zig) [Permalink](https://git.pika-os.com/otter-shell/otter-term/src/commit/c754c2e16a8123222718a164949cd69f39b45a87/build.zig) [Blame](https://git.pika-os.com/otter-shell/otter-term/blame/branch/main/build.zig) [History](https://git.pika-os.com/otter-shell/otter-term/commits/branch/main/build.zig)

| | `const std = @import("std");` |
| --- | --- |
| | |
| | `const CAllocator = enum { libc, jemalloc, mimalloc };` |
| | |
| | `pub fn build(b: *std.Build) void {` |
| | `const target = b.standardTargetOptions(.{});` |
| | `const optimize = b.standardOptimizeOption(.{});` |
| | `const c_allocator = b.option(CAllocator, "c_allocator", "C allocator for linked libraries (jemalloc, mimalloc)") orelse .libc;` |
| | |
| | `const otter_geo = b.dependency("otter_geo", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `});` |
| | `const otter_utils = b.dependency("otter_utils", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `});` |
| | `const otter_render = b.dependency("otter_render", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const otter_wayland = b.dependency("otter_wayland", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const otter_theme = b.dependency("otter_theme", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const otter_conf = b.dependency("otter_conf", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `});` |
| | `const otter_vte = b.dependency("otter_vte", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const otter_ui = b.dependency("otter_ui", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const otter_config_types = b.dependency("otter_config_types", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | |
| | `const translate_c = b.addTranslateC(.{` |
| | `.root_source_file = b.path("src/c.h"),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `});` |
| | `translate_c.linkSystemLibrary("ghostty-vt", .{});` |
| | |
| | `const imports: []const std.Build.Module.Import = &.{` |
| | `.{ .name = "ghostty_vt", .module = translate_c.createModule() },` |
| | `.{ .name = "otter_geo", .module = otter_geo.module("otter_geo") },` |
| | `.{ .name = "otter_utils", .module = otter_utils.module("otter_utils") },` |
| | `.{ .name = "otter_render", .module = otter_render.module("otter_render") },` |
| | `.{ .name = "otter_wayland", .module = otter_wayland.module("otter_wayland") },` |
| | `.{ .name = "otter_theme", .module = otter_theme.module("otter_theme") },` |
| | `.{ .name = "otter_conf", .module = otter_conf.module("otter_conf") },` |
| | `.{ .name = "otter_vte", .module = otter_vte.module("otter_vte") },` |
| | `.{ .name = "otter_ui", .module = otter_ui.module("otter_ui") },` |
| | `.{ .name = "otter_config_types", .module = otter_config_types.module("otter_config_types") },` |
| | `};` |
| | |
| | `const exe = b.addExecutable(.{` |
| | `.name = "otter-term",` |
| | `.root_module = b.createModule(.{` |
| | `.root_source_file = b.path("src/main.zig"),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = imports,` |
| | `.link_libc = true,` |
| | `}),` |
| | `});` |
| | `exe.root_module.linkSystemLibrary("ghostty-vt", .{});` |
| | `exe.root_module.linkSystemLibrary("wayland-client", .{});` |
| | `exe.root_module.linkSystemLibrary("xkbcommon", .{});` |
| | |
| | `b.installArtifact(exe);` |
| | `b.installDirectory(.{` |
| | `.source_dir = b.path("data/applications"),` |
| | `.install_dir = .prefix,` |
| | `.install_subdir = "share/applications",` |
| | `});` |
| | `b.installDirectory(.{` |
| | `.source_dir = b.path("data/icons/hicolor"),` |
| | `.install_dir = .prefix,` |
| | `.install_subdir = "share/icons/hicolor",` |
| | `});` |
| | |
| | `const run_cmd = b.addRunArtifact(exe);` |
| | `run_cmd.step.dependOn(b.getInstallStep());` |
| | `if (b.args) |args| run_cmd.addArgs(args);` |
| | `b.step("run", "Run otter-term").dependOn(&run_cmd.step);` |
| | |
| | `const exe_tests = b.addTest(.{` |
| | `.root_module = b.createModule(.{` |
| | `.root_source_file = b.path("src/main.zig"),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = imports,` |
| | `.link_libc = true,` |
| | `}),` |
| | `});` |
| | `exe_tests.root_module.linkSystemLibrary("ghostty-vt", .{});` |
| | `exe_tests.root_module.linkSystemLibrary("wayland-client", .{});` |
| | `exe_tests.root_module.linkSystemLibrary("xkbcommon", .{});` |
| | |
| | `const run_exe_tests = b.addRunArtifact(exe_tests);` |
| | `b.step("test", "Run unit tests").dependOn(&run_exe_tests.step);` |
| | |
| | `const profile_exe = b.addExecutable(.{` |
| | `.name = "otter-term-profile",` |
| | `.root_module = b.createModule(.{` |
| | `.root_source_file = b.path("src/profile_scenarios.zig"),` |
| | `.target = target,` |
| | `.optimize = .ReleaseFast,` |
| | `.imports = imports,` |
| | `.link_libc = true,` |
| | `}),` |
| | `});` |
| | `profile_exe.root_module.linkSystemLibrary("ghostty-vt", .{});` |
| | `profile_exe.root_module.linkSystemLibrary("wayland-client", .{});` |
| | `profile_exe.root_module.linkSystemLibrary("xkbcommon", .{});` |
| | |
| | `const run_profile = b.addRunArtifact(profile_exe);` |
| | `b.step("profile", "Run otter-term profiling scenarios").dependOn(&run_profile.step);` |
| | `}` |

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-term/blame/commit/c754c2e16a8123222718a164949cd69f39b45a87/build.zig) [Copy Permalink]()