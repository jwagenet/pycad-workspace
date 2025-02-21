"""
Too Tall Toby challenge 23-T-24 CURVED SUPPORT
"""

from math import sin, cos, tan, radians
from build123d import *
from ocp_vscode import set_port, show
import sympy
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart() as ttt_23t24:
    with BuildSketch() as s1:
        c1 = Circle(55/2)
        with Locations((125, 0)):
            c2 = Circle(30/2)
        a = make_hull()
    extrude(amount=11)

    c1 = Cylinder(55/2, 60, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(35/2, 60, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
    with Locations((125, 0)):
        c2 = Cylinder(30/2, 32, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0,0,180))
        Cylinder(20/2, 32, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT, rotation=(0,0,180))

    with BuildSketch(Plane.XZ) as s2:
        with BuildLine() as l1:
            l2 = c1.edges().filter_by(Axis.Z).vertices().sort_by(Axis.Z)
            l3 = c2.edges().filter_by(Axis.Z).vertices().sort_by(Axis.Z)

            Polyline(l2[1]-Vertex(0,0,10), l2[0],l3[0], l3[1]+Vertex(1,0,0), (125-20,0,32), close=True)
        make_face()
    extrude(amount=11/2, both=True)

show(l1, ttt_23t24)
print(f"\npart mass = {ttt_23t24.part.volume*densa:0.2f}")
print(f"ref mass = 1294")