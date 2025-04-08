from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T24SPO06(TooTallToby):
    """Too Tall Toby 24-SPO-06 Buffer Stand
    """

    def __init__(self):
        with BuildPart() as part:
            plane = Plane.YZ.offset(-5.5/2)
            with BuildSketch(plane):
                t0 = Trapezoid(2.5, 4, 90-6, align=(Align.CENTER, Align.MIN), mode=Mode.PRIVATE)
                _, center, radius = full_round(t0.edges().sort_by(Axis.Y)[-1])

                t1 = Trapezoid(2.5, 4-radius, 90-6, align=(Align.CENTER, Align.MIN))
                t2 = Trapezoid(2.5, .25, 90-6, align=(Align.CENTER, Align.MIN))
                with Locations(center):
                    c = Circle(radius)

            part.pending_faces = []
            part.pending_face_planes = []
            extrude(to_extrude=t1.locate(plane.location), amount=(5.5-4.25)/2)
            extrude(to_extrude=t2.locate(plane.location), amount=5.5/2)
            fillet(part.edges(Select.NEW), .5)

            with BuildSketch(plane):
                with Locations((0, .25)):
                    Trapezoid(.5, 1, 90-16/2, align=(Align.CENTER, Align.MIN))
                full_round(edges().sort_by(Axis.Y)[-1])
            extrude(amount=5.5/2)

            extrude(to_extrude=c.locate(plane.location), amount=(5.5-3.5)/2)

            cbore_face = part.faces(Select.LAST).sort_by(Axis.X)[-1]
            with Locations(Location(cbore_face.center(), cbore_face.orientation)):
                CounterBoreHole(.625/2, 1.25/2, .5)

            with BuildSketch():
                with BuildLine():
                    l1 = Polyline((-5/2, -2.5/2), (-5.5/2, -2.5/2), (-5.5/2, 2.5/2), (-5/2, 2.5/2))
                    ThreePointArc(l1 @ 0, l1 @ .5, l1 @ 1)
                make_face()
                mirror(about=Plane.XZ)
            extrude(amount=4, mode=Mode.SUBTRACT)

            mirror(about=Plane.YZ)
            scale(by=IN)

        super().__init__(part=part.part, id="24-SPO-06", name="Buffer Stand", ref_mass=3.92 / 0.00220462, density=Density.ST)


if __name__ == "__main__":
    t = T24SPO06()
    t.show_properties()
    show(t)