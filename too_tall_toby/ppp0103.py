from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart(Plane.XY) as ppp0103:
    Box(95, 34, 16, align=(Align.MAX, Align.MAX, Align.CENTER))

    with Locations(Plane.YZ):
        Cylinder(8, 95 - 14 + 23, align=(Align.CENTER, Align.CENTER, Align.MAX))

    with Locations((-18, 8, 0)):
        Box(95-18-14, 34-16 + 8, 16, align=(Align.MAX, Align.MAX, Align.CENTER), mode=Mode.SUBTRACT)

    filtered = ppp0103.edges().filter_by(Axis.Z).sort_by(Axis.Y)
    fillet(filtered[:2], 18)
    fillet(filtered[2:4], 7)

    face = ppp0103.faces().sort_by(Axis.X)[0]
    with Locations(face):
        CounterSinkHole(5.5/2, 11.2/2, 95 +23 - 14, counter_sink_angle=90)


show(ppp0103)
print(f"\npart mass = {ppp0103.part.volume*densb:0.2f}")
print(f"ref mass = 96.13")
