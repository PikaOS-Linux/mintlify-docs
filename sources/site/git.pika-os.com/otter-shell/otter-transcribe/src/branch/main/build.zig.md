# Source: https://git.pika-os.com/otter-shell/otter-transcribe/src/branch/main/build.zig

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-transcribe](https://git.pika-os.com/otter-shell/otter-transcribe)

Watch [1](https://git.pika-os.com/otter-shell/otter-transcribe/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-transcribe/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-transcribe/forks)

You've already forked otter-transcribe

**Files**

**main**

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [c0a6586e07](https://git.pika-os.com/otter-shell/otter-transcribe/commit/c0a6586e07ff5caf044b2dfadf467cee6c2e50eb) [Use direct PipeWire capture](https://git.pika-os.com/otter-shell/otter-transcribe/commit/c0a6586e07ff5caf044b2dfadf467cee6c2e50eb)

2026-06-06 18:27:48 +01:00

#### 

179 lines

7.9 KiB

Zig

[Raw](https://git.pika-os.com/otter-shell/otter-transcribe/raw/branch/main/build.zig) [Permalink](https://git.pika-os.com/otter-shell/otter-transcribe/src/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5/build.zig) [Blame](https://git.pika-os.com/otter-shell/otter-transcribe/blame/branch/main/build.zig) [History](https://git.pika-os.com/otter-shell/otter-transcribe/commits/branch/main/build.zig)

| | `const std = @import("std");` |
| --- | --- |
| | |
| | `const CAllocator = enum { libc, jemalloc, mimalloc };` |
| | `const EmbeddedModel = enum { q8_0, f16 };` |
| | |
| | `const parakeet_static_archives = [_][]const u8{` |
| | `"vendor/parakeet.cpp/build-static/libparakeet.a",` |
| | `"vendor/parakeet.cpp/build-static/third_party/ggml/src/libggml.a",` |
| | `"vendor/parakeet.cpp/build-static/third_party/ggml/src/libggml-cpu.a",` |
| | `"vendor/parakeet.cpp/build-static/third_party/ggml/src/libggml-base.a",` |
| | `};` |
| | |
| | `pub fn build(b: *std.Build) void {` |
| | `const target = b.standardTargetOptions(.{});` |
| | `const optimize = b.standardOptimizeOption(.{});` |
| | `const c_allocator = b.option(CAllocator, "c_allocator", "C allocator for linked libraries (jemalloc, mimalloc)") orelse .libc;` |
| | `const embedded_model = b.option(EmbeddedModel, "embedded_model", "Embedded GGUF model variant (f16, q8_0)") orelse .f16;` |
| | `const embedded_model_file = switch (embedded_model) {` |
| | `.q8_0 => "realtime_eou_120m-v1-q8_0.gguf",` |
| | `.f16 => "realtime_eou_120m-v1-f16.gguf",` |
| | `};` |
| | `const embedded_model_runtime_name = switch (embedded_model) {` |
| | `.q8_0 => "otter-transcribe-realtime_eou_120m-v1-q8_0.gguf",` |
| | `.f16 => "otter-transcribe-realtime_eou_120m-v1-f16.gguf",` |
| | `};` |
| | `const options = b.addOptions();` |
| | `options.addOption([]const u8, "embedded_model_file", embedded_model_file);` |
| | `options.addOption([]const u8, "embedded_model_runtime_name", embedded_model_runtime_name);` |
| | |
| | `const utils = b.dependency("otter_utils", .{ .target = target, .optimize = optimize });` |
| | `const geo = b.dependency("otter_geo", .{ .target = target, .optimize = optimize });` |
| | `const render = b.dependency("otter_render", .{ .target = target, .optimize = optimize, .c_allocator = c_allocator });` |
| | `const wayland = b.dependency("otter_wayland", .{ .target = target, .optimize = optimize, .c_allocator = c_allocator });` |
| | `const conf = b.dependency("otter_conf", .{ .target = target, .optimize = optimize });` |
| | `const theme = b.dependency("otter_theme", .{ .target = target, .optimize = optimize, .c_allocator = c_allocator });` |
| | `const ui = b.dependency("otter_ui", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.enable_dbus = false,` |
| | `.enable_pipewire = false,` |
| | `.enable_pam = false,` |
| | `.c_allocator = c_allocator,` |
| | `});` |
| | `const config_types = b.dependency("otter_config_types", .{ .target = target, .optimize = optimize, .c_allocator = c_allocator });` |
| | `const pipewire = b.dependency("pipewire", .{` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.use_translate_c = true,` |
| | `});` |
| | |
| | `const daemon_imports = [_]std.Build.Module.Import{` |
| | `.{ .name = "otter_utils", .module = utils.module("otter_utils") },` |
| | `.{ .name = "otter_geo", .module = geo.module("otter_geo") },` |
| | `.{ .name = "otter_render", .module = render.module("otter_render") },` |
| | `.{ .name = "otter_wayland", .module = wayland.module("otter_wayland") },` |
| | `.{ .name = "otter_conf", .module = conf.module("otter_conf") },` |
| | `.{ .name = "otter_theme", .module = theme.module("otter_theme") },` |
| | `.{ .name = "otter_ui", .module = ui.module("otter_ui") },` |
| | `.{ .name = "otter_config_types", .module = config_types.module("otter_config_types") },` |
| | `.{ .name = "pipewire", .module = pipewire.module("pipewire") },` |
| | `.{ .name = "build_options", .module = options.createModule() },` |
| | `};` |
| | `const cli_imports = [_]std.Build.Module.Import{` |
| | `.{ .name = "otter_utils", .module = utils.module("otter_utils") },` |
| | `};` |
| | |
| | `const parakeet_static = b.addSystemCommand(&.{ "sh", "scripts/build-parakeet-static.sh" });` |
| | |
| | `const daemon = addExe(b, "otter-transcribe", "src/main.zig", target, optimize, &daemon_imports);` |
| | `linkParakeetStatic(b, daemon, parakeet_static);` |
| | `daemon.root_module.linkSystemLibrary("wayland-client", .{});` |
| | `daemon.root_module.linkSystemLibrary("xkbcommon", .{});` |
| | `const cli = addExe(b, "otter-transcribectl", "src/ctl.zig", target, optimize, &cli_imports);` |
| | |
| | `const run_cmd = b.addRunArtifact(daemon);` |
| | `run_cmd.step.dependOn(b.getInstallStep());` |
| | `if (b.args) |args| run_cmd.addArgs(args);` |
| | `b.step("run", "Run otter-transcribe daemon").dependOn(&run_cmd.step);` |
| | |
| | `const ctl_cmd = b.addRunArtifact(cli);` |
| | `ctl_cmd.step.dependOn(b.getInstallStep());` |
| | `if (b.args) |args| ctl_cmd.addArgs(args);` |
| | `b.step("ctl", "Run otter-transcribectl").dependOn(&ctl_cmd.step);` |
| | |
| | `const test_step = b.step("test", "Run unit tests");` |
| | `addTest(b, test_step, "src/protocol.zig", target, optimize, &cli_imports, null, false);` |
| | `addTest(b, test_step, "src/socket.zig", target, optimize, &cli_imports, null, false);` |
| | `addTest(b, test_step, "src/main.zig", target, optimize, &daemon_imports, parakeet_static, true);` |
| | `addTest(b, test_step, "src/ctl.zig", target, optimize, &cli_imports, null, false);` |
| | `}` |
| | |
| | `fn addExe(` |
| | `b: *std.Build,` |
| | `name: []const u8,` |
| | `path: []const u8,` |
| | `target: std.Build.ResolvedTarget,` |
| | `optimize: std.builtin.OptimizeMode,` |
| | `imports: []const std.Build.Module.Import,` |
| | `) *std.Build.Step.Compile {` |
| | `const exe = b.addExecutable(.{` |
| | `.name = name,` |
| | `.root_module = b.createModule(.{` |
| | `.root_source_file = b.path(path),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = imports,` |
| | `.link_libc = true,` |
| | `}),` |
| | `});` |
| | `b.installArtifact(exe);` |
| | `return exe;` |
| | `}` |
| | |
| | `fn addTest(` |
| | `b: *std.Build,` |
| | `step: *std.Build.Step,` |
| | `path: []const u8,` |
| | `target: std.Build.ResolvedTarget,` |
| | `optimize: std.builtin.OptimizeMode,` |
| | `imports: []const std.Build.Module.Import,` |
| | `parakeet_static: ?*std.Build.Step.Run,` |
| | `link_wayland: bool,` |
| | `) void {` |
| | `const tests = b.addTest(.{` |
| | `.root_module = b.createModule(.{` |
| | `.root_source_file = b.path(path),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = imports,` |
| | `.link_libc = true,` |
| | `}),` |
| | `});` |
| | `if (parakeet_static) |build_step| linkParakeetStatic(b, tests, build_step);` |
| | `if (link_wayland) {` |
| | `tests.root_module.linkSystemLibrary("wayland-client", .{});` |
| | `tests.root_module.linkSystemLibrary("xkbcommon", .{});` |
| | `}` |
| | `step.dependOn(&b.addRunArtifact(tests).step);` |
| | `}` |
| | |
| | `fn linkParakeetStatic(b: *std.Build, artifact: *std.Build.Step.Compile, build_step: *std.Build.Step.Run) void {` |
| | `artifact.step.dependOn(&build_step.step);` |
| | `for (&parakeet_static_archives) |archive| {` |
| | `artifact.root_module.addObjectFile(if (std.fs.path.isAbsolute(archive)) .{ .cwd_relative = archive } else b.path(archive));` |
| | `}` |
| | `addCompilerRuntimeArchive(b, artifact, "gcc", "libgomp.a", "gomp");` |
| | `addCompilerRuntimeArchive(b, artifact, "g++", "libstdc++.a", "stdc++");` |
| | `addCompilerRuntimeArchive(b, artifact, "gcc", "libgcc_eh.a", "gcc_eh");` |
| | `artifact.root_module.linkSystemLibrary("pthread", .{ .preferred_link_mode = .static });` |
| | `artifact.root_module.linkSystemLibrary("dl", .{ .preferred_link_mode = .static });` |
| | `}` |
| | |
| | `fn addCompilerRuntimeArchive(` |
| | `b: *std.Build,` |
| | `artifact: *std.Build.Step.Compile,` |
| | `compiler_name: []const u8,` |
| | `archive_name: []const u8,` |
| | `fallback_library: []const u8,` |
| | `) void {` |
| | `const compiler = b.findProgram(&.{compiler_name}, &.{}) catch {` |
| | `artifact.root_module.linkSystemLibrary(fallback_library, .{ .preferred_link_mode = .static });` |
| | `return;` |
| | `};` |
| | `var code: u8 = 0;` |
| | `const arg = std.fmt.allocPrint(b.allocator, "-print-file-name={s}", .{archive_name}) catch @panic("oom");` |
| | `const stdout = b.runAllowFail(&.{ compiler, arg }, &code, .inherit) catch {` |
| | `artifact.root_module.linkSystemLibrary(fallback_library, .{ .preferred_link_mode = .static });` |
| | `return;` |
| | `};` |
| | `if (code == 0) {` |
| | `const archive = std.mem.trim(u8, stdout, " \t\r\n");` |
| | `if (!std.mem.eql(u8, archive, archive_name) and std.fs.path.isAbsolute(archive)) {` |
| | `artifact.root_module.addObjectFile(.{ .cwd_relative = archive });` |
| | `return;` |
| | `}` |
| | `}` |
| | `artifact.root_module.linkSystemLibrary(fallback_library, .{ .preferred_link_mode = .static });` |
| | `}` |

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-transcribe/blame/commit/25ba37100d17ad7d3157a07b046ea7190f70e7f5/build.zig) [Copy Permalink]()