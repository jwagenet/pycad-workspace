from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS


with BuildPart() as ppp0106:
    with BuildSketch() as s1:
        with Locations((69-30/2-10, 0)):
            t = Triangle(a=44, B=45, C=45, align=(Align.CENTER, Align.MIN), rotation=90)
            offset(t, 10)

        Rectangle(69-30/2, 30, align=(Align.MIN, Align.CENTER))

        with Locations((69-30/2-10, 44/2)):
            c = Circle(13/2, mode=Mode.SUBTRACT)
        mirror(c, about=Plane.XZ, mode=Mode.SUBTRACT)

        fillet(s1.vertices().sort_by(Axis.X)[2:4], 12)

    extrude(amount=22)

    Cylinder(30/2, 36, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0, 0, 180))
    Cylinder(12/2, 36, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
    Box(15-12/2, 4, 36, align=(Align.MIN, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    with Locations((69-30/2, 0, 6)):
        Box(42, 44+10*2, 10, align=(Align.MAX, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # fillet workaround
    with Locations((0, 30/2, 0)) as l1:
        b = Box(30/2, 7, 22 , align=Align.MIN)
    mirror(b, about=Plane.XZ)

    e2 = ppp0106.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.X)[:5].sort_by(Axis.Z)[-2]
    fillet(e2, 6)

    with l1:
        bs = Box(30/2, 7, 36, align=Align.MIN, mode=Mode.SUBTRACT)
    mirror(bs, about=Plane.XZ, mode=Mode.SUBTRACT)


show(ppp0106)
print(f"\npart mass = {ppp0106.part.volume*densa:0.2f}")
print(f"ref mass = 328.02")
