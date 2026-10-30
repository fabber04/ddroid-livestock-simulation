"""Build a 3D model of the whole DDROID water point, assembled.

Supply tank -> pump (in its mount) -> pipe -> trough, with the float-switch
bracket on the trough and the controller enclosure wired in. Uses the real
tank/trough sizes and switch heights from simulation/ddroid_scene.py and
drops in the printed parts (enclosure, bracket, pump mount).

Outputs (in this folder):
  system_assembly.stl  - single mesh, rotatable in GitHub's 3D viewer
  system_assembly.glb  - coloured, for any glTF viewer
  preview.png          - shaded render

Units are millimetres. Requires: trimesh, manifold3d, numpy, matplotlib.
Run:  python generate_assembly.py
"""

import os
import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)

# Colours (0-255 RGBA)
C_TANK = [158, 168, 180, 255]
C_WATER = [30, 115, 210, 150]
C_PUMP = [40, 42, 48, 255]
C_PIPE = [70, 80, 92, 255]
C_BENCH = [140, 102, 64, 255]
C_ENC = [92, 202, 165, 255]
C_BRACKET = [240, 153, 123, 255]
C_MOUNT = [176, 169, 236, 255]
C_SW = [120, 150, 190, 255]
C_SW_CUT = [217, 75, 75, 255]
C_WIRE = [50, 50, 55, 255]

WALL = 12.0
items = []  # (mesh, rgba)


def add(mesh, rgba):
    items.append((mesh, rgba))
    return mesh


def box(size, center):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(center)
    return m


def vcyl(r, h, center):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=40)
    m.apply_translation(center)
    return m


def pipe(r, p0, p1):
    return trimesh.creation.cylinder(radius=r, segment=[np.array(p0), np.array(p1)], sections=24)


def tank(spec, rgba):
    cx, cy, z0, sx, sy, h = (spec[k] for k in ("cx", "cy", "z0", "sx", "sy", "h"))
    add(box((sx + 2 * WALL, sy + 2 * WALL, WALL), (cx, cy, z0 - WALL / 2)), rgba)
    add(box((WALL, sy, h), (cx - sx / 2 - WALL / 2, cy, z0 + h / 2)), rgba)
    add(box((WALL, sy, h), (cx + sx / 2 + WALL / 2, cy, z0 + h / 2)), rgba)
    add(box((sx + 2 * WALL, WALL, h), (cx, cy + sy / 2 + WALL / 2, z0 + h / 2)), rgba)
    fl = h * 0.45
    add(box((sx + 2 * WALL, WALL, fl), (cx, cy - sy / 2 - WALL / 2, z0 + fl / 2)), rgba)  # low front
    # water
    wl = h * spec.get("fill", 0.5)
    add(box((sx * 0.96, sy * 0.96, wl), (cx, cy, z0 + wl / 2)), C_WATER)


def load_part(rel, transform=None):
    m = trimesh.load(os.path.join(HW, rel))
    if transform is not None:
        m.apply_transform(transform)
    return m


def rot_z(deg):
    return trimesh.transformations.rotation_matrix(np.radians(deg), [0, 0, 1])


def build():
    SUP = {"cx": -600, "cy": 0, "z0": 0, "sx": 300, "sy": 300, "h": 340, "fill": 0.6}
    TRO = {"cx": 550, "cy": 0, "z0": 0, "sx": 660, "sy": 320, "h": 160, "fill": 0.45}

    add(box((1820, 820, 20), (65, 0, -10)), C_BENCH)  # bench top
    tank(SUP, C_TANK)
    tank(TRO, C_TANK)

    # Pump mount (printed) + pump between the tanks
    mount = load_part("pump-mount/pump_mount.stl")
    mount.apply_translation((-115, 0, 0))
    add(mount, C_MOUNT)
    pump = trimesh.creation.cylinder(radius=20, segment=[(-160, 0, 28), (-70, 0, 28)], sections=40)
    add(pump, C_PUMP)

    # Pipe: tank outlet -> pump -> trough inlet
    add(pipe(8, (-450, 0, 70), (-160, 0, 28)), C_PIPE)
    add(pipe(8, (-70, 0, 28), (220, 0, 90)), C_PIPE)
    add(pipe(8, (220, 0, 90), (300, 0, 60)), C_PIPE)

    # Float-switch bracket (printed) on the trough front wall
    br = load_part("float-switch-bracket/float_switch_bracket.stl", rot_z(90))
    br.apply_translation((TRO["cx"], -TRO["sy"] / 2, 0))
    add(br, C_BRACKET)
    # switch bodies on the shelves (48/120/147 mm)
    for h, col in [(48, C_SW), (120, C_SW), (147, C_SW_CUT)]:
        add(vcyl(10, 26, (TRO["cx"], -TRO["sy"] / 2 + 22, h)), col)
    # supply-low switch
    add(vcyl(9, 22, (SUP["cx"], -SUP["sy"] / 2 - 10, 0.20 * SUP["h"])), C_SW)

    # Controller enclosure (printed) at the bench front
    enc = load_part("esp32-pump/enclosure/ddroid_controller_box.stl")
    enc.apply_translation((-115, -330, 0))
    add(enc, C_ENC)

    # "Wires" tying switches and pump to the controller
    add(pipe(2.5, (TRO["cx"], -TRO["sy"] / 2 + 22, 120), (-90, -330, 25)), C_WIRE)
    add(pipe(2.5, (-115, 0, 28), (-130, -330, 20)), C_WIRE)
    add(pipe(2.5, (SUP["cx"], -SUP["sy"] / 2 - 10, 68), (-140, -330, 25)), C_WIRE)


def export_models():
    scene = trimesh.Scene()
    solids = []
    for i, (m, rgba) in enumerate(items):
        g = m.copy()
        g.visual = trimesh.visual.ColorVisuals(g, face_colors=np.tile(rgba, (len(g.faces), 1)))
        scene.add_geometry(g, geom_name=f"part_{i}")
        solids.append(m)
    scene.export(os.path.join(HERE, "system_assembly.glb"))
    combined = trimesh.util.concatenate(solids)
    combined.export(os.path.join(HERE, "system_assembly.stl"))
    print(f"  assembly: {combined.bounding_box.extents.round(0)} mm, {len(items)} parts")


def render():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    light = np.array([0.35, 0.4, 0.85]); light /= np.linalg.norm(light)
    allv = np.vstack([m.vertices for m, _ in items])
    lo, hi = allv.min(0), allv.max(0)

    tris_all, fc_all = [], []
    for m, rgba in items:
        inten = np.clip(m.face_normals @ light, 0, 1) * 0.6 + 0.4
        base = np.array(rgba[:3]) / 255.0
        fc = np.clip(base[None, :] * inten[:, None], 0, 1)
        a = rgba[3] / 255.0
        fc = np.hstack([fc, np.full((len(fc), 1), a)])
        tris_all.append(m.vertices[m.faces])
        fc_all.append(fc)
    tris_all = np.vstack(tris_all)
    fc_all = np.vstack(fc_all)

    def draw(ax, elev, azim):
        pc = Poly3DCollection(tris_all, linewidths=0)
        pc.set_facecolors(fc_all)
        ax.add_collection3d(pc)
        ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
        ax.set_box_aspect((hi - lo))
        ax.view_init(elev=elev, azim=azim); ax.set_axis_off()

    fig = plt.figure(figsize=(14, 6))
    for i, (e, a, t) in enumerate([(30, -58, "assembled water point"), (26, -112, "other side")]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        draw(ax, e, a)
        ax.set_title(t, fontsize=11, color="#444441")
    plt.tight_layout()
    out = os.path.join(HERE, "preview.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", transparent=True)
    print("  wrote", out)


def main():
    build()
    export_models()
    render()


if __name__ == "__main__":
    main()
