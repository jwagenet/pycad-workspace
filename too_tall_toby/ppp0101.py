from math import radians, tan

from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0101(TooTallToby):
    """Too Tall Toby Party Pack 01-01 Bearing Bracket

    Requires workaround to prevent fillet from following tangent edge
    """

    def __init__(self):
        with BuildPart() as p:
            with BuildSketch():
                Rectangle(115, 50)
                SlotOverall(90, 12, mode=Mode.SUBTRACT)
            extrude(amount=15)

            v = p.faces().sort_by(Axis.X)[0].vertices().sort_by(Axis.Y)[:2].sort_by(Axis.Z)[0]

            with BuildSketch(Plane.YZ):
                Trapezoid(18 + 2*8/tan(radians(60)), 8, 60, align=(Align.CENTER, Align.MAX), rotation=180)
            extrude(both=True, until=p.part, mode=Mode.SUBTRACT)

            with BuildSketch(p.faces().sort_by(Axis.Y)[0]) as s3:
                with Locations((-115 / 2 + 26, 42 - 15/2)):
                    Circle(26)
                    Rectangle(26 * 2, 42 - 15, align=(Align.CENTER,Align.MAX))
            s3 = extrude(amount=-12)

            face = p.faces().sort_by(Axis.Y)[0]
            center = face.edges().filter_by(GeomType.CIRCLE).edge().arc_center
            with Locations(center):
                with Locations(Plane.XZ):
                    cbore = CounterBoreHole(24/2, 34/2, 4)

            f = fillet(s3.faces().sort_by(Axis.X)[-1].edges().sort_by(Axis.Z)[0], 9)

            mirror(s3, about=Plane.XZ)
            mirror(f, about=Plane.XZ)
            mirror(cbore, about=Plane.XZ, mode=Mode.SUBTRACT)

            fillet(p.edges().filter_by(Axis.Z).filter_by(lambda e: e.length == 15), 6)
            # fillet(ppp0101.edges().filter_by(Axis.Z).filter_by(lambda e:e.length == 42), 6)

            # workaround to stop fillet following tangent edges
            with BuildSketch(Plane(v)) as s4:
                with BuildLine():
                    l = Polyline((0, 6), (0, 0), (6, 0))
                    RadiusArc((l @ 1), (l @ 0), radius=6)
                make_face()
            f = extrude(amount=42 + 26, mode=Mode.SUBTRACT)
            mirror(f, mode=Mode.SUBTRACT)

        super().__init__(part=p.part, id="Party Pack 01-01", name="Bearing Bracket", ref_mass=797.15, density=Density.ST)

t = TPPP0101()
show(t)