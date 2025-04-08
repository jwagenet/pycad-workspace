from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T240104(TooTallToby):
    """Too Tall Toby 24-01-04 Clamp Base
    """

    def __init__(self):
        with BuildPart() as part:
            Box(98, 18, 32, align=(Align.MAX, Align.CENTER, Align.MAX))
            Cylinder(18/2, 98-14+25, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0, -90, 0))
            with Locations((-16, 0, 18/2)):
                Box(98-14-16, 18, 18/2+32-16, align=(Align.MAX, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

            with Locations(((-98+14), 0, 0)):
                Cylinder(8/2, 25, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0, -90, 0), mode=Mode.SUBTRACT)

            e = part.edges().filter_by(Axis.Y).group_by(Axis.Z)
            fillet(e[0], 20)
            fillet(e[1], 7)

        super().__init__(part=part.part, id="24-01-04", name="Clamp Base", ref_mass=308.192, density=Density.ST)


if __name__ == "__main__":
    t = T240104()
    print(t.volume * t.density)
    t.show_properties()
    show(t)