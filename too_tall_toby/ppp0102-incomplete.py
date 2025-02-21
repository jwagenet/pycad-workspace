from math import radians, tan
from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS


with BuildPart() as ppp0102:
    with BuildSketch(Plane.XZ) as s1:
        with BuildLine() as l1:
            Polyline((49/2-20, 48), (0, 48), (0, 0), (49/2, 0), (49/2, 48-8))
            EllipticalCenterArc((49/2-20, 48-8), 20, 8)
        make_face()
    revolve()

    with BuildLine(Plane.YZ):
        path = CenterArc((-15, 20), 17, 90, 180)

    with BuildSketch(Plane(path ^ 0, x_dir=(1, 0, 0), z_dir=(0, 1, 0))) as profile:
        Ellipse(4/2, 10/2)

    sweep(path=path)
    fillet(ppp0102.edges(Select.NEW), 1)

    with BuildSketch(Plane.XZ) as s2:
        with BuildLine() as l1:
            FilletPolyline((0, 37), (42/2 - 37*tan(radians(4)), 37), (42/2, 0), radius=3)
            Polyline((0, 37), (0,0), (42/2, 0))
        make_face()
    revolve(mode=Mode.SUBTRACT)


show(ppp0102)
print(f"\npart mass = {ppp0102.part.volume*densa:0.2f}")
print(f"ref mass = 328.02")
