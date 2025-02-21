"""
Too Tall Toby Party Pack 01-08 Tie Plate
"""

from build123d import *
from ocp_vscode import *

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart() as ppp0108:
    with BuildSketch() as s1:
        Rectangle(188-33*2, 162)
        Rectangle(188, 190-33*2)
        Circle(84/2, mode=Mode.SUBTRACT)
        with GridLocations(188-33*2, 190-33*2, 2, 2):
            Circle(33)
            Circle(29/2, mode=Mode.SUBTRACT)
    extrude(amount=16)

    with BuildSketch(Plane.XZ.move(Location((222/2+14, 0, -35+16)))) as s2:
        Rectangle(40, 30, align=(Align.MAX, Align.MIN))
        with Locations((-14, 14)):
            Circle(11/2, mode=Mode.SUBTRACT)
    e2 = extrude(amount=20/2, both=True)

    with BuildSketch(Plane.XZ.move(Location((222/2+14-40, 0, -35+16)))) as s3:
        Triangle(a=40, c=35-16, B=90, align=(Align.MIN, Align.MAX), rotation=180)
    e3 = extrude(amount=8/2, both=True)

    mirror([e2,e3], Plane.YZ)

show(ppp0108)
print(f"\npart mass = {ppp0108.part.volume*densa:0.2f}")
print(f"ref mass = 3387.06")