from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T240401(TooTallToby):
    """Too Tall Toby 24-04-01 Depth Gauge Base
    """

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch(Plane.XZ):
                with BuildLine():
                    Polyline((0, 0), (150/2, 0), (150/2, 11), (50/2, 40), (0, 40), close=True)
                make_face()
                with Locations((33/2, 20)):
                    Circle(6/2, mode=Mode.SUBTRACT)

            extrude(amount=33/2, both=True)
            mirror(about=Plane.YZ)

            with Locations((0, 0, 40)):
                CounterBoreHole(12/2, 22/2, 6)

        super().__init__(part=part.part, id="24-04-01", name="Depth Gauge Base", ref_mass=145.0, density=Density.ABS)


if __name__ == "__main__":
    t = T240401()
    t.show_properties()
    show(t)