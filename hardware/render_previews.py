"""Render clean shaded preview images for the DDROID printed parts.

Uses matplotlib with per-face lighting (no wireframe) so the STLs look like
solid models. Regenerates each part's preview.png and a combined thumbnail
strip for the hardware index.

Requires: trimesh, numpy, matplotlib.
Run:  python render_previews.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
LIGHT = np.array([0.3, 0.45, 0.85])
LIGHT = LIGHT / np.linalg.norm(LIGHT)
AMBIENT = 0.4


def shaded_faces(mesh, base_rgb):
    inten = mesh.face_normals @ LIGHT
    inten = np.clip(inten, 0, 1)
    inten = AMBIENT + (1 - AMBIENT) * inten
    base = np.array(base_rgb)
    cols = np.clip(base[None, :] * inten[:, None], 0, 1)
    return np.hstack([cols, np.ones((len(cols), 1))])


def add_mesh(ax, mesh, base_rgb, elev, azim):
    pc = Poly3DCollection(mesh.vertices[mesh.faces], linewidths=0)
    pc.set_facecolors(shaded_faces(mesh, base_rgb))
    ax.add_collection3d(pc)
    v = mesh.vertices
    ax.set_xlim(v[:, 0].min(), v[:, 0].max())
    ax.set_ylim(v[:, 1].min(), v[:, 1].max())
    ax.set_zlim(v[:, 2].min(), v[:, 2].max())
    ax.set_box_aspect(tuple(mesh.extents))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


def render(panels, out, figsize):
    fig = plt.figure(figsize=figsize)
    n = len(panels)
    for i, (mesh, color, elev, azim, title) in enumerate(panels):
        ax = fig.add_subplot(1, n, i + 1, projection="3d")
        add_mesh(ax, mesh, color, elev, azim)
        if title:
            ax.set_title(title, fontsize=11, color="#444441", pad=0)
    plt.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("wrote", out)


def load(rel):
    return trimesh.load(os.path.join(HERE, rel))


TEAL = (0.36, 0.79, 0.65)
BLUE = (0.52, 0.72, 0.92)
CORAL = (0.94, 0.60, 0.48)
PURPLE = (0.69, 0.66, 0.92)


def main():
    box = load("esp32-pump/enclosure/ddroid_controller_box.stl")
    lid = load("esp32-pump/enclosure/ddroid_controller_lid.stl")
    bracket = load("float-switch-bracket/float_switch_bracket.stl")
    pump = load("pump-mount/pump_mount.stl")

    render(
        [(box, TEAL, 26, -52, "box"), (lid, BLUE, 32, -128, "lid")],
        os.path.join(HERE, "esp32-pump/enclosure/preview.png"), (11, 4.5),
    )
    render(
        [(bracket, CORAL, 16, -64, "front"), (bracket, CORAL, 8, -102, "hook over rim")],
        os.path.join(HERE, "float-switch-bracket/preview.png"), (8, 6),
    )
    render(
        [(pump, PURPLE, 26, -58, "saddles + pipe clip"), (pump, PURPLE, 6, -24, "end view")],
        os.path.join(HERE, "pump-mount/preview.png"), (10, 5),
    )
    # Thumbnail strip for the hardware index
    render(
        [(box, TEAL, 24, -52, "enclosure"),
         (bracket, CORAL, 14, -66, "float-switch bracket"),
         (pump, PURPLE, 24, -58, "pump mount")],
        os.path.join(HERE, "parts.png"), (13, 4),
    )


if __name__ == "__main__":
    main()
