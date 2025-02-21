"""
Too Tall Toby challenge 
"""

from math import sqrt, tan, radians
from build123d import *
from ocp_vscode import set_port, show
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

workplane = Plane((84/2-8, 0, 25), x_dir=(0,-1,0), z_dir=(0,0,1)).rotated((0,-45,0))
with BuildPart() as rib:
    with BuildSketch(workplane) as s1:
        h = (84-35)/2 * sqrt(2)
        with BuildLine() as l1:
            Polyline((0,0), (3/2, 0), (h/2 * tan(radians(10)), -h/2), (0, -h/2))
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=h)

with BuildPart() as ppp0107:
    Cylinder(130/2, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(84/2, 25, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(35/2, 52, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with PolarLocations(0, 3):
        add(rib.part)

    Cylinder(20/2, 52, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
    Cylinder(73/2, 18, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    fillet(ppp0107.faces().filter_by(Plane.XY).sort_by(Axis.Z)[1:4].edges().filter_by(GeomType.CIRCLE), 3)

    with Locations(Plane.XY.offset(8)):
        with PolarLocations(107.95/2, 6):
            CounterBoreHole(6/2, 13/2, 4)

show(ppp0107)
print(f"\npart mass = {ppp0107.part.volume*densb:0.2f}")
print(f"ref mass = 372.99")