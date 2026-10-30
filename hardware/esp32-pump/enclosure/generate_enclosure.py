"""Generate the DDROID ESP32 controller enclosure (box + lid) as STL.

Parametric, printable project box sized for an ESP32 DevKit v1 (30-pin),
matching the hardware/esp32-pump build:
  - USB slot on one short wall
  - cable/sensor slot on the opposite short wall
  - lid with 3 button holes (LOW / FULL / STOP) and 2 LED holes (PUMP / IDLE)

Units are millimetres. Requires: trimesh, manifold3d, numpy.
Run:  python generate_enclosure.py
"""

import os
import trimesh

ENGINE = "manifold"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Parameters (mm) -------------------------------------------------------
WALL = 2.5          # side wall thickness
FLOOR = 2.5         # base thickness
INNER_L = 70.0      # cavity length  (X)
INNER_W = 50.0      # cavity width   (Y)
INNER_H = 28.0      # cavity height  (Z)

OUTER_L = INNER_L + 2 * WALL     # 75
OUTER_W = INNER_W + 2 * WALL     # 55
BOX_H = FLOOR + INNER_H          # 30.5 (open-top tray)

STANDOFF = 4.0      # board rests this high off the floor
POST = 6.0          # square standoff footprint
BOARD_L = 55.0      # ESP32 DevKit board footprint
BOARD_W = 28.0

USB_W, USB_H, USB_Z = 13.0, 9.0, 10.0     # USB slot (Y width, Z height, Z centre)
WIRE_W, WIRE_H, WIRE_Z = 16.0, 7.0, 24.0  # sensor/pump cable slot

LID_T = 2.5         # lid top-plate thickness
LIP_H = 5.0         # lip that drops into the cavity
LIP_CLR = 0.25      # clearance per side so the lid seats easily

BTN_D = 6.5         # 6 mm panel button hole
LED_D = 5.2         # 5 mm LED hole


def box(size, center):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(center)
    return m


def cyl(d, h, center):
    m = trimesh.creation.cylinder(radius=d / 2.0, height=h, sections=64)
    m.apply_translation(center)
    return m


def diff(a, b):
    return trimesh.boolean.difference([a, b], engine=ENGINE)


def union(parts):
    return trimesh.boolean.union(parts, engine=ENGINE)


def build_box():
    outer = box((OUTER_L, OUTER_W, BOX_H), (0, 0, BOX_H / 2))
    cavity = box((INNER_L, INNER_W, INNER_H + WALL),
                 (0, 0, FLOOR + (INNER_H + WALL) / 2))
    tray = diff(outer, cavity)

    posts = []
    px = BOARD_L / 2 - POST / 2
    py = BOARD_W / 2 - POST / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            posts.append(box((POST, POST, STANDOFF),
                             (sx * px, sy * py, FLOOR + STANDOFF / 2)))
    body = union([tray] + posts)

    usb = box((WALL * 3, USB_W, USB_H), (OUTER_L / 2, 0, USB_Z))
    wire = box((WALL * 3, WIRE_W, WIRE_H), (-OUTER_L / 2, 0, WIRE_Z))
    body = diff(body, union([usb, wire]))
    return body


def build_lid():
    plate = box((OUTER_L, OUTER_W, LID_T), (0, 0, LID_T / 2))

    lip_out = box((INNER_L - 2 * LIP_CLR, INNER_W - 2 * LIP_CLR, LIP_H),
                  (0, 0, LID_T + LIP_H / 2))
    lip_in = box((INNER_L - 2 * LIP_CLR - 2 * WALL,
                  INNER_W - 2 * LIP_CLR - 2 * WALL, LIP_H + 2),
                 (0, 0, LID_T + LIP_H / 2))
    lip = diff(lip_out, lip_in)
    lid = union([plate, lip])

    holes = []
    # buttons: LOW / FULL / STOP in a row
    for x in (-20.0, 0.0, 20.0):
        holes.append(cyl(BTN_D, LID_T + 4, (x, 14.0, LID_T / 2)))
    # LEDs: PUMP / IDLE
    for x in (-10.0, 10.0):
        holes.append(cyl(LED_D, LID_T + 4, (x, -14.0, LID_T / 2)))
    lid = diff(lid, union(holes))
    return lid


def report(name, mesh):
    ext = mesh.bounding_box.extents
    print(f"  {name}: {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"watertight={mesh.is_watertight}, volume={mesh.volume/1000:.1f} cm^3")


def main():
    box_mesh = build_box()
    lid_mesh = build_lid()
    box_path = os.path.join(OUT_DIR, "ddroid_controller_box.stl")
    lid_path = os.path.join(OUT_DIR, "ddroid_controller_lid.stl")
    box_mesh.export(box_path)
    lid_mesh.export(lid_path)
    print("Wrote:")
    report("box", box_mesh)
    report("lid", lid_mesh)
    print(box_path)
    print(lid_path)


if __name__ == "__main__":
    main()
