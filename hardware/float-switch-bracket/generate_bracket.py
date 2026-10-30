"""Generate the DDROID float-switch mounting bracket as STL.

A clip-on bracket that hooks over the trough rim and holds three float
switches at the water-level thresholds from simulation/ddroid_scene.py:
  LOW 30% = 48 mm, FULL 75% = 120 mm, cutoff 92% = 147.2 mm
(all measured from the trough floor; trough water depth h = 160 mm).

Each switch sits on a horizontal shelf with a vertical mounting hole
(default M10 / 10.5 mm - change HOLE_D for your switch).

Units are millimetres. Requires: trimesh, manifold3d, numpy.
Run:  python generate_bracket.py
"""

import os
import trimesh

ENGINE = "manifold"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Trough reference (from simulation/ddroid_scene.py) --------------------
TROUGH_H = 160.0          # water depth, mm (h = 0.16 m)
RIM_HEIGHT = 160.0        # height of the trough rim above the floor, mm
LOW_H = 0.30 * TROUGH_H   # 48.0
FULL_H = 0.75 * TROUGH_H  # 120.0
CUTOFF_H = 0.92 * TROUGH_H  # 147.2
SWITCH_HEIGHTS = [LOW_H, FULL_H, CUTOFF_H]

# --- Bracket parameters (mm) ----------------------------------------------
WALL_GAP = 10.0     # trough wall thickness the hook clamps over
LEG_T = 5.0         # outer hook leg thickness (X)
HOOK_DROP = 18.0    # how far the outer leg grips down the outside wall
BRIDGE_T = 5.0      # top bridge thickness (Z)

RAIL_T = 5.0        # rail thickness into the water (X)
RAIL_W = 24.0       # rail / shelf width along the wall (Y)
SHELF_LEN = 25.0    # how far each shelf reaches into the water (X)
SHELF_T = 6.0       # shelf thickness (Z)

HOLE_D = 10.5       # switch mounting hole (M10); set to your switch stem
HOLE_INSET = 8.0    # hole distance from the shelf tip


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


def build():
    rail_bottom = min(SWITCH_HEIGHTS) - 8.0     # a little below the LOW shelf
    rail_top = RIM_HEIGHT
    rail_len = rail_top - rail_bottom

    # Vertical rail on the inside face of the wall: X in [0, RAIL_T]
    rail = box((RAIL_T, RAIL_W, rail_len),
               (RAIL_T / 2, 0, (rail_top + rail_bottom) / 2))

    # Hook over the rim
    bridge = box((WALL_GAP + LEG_T + RAIL_T, RAIL_W, BRIDGE_T),
                 ((RAIL_T - (WALL_GAP + LEG_T)) / 2, 0, RIM_HEIGHT + BRIDGE_T / 2))
    outer_leg = box((LEG_T, RAIL_W, HOOK_DROP),
                    (-WALL_GAP - LEG_T / 2, 0, RIM_HEIGHT - HOOK_DROP / 2))

    parts = [rail, bridge, outer_leg]
    holes = []
    for h in SWITCH_HEIGHTS:
        parts.append(box((RAIL_T + SHELF_LEN, RAIL_W, SHELF_T),
                         ((RAIL_T + SHELF_LEN) / 2, 0, h)))
        hole_x = RAIL_T + SHELF_LEN - HOLE_INSET
        holes.append(cyl(HOLE_D, SHELF_T + 4, (hole_x, 0, h)))

    bracket = union(parts)
    bracket = diff(bracket, union(holes))
    return bracket


def main():
    bracket = build()
    path = os.path.join(OUT_DIR, "float_switch_bracket.stl")
    bracket.export(path)
    ext = bracket.bounding_box.extents
    print("Wrote:")
    print(f"  bracket: {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"watertight={bracket.is_watertight}, volume={bracket.volume/1000:.1f} cm^3")
    print(f"  switch shelf heights (from floor): "
          f"{', '.join(f'{h:.1f}' for h in SWITCH_HEIGHTS)} mm")
    print(path)


if __name__ == "__main__":
    main()
