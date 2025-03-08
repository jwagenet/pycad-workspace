import copy
from build123d import *
from ocp_vscode import show, show_object, set_viewer_config, set_port, set_defaults, get_defaults
set_port(3940)
set_viewer_config(black_edges=False)

from math import pi
from OCP.BRepLib import BRepLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

def map_to_surface(path, surface):
    # pseudo {
    geom_curve = path.edge().geom_adaptor()
    geom_surface = surface.face().geom_adaptor()

    print(geom_curve, geom_surface)
    # geom_surf = cast(surface to Geom_Surface)
    # }

    # reference cylindrical surface
    # center = (0, 0)
    # radius = 10
    # normal = (0, 1)
    # geom_surf: Geom_Surface = Geom_CylindricalSurface(
    #     gp_Ax3(Vector(center).to_pnt(), Vector(normal).to_dir()), radius
    # )

    # 3. Wrap the line around the surface
    edge_builder = BRepBuilderAPI_MakeEdge(geom_curve, geom_surface)
    topods_edge = edge_builder.Edge()

    # 4. Convert the edge made with 2d geometry to 3d
    BRepLib.BuildCurves3d_s(topods_edge, 1e-9, MaxSegment=2000)

    return Edge(topods_edge)


# bottle
# https://dev.opencascade.org/doc/overview/html/occt__tutorial.html
height = 70
width = 50
thick = 30
fillet_r = thick / 12
neck_r = thick / 4
neck_height = height / 10
wall_thick = .9
with BuildPart() as bottle:
    with BuildSketch():
        with BuildLine() as base:
            a1 = ThreePointArc((width / 2, thick / 4), (0, thick / 2), (-width / 2, thick / 4))
            l1 = PolarLine(a1 @ 0, thick / 2, direction=(0, -1))
            mirror(a1, about=Plane.XZ)
            mirror(l1, about=Plane.YZ)
        make_face()
    extrude(amount=height)
    fillet(bottle.edges(), radius=fillet_r)

    with Locations((0, 0, height + neck_height / 2)):
        Cylinder(neck_r, neck_height)

    offset(amount=wall_thick, openings=bottle.faces().sort_by(Axis.Z)[-1])

    point = Vector(2 * pi, neck_height / 2)
    direction = Vector(2 * pi, neck_height / 4)
    plane = Plane(point, direction)

    major_r = 2 * pi
    minor_r = neck_height / 10

    with BuildSketch():
        with BuildLine(plane) as thread:
            e1 = EllipticalCenterArc((0, 0), major_r, minor_r, 0, 180)
            e2 = EllipticalCenterArc((0, 0), major_r, minor_r / 4, 0, 180)
            l1 = Line(e1 @ 0, e1 @ 1)

    s1 = Cylinder(neck_r, neck_height).faces().filter_by(GeomType.CYLINDER)
    p = map_to_surface(e1, s1)
    # no way to wrap line around face natively yet

show(s1, p, bottle)