# for NickeaTea

from build123d import *
from ocp_vscode import *

offsets = [0, .1, .2, -.1, 0]
plane = Plane.XY
with BuildLine(plane):
    l1 = Polyline((2, 2), (2, 1.5), (1, .5), (2, 0), (4, 0), (3, 1.5))

    new_edges = []
    intersections = []
    for i, e in enumerate(l1.edges()):
        center = e.center()
        direction = (e @ 1 - center)
        line = Line(center + direction * 2 , center - direction * 2)
        perp = direction.cross(plane.z_dir).normalized()
        new_edges.append(line.move(Location(offsets[i] * perp)))
        if i > 0:
            intersections.append(new_edges[-1].intersect(new_edges[-2]))

    print(intersections)

    l2 = Polyline(l1 @ 0, intersections, l1 @ 1)












show(l1, l2, new_edges, position=(2,0,1), target=(2,0,0), up="Y")