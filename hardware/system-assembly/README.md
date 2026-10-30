# System assembly model

A 3D model of the whole DDROID water point, assembled: the supply tank, the
pump in its mount, the pipe, the trough with the float-switch bracket, and the
controller enclosure wired in. Built from the real tank/trough sizes and switch
heights in `../../simulation/ddroid_scene.py`.

![Assembled DDROID water point](preview.png)

## Files

| File | What it is |
| --- | --- |
| `system_assembly.stl` | Single mesh - drag to rotate it in GitHub's 3D viewer |
| `system_assembly.glb` | Coloured model for any glTF viewer |
| `generate_assembly.py` | Rebuilds the model + preview |
| `preview.png` | Shaded render |

Open `system_assembly.stl` on GitHub to spin the whole rig around in the
browser, or drop `system_assembly.glb` into a glTF viewer for the colours.

## What's in it

- **Supply tank** (300 x 300 x 340 mm) and **trough** (660 x 320 x 160 mm),
  both with a water fill.
- **Pump** sitting in the printed `pump-mount`, with the pipe running
  supply -> pump -> trough.
- **Float-switch bracket** on the trough front wall holding three switches at
  48 / 120 / 147 mm (LOW / FULL / cutoff); a supply-low switch on the tank.
- **Controller enclosure** on the bench, with wires back to the switches and
  pump (the ESP32 reads the switches and drives the pump - see
  `../esp32-pump/README.md`).

## Rebuild

```bash
pip install trimesh manifold3d numpy matplotlib
python generate_assembly.py
```

It loads the printed-part STLs from the sibling folders and places them, so if
you resize a part, re-run this to refresh the assembled model.
