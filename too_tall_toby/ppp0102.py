from math import radians, tan

from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0102(TooTallToby):
    """Too Tall Toby Party Pack 01-02 Post Cap
    """

    def __init__(self):
        with BuildPart() as p:
            with BuildSketch(Plane.XZ):
                with BuildLine():
                    Polyline((49/2-20, 48), (0, 48), (0, 0), (49/2, 0), (49/2, 48-8))
                    EllipticalCenterArc((49/2-20, 48-8), 20, 8)
                make_face()
            revolve()

            with BuildLine(Plane.YZ):
                path = CenterArc((-15, 20), 17, 90, 180)

            with BuildSketch(Plane(path ^ 0, x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
                Ellipse(4/2, 10/2)

            sweep(path=path)
            fillet(p.edges(Select.NEW), 1)

            with BuildSketch(Plane.XZ):
                with BuildLine():
                    FilletPolyline((0, 37), (42/2 - 37*tan(radians(4)), 37), (42/2, 0), radius=3)
                    Polyline((0, 37), (0,0), (42/2, 0))
                make_face()
            revolve(mode=Mode.SUBTRACT)

        super().__init__(part=p.part, id="Party Pack 01-02", name="Post Cap", ref_mass=328.02, density=Density.ST)

t = TPPP0102()
show(t)