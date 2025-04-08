from build123d import *
from ocp_vscode import *

from helpers import Density, TooTallToby


class T250201(TooTallToby):
    """Too Tall Toby 25-02-01 Soap Dish Shelf
    """

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch():
                RectangleRounded(95.2, 59.2, 17.6)
                with GridLocations(17, 17, 5, 3):
                    Circle(13/2, mode=Mode.SUBTRACT)
            extrude(amount=2)

        super().__init__(part=part.part, id="25-02-01", name="Soap Dish Shelf", ref_mass=6.893, density=Density.ABS)


if __name__ == "__main__":
    t = T250201()
    print(t.volume * t.density)
    t.show_properties()
    show(t)