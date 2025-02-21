from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart() as ppp0104:
    Box(80 - 38/2, 38, 7, align=(Align.MIN, Align.CENTER, Align.MIN))
    Cylinder(38/2, 7+21-8, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(0, 0, 180))
    Cylinder(26/2, 7+21, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(16/2, 7+21, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    with Locations((80 - 38/2, 0, 0)):
        Box(10, 38, 30 - 7, align=(Align.MAX, Align.CENTER, Align.MAX))

    e1 = ppp0104.faces().filter_by(Axis.X).sort_by(Axis.X)[-2].edges().sort_by(Axis.Z)[-1]

    with BuildSketch(Plane((80 - 38/2, 0, 17-9-30+7), x_dir=(0, 1, 0), z_dir=(1, 0, 0))) as s1:
        Circle(12/2)
        Rectangle(12, 17-9, align=(Align.CENTER, Align.MAX))

    extrude(amount=-10, mode=Mode.SUBTRACT)
    extrude(offset(s1.sketch, amount=3), amount=-5, mode=Mode.SUBTRACT)


    fillet(e1, 5)
    fillet(ppp0104.edges().sort_by(Axis.X)[-4:].sort_by(Axis.Z)[-1], 10)

    # fillet workaround
    with Locations((0, 38/2, 0)) as l1:
        b = Box(38/2, 5, 7, align=Align.MIN)
    mirror(b, about=Plane.XZ)

    e2 = ppp0104.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-5]
    fillet(e2, 4)

    with l1:
        bs = Box(38/2, 5, 12, align=Align.MIN, mode=Mode.SUBTRACT)
    mirror(bs, about=Plane.XZ, mode=Mode.SUBTRACT)


show(ppp0104)
print(f"\npart mass = {ppp0104.part.volume*densa:0.2f}")
print(f"ref mass = 310.00")
