from math import sqrt, tan, radians

from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0107(TooTallToby):
    """Too Tall Toby Party Pack 01-07 Flanged Hub

    Requires workaround for fillet connecting plane to cylinder where plane is width of cylinder diameter
    """

    def __init__(self):
        workplane = Plane((84/2-8, 0, 25), x_dir=(0,-1,0), z_dir=(0,0,1)).rotated((0,-45,0))
        with BuildPart() as rib:
            with BuildSketch(workplane):
                h = (84-35)/2 * sqrt(2)
                with BuildLine():
                    Polyline((0,0), (3/2, 0), (h/2 * tan(radians(10)), -h/2), (0, -h/2))
                    mirror(about=Plane.YZ)
                make_face()
            extrude(amount=h)

        with BuildPart() as p:
            Cylinder(130/2, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(84/2, 25, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(35/2, 52, align=(Align.CENTER, Align.CENTER, Align.MIN))

            with PolarLocations(0, 3):
                add(rib.part)

            Cylinder(20/2, 52, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            Cylinder(73/2, 18, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

            fillet(p.faces().filter_by(Plane.XY).sort_by(Axis.Z)[1:4].edges().filter_by(GeomType.CIRCLE), 3)

            with Locations(Plane.XY.offset(8)):
                with PolarLocations(107.95/2, 6):
                    CounterBoreHole(6/2, 13/2, 4)

        super().__init__(part=p.part, id="Party Pack 01-07", name="Flanged Hub", ref_mass=372.99, density=Density.AL)


if __name__ == "__main__":
    t = TPPP0107()
    t.show_properties()
    show(t)