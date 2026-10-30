# ESP32 controller enclosure

3D-printable project box and lid for the DDROID water-point controller
(`../ddroid_pump_logic.ino`). Sized for an ESP32 DevKit v1 (30-pin).

![Box and lid preview](preview.png)

## Files

| File | What it is |
| --- | --- |
| `ddroid_controller_box.stl` | Open-top enclosure (75 x 55 x 30.5 mm) |
| `ddroid_controller_lid.stl` | Lid with button/LED holes (75 x 55 x 7.5 mm) |
| `generate_enclosure.py` | Parametric generator (edit + re-run to resize) |
| `preview.png` | Rendered preview of both parts |

## Features

- Internal cavity 70 x 50 x 28 mm, 2.5 mm walls and floor.
- Four 4 mm standoffs that raise the ESP32 board off the floor.
- USB slot on one short wall (for the programming/power cable).
- Cable slot on the opposite short wall (float-switch and pump-relay wires).
- Lid with a drop-in lip (0.25 mm clearance, friction fit) and:
  - 3 button holes (6.5 mm) for the LOW / FULL / STOP panel buttons,
  - 2 LED holes (5.2 mm) for the PUMP (red) and IDLE (green) LEDs.

Button/LED positions on the lid: buttons in a row on one side, LEDs on the
other. Panel-mount 6 mm momentary buttons and 5 mm LEDs wire to the GPIOs in
the pin map in `../README.md`.

## Printing

- Material: PLA or PETG.
- Layer height: 0.2 mm, 2-3 perimeters, ~20% infill.
- No supports needed: print the box open-side up and the lid flat (lip up).
- The USB and cable slots bridge a short gap at the wall top - printable as-is.

## Regenerate / resize

Edit the parameters at the top of `generate_enclosure.py` (wall thickness,
cavity size, hole diameters and positions) and re-run:

```bash
pip install trimesh manifold3d numpy
python generate_enclosure.py
```

Both STLs are watertight (manifold) and ready to slice.

## Assembly

1. Drop the ESP32 onto the four standoffs, USB port facing the USB slot.
2. Route the float-switch and pump-relay wires through the cable slot.
3. Fit the panel buttons and LEDs into the lid holes and wire them to the GPIOs.
4. Press the lid on - the lip is a friction fit (add M3 screw bosses in the
   generator if you want a fastened lid).
