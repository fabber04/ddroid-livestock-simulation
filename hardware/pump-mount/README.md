# Pump / pipe mount

3D-printable base bracket that holds the pump body in two saddle cradles and
clips the outlet pipe, for the DDROID water point.

![Pump mount preview](preview.png)

## Files

| File | What it is |
| --- | --- |
| `pump_mount.stl` | The mount (120 x 52 x 31 mm) |
| `generate_pump_mount.py` | Parametric generator (edit + re-run) |
| `preview.png` | Rendered preview |

## Design

- Base plate 120 x 52 x 5 mm with four M4 corner mounting holes.
- Two saddle cradles (70 mm apart) that cradle the pump body horizontally; the
  cradle rises just past the pump centre so the pump snaps in and is retained.
- Zip-tie slots in the base either side of each cradle - loop a tie up through
  one slot, over the pump, and down the other to clamp it.
- A snap-in C-clip at one end holds the outlet pipe.

## Sizing to your parts

The Gazebo scene draws the pump as a 110 mm cylinder and the pipe as a 30 mm
box - those are scene stand-ins. The defaults here suit a small 12 V bench
pump. Edit the parameters at the top of `generate_pump_mount.py`:

- `PUMP_D` - your pump body diameter.
- `PIPE_D` - your outlet pipe outer diameter.
- `CRADLE_SPACING` - move the cradles to clear the pump's inlet/outlet ports.
- `BASE_L` / `BASE_W` - base footprint.

```bash
pip install trimesh manifold3d numpy
python generate_pump_mount.py
```

## Printing

- Material: PETG (near water) or PLA for a dry bench.
- Layer height 0.2 mm, 3 perimeters, ~25% infill.
- Print base-down; the saddle valleys and pipe clip are self-supporting
  (open side up). No supports needed.
- Screw the base to the tank stand / bench, drop the pump into the saddles and
  zip-tie it down, clip the pipe in, then run the pump wire to the relay/MOSFET
  on the ESP32 pump output (GPIO 26) per `../esp32-pump/README.md`.
