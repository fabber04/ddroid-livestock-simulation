"""Build a 3D model of the whole DDROID water point, mirroring the Gazebo scene.

Ports the geometry from ../../simulation/build_world.py and ddroid_scene.py:
wood bench on legs, supply stand, open-top supply tank and trough with water,
the vertical pump, the supply->trough pipe, the float-switch markers, the
status/pump lamps, and two livestock, on a green ground.

Outputs (in this folder):
  system_assembly.stl  - single mesh (mm), rotatable in GitHub's 3D viewer
  system_assembly.glb  - coloured, for any glTF viewer
  preview.png          - shaded render with a sky background

Units here are metres (as in Gazebo); exports are scaled to mm.
Requires: trimesh, numpy, matplotlib.  Run:  python generate_assembly.py
"""

import os
import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))

# Colours (0-255 RGBA), from build_world.py
GROUND = [92, 117, 71, 255]
WOOD = [115, 77, 41, 255]
PLASTIC = [158, 168, 179, 255]
PLASTIC_DARK = [71, 82, 92, 255]
WATER = [31, 115, 209, 235]
PUMP_BODY = [38, 41, 46, 255]
COW = [107, 71, 41, 255]
COW_DARK = [56, 36, 20, 255]
LAMP_ON = [242, 140, 13, 255]
MODE_REFILL = [26, 89, 230, 255]
SW_WET = [26, 89, 217, 255]
SW_DRY = [191, 191, 184, 255]
SW_CUT = [217, 38, 31, 255]
SKY = (0.62, 0.76, 0.88)

# Scene constants (metres), from ddroid_scene.py
SUPPLY = {"cx": -0.72, "cy": 0.0, "z0": 0.90, "sx": 0.30, "sy": 0.30, "h": 0.34}
TROUGH = {"cx": 0.62, "cy": 0.02, "z0": 0.84, "sx": 0.66, "sy": 0.32, "h": 0.16}
PUMP_XYZ = (-0.05, 0.0, 0.98)
MODE_LAMP_XYZ = (0.0, -0.42, 0.82)
WALL = 0.018

items = []


def add(mesh, rgba):
    items.append((mesh, rgba))


def box(size, center):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(center)
    return m


def vcyl(r, h, center):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=36)
    m.apply_translation(center)
    return m


def ball(r, center):
    m = trimesh.creation.icosphere(subdivisions=2, radius=r)
    m.apply_translation(center)
    return m


def vessel(spec, wall_h):
    cx, cy, z0, sx, sy = spec["cx"], spec["cy"], spec["z0"], spec["sx"], spec["sy"]
    add(box((sx + 2 * WALL, sy + 2 * WALL, WALL), (cx, cy, z0 - WALL / 2)), PLASTIC)
    sz = z0 + wall_h / 2
    add(box((WALL, sy, wall_h), (cx - sx / 2 - WALL / 2, cy, sz)), PLASTIC)
    add(box((WALL, sy, wall_h), (cx + sx / 2 + WALL / 2, cy, sz)), PLASTIC)
    add(box((sx + 2 * WALL, WALL, wall_h), (cx, cy + sy / 2 + WALL / 2, sz)), PLASTIC)
    lip = wall_h * 0.42
    add(box((sx + 2 * WALL, WALL, lip), (cx, cy - sy / 2 - WALL / 2, z0 + lip / 2)), PLASTIC)


def water(spec, fill):
    wl = spec["h"] * fill
    add(box((spec["sx"] * 0.96, spec["sy"] * 0.96, wl),
            (spec["cx"], spec["cy"], spec["z0"] + wl / 2)), WATER)


def switch_anchor(spec, level, x_shift=0.0):
    z = spec["z0"] + level * spec["h"]
    y = spec["cy"] - spec["sy"] / 2 - 0.045
    return (spec["cx"] + x_shift, y, z)


def livestock(x, y, z):
    add(box((0.34, 0.16, 0.16), (x, y, z + 0.16)), COW)
    add(box((0.12, 0.10, 0.12), (x + 0.20, y, z + 0.22)), COW_DARK)
    for dx, dy in ((-0.10, -0.05), (-0.10, 0.05), (0.10, -0.05), (0.10, 0.05)):
        add(box((0.04, 0.04, 0.12), (x + dx, y + dy, z + 0.06)), COW_DARK)


def build():
    add(box((3.6, 2.4, 0.02), (0.0, 0.0, -0.01)), GROUND)

    # Bench (table) + legs
    add(box((2.15, 1.15, 0.06), (0.0, 0.0, 0.74)), WOOD)
    for x, y in ((-0.95, -0.45), (-0.95, 0.45), (0.95, -0.45), (0.95, 0.45)):
        add(vcyl(0.035, 0.72, (x, y, 0.36)), PLASTIC_DARK)

    add(box((0.22, 0.22, 0.12), (-0.72, 0.0, 0.83)), WOOD)  # supply stand

    vessel(SUPPLY, SUPPLY["h"] + 0.04)
    vessel(TROUGH, TROUGH["h"] + 0.03)
    water(SUPPLY, 0.6)
    water(TROUGH, 0.45)

    # Pipe supply -> trough
    sx_r = SUPPLY["cx"] + SUPPLY["sx"] / 2
    tx_l = TROUGH["cx"] - TROUGH["sx"] / 2
    add(box((tx_l - sx_r, 0.03, 0.03), ((sx_r + tx_l) / 2, 0.0, 0.96)), PLASTIC_DARK)

    # Pump + lamps
    add(vcyl(0.055, 0.14, PUMP_XYZ), PUMP_BODY)
    add(ball(0.03, (PUMP_XYZ[0], PUMP_XYZ[1], PUMP_XYZ[2] + 0.10)), LAMP_ON)
    add(ball(0.045, MODE_LAMP_XYZ), MODE_REFILL)

    # Float-switch markers
    add(ball(0.022, switch_anchor(SUPPLY, 0.20)), SW_WET)
    add(ball(0.022, switch_anchor(TROUGH, 0.30, -0.18)), SW_WET)
    add(ball(0.022, switch_anchor(TROUGH, 0.75, 0.05)), SW_DRY)
    add(ball(0.026, switch_anchor(TROUGH, 0.92, 0.22)), SW_CUT)

    # Livestock at the trough
    livestock(0.35, -0.48, 0.77)
    livestock(0.78, -0.50, 0.77)


def export_models():
    scene = trimesh.Scene()
    solids = []
    S = trimesh.transformations.scale_matrix(1000.0)  # m -> mm
    for i, (m, rgba) in enumerate(items):
        g = m.copy()
        g.apply_transform(S)
        g.visual = trimesh.visual.ColorVisuals(g, face_colors=np.tile(rgba, (len(g.faces), 1)))
        scene.add_geometry(g, geom_name=f"part_{i}")
        solids.append(g)
    scene.export(os.path.join(HERE, "system_assembly.glb"))
    trimesh.util.concatenate(solids).export(os.path.join(HERE, "system_assembly.stl"))
    print(f"  assembly: {trimesh.util.concatenate(solids).bounding_box.extents.round(0)} mm, {len(items)} parts")


def render():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    light = np.array([0.4, 0.5, 0.75]); light /= np.linalg.norm(light)
    allv = np.vstack([m.vertices for m, _ in items])
    lo, hi = allv.min(0), allv.max(0)

    tris, cols = [], []
    for m, rgba in items:
        inten = np.clip(m.face_normals @ light, 0, 1) * 0.55 + 0.45
        base = np.array(rgba[:3]) / 255.0
        fc = np.clip(base[None, :] * inten[:, None], 0, 1)
        a = rgba[3] / 255.0
        tris.append(m.vertices[m.faces])
        cols.append(np.hstack([fc, np.full((len(fc), 1), a)]))
    tris = np.vstack(tris); cols = np.vstack(cols)

    fig = plt.figure(figsize=(14, 6)); fig.patch.set_facecolor(SKY)
    for i, (e, a, t) in enumerate([(20, -58, "overview"), (16, -118, "trough side")]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        pc = Poly3DCollection(tris, linewidths=0); pc.set_facecolors(cols)
        ax.add_collection3d(pc)
        ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
        ax.set_box_aspect((hi - lo))
        ax.view_init(elev=e, azim=a); ax.set_axis_off()
        ax.patch.set_facecolor(SKY)
        ax.set_title(t, fontsize=11, color="#2c2c2a")
    plt.tight_layout()
    out = os.path.join(HERE, "preview.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=SKY)
    print("  wrote", out)


def main():
    build()
    export_models()
    render()


if __name__ == "__main__":
    main()
