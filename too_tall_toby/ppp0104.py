from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0104(TooTallToby):
    """Too Tall Toby Party Pack 01-04 Angle Bracket

    Requires workaround for fillet connecting plane to cylinder where plane is width of cylinder diameter
    """

    def __init__(self):
        with BuildPart() as p:
            Box(80 - 38/2, 38, 7, align=(Align.MIN, Align.CENTER, Align.MIN))
            Cylinder(38/2, 7+21-8, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0, 0, 180))
            Cylinder(26/2, 7+21, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(16/2, 7+21, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

            with Locations((80 - 38/2, 0, 0)):
                Box(10, 38, 30 - 7, align=(Align.MAX, Align.CENTER, Align.MAX))

            e1 = p.faces().filter_by(Axis.X).sort_by(Axis.X)[-2].edges().sort_by(Axis.Z)[-1]

            with BuildSketch(Plane((80 - 38/2, 0, 17-9-30+7), x_dir=(0, 1, 0), z_dir=(1, 0, 0))) as s1:
                Circle(12/2)
                Rectangle(12, 17-9, align=(Align.CENTER, Align.MAX))

            extrude(amount=-10, mode=Mode.SUBTRACT)
            extrude(offset(s1.sketch, amount=3), amount=-5, mode=Mode.SUBTRACT)


            fillet(e1, 5)
            fillet(p.edges().sort_by(Axis.X)[-4:].sort_by(Axis.Z)[-1], 10)

            # fillet workaround
            with Locations((0, 38/2, 0)) as l1:
                b = Box(38/2, 5, 7, align=Align.MIN)
            mirror(b, about=Plane.XZ)

            e2 = p.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-5]
            fillet(e2, 4)

            with l1:
                bs = Box(38/2, 5, 12, align=Align.MIN, mode=Mode.SUBTRACT)
            mirror(bs, about=Plane.XZ, mode=Mode.SUBTRACT)

        super().__init__(part=p.part, id="Party Pack 01-04", name="Angle Bracket", ref_mass=310.00, density=Density.ST)

t = TPPP0104()
show(t)