import copy

from build123d import *
from ocp_vscode import show, set_port

from helpers import Density, TooTallToby

set_port(3939)


class TPPP0105(TooTallToby):
    """Too Tall Toby Party Pack 01-05 Paste Sleeve

    loft() does not maintain hollow sketch portions, so two lofts are required
    """

    def __init__(self):
        with BuildPart() as p:
            with BuildSketch() as s1:
                SlotOverall(45, 38)

            with BuildSketch(Plane.XY.offset(amount=133)) as s2:
                SlotOverall(60, 4)

            profiles = [s1.sketch, copy.copy(s1.sketch).translate((0, 0, 30)), s2.sketch]
            loft([offset(s, amount=3) for s in profiles], ruled=True)
            loft(profiles, ruled=True, mode=Mode.SUBTRACT)


        super().__init__(part=p.part, id="Party Pack 01-05", name="Paste Sleeve", ref_mass=57.08, density=Density.ABS)

t = TPPP0105()
show(t)