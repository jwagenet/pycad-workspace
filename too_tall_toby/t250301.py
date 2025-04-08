from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T250301(TooTallToby):
    """Too Tall Toby 25-03-01 Lever Mount
    """

    def __init__(self):
        with BuildPart() as part:
            Box(90, 70, 25, align=(Align.CENTER, Align.MAX, Align.MIN))
            fillet(part.edges().filter_by(lambda e: e.length == 25).sort_by(Axis.Y)[:2], 15)

            with BuildSketch(Plane.XZ):
                with BuildLine() as line:
                    l1 = Polyline((0, 0,), (45, 0), (45, 75))
                    a1 = JernArc(l1 @ 1, l1 % 1, 70, -35)
                    a2 = CenterArc((0, 75), 115, start_angle=0, arc_size=90, mode=Mode.PRIVATE)
                    l2 = IntersectingLine(a1 @ 1, a1 % 1, a2)
                    RadiusArc(a2 @ 1, l2 @ 1, 115)

                    fillet(line.vertices().sort_by(Axis.Y)[-2], 20)
                    mirror(about=Plane.YZ)

                    e = line.edges().filter_by(GeomType.CIRCLE).group_by(Edge.radius)[0]
                    a3 = RadiusArc(e[1].arc_center, e[0].arc_center, 115 - 20, mode=Mode.PRIVATE)
                make_face()

                SlotArc(a3, 20, mode=Mode.SUBTRACT)

            extrude(amount=25)

            with BuildSketch(Plane.XZ.offset(25)):
                Rectangle(50, 75, align=(Align.CENTER, Align.MIN))
                with Locations((0, 75)):
                    Circle(25)
            extrude(amount=15)

            e = part.edges(Select.NEW).group_by(Edge.length)[0]
            fillet(e, 5)

            f2 = part.edges().filter_by(GeomType.CIRCLE).group_by(Edge.radius).group(25).sort_by(Axis.Y)[-1]
            fillet(f2, 5)

            with Locations(Location((0, 0, 75), (90, 0, 0))):
                Hole(20 / 2)

            with Locations((0, -55, 25)):
                with GridLocations(60, 0, 2, 1):
                    CounterBoreHole(9/2, 15/2, 8)

        super().__init__(part=part.part, id="25-03-01", name="Lever Mount", ref_mass=4453.08, density=Density.ST)


if __name__ == "__main__":
    t = T250301()
    t.show_properties()
    show(t)