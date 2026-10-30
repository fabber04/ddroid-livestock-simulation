# System assembly model

A 3D model of the whole DDROID water point, mirroring the Gazebo scene. The
geometry is ported straight from `../../simulation/build_world.py` and
`ddroid_scene.py`, so it matches the simulation layout, dimensions and colours.

![Assembled DDROID water point](preview.png)

## Files

| File | What it is |
| --- | --- |
| `system_assembly.stl` | Single mesh (mm) - drag to rotate it in GitHub's 3D viewer |
| `system_assembly.glb` | Coloured model for any glTF viewer |
| `generate_assembly.py` | Rebuilds the model + preview from the scene constants |
| `preview.png` | Shaded render with a sky background |

Open `system_assembly.stl` on GitHub to spin the rig around in the browser, or
drop `system_assembly.glb` into a glTF viewer for the colours.

## What's in it (same as the Gazebo world)

- **Wood bench** on four legs, with the **supply stand**.
- **Supply tank** (300 x 300 x 340 mm) and **trough** (660 x 320 x 160 mm),
  open-top with a lower front wall and a blue water fill.
- **Pump** (vertical cylinder) and the **supply -> trough pipe**.
- **Status lamps**: the pump lamp (orange = running) and the mode lamp
  (blue = refilling).
- **Float-switch markers**: supply-low and trough-low (blue, wet), trough-high
  (grey, dry) and the independent high **cutoff** (red), at the
  30 / 75 / 92% heights.
- **Two livestock** at the trough.

The matching printable mounts (enclosure, float-switch bracket, pump mount) are
in the sibling `../` folders.

## Rebuild

```bash
pip install trimesh numpy matplotlib
python generate_assembly.py
```

Edit the scene constants at the top of `generate_assembly.py` (they mirror
`ddroid_scene.py`) and re-run to refresh the model and render.
