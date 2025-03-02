"""Two ways of constructing a sketch profile to revolve for @x10510n

It can be cumbersome to produce a 2D sketch profile with lines, although this might be a natural way
to do it in MCAD. An alternative is to cosntruct the profile with 2D sketch objects. In this case
A hull from a line is still used since the relief is more easily defined by an arc with endpoints 
rather than finding a centerpoint for the circle."""

from build123d import *

with BuildPart() as with_lines:
    with BuildSketch(Plane.XZ) as profile:
        with BuildLine() as outline:
            l1 = Polyline((15, 0), (0, 0), (0, 10), (4.5, 10))
            l2 = JernArc(l1 @ 1, l1 % 1, 1.5, -90)
            l3 = Line(l2 @ 1, l2 @ 1 - (0, 1))
            l4 = ThreePointArc(l3 @ 1, l3 @ 1 - (0.75, 1.125), l3 @ 1 - (0, 2.5))
            l5 = Line(l4 @ 1, l4 @ 1 + (4.0, 0))
            l6 = JernArc(l5 @ 1, l5 % 1, 5, -90)
        make_face()
    revolve()


with BuildPart() as with_sketch:
    with BuildSketch(Plane.XZ) as profile:
        Rectangle(6, 10, align=Align.MIN)
        fillet(profile.edges().sort_by(Axis.X)[-1].vertices().sort_by(Axis.Y)[-1], 1.5)
        with BuildLine(Plane((6, 5))):
            a = ThreePointArc((0, 0), (-0.75, 1.125), (0, 2.5))
        make_hull(edges=a, mode=Mode.SUBTRACT)
        Rectangle(15, 5, align=Align.MIN)
        fillet(profile.edges().sort_by(Axis.X)[-1].vertices().sort_by(Axis.Y)[-1], 5)
    revolve()