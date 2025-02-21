import copy
import math

from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


def chair():
    frame_dia = 24
    frame_r = 70
    frame_w = 450
    frame_base_d = 465
    frame_h = 400
    frame_seat = 430
    frame_rise = 200
    frame_kick = 150
    frame_a = math.radians(5)

    with BuildPart() as frame:
        with BuildLine() as frame_path:
            path = [Vertex(0, 0, 0)]
            path.append(copy.copy(path[-1]) + Vertex(0, frame_w/2, 0))
            path.append(copy.copy(path[-1]) + Vertex(frame_base_d, 0, 0))
            path.append(copy.copy(path[-1]) + Vertex(0, 0, frame_h))
            path.append(copy.copy(path[-1]) + Vertex(-frame_seat, 0, 0))
            path.append(copy.copy(path[-1]) + Vertex(0, 0, frame_rise))
            path.append(copy.copy(path[-1]) + Vertex(-frame_kick * math.sin(frame_a), 0, frame_kick * math.cos(frame_a)))

            FilletPolyline(path, radius=frame_r)
            mirror(about=Plane.XZ)

        with BuildSketch(Plane.XZ) as section:
            Circle(frame_dia/2)

        sweep(section.sketch, frame_path)


    seat_w = frame_w + frame_dia
    seat_d = 400
    seat_f = 70
    seat_t = 30
    strip_t = 10
    seat_sag = 25

    with BuildPart() as seat:
        with BuildSketch() as base:
            Rectangle(seat_d - seat_sag, seat_w)

            with BuildLine() as arc:
                points = base.vertices().sort_by(Axis.X)[:2].sort_by(Axis.Y)
                points = [p.to_tuple() for p in points]
                print(points)
                SagittaArc(points[0], points[1], seat_sag)

            make_hull()
            fillet(base.vertices().sort_by(Axis.X)[:2], seat_f)

            with BuildLine():
                o = offset(base.edges(), -strip_t)

            make_face(mode=Mode.SUBTRACT)

            ref_point = base.vertices().sort_by(Axis.X)[-2:].sort_by(Axis.Y)[0]

        extrude(amount=seat_t)

        ref_line = seat.faces().sort_by(Axis.Z)[-1].edges().filter_by(Axis.X).sort_by(Axis.Y)[0]
        show_object(seat.faces().sort_by(Axis.Z)[-1].edges().filter_by(Axis.X).sort_by(Axis.Y)[0])

        angle = math.radians(80)
        length = seat_t * .8

        with BuildSketch(Plane(ref_point, x_dir=(1, 0, 0), z_dir=(0, -1, 0))):
            points = [Vertex(0, seat_t, 0), Vertex(0, 0, 0)]
            points.append(copy.copy(points[-1]) + Vertex(25, 0, 0))
            points.append(copy.copy(points[-1]) + Vertex(math.cos(angle) * length, math.sin(angle) * length, 0))

            with BuildLine() as profile:
                Polyline(points)
                TangentArc(points[0], points[-1], tangent=ref_line.tangent_at())

            show_object(profile)
            f = make_face()

            show_object(f)

        extrude(amount=-seat_w)

    show_object(seat)





def stool():
    """Stool based on IKEA KYRRE with approximate dimensions in mm"""

    ## Parameters
    n_legs = 3

    seat_r = 200
    seat_t = 20
    corner_r = 80
    arc_r = 300
    top_f = 3

    leg_t = 20
    leg_start_w = 43
    leg_end_w = 25

    leg_rad = 55
    leg_seg_1 = 120 + leg_rad
    leg_seg_2 = 360 + leg_rad
    leg_angle = math.radians(80)

    center_dist = 30
    cbore_pos = [25, 116]
    pin_pos = 68


    ## Seat
    with BuildPart() as seat:
        with BuildSketch() as profile:
            RegularPolygon(seat_r, n_legs)
            v = profile.vertices()
            v = sorted(v, key=lambda k: -math.atan2(k.Y, k.X))
            v.append(v[0])

            with BuildLine() as line:
                for i in range(len(v)-1):
                    RadiusArc(v[i].to_tuple(), v[i + 1].to_tuple(), arc_r)

            make_face(mode=Mode.REPLACE)

        extrude(profile.sketch, seat_t)

        with Locations(Plane(seat.faces().filter_by(Axis.Z)[0], x_dir=(1, 0, 0))):
            for pos in cbore_pos:
                with PolarLocations(center_dist + pos, n_legs):
                    Hole(6/2, seat_t + leg_t - 33 + 3 + 1 )

        fillet(seat.edges().filter_by(Axis.Z), corner_r)
        fillet(seat.faces().sort_by(Axis.Z)[-1].edges(), top_f)


    ## Leg
    wire_pts = [(0,0)]
    wire_pts.append((leg_seg_1, 0))
    wire_pts.append((wire_pts[-1][0] - math.cos(leg_angle) * (leg_seg_2),
                     wire_pts[-1][1] + math.sin(leg_angle) * (leg_seg_2)))

    with BuildPart() as leg:
        with BuildLine() as wire:
            FilletPolyline(wire_pts, radius=leg_rad)

        with BuildSketch(wire.line ^ 0) as start:
            Rectangle(leg_start_w, leg_t)

        with BuildSketch(wire.line ^ 0.35) as mid:
            Rectangle(leg_t, leg_start_w)

        with BuildSketch(wire.line ^ 1) as end:
            Rectangle(leg_t, leg_end_w)

        sweep(leg.pending_faces, wire, multisection=True)

        locs = [(x, 0 ,0) for x in cbore_pos]
        point = leg.faces().sort_by(Axis.X)[0].edges().sort_by(Axis.Y)[0].center()
        with Locations(Plane(point, x_dir=(1, 0, 0), z_dir=(0, -1, 0))):
            with Locations((pin_pos, 0, 0)):
                Hole(8/2)

            with Locations(locs):
                CounterBoreHole(8/2, 16/2, 3)

        temp_edges = leg.edges().sort_by(Axis.X).filter_by(lambda e: e.length == leg_end_w)
        chamfer(temp_edges[0], 1)
        chamfer(temp_edges[-1], 2)

        temp_edges = leg.edges().sort_by(Axis.X).sort_by(Axis.Y).filter_by(lambda e: e.length == leg_start_w)
        chamfer(temp_edges[0], 5, leg_t - .01)

    ## Screw
    maj_d = 7
    min_d = 5
    length = 33
    head_d = 15
    head_h = 3
    socket_d = 4

    with BuildPart(Plane.YZ) as screw:
        Cylinder(min_d/2, length, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Plane((0, 0, 3), x_dir=(0, 1, 0), z_dir=(0, 0, 1))):
            threads = Cylinder(maj_d/2, length - 5, align=(Align.CENTER, Align.CENTER, Align.MIN))

        chamfer(threads.edges(), .9999)

        top_face = screw.faces().sort_by(Axis.X)[0]
        with BuildSketch(Plane.XZ) as head:
            with BuildLine() as profile:
                arc = ThreePointArc([(0, head_d/2, 0), (-head_h, 0, 0), (0, -head_d/2, 0)])
                split(arc, Plane.XZ, keep=Keep.BOTTOM)
                Polyline([(-head_h, 0, 0), (0, 0, 0), (0, head_d/2, 0)])

            make_face()

        head = revolve(axis=Axis.X)
        chamfer(top_face.edge(), 1)

        show_object(Plane((-head_h, 0, 0), z_dir=(1, 0, 0)))

        with BuildSketch(Plane((-head_h, 0, 0), z_dir=(1, 0, 0))):
            RegularPolygon(socket_d/2, 6)

        extrude(amount=3, mode=Mode.SUBTRACT)
        fillet(head.edge(), .5)


        show_object(screw)


    ## Assembly
    leg.part.orientation = (90, 0, 0)
    leg.part.position = (center_dist, 0, -leg_t/2)
    children = [seat.part]
    for i in range(n_legs):
        children.append(copy.copy(leg.part).rotate(Axis.Z, i * 360 / n_legs))

    return Compound(label="assembly", children=children)


if __name__ == "__main__":
    chair()
    # show_object(stool())