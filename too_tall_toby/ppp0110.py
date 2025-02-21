"""
Too Tall Toby Party Pack 01-10 Light Cap
"""
from build123d import *
from ocp_vscode import set_port, show, show_object
set_port(3939)

densa = 7800 / 1e6  # carbon steel density g/mm^3
densb = 2700 / 1e6  # aluminum alloy
densc = 1020 / 1e6  # ABS

with BuildPart() as ppp0110:
    with BuildSketch(Plane.YZ) as s:
        with BuildLine() as l:
            JernArc((0, 0), (1, 0), 40, 90)
            Line((0, 46), (42, 46))
        make_hull()

    with BuildSketch(Plane.YZ) as s2:
        arc = s.edges().sort_by(Axis.Y)[:-1].sort_by(Axis.X)[1:]
        make_face(offset(arc, amount=8, side=Side.LEFT))
        Rectangle(46, 16, align=Align.MIN)
        add(s, mode=Mode.INTERSECT)

        # This fails but it should work
        # v = s2.edges().filter_by(Axis.X).sort_by(Axis.X)[0].vertices().sort_by(Axis.X)[-1]
        # fillet(v, 8)

    if True:
        # Workaround
        extrude(s2.sketch, amount=100)
        ex = fillet(ppp0110.faces().filter_by(Plane.XY).sort_by(Axis.Y)[0].edges().sort_by(Axis.Y)[-1], 8)
        mirror(about=Plane.XZ)
        rev = revolve(ex.faces().sort_by(Axis.X)[0], axis=Axis.Z, revolution_arc=180)
        mirror(rev, about=Plane.YZ.offset(100 / 2))

    else:
        # This fails but it should work
        extrude(s2.sketch, amount=100 / 2)
        # fillet(ppp0110.faces().filter_by(Plane.XY).sort_by(Axis.Y)[0].edges().sort_by(Axis.Y)[-1], 8)
        revolve(ppp0110.faces().sort_by(Axis.X)[0], axis=Axis.Z, revolution_arc=90)
        mirror(about=Plane.YZ.offset(100 / 2))
        mirror(about=Plane.XZ)


show(ppp0110)
print(f"\npart mass = {ppp0110.part.volume*densc:0.2f}")
print(f"ref mass = 211.30")