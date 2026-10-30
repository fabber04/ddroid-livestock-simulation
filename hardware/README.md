# DDROID hardware

Physical build of the DDROID smart livestock water point: the ESP32 controller
that runs the pump logic, and the 3D-printed parts that mount it on the trough.
The control logic here is the same state machine as the Node-RED flow
(`../flows.json`) and the XOD patch (`../xod/`):

> Pump starts OFF. Water **LOW** -> pump **ON** (fill). Water **FULL** or
> **STOP** -> pump **OFF**.

## Contents

| Folder | Part | STL size |
| --- | --- | --- |
| [`esp32-pump/`](esp32-pump/) | ESP32 firmware (`.ino`) + wiring guide | - |
| [`esp32-pump/enclosure/`](esp32-pump/enclosure/) | Controller box + lid | 75 x 55 x 30.5 mm |
| [`float-switch-bracket/`](float-switch-bracket/) | Trough float-switch bracket | 45 x 24 x 125 mm |
| [`pump-mount/`](pump-mount/) | Pump / outlet-pipe mount | 120 x 52 x 31 mm |

Each printed part ships with its STL, a parametric generator
(`generate_*.py`, trimesh + manifold3d), a README and a preview image.

## How the parts fit together

```
          supply tank                         trough (66 x 32 x 16 cm)
         +-----------+                      +----------------------+
         |           |     outlet pipe      |  [float-switch       |
         |   pump >==|======================|   bracket]           |
         |  [pump-   |   (held by pump-     |   - cutoff  147 mm    |
         |   mount]  |    mount clip)       |   - FULL    120 mm    |
         +-----------+                      |   - LOW      48 mm    |
                                            +----------------------+

                 [ESP32 controller enclosure]
                  LOW/FULL float switches --> GPIO 32 / 33
                  STOP button              --> GPIO 25
                  pump relay/MOSFET        <-- GPIO 26
                  PUMP (red) / IDLE (green) LEDs
```

1. **Pump** sits in the `pump-mount` saddles (zip-tied down), its outlet pipe
   snapped into the clip and run to the trough.
2. **Float switches** clip onto the trough wall in the `float-switch-bracket` at
   the LOW (48 mm) / FULL (120 mm) / cutoff (147 mm) heights - the 30 / 75 / 92%
   thresholds from `../simulation/ddroid_scene.py`.
3. **ESP32** lives in the `enclosure`; the float switches and pump relay wire to
   its GPIOs (see `esp32-pump/README.md`), and the LOW/FULL/STOP buttons + PUMP/
   IDLE LEDs sit on the lid.

## Build order

1. Flash the ESP32 with `esp32-pump/ddroid_pump_logic.ino` and bench-test it
   with the three buttons and two LEDs.
2. Print the three parts (PLA for a dry bench demo, PETG for anything near
   water). Tune each generator's parameters to your real pump, pipe, trough wall
   and switches first, then re-run.
3. Mount the pump and float switches, swap the demo buttons for the float
   switches and the PUMP LED for a pump relay/MOSFET, and wire everything to the
   enclosure.

## Printing summary

All STLs are watertight. Suggested slice: 0.2 mm layers, 3 perimeters, ~20-25%
infill. The enclosure and bracket need light supports under their overhangs; the
pump mount prints support-free base-down.
