from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0110(TooTallToby):
    """Too Tall Toby Party Pack 01-10 Light Cap
    """

    def __init__(self):
        with BuildPart() as p:
            with BuildSketch(Plane.YZ) as s:
                with BuildLine() as l:
                    JernArc((0, 0), (1, 0), 40, 90)
                    Line((0, 46), (42, 46))
                make_hull()

            with BuildSketch(Plane.YZ) as s2:
                arc = s.edges().sort_by(Axis.Y)[:-1].sort_by(Axis.X)[1:]
                make_face(offset(arc, amount=8, side=Side.LEFT))
                Rectangle(46, 16, align=Align.MIN)
                add(s, mode=Mode.INTERSECT)

                # This fails but it should work
                # v = s2.edges().filter_by(Axis.X).sort_by(Axis.X)[0].vertices().sort_by(Axis.X)[-1]
                # fillet(v, 8)

            if True:
                # Workaround
                extrude(s2.sketch, amount=100)
                ex = fillet(p.faces().filter_by(Plane.XY).sort_by(Axis.Y)[0].edges().sort_by(Axis.Y)[-1], 8)
                mirror(about=Plane.XZ)
                rev = revolve(ex.faces().sort_by(Axis.X)[0], axis=Axis.Z, revolution_arc=180)
                mirror(rev, about=Plane.YZ.offset(100 / 2))

            else:
                # This fails but it should work
                extrude(s2.sketch, amount=100 / 2)
                # fillet(ppp0110.faces().filter_by(Plane.XY).sort_by(Axis.Y)[0].edges().sort_by(Axis.Y)[-1], 8)
                revolve(p.faces().sort_by(Axis.X)[0], axis=Axis.Z, revolution_arc=90)
                mirror(about=Plane.YZ.offset(100 / 2))
                mirror(about=Plane.XZ)

        super().__init__(part=p.part, id="Party Pack 01-10", name="Light Cap", ref_mass=211.30, density=Density.ABS)

t = TPPP0110()
show(t)