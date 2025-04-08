from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T240101(TooTallToby):
    """Too Tall Toby 24-01-01 Tier 1 Part
    """

    def __init__(self):
        with BuildPart() as part:
            Box(30, 29, 62, align=(Align.MIN, Align.CENTER, Align.MIN))
            Box(65-14.5, 29, 15, align=(Align.MIN, Align.CENTER, Align.MIN))
            with Locations((65-14.5, 0)):
                Cylinder(14.5, 15, align=(Align.CENTER, Align.CENTER, Align.MIN))

        super().__init__(part=part.part, id="24-01-01", name="Tier 1 Part", ref_mass=528.93, density=Density.ST)


if __name__ == "__main__":
    t = T240101()
    t.show_properties()
    show(t)