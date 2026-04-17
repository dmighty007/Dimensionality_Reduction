import math

from pymol import cmd
from pymol.cgo import CYLINDER


def lerp_color(c1, c2, t):
    """Linear interpolation between two RGB colors"""
    return (
        (1 - t) * c1[0] + t * c2[0],
        (1 - t) * c1[1] + t * c2[1],
        (1 - t) * c1[2] + t * c2[2],
    )


def draw_helix_tube(
    R=1.0,
    pitch=2.0,
    z_min=0.0,
    z_max=10.0,
    steps=500,
    tube_radius=0.5,
    color_low=(0.2, 0.4, 1.0),  # blue
    color_high=(1.0, 0.3, 0.3),  # red
    name="reference_helix",
):
    """
    Draw a helical tube using CGO cylinders with z-gradient coloring.
    """

    obj = []

    last_x = last_y = last_z = None
    last_color = None

    for i in range(steps + 1):
        z = z_min + (i / steps) * (z_max - z_min)

        theta = 2 * math.pi * z / pitch
        x = R * math.cos(theta)
        y = R * math.sin(theta)

        # Normalize z for color gradient
        t = (z - z_min) / (z_max - z_min)
        color = lerp_color(color_low, color_high, t)

        if last_x is not None:
            obj.extend(
                [
                    CYLINDER,
                    last_x,
                    last_y,
                    last_z,
                    x,
                    y,
                    z,
                    tube_radius,
                    *last_color,
                    *color,
                ]
            )

        last_x, last_y, last_z = x, y, z
        last_color = color

    cmd.load_cgo(obj, name)
    # cmd.set("cgo_transparency", 0.35, name)


# ------------------------------------------------------------------
# Load structure + trajectory
# ------------------------------------------------------------------
cmd.load("./start.pdb", "traj")
cmd.load_traj("./traj.xtc", "traj", interval=1)

# ------------------------------------------------------------------
# Draw reference helix (MATCHES YOUR FORCE PARAMETERS)
# ------------------------------------------------------------------
draw_helix_tube(
    R=10.0,
    pitch=20.0,
    z_min=-10.0,
    z_max=100.0,
    tube_radius=0.6,
)

# ------------------------------------------------------------------
# Visual settings
# ------------------------------------------------------------------
cmd.show("spheres", "traj and name C0")
cmd.set("sphere_scale", 1.0, "traj")
cmd.color("cyan", "traj")

cmd.zoom("all")
