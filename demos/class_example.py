"""Example of a lasercut joint class for elz"""

from build123d import *
from ocp_vscode import *

class ClipJoint(BasePartObject):
    def __init__(self, mode = Mode.ADD):
        if mode == Mode.ADD:
            with BuildPart() as part:
                with BuildSketch():
                    with BuildLine() as line:
                        Polyline((-1, 25), (-1, 0), (-6, 0), (-6, 20), (-9, 20), (-9, 22))
                        RadiusArc(line.wire() @ 1, line.wire() @ 0, 10)
                    make_face()
                    with Locations((-9, 0)):
                        Rectangle(1, 15, align=(Align.MIN, Align.MIN))
                    mirror(about=Plane.YZ)
                extrude(amount=3)

        elif mode == Mode.SUBTRACT:
            with BuildPart() as part:
                Box(18, 25, 3, align=(Align.CENTER, Align.MIN, Align.MIN))

        super().__init__(part.part, mode=mode)


with BuildPart() as part:
    Box(200, 100, 3, align=(Align.CENTER, Align.MIN, Align.MIN))
    with Locations((0, 85)):
        with GridLocations(50, 0, 3, 1):
            ClipJoint(mode=Mode.SUBTRACT)
            ClipJoint(mode=Mode.ADD)

show(part)
