from math import sqrt

from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0109(TooTallToby):
    """Too Tall Toby Party Pack 01-09 Corner Tie
    """

    def __init__(self):
        with BuildPart() as p:
            b = Box(69, 75, 13, align=(Align.MAX, Align.CENTER, Align.MIN))
            fillet(b.edges().filter_by(Axis.Z).sort_by(Axis.X)[:2], 17)
            with Locations((-69+17, -75/2+17, 13), (-69+17, 75/2-17, 13)):
                CounterBoreHole(8/2, 15/2, 4, 13)

            with BuildSketch(Plane.YZ) as s1:
                with Locations((0,60-15)):
                    Circle(15)

                with BuildLine():
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
            fillet(p.edge(Select.NEW), 16)

        super().__init__(part=p.part, id="Party Pack 01-09", name="Corner Tie", ref_mass=307.23, density=Density.AL)


if __name__ == "__main__":
    t = TPPP0109()
    t.show_properties()
    show(t)