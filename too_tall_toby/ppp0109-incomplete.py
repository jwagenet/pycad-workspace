"""
Too Tall Toby Party Pack 01-09 Corner Tie
"""

from math import sqrt
from build123d import *
from ocp_vscode import *

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS


with BuildPart() as ppp0109:
    b = Box(69, 75, 13, align=(Align.MAX, Align.CENTER, Align.MIN))
    fillet(b.edges().filter_by(Axis.Z).sort_by(Axis.X)[:2], 17)
    with Locations((-69+17, -75/2+17, 13), (-69+17, 75/2-17, 13)):
        CounterBoreHole(8/2, 15/2, 4, 13)

    with BuildSketch(Plane.YZ) as s1:
        with Locations((0,60-15)):
            Circle(15)

        with BuildLine() as l:
            c = Line((75 / 2, 0), (75 / 2, 60), mode=Mode.PRIVATE)
            u = s1.edge().find_tangent(75 / 2 + 90)[0]  # where is the slope 75/2?
            l1 = IntersectingLine(s1.edge().position_at(u), -s1.edge().tangent_at(u), other=c)

            Line(l1 @ 0, (0, 45))
            Polyline((0, 0), c @ 0, l1 @ 1)
            mirror(about=Plane.YZ)
        make_face()

        with Locations((0, 60-15)):
            Circle(12/2, mode=Mode.SUBTRACT)

    extrude(amount=-16)

    with BuildSketch(Plane.XY.rotated((0,45,0))) as s2:
        Rectangle(45*sqrt(2) - 75/2, 75, align=(Align.MIN, Align.CENTER))
        Rectangle(75 - 45*sqrt(2), 75, align=(Align.MAX, Align.CENTER))
        with Locations(s2.edges().sort_by(Axis.X)[-1].center()):
            Circle(75/2)
            Circle(33/2, mode=Mode.SUBTRACT)

    extrude(amount=6)
    fillet(ppp0109.edge(Select.NEW), 16)


show(ppp0109)
print(f"\npart mass = {ppp0109.part.volume*densb:0.2f}")
print(f"ref mass = 307.23")