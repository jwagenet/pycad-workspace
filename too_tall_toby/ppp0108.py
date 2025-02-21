from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0108(TooTallToby):
    """Too Tall Toby Party Pack 01-08 Tie Plate
    """

    def __init__(self):
        with BuildPart() as p:
            with BuildSketch():
                Rectangle(188-33*2, 162)
                Rectangle(188, 190-33*2)
                Circle(84/2, mode=Mode.SUBTRACT)
                with GridLocations(188-33*2, 190-33*2, 2, 2):
                    Circle(33)
                    Circle(29/2, mode=Mode.SUBTRACT)
            extrude(amount=16)

            with BuildSketch(Plane.XZ.move(Location((222/2+14, 0, -35+16)))):
                Rectangle(40, 30, align=(Align.MAX, Align.MIN))
                with Locations((-14, 14)):
                    Circle(11/2, mode=Mode.SUBTRACT)
            e2 = extrude(amount=20/2, both=True)

            with BuildSketch(Plane.XZ.move(Location((222/2+14-40, 0, -35+16)))):
                Triangle(a=40, c=35-16, B=90, align=(Align.MIN, Align.MAX), rotation=180)
            e3 = extrude(amount=8/2, both=True)

            mirror([e2, e3], Plane.YZ)

        super().__init__(part=p.part, id="Party Pack 01-08", name="Tie Plate", ref_mass=3387.06, density=Density.ST)


if __name__ == "__main__":
    t = TPPP0108()
    t.show_properties()
    show(t)