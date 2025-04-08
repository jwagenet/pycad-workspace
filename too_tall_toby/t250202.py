from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T250202(TooTallToby):
    """Too Tall Toby 25-02-02 Soap Dish Base
    """

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch(Plane.YZ):
                with BuildLine():
                    l1 = FilletPolyline((64/2-16, 0), (64/2, 0), (64/2, 25), radius=12)
                    l2 = FilletPolyline((64/2-16, 4), (64/2-4, 4), (64/2-4, 25-10), radius=12-4)
                    Line(l1 @ 0, l2 @ 0)
                    Polyline(l1 @ 1, l1 @ 1 - Vector(2, 0), l2 @ 1 + Vector(2, 0), l2 @ 1)
                make_face()
            extrude(amount=100/2-16)

            face = part.faces().sort_by(Axis.X)[-1]
            edge = face.edges().sort_by(Axis.Y)[0]
            revolve(face, -Axis(edge), 90)

            e_face = part.faces(Select.LAST).sort_by(Axis.Y)[0]
            extrude(e_face, amount=64/2-12)

            mirror(about=Plane.XZ)
            mirror(about=Plane.YZ)

            with BuildSketch(Plane.XZ.offset(64/2)):
                SlotCenterPoint((100, 6 + 2.5), (100/2-22, 6 + 2.5), 5)
            extrude(amount=-10, mode=Mode.SUBTRACT)

            with BuildSketch(Plane.YZ.offset(100/2)):
                SlotCenterPoint((-64, 6 + 2.5), (-64/2+22, 6 + 2.5), 5)
            extrude(amount=-10, mode=Mode.SUBTRACT)

            with BuildSketch(Plane.YZ):
                with BuildLine():
                    l3 = FilletPolyline((64/2-4, 15), (64/2-4, 4), (-64/2+4, 4), (-64/2+4, 15), radius=12-4)
                    Line(l3 @ 0, l3 @ 1)
                make_face()
            ex = extrude(amount=1, both=True)
            f_edge = ex.faces().group_by(Face.area)[-1].edges().filter_by(lambda e: e.length != 64-8)
            fillet(f_edge, 2)

            with BuildSketch(Plane.YZ):
                with GridLocations(14, 0, 3, 1):
                    with Locations((0, 4)):
                        Circle(5)
                Rectangle(64, 8, mode=Mode.SUBTRACT)
            extrude(amount=3, both=True, mode=Mode.SUBTRACT)

            c_face = part.faces().sort_by(Axis.Z)[-1].edges()
            fillet(c_face, 1-1e-4)

        super().__init__(part=part.part, id="25-02-02", name="Soap Dish Base", ref_mass=103.20, density=Density.AL)


if __name__ == "__main__":
    t = T250202()
    t.show_properties()
    show(t)