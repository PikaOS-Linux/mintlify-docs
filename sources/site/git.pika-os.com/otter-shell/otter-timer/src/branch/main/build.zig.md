# Source: https://git.pika-os.com/otter-shell/otter-timer/src/branch/main/build.zig

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-timer](https://git.pika-os.com/otter-shell/otter-timer)

Watch [1](https://git.pika-os.com/otter-shell/otter-timer/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-timer/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-timer/forks)

You've already forked otter-timer

**Files**

**main**

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [074a3fc190](https://git.pika-os.com/otter-shell/otter-timer/commit/074a3fc19088155d34f6c566e5fa409fd343cf62) [Resolve timer OSD from Otter install](https://git.pika-os.com/otter-shell/otter-timer/commit/074a3fc19088155d34f6c566e5fa409fd343cf62)

2026-06-06 20:18:40 +01:00

#### 

32 lines

1.3 KiB

Zig

[Raw](https://git.pika-os.com/otter-shell/otter-timer/raw/branch/main/build.zig) [Permalink](https://git.pika-os.com/otter-shell/otter-timer/src/commit/27f66aae09051798e95e57b90a75bf6cec453da0/build.zig) [Blame](https://git.pika-os.com/otter-shell/otter-timer/blame/branch/main/build.zig) [History](https://git.pika-os.com/otter-shell/otter-timer/commits/branch/main/build.zig)

| | `const std = @import("std");` |
| --- | --- |
| | |
| | `pub fn build(b: *std.Build) void {` |
| | `const target = b.standardTargetOptions(.{});` |
| | `const optimize = b.standardOptimizeOption(.{});` |
| | `const core = b.dependency("otter_tools_core", .{ .target = target, .optimize = optimize });` |
| | `const utils = b.dependency("otter_utils", .{ .target = target, .optimize = optimize });` |
| | `const imports = [_]std.Build.Module.Import{` |
| | `.{ .name = "otter_tools_core", .module = core.module("otter_tools_core") },` |
| | `.{ .name = "otter_utils", .module = utils.module("otter_utils") },` |
| | `};` |
| | `const root_module = b.createModule(.{` |
| | `.root_source_file = b.path("src/main.zig"),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = &imports,` |
| | `});` |
| | `const exe = b.addExecutable(.{ .name = "otter-timer", .root_module = root_module });` |
| | `b.installArtifact(exe);` |
| | `const run_cmd = b.addRunArtifact(exe);` |
| | `run_cmd.step.dependOn(b.getInstallStep());` |
| | `if (b.args) |args| run_cmd.addArgs(args);` |
| | `b.step("run", "Run otter-timer").dependOn(&run_cmd.step);` |
| | `const tests = b.addTest(.{ .root_module = b.createModule(.{` |
| | `.root_source_file = b.path("src/main.zig"),` |
| | `.target = target,` |
| | `.optimize = optimize,` |
| | `.imports = &imports,` |
| | `}) });` |
| | `b.step("test", "Run unit tests").dependOn(&b.addRunArtifact(tests).step);` |
| | `}` |

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-timer/blame/commit/27f66aae09051798e95e57b90a75bf6cec453da0/build.zig) [Copy Permalink]()