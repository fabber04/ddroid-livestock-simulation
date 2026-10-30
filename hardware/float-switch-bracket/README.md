# Float-switch bracket

3D-printable bracket that hooks over the trough rim and holds three float
switches at the DDROID water-level thresholds.

![Bracket preview](preview.png)

## Heights (from the trough floor)

Taken from `simulation/ddroid_scene.py` (trough water depth `h` = 160 mm):

| Switch | Threshold | Height |
| --- | --- | --- |
| LOW | 30% | 48 mm |
| FULL | 75% | 120 mm |
| Cutoff (independent high) | 92% | 147 mm |

Each switch sits on a horizontal shelf with a vertical mounting hole.

## Files

| File | What it is |
| --- | --- |
| `float_switch_bracket.stl` | The bracket (45 x 24 x 125 mm) |
| `generate_bracket.py` | Parametric generator (edit + re-run) |
| `preview.png` | Rendered preview |

## Design

- A U-hook at the top clamps over the trough rim (`WALL_GAP` = 10 mm wall by
  default; the outer leg grips 18 mm down the outside).
- A vertical rail runs down the inside face of the wall.
- Three shelves reach 25 mm into the water at the LOW / FULL / cutoff heights,
  each with a 10.5 mm (M10) vertical mounting hole 8 mm from the tip.

## Fit it to your trough

Edit the parameters at the top of `generate_bracket.py` and re-run:

- `RIM_HEIGHT` - measured height of your trough rim above the floor.
- `WALL_GAP` - your trough wall thickness (so the hook clamps snugly).
- `HOLE_D` - your float switch's thread/stem (M10 = 10.5, M8 = 8.5, ...).
- `TROUGH_H` - water depth if different from 160 mm; shelf heights recompute
  from the 30% / 75% / 92% thresholds automatically.

```bash
pip install trimesh manifold3d numpy
python generate_bracket.py
```

## Printing

- Material: PETG recommended (it will be near water); PLA is fine for a dry
  bench demo.
- Layer height 0.2 mm, 3 perimeters, ~25% infill.
- Print with the flat back (wall side) on the bed; add supports under the three
  shelf overhangs and the hook bridge.
- Secure each float switch with its nut through the shelf hole, wire to the
  ESP32 inputs (LOW -> GPIO 32, FULL -> GPIO 33) per `../esp32-pump/README.md`.
  The cutoff switch is the independent high-level safety cut described in the SRS.
