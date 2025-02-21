from math import radians, tan

from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

sheet_t = 4
sheet_r = 4
outer_r = sheet_r + sheet_t
with BuildPart() as p:
    with BuildLine(Plane.XZ) as l1:
        FilletPolyline((0, 0), (170/2, 0), (170/2 + 65/tan(radians(60)), -65), (170/2, -65), radius=outer_r)

    # can the vertices be sorted along the line?
    widths = [80/2, 80/2, 80/2, 80/2 + 53*tan(radians(26/2)), 80/2 + 65*tan(radians(26/2)), 80/2 + 65*tan(radians(26/2))]
    make_brake_formed(
        thickness=sheet_t,
        station_widths=widths,
        side=Side.RIGHT,
    )
    e1 = p.faces().sort_by(Axis.Y)[-1].edges().sort_by(Axis.X)[0]
    fillet(e1, 7)

    with BuildSketch():
        s1 = SlotCenterPoint((170/2 + 65/tan(radians(60)), 0), (206/2, 0), height=10*2)
        s2 = SlotCenterPoint((170/2 + 65/tan(radians(60)), 0), (154/2, 0), height=10*2)
        with BuildLine():
            l2 = Polyline((40/2, 30/2), (40/2, 0), (40/2 + 30, 0))
            FilletPolyline(l2 @ 0, (40/2 + 30, 30/2), l2 @ 1, radius=7)
        s3 = make_face()

    extrude(s1, amount=-65, mode=Mode.SUBTRACT)
    extrude(s2, amount=-65+sheet_t, mode=Mode.SUBTRACT)
    extrude(s3, amount=-sheet_t, mode=Mode.SUBTRACT)

    with BuildLine(Plane.XZ) as l2:
        FilletPolyline((40/2 -1, -sheet_t), (56/2, -sheet_t), (56/2, 88-65), radius=outer_r)
    make_brake_formed(
        line=l2.line,
        thickness=sheet_t,
        station_widths=-(30/2-2),
        side=Side.RIGHT,
    )

    with BuildSketch(Plane.YZ) as s1:
        with Locations((0, 80-65)):
            Circle(10/2)
    extrude(s1.sketch, amount=40/2+30, mode=Mode.SUBTRACT)

    e2 = p.faces().sort_by(Axis.Z)[-1].edges().sort_by(Axis.Y)[-1]
    fillet(e2, 5)

    with BuildLine(Plane.YZ) as l3:
        l4 = Line((80/2 - 1, 0), (80/2 + outer_r, 0))
        PolarLine(l4 @ 1, 15 + outer_r, -75)
        fillet(l3.vertices().sort_by(Axis.Y)[1], outer_r)

    p1 = make_brake_formed(
        line=l3.line,
        thickness=sheet_t,
        station_widths=110/2,
        side=Side.RIGHT,
    )
    e3 = p1.faces().sort_by(Axis.Z)[0].edges().sort_by(Axis.X)[-1]
    fillet(e3, 7)

    mirror()
    mirror(about=Plane.YZ)


show(p)
print(f"\npart mass = {p.part.volume*densa:0.2f}")
print(f"ref mass = 1028")
