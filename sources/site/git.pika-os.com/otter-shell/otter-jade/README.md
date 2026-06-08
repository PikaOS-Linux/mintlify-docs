# otter-jade

Animated Wayland layer-shell pet for Otter Shell.

`otter-jade` creates a small transparent overlay surface containing an otter tamagotchi. Jade grows from egg to pup, teen, and adult stages, moves mostly near the top or bottom desktop edges, persists care state, and reacts to pointer input.

## Features

- Four growth stages: egg, pup, teen, adult
- Sprite-sheet animation for idle, walk, sleep, happy, hungry, dirty, eating, cleaning, petting, quirky, wink, and yawn actions
- PNG overlay animations for feeding fish, sleep Zs, cleaning suds, and mood emotes
- Cracked egg progress frames before hatching, plus visual need cues without meters
- Stage-specific speech for egg, pup, teen, and adult
- Random color and rare shiny rolls when egg hatches
- Left click pets Jade
- Right click opens a menu for feed, clean, nap, and quit
- Input region is limited to the pet and menu
- State stored at `$XDG_STATE_HOME/otter-shell/otter-jade.state`, falling back to `$HOME/.local/state/otter-shell/otter-jade.state`

## Build

```bash
cd otter-jade
zig build
zig build test
```

## Run

```bash
cd otter-jade
zig build run
```

Reset persisted pet state on launch:

```bash
zig build run -- --reset
```

Run a non-persistent showcase:

```bash
zig build run -- --demo
```

## Configuration

Config file: `~/.config/otter-shell/otter-jade.conf` with system fallback at `/etc/otter-shell/otter-jade.conf`.

Defaults:

```conf
size = 96
fps = 60
movement_speed = 90
idle_pose_interval_ms = 2700
edge_bias_percent = 55
margin = 24
shiny_odds = 4096
growth_minutes_per_stage = 180
show_speech = true
```

Color is not configurable. It is rolled once when the egg hatches and then persisted with the shiny roll.

## Sprites

Sprite sheets are embedded from `assets/sprites/`. Base pet sheets are `otter-jade-egg.png` and `otter-jade-otter.png`; overlay sheets are `otter-jade-overlay-fish.png`, `otter-jade-overlay-sleep.png`, `otter-jade-overlay-suds.png`, and `otter-jade-emotes.png`.

Sheets use 128x128 frames. Otter sheets use four frames per action and twelve actions per stage. Egg frames show increasing cracks as hatch time approaches and reuse existing egg motion for otter-only actions. Egg sprites stay uncolored; otter sprites are palette-recolored from the persisted hatch color or shiny state.

## Architecture

| File | Purpose |
|------|---------|
| `src/main.zig` | Wayland connection, layer-shell surface, pointer callbacks, frame timer |
| `src/config.zig` | Config loading, normalization, and defaults |
| `src/state.zig` | Persistent care/growth state load and save |
| `src/sim.zig` | Care math, movement, and action selection |
| `src/pet_types.zig` | Shared pet action and emote enums |
| `src/action_meta.zig` | Data table for action timing, overlays, and egg sprite fallback |
| `src/speech.zig` | Stage/action speech table |
| `src/demo.zig` | Non-persistent showcase sequence |
| `src/sprites.zig` | Embedded sheet loading, frame lookup, palette recolor |
| `src/draw.zig` | `otter-ui` frame drawing for sprite, speech, and menu |
| `src/input.zig` | Hit tests, menu sizing, input-region geometry |

## License

MIT License — see [LICENSE](LICENSE).
