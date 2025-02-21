from math import radians, tan

from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart() as ppp0101:
    with BuildSketch() as s1:
        Rectangle(115, 50)
        SlotOverall(90, 12, mode=Mode.SUBTRACT)
    extrude(amount=15)

    v = ppp0101.faces().sort_by(Axis.X)[0].vertices().sort_by(Axis.Y)[:2].sort_by(Axis.Z)[0]

    with BuildSketch(Plane.YZ) as s2:
        Trapezoid(18 + 2*8/tan(radians(60)), 8, 60, align=(Align.CENTER, Align.MAX), rotation=180)
    extrude(both=True, until=ppp0101.part, mode=Mode.SUBTRACT)

    with BuildSketch(ppp0101.faces().sort_by(Axis.Y)[0]) as s3:
        with Locations((-115 / 2 + 26, 42 - 15/2)):
            Circle(26)
            Rectangle(26 * 2, 42 - 15, align=(Align.CENTER,Align.MAX))
    s3 = extrude(amount=-12)

    face = ppp0101.faces().sort_by(Axis.Y)[0]
    center = face.edges().filter_by(GeomType.CIRCLE).edge().arc_center
    with Locations(center):
        with Locations(Plane.XZ):
            cbore = CounterBoreHole(24/2, 34/2, 4)

    f = fillet(s3.faces().sort_by(Axis.X)[-1].edges().sort_by(Axis.Z)[0], 9)

    mirror(s3, about=Plane.XZ)
    mirror(f, about=Plane.XZ)
    mirror(cbore, about=Plane.XZ, mode=Mode.SUBTRACT)

    fillet(ppp0101.edges().filter_by(Axis.Z).filter_by(lambda e: e.length == 15), 6)
    # fillet(ppp0101.edges().filter_by(Axis.Z).filter_by(lambda e:e.length == 42), 6)

    # workaround to stop fillet following tangent edges
    with BuildSketch(Plane(v)) as s4:
        with BuildLine():
            l = Polyline((0, 6), (0, 0), (6, 0))
            RadiusArc((l @ 1), (l @ 0), radius=6)
        make_face()
    f = extrude(amount=42 + 26, mode=Mode.SUBTRACT)
    mirror(f, mode=Mode.SUBTRACT)


show(ppp0101)
print(f"\npart mass = {ppp0101.part.volume*densa:0.2f}")
print(f"ref mass = 797.15")