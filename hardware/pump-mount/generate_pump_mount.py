"""Generate the DDROID pump / pipe mount bracket as STL.

A base plate with two saddle cradles that hold the pump body horizontally
(secured with zip ties through the base slots) and a snap-in clip for the
outlet pipe.

The Gazebo scene (simulation/build_world.py) draws the pump as a cylinder of
radius 55 mm and the supply->trough pipe as a 30 mm box. Those are scene
stand-ins; the defaults below suit a small 12 V bench pump. Edit PUMP_D and
PIPE_D for your real parts.

Units are millimetres. Requires: trimesh, manifold3d, numpy.
Run:  python generate_pump_mount.py
"""

import os
import numpy as np
import trimesh

ENGINE = "manifold"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Parameters (mm) -------------------------------------------------------
PUMP_D = 40.0        # pump body diameter (scene stand-in is 110 mm)
PIPE_D = 16.0        # outlet pipe outer diameter (scene stand-in is 30 mm)

BASE_L = 120.0       # base length along the pump axis (X)
BASE_W = 52.0        # base width (Y)
BASE_T = 5.0         # base thickness (Z)
CLEAR = 3.0          # gap between pump bottom and base

CRADLE_SPACING = 70.0  # distance between the two cradles (X)
CRADLE_WALL = 8.0      # cradle thickness along the axis (X)
CRADLE_H = 31.0        # cradle height (just above pump centre -> snap retain)

MOUNT_D = 4.2        # M4 base mounting holes
PIPE_X = 50.0        # pipe clip position along X

PUMP_R = PUMP_D / 2
PIPE_R = PIPE_D / 2
PUMP_CZ = BASE_T + CLEAR + PUMP_R      # pump centre height
PIPE_CZ = BASE_T + 2.0 + PIPE_R        # pipe centre height


def box(size, center):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(center)
    return m


def cyl_z(d, h, center):
    m = trimesh.creation.cylinder(radius=d / 2.0, height=h, sections=72)
    m.apply_translation(center)
    return m


def cyl_x(d, length, center):
    m = trimesh.creation.cylinder(radius=d / 2.0, height=length, sections=72)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m


def diff(a, b):
    return trimesh.boolean.difference([a, b], engine=ENGINE)


def union(parts):
    return trimesh.boolean.union(parts, engine=ENGINE)


def build():
    parts, cuts = [], []

    # Base plate
    parts.append(box((BASE_L, BASE_W, BASE_T), (0, 0, BASE_T / 2)))

    # Two cradles
    for cx in (-CRADLE_SPACING / 2, CRADLE_SPACING / 2):
        parts.append(box((CRADLE_WALL, BASE_W, CRADLE_H), (cx, 0, CRADLE_H / 2)))
        cuts.append(cyl_x(PUMP_D, CRADLE_WALL + 4, (cx, 0, PUMP_CZ)))  # saddle valley
        # zip-tie slots in the base, one each side of the pump
        for sy in (-1, 1):
            cuts.append(box((7.0, 3.5, BASE_T + 4),
                            (cx, sy * (PUMP_R + 4), BASE_T / 2)))

    # Pipe clip (C-ring) at +X end
    parts.append(box((16.0, 18.0, PIPE_CZ), (PIPE_X, 0, PIPE_CZ / 2)))  # riser
    parts.append(cyl_x(PIPE_D + 6, 14.0, (PIPE_X, 0, PIPE_CZ)))         # ring body
    cuts.append(cyl_x(PIPE_D, 18.0, (PIPE_X, 0, PIPE_CZ)))              # bore
    cuts.append(box((16.0, PIPE_D - 3, PIPE_R + 4),
                    (PIPE_X, 0, PIPE_CZ + (PIPE_R + 4) / 2 + 1)))        # top opening

    # Corner mounting holes
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(cyl_z(MOUNT_D, BASE_T + 4,
                              (sx * (BASE_L / 2 - 8), sy * (BASE_W / 2 - 8), BASE_T / 2)))

    return diff(union(parts), union(cuts))


def main():
    m = build()
    path = os.path.join(OUT_DIR, "pump_mount.stl")
    m.export(path)
    ext = m.bounding_box.extents
    print("Wrote:")
    print(f"  pump_mount: {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"watertight={m.is_watertight}, volume={m.volume/1000:.1f} cm^3")
    print(f"  pump dia {PUMP_D} mm (centre {PUMP_CZ:.1f} mm), "
          f"pipe dia {PIPE_D} mm (centre {PIPE_CZ:.1f} mm)")
    print(path)


if __name__ == "__main__":
    main()
