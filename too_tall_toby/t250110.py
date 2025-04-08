from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T250110(TooTallToby):
    """Too Tall Toby 25-01-10 Spool
    """

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch(Plane.YZ):
                with BuildLine() as line:
                    l1 = Line((75/2, 0), (75/2, 45/2))
                    l3 = Line((175/2, 150-45), (175/2, 150-60))
                    Line(l3 @ 0, (0, 150-45))
                    Line(l1 @ 0, (0, 0))
                    Line((0, 150-45), (0, 0))
                    RadiusArc(l1 @ 1, l3 @ 1, 70)

                make_face()
                mirror(about=Plane.YZ)
                with Locations((0, 150-45)):
                    Trapezoid(175, 45, 45, align=(Align.CENTER, Align.MIN))

            extrude(amount=200)

            with BuildSketch(Plane.XZ) as tcut:
                with BuildLine():
                    l4 = Line((70, 150), (120, 150))
                    PolarLine(l4 @ 0, -150, 90 - 10, length_mode=LengthMode.VERTICAL)
                    PolarLine(l4 @ 1, -150, 90 + 5, length_mode=LengthMode.VERTICAL)
                make_hull()
            e = extrude(amount=175/2, both=True, mode=Mode.INTERSECT)

            show_object([part, tcut, e, line])

            with BuildSketch(Plane.XZ):
                with BuildLine():
                    Polyline((0, 45/2), (0, 110/2), (25, 110/2), (25, 75/2), (200-35, 75/2),
                            (200-35, 155/2), (200, 155/2), (200, 45/2), close=True)
                make_face()
            revolve(axis=Axis.X)

            with Locations(Location((0,0,0), (0, 90, 0))):
                Hole(45/2, 200)

        super().__init__(part=part.part, id="25-01-10", name="Spool", ref_mass=5823.97, density=Density.AL)


if __name__ == "__main__":
    t = T250110()
    t.show_properties()
    show(t)