# otter-geo

Pure geometry types for the Otter desktop shell. No rendering dependencies.

## Types

- **Point** - 2D coordinate with `u16` x/y values
- **Rect** - Rectangle with position and dimensions
- **Circle** - Circle defined by diameter and center point
- **Padding** - Four-sided padding (north, south, east, west)
- **Transform** - 2D rotation matrix using i32 fixed-point arithmetic (16.16)
- **Align** - Alignment enum (start, center, end)

## Usage

```zig
const geo = @import("otter_geo");

// Points
const p1 = geo.Point{ .x = 10, .y = 20 };
const p2 = geo.Point{ .x = 5, .y = 10 };
const sum = p1.add(p2);
const rect_from_points = p1.spanningRect(p2);

// Rectangles
const rect = geo.Rect{ .x = 0, .y = 0, .width = 100, .height = 100 };
const inner = geo.Point{ .x = 20, .y = 20 };
const centered = rect.center(inner);

if (rect.containsPoint(p1)) {
    // point is inside rectangle
}

if (rect.intersection(other_rect)) |inter| {
    // rectangles overlap
}

// Padding
const padding = geo.Padding.uniform(10);
if (rect.removePadding(padding)) |shrunk| {
    // shrunk rect with padding removed
}

// Circles
const circle = geo.Circle.largestCircle(rect);
if (circle.containsPoint(p1)) {
    // point is inside circle
}

// Transforms
const rotated = geo.Transform.rotate_cw; // 90 degree rotation
const combined = geo.Transform.identity.compose(rotated);
```

## Running Tests

```bash
zig build test
```

## Dependencies

None. This is a pure Zig library with no external dependencies.

## License

MIT License — see [LICENSE](LICENSE).
