from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0103(TooTallToby):
    """Too Tall Toby Party Pack 01-03 C Clamp Base
    """

    def __init__(self):
        with BuildPart(Plane.XY) as p:
            Box(95, 34, 16, align=(Align.MAX, Align.MAX, Align.CENTER))

            with Locations(Plane.YZ):
                Cylinder(8, 95 - 14 + 23, align=(Align.CENTER, Align.CENTER, Align.MAX))

            with Locations((-18, 8, 0)):
                Box(95-18-14, 34-16 + 8, 16, align=(Align.MAX, Align.MAX, Align.CENTER), mode=Mode.SUBTRACT)

            filtered = p.edges().filter_by(Axis.Z).sort_by(Axis.Y)
            fillet(filtered[:2], 18)
            fillet(filtered[2:4], 7)

            face = p.faces().sort_by(Axis.X)[0]
            with Locations(face):
                CounterSinkHole(5.5/2, 11.2/2, 95 +23 - 14, counter_sink_angle=90)

        super().__init__(part=p.part, id="Party Pack 01-03", name="C Clamp Base", ref_mass=96.13, density=Density.AL)

t = TPPP0103()
show(t)