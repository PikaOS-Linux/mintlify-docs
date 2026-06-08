# otter-render

Rendering primitives for the Otter desktop shell. Provides color management, surface abstraction, font rendering with FreeType, text backend wiring for shaping/bidi/font lookup, and image loading via zigimg.

## Features

- ARGB color operations compatible with Wayland's argb8888 format
- Surface abstraction for rectangular pixel buffers with HiDPI scaling support
- FreeType font rendering with glyph caching and fallback font support
- Text backend boundary for HarfBuzz shaping, itijah bidi checks, and Fontconfig system font lookup
- Image loading (PNG, JPG, BMP, GIF, etc. via zigimg)
- Sprite-sheet helpers plus source-rect sprite draw commands
- Fallback fonts from Fontconfig and `/usr/share/fonts/otter-shell/` are queued at startup and mmap-loaded lazily on first primary-font glyph miss
- Per-surface scale factor for sharp rendering on HiDPI displays
- Generic integer-only animation controller (ease-out quadratic, no floats)
- Command-based deferred rendering via CommandList + quad_renderer with scissor clipping and damage-rect culling

## Dependencies

### System Libraries

- **Fontconfig** - System font discovery (`fontconfig` pkg-config)

### Zig Dependencies (fetched via build.zig.zon)

- **allyourcodebase/freetype** - FreeType font rasterization
- **allyourcodebase/harfbuzz** - Text shaping
- **zigimg** - Pure Zig image loading (PNG, JPG, BMP, GIF, etc.)
- **otter_geo** - Geometry types (Point, Rect, Size, Padding)

### Vendored Dependencies

- **itijah** - Zig-native Unicode Bidirectional Algorithm, vendored from latest main with a Zig 0.16 build wrapper

## Usage

```zig
const render = @import("otter_render");

// Colors
const color = try render.parseColor("#FF5500");
const white = render.Color.white;
const semi_transparent = white.withAlpha(128);

// Surface operations
var pixels: [100]render.Color = undefined;
var surface = render.Surface.fromPixels(&pixels, 10, 10);
surface.clear(render.Color.black);
surface.fillRect(.{ .x = 2, .y = 2, .width = 3, .height = 3 }, render.Color.red);

// Font rendering (requires FreeType)
const font = try render.Font.init(allocator, .{});
defer font.deinit();
font.drawText(&surface, "Hello", .{ .x = 0, .y = 20 }, 16, render.Color.white);
const width = font.measureText("Hello", 16);

// Image loading (zigimg for PNG/JPG/BMP/GIF)
var image = try render.Image.loadFromFile(allocator, "icon.png");
defer image.deinit();
image.draw(&surface, .{ .x = 0, .y = 0, .width = 32, .height = 32 });

// Sprite sheets choose frames in app code, then record one draw command.
const sheet = render.SpriteSheet.init(image.width, image.height, 32, 32, 16);
const frame = sheet.frameRect(3).?;
cmds.sprite(.{ .x = 10, .y = 10, .width = 64, .height = 64 }, &image, frame, .{ .flip_x = true });

// Animation (integer-only ease-out quadratic)
var anim = render.Animation.init(750, 144); // 750ms at 144hz
while (anim.tick(true)) { // tick toward expanded (256)
    const width = anim.lerp(collapsed_width, expanded_width);
    // ... use interpolated width
}

// Low-level compatibility path: command-based deferred rendering
// New app UI should normally describe a Surface Description frame in otter-ui,
// then rasterize the UiState-owned command list.
var cmds: render.DefaultCommandList = .{};
cmds.scale = surface.scale;
cmds.font = &font;
cmds.clear(render.Color.black);
cmds.solidRect(.{ .x = 10, .y = 10, .width = 100, .height = 30 }, bg_color);
cmds.text(.{ .x = 15, .y = 35 }, "Hello", 16, render.Color.white);
cmds.scissorPush(.{ .x = 0, .y = 0, .width = 200, .height = 100 });
// ... clipped content ...
cmds.scissorPop();

// Rasterize all commands onto a Surface with damage culling
render.quad_renderer.rasterize(
    render.DefaultCommandList, &cmds, &surface, null,
    damage_rects, full_damage,
);
```

## Building

```bash
zig build
```

Build options:

- `-Denable_text=false` omits FreeType, HarfBuzz, itijah, and Fontconfig from render consumers that only need color/surface/image APIs.
- `-Denable_svg=false` omits NanoSVG rasterization and returns `error.SvgDisabled` for SVG image paths.
- `-Denable_wide_image_formats=false` limits zigimg decode registration to PNG/JPEG for image-only daemons.

Example lean image-only build:

```bash
zig build -Denable_text=false -Denable_svg=false -Denable_wide_image_formats=false
```

## Running Tests

```bash
zig build test
```

## API Overview

### color.zig

- `Color` - ARGB color type with compositing, blending, and luminance checks
  - `parseHex` - Parse hex strings (`#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`) or named colors (LUT-based, branchless)
- `parseColor` - Module-level parse function (same as `Color.parseHex`)
- `PixelFormat` - Pixel format identifiers (argb8888, rgba8888, bgra8888)

### surface.zig

- `Surface` - Rectangular pixel buffer with drawing primitives
  - `clear`, `fillRect`, `fillRectComposite`
  - `drawRectOutline`, `fillCircle`, `drawCircleOutline`
  - `setPixel`, `getPixel`, `compositePixel`
  - `subSurface` - Create a view into a portion of the surface
  - HiDPI support:
    - `fromPixelsScaled` - Create surface with scale factor
    - `toPhysicalRect`, `toPhysicalPoint` - Convert logical to physical coordinates
    - `fillRectLogical`, `fillCircleLogical`, etc. - Draw using logical coordinates

### font.zig

- `Font` - FreeType font with glyph caching
  - `init` / `deinit` - Create/destroy font with optional custom font path or font family name
  - Font loading priority: explicit `font_path` > `font_family` discovery (scans system font directories) > system fallback font (`/usr/share/fonts/otter-shell/IoskeleyMonoNerdFont-Regular.ttf`)
  - Fallback loading is lazy: Fontconfig/system fallback candidates are stored in fixed buffers and only opened/mmaped when `loadChar` cannot resolve a codepoint in the primary face
  - `drawText` - Render text to a surface (skips .notdef glyphs to avoid rendering boxes)
  - `measureText` - Calculate text width in pixels
  - `loadChar` - Load a glyph (cached); proactive culling at 8192 entries plus reactive O(n) eviction on allocation failure via time-based cutoff with O(1) swap-removes
  - HiDPI support:
    - `drawTextScaled` - Draw text using logical coordinates and font size
    - `measureTextScaled` - Measure text at physical resolution, return logical width (requires Surface)
    - `measureTextAtScale` - Measure text at physical resolution with explicit scale factor (no Surface required, used with CommandList)

### text.zig

- Text backend boundary for the future shared `TextSystem`
  - `TextSystem.init` / `deinit` - Own reusable HarfBuzz font and buffer state around an existing `Font`
  - `TextSystem.measure` - Measure with the FreeType fast path for simple ASCII and shaped advances for complex text
  - `TextSystem.shapeInto` - Shape UTF-8 into caller-owned scratch, returning glyph advances and bidi layout slices
  - `TextSystem.draw` - Draw simple text through the current FreeType path or shaped glyph IDs through cached FreeType glyph rasterization
  - `TextSystem.wrap` / `truncate` / `cursorRect` - Layout-facing helpers over measured UTF-8 byte ranges
  - Shaped `.notdef` glyphs route back through `Font.loadChar` so existing fallback fonts can cover missing codepoints
  - `ShapeScratch` - Reusable caller-owned scratch for shaped glyphs, decoded codepoints, and itijah bidi state
  - `backendVersions` - Runtime version probe for HarfBuzz and Fontconfig linkage
  - `hasStrongRtlUtf8` / `hasStrongRtlCodepoints` - Cheap bidi preflight helpers
  - `isCjkCodepoint` - CJK range preflight for future fallback routing
  - `Direction` - Shared mapping to HarfBuzz direction and itijah paragraph direction
- `CommandList.text` uses attached `TextSystem`/`ShapeScratch` during quad rasterization when provided; otherwise it keeps the direct FreeType path.

### image.zig

- `Image` - Loaded image data
  - `loadFromFile` - Load PNG, JPG, BMP, GIF from file
  - `loadFromMemory` - Load image from memory
  - `loadFromFileAtSize` - Load any image (SVG or raster) at a target pixel size; SVGs rasterize at target, rasters downsample to fit
  - `loadFromFileDownsampled(allocator, path, w, h, blur, cover)` - Load and downsample large images; `cover=true` uses `max(scale_x, scale_y)` so the result covers the target area, `cover=false` uses `min` to fit within
  - `loadFromMemoryDownsampled(allocator, data, w, h, blur, cover)` - Same from memory buffer
  - `draw` - Draw scaled to fit within area (bilinear interpolation when upscaling, box filter when downscaling)
  - `drawUnscaled` - Draw at original size
  - `drawScaled` - Draw using logical coordinates with HiDPI support
  - `drawRegionScaledClipped` - Draw a source rectangle into a logical destination, with clipping and optional horizontal flip
  - `drawCover` - Draw scaled to cover area (crop overflow, bilinear when upscaling)
  - `drawScaledFill` - Draw stretched to fill exact target area (box-filter downscale)

### sprite.zig

- `SpriteSheet` - Fixed-grid sprite sheet metadata and frame rectangle lookup
- `SpriteAnim` - Frame lookup helper from elapsed time; no scheduler or runtime state
- `SpriteOptions` - Per-command sprite options, currently `flip_x`

### command_list.zig

Low-level renderer boundary and compatibility API. New application UI should prefer `otter-ui` Surface Description components and let `UiState` own the command list; direct command recording remains for renderer internals, compatibility widgets, and specialized primitives.

- `CommandList(max_commands, string_capacity)` - Comptime-generic command buffer for deferred rendering
  - `solidRect`, `blendRect`, `rectOutline`, `circle` - Shape commands
  - `text` - Text command with string interning (zero-copy deduplication)
  - `image`, `imageFill`, `sprite` - Image rendering commands via opaque `ImageHandle`
  - `clear` - Full surface clear
  - `scissorPush` / `scissorPop` - Nested scissor clipping
  - `scale: u31` - HiDPI scale factor for logical-to-physical coordinate conversion
  - `font: ?*Font` - Font instance used by quad_renderer for text rasterization
  - `reset()` - Reuse buffer across frames without reallocation
- `DefaultCommandList` - Pre-configured `CommandList(2048, 32 * 1024)` used by all apps
- `ImageHandle` - Type-erased pointer to Image for command storage

### quad_renderer.zig

- `rasterize(CmdList, list, surface, font_instance, damage_rects, full_damage)` - Plays back CommandList commands onto a Surface
  - Scissor stack (max depth 8) clips all shape/image commands
  - Damage-rect culling: skips commands outside damaged regions when `full_damage` is false
  - Font resolution: uses `font_instance` parameter, falls back to `list.font`

### animation.zig

- `Animation` - Generic integer-only ease-out quadratic animation controller
  - `init(duration_ms, refresh_hz)` - Compute total frames from duration and display refresh rate
  - `tick(target_forward)` - Advance one frame toward target (true = 256, false = 0); handles mid-animation direction reversal
  - `lerp(from, to)` - Interpolate between two `u31` values using current progress
  - No floats, no allocations; progress range is 0–256

### freetype.zig

- Low-level FreeType C bindings
- Error handling utilities (`isErr`, `errorAssert`, `errorPrint`)
- Custom allocator support for tracking FreeType memory

## Third-party licenses

Otter Shell code is MIT — see [LICENSE](LICENSE). Bundled dependencies retain their own licenses:

- **zigimg** — MIT — `vendor/zigimg/LICENSE`
- **itijah** — MIT — `vendor/itijah/LICENSE`
- **NanoSVG** — zlib — `vendor/nanosvg/LICENSE.txt`
- **FreeType** — FTL/GPL — Zig package (`allyourcodebase/freetype`)
- **HarfBuzz** — Old MIT — Zig package (`allyourcodebase/harfbuzz`)

## License

MIT License — see [LICENSE](LICENSE).
