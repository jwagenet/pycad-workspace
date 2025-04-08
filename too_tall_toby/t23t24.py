from math import sin, cos, tan, radians

import sympy
from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class T23T24(TooTallToby):
    """Too Tall Toby 23-T-24 Curved Support
    """

    def __init__(self):
        with BuildPart() as p:
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

        super().__init__(part=p.part, id="23-T-24", name="Curved Support", ref_mass=1294, density=Density.ST, tolerance=3)


if __name__ == "__main__":
    t = T23T24()
    t.show_properties()
    show(t)