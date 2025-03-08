from math import acos, atan2, degrees

from build123d import *
from ocp_vscode import show, show_object, set_viewer_config, set_port, set_defaults, get_defaults
set_port(3939)


class ArcTangentLine(BaseLineObject):
    """Line Object: Arc Point Tangent Line

    Create a line tangent to arc to point

    Args:
        start_arc (Curve | Edge | Wire): arc, must be GeomType.CIRCLE
        target (VectorLike): target point for tangent
        side (Side, optional): side of arcs to place tangent arc center, LEFT or RIGHT. Defaults to Side.LEFT
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(
        self,
        arc: Curve | Edge | Wire,
        angle: float,
        other: Curve | Edge | Wire = None,
        length: float = None,
        side: Side = Side.LEFT,
        mode=Mode.ADD,
        ):

        side_sign = {
            Side.LEFT: 1,
            Side.RIGHT: -1,
        }

        center = arc.arc_center
        radius = arc.radius

        intersect = PolarLine(center, radius, angle)
        normal = Vector((intersect @ 1).Y, -(intersect @ 1).X)

        if other is not None:
            tangent = IntersectingLine(intersect @ 1, direction=normal, other=other)

        elif length is not None:
            tangent = PolarLine(intersect @ 1, length, direction=side_sign[side] * -normal)

        else:
            raise ValueError("Need either other or a length to find tangent.")

        show_object(tangent)

        wire = Wire(tangent)
        super().__init__(wire, mode)

c1 = CenterArc((0, 0), 3, 0, 360)

target = Line((-6, 6), (6,6))
wire = ArcTangentLine(c1, 30, other=target)
print(wire.length)
show(c1, target, wire, position=(0,0,1), target=(0,0,0))


class ArcPointTangentLine(BaseLineObject):
    """Line Object: Arc Point Tangent Line

    Create a line tangent to arc to point

    Args:
        start_arc (Curve | Edge | Wire): arc, must be GeomType.CIRCLE
        target (VectorLike): target point for tangent
        side (Side, optional): side of arcs to place tangent arc center, LEFT or RIGHT. Defaults to Side.LEFT
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(
        self,
        arc: Curve | Edge | Wire,
        target: VectorLike,
        side=Side.LEFT,
        mode=Mode.ADD,
        ):

        side_sign = {
            Side.LEFT: 1,
            Side.RIGHT: -1,
        }

        points = [arc.arc_center, Vector(target)]
        radius = arc.radius
        midline = points[1] - points[0]

        if midline.length < radius:
            raise ValueError("Cannot find tangent for point inside arc.")

        phi = degrees(atan2(midline.Y, midline.X))
        theta = degrees(acos((radius) / midline.length))
        angle = side_sign[side] * theta + phi
        intersect = PolarLine(points[0], radius, angle)
        tangent = Line(intersect @ 1, points[1])

        wire = Wire(tangent)
        super().__init__(wire, mode)


class DoubleArcTangentLine(BaseLineObject):
    """Line Object: Double Arc Tangent Line

    Create a line tangent to supplied arcs

    Args:
        start_arc (Curve | Edge | Wire): starting arc, must be GeomType.CIRCLE
        end_arc (Curve | Edge | Wire): ending arc, must be GeomType.CIRCLE
        side (Side): side of arcs to place tangent arc center, LEFT or RIGHT. Defaults to Side.LEFT
        keep (Keep): which tangent arc to keep, INSIDE, OUTSIDE, or BOTH. Defaults to Keep.INSIDE
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(
        self,
        start_arc: Curve | Edge | Wire,
        end_arc: Curve | Edge | Wire,
        side=Side.LEFT,
        keep=Keep.INSIDE,
        mode=Mode.ADD,
        ):

        side_sign = {
            Side.LEFT: 1,
            Side.RIGHT: -1,
        }

        keep_sign = {
            Keep.INSIDE: [1],
            Keep.OUTSIDE: [-1],
            Keep.BOTH: [1, -1],
        }

        arcs = [start_arc, end_arc]
        points = [arc.arc_center for arc in arcs]
        radii = [arc.radius for arc in arcs]
        midline = points[1] - points[0]

        if midline.length == 0:
            raise ValueError("Cannot find tangent for concentric arcs.")

        if (keep == Keep.INSIDE or keep == Keep.BOTH):
            if midline.length < sum(radii):
                raise ValueError("Cannot find INSIDE tangent for overlapping arcs.")

            if midline.length == sum(radii):
                raise ValueError("Cannot find INSIDE tangent for tangent arcs.")

        # Method:
        # https://en.wikipedia.org/wiki/Tangent_lines_to_circles#Tangent_lines_to_two_circles
        # - angle to point on circle of tangent incidence is theta + phi
        # - phi is angle between x axis and midline
        # - OUTSIDE theta is angle formed by triangle legs (midline.length) and (r0 - r1)
        # - INSIDE theta is angle formed by triangle legs (midline.length) and (r0 + r1)
        # - INSIDE theta for arc1 is 180 from theta for arc0

        phi = degrees(atan2(midline.Y, midline.X))
        tangent = []
        for sign in keep_sign[keep]:
            if sign == keep_sign[Keep.OUTSIDE][0]:
                theta = degrees(acos((radii[0] - radii[1]) / midline.length))
                angle = side_sign[side] * theta + phi
                intersect = [PolarLine(points[i], radii[i], angle) for i in [0, 1]]

            elif sign == keep_sign[Keep.INSIDE][0]:
                theta = degrees(acos((radii[0] + radii[1]) / midline.length))
                angle = side_sign[side] * theta + phi
                intersect = [PolarLine(points[i], radii[i], i * 180 + angle) for i in [0, 1]]

            tangent.append(Line(intersect[0] @ 1, intersect[1] @ 1))

        wire = Wire(tangent)
        super().__init__(wire, mode)


class DoubleArcTangentArc(BaseLineObject):
    """Line Object: Double Arc Tangent Arc

    Create an arc tangent to supplied arcs

    Args:
        start_arc (Curve | Edge | Wire): starting arc, must be GeomType.CIRCLE
        end_arc (Curve | Edge | Wire): ending arc, must be GeomType.CIRCLE
        radius (float): radius of tangent arc
        side (Side): side of arcs to place tangent arc center, LEFT or RIGHT. Defaults to Side.LEFT
        keep (Keep): which tangent arc to keep, INSIDE, OUTSIDE, or BOTH. Defaults to Keep.INSIDE
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(
        self,
        start_arc: Curve | Edge | Wire,
        end_arc: Curve | Edge | Wire,
        radius: float,
        side=Side.LEFT,
        keep=Keep.INSIDE,
        mode=Mode.ADD,
        ):

        side_sign = {
            Side.LEFT: 1,
            Side.RIGHT: -1,
        }

        keep_sign = {
            Keep.INSIDE: [1],
            Keep.OUTSIDE: [-1],
            Keep.BOTH: [1, -1],
        }

        arcs = [start_arc, end_arc]
        points = [arc.arc_center for arc in arcs]
        radii = [arc.radius for arc in arcs]

        # make a normal vector for sorting intersections
        midline = points[1] - points[0]
        normal = side_sign[side] * Vector(midline.Y, -midline.X)

        arc = []
        for sign in keep_sign[keep]:
            net_radius = radius + sign * (radii[0] + radii[1]) / 2

            # allow errors to fall through with Keep.BOTH to handle later
            if keep != Keep.BOTH:
                # technically the range midline.length / 2 < radius < math.inf should be valid
                if net_radius <= midline.length / 2:
                    raise ValueError(f"The arc radius is too small. Should be greater than {(midline.length - sign * (radii[0] + radii[1])) / 2} (and probably larger).")

                # current intersection method doesn't work out to expected range and may return 0
                # workaround to catch error midline.length / net_radius needs to be less than 1.888 or greater than .666 from testing
                max_ratio = 1.888
                min_ratio = .666
                if midline.length / net_radius > max_ratio:
                    raise ValueError(f"The arc radius is too small. Should be greater than {midline.length / max_ratio - sign * (radii[0] + radii[1]) / 2}.")

                if midline.length / net_radius < min_ratio:
                    raise ValueError(f"The arc radius is too large. Should be less than {midline.length / min_ratio - sign * (radii[0] + radii[1]) / 2}.")

            # Method:
            # https://www.youtube.com/watch?v=-STj2SSv6TU
            # - solves geometrically rather than algebraically
            # - the centerpoint of the inner arc is found by the intersection of the
            #   arcs made by adding the inner radius to the point radii
            # - the centerpoint of the outer arc is found by the intersection of the
            #   arcs made by subtracting the outer radius from the point radii
            # - then it's a matter of finding the points where the connecting lines
            #   intersect the point circles
            ref_arcs = [CenterArc(points[i], sign * radii[i] + radius, start_angle=0, arc_size=360) for i in [0, 1]]
            ref_intersections = ref_arcs[0].edge().intersect(ref_arcs[1].edge())

            try:
                arc_center = ref_intersections.sort_by(Axis(points[0], normal))[0]
            except AttributeError as exception:
                if keep == Keep.BOTH:
                    continue
                else:
                    raise exception

            intersect = [IntersectingLine(points[i], sign * (Vector(arc_center) - Vector(points[i])), arcs[i]) for i in [0, 1]]
            intersect_points = [intersect[0] @ 1, intersect[1] @ 1]

            if side == Side.LEFT:
                intersect_points.reverse()

            arc.append(RadiusArc(*intersect_points, radius=radius))

        if keep == Keep.BOTH and not arc:
            # no intersections were found for Keep.BOTH after other checks ignored
            raise ValueError("Unable to find any sides to keep with radius. Try Keep.INSIDE or Keep.OUTSIDE for more detailed information.")

        wire = Wire(arc)
        super().__init__(wire, mode)


class AubergineSlot(BaseSketchObject):
    """Sketch Object: Aubergine Slot

    Add a curved slot of varying width defined by center length, and start, end, inner, and outer radii.

    Args:
        float (float): center spacing of slot
        start_radius (float): radius of start circle
        end_radius (float): radius of end circle
        inner_radius (float): radius of inner arc
        outer_radius (float): radius of outer arc
        side (Side): side of slot to place arc centers. Defaults to Side.LEFT
        rotation (float, optional): angles to rotate objects. Defaults to 0.
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(self,
                 length,
                 start_radius,
                 end_radius,
                 inner_radius,
                 outer_radius,
                 side = Side.LEFT,
                 rotation = 0,
                 mode = Mode.ADD):

        start_point = Vector(0, 0)
        end_point = Vector(length, 0)

        center_side = 1
        if side == Side.RIGHT:
            center_side = -1

        with BuildSketch() as sketch:
            with BuildLine():
                with BuildLine(mode=Mode.PRIVATE):
                    # The normal could be Axis.Y if end_point.Y is 0
                    # originally end_point could be an arbitrary point
                    # keeping for now
                    midline = Line(start_point, end_point)
                    normal = center_side * Vector(end_point.Y, -end_point.X)

                    # Method:
                    # - the centerpoint of the inner arc is found by the intersection of the
                    #   arcs made by adding the inner radius to the point radii
                    # - the centerpoint of the outer arc is found by the intersection of the
                    #   arcs made by subtracting the outer radius from the point radii
                    # then its a matter of finding the points where the connecting lines
                    # intersect the point circles

                    c1 = CenterArc(start_point, start_radius, start_angle=0, arc_size=360)
                    c13 = CenterArc(start_point, start_radius + inner_radius, start_angle=0, arc_size=360)
                    c14 = CenterArc(start_point, outer_radius - start_radius, start_angle=0, arc_size=360)
                    c2 = CenterArc(end_point, end_radius, start_angle=0, arc_size=360)
                    c23 = CenterArc(end_point, end_radius + inner_radius, start_angle=0, arc_size=360)
                    c24 = CenterArc(end_point, outer_radius - end_radius, start_angle=0, arc_size=360)

                    # perform checks on validity of inner and outer radii
                    inner_radius_length = inner_radius + (start_radius + end_radius) / 2
                    outer_radius_length = outer_radius - (start_radius + end_radius) / 2

                    if inner_radius_length <= midline.length / 2:
                        raise ValueError(f"The inner arc radius is too small. Should be greater than {(midline.length - (start_radius + end_radius)) / 2} (and probably larger).")

                    if outer_radius_length <= midline.length / 2:
                        raise ValueError(f"The outer arc radius is too small. Should be greater than {(midline.length + (start_radius + end_radius)) / 2} (and probably larger).")

                    # xs* can have no intersections as some small amount
                    # can also only have 1 vertex
                    # workaround to catch error center_spacing / average radius needs to be less than 1.888 or greater than .66 from testing
                    max_ratio = 1.888
                    min_ratio = .666

                    if midline.length / inner_radius_length < min_ratio:
                        raise ValueError(f"The inner arc radius is too large. Should be less than {(midline.length / min_ratio - (start_radius + end_radius) / 2)}.")

                    if midline.length / inner_radius_length > max_ratio:
                        raise ValueError(f"The inner arc radius is too small. Should be greater than {(midline.length / max_ratio - (start_radius + end_radius) / 2)}.")

                    if midline.length / outer_radius_length < min_ratio:
                        raise ValueError(f"The outer arc radius is too large. Should be less than {(midline.length / min_ratio + (start_radius + end_radius) / 2)}.")

                    if midline.length / outer_radius_length > max_ratio:
                        raise ValueError(f"The outer arc radius is too small. Should be greater than {(midline.length / max_ratio + (start_radius + end_radius) / 2)}.")

                    # check we get intersections anyway
                    xsa = c13.edge().intersect(c23.edge())
                    xsb = c14.edge().intersect(c24.edge())

                    if xsa is None:
                        raise ValueError("Could not find intersections. Try larger or smaller inner_radius")

                    if xsb is None:
                        raise ValueError("Could not find intersections. Try larger or smaller outer_radius")

                    # find intersections and tangents
                    xa = xsa.sort_by(Axis(start_point, normal))[0]
                    xb = xsb.sort_by(Axis(start_point, normal))[0]

                    ia1 = IntersectingLine(start_point, Vector(xa), c1)
                    ib1 = IntersectingLine(start_point, -Vector(xb), c1)
                    ia2 = IntersectingLine(end_point, (Vector(xa) - Vector(end_point)), c2)
                    ib2 = IntersectingLine(end_point, (-Vector(xb) + Vector(end_point)), c2)

                    ta1 = Vector((ia1 % 1).Y, -(ia1 % 1).X)
                    ta2 = Vector((ia2 % 1).Y, -(ia2 % 1).X)
                    tb1 = Vector((ib1 % 1).Y, -(ib1 % 1).X)

                a1x = TangentArc([ia1 @ 1, ib1 @ 1], tangent=center_side * -ta1)
                a2x = TangentArc([ia1 @ 1, ia2 @ 1], tangent=center_side * ta1)
                a3x = TangentArc([ia2 @ 1, ib2 @ 1], tangent=center_side * ta2)
                a4x = TangentArc([ib1 @ 1, ib2 @ 1], tangent=center_side * -tb1)

            make_face()

        # removed align option because its a little weird
        super().__init__(obj=sketch.sketch, rotation=rotation, mode=mode)


class AubergineArcSlot(BaseSketchObject):
    """Sketch Object: Aubergine Arc Slot

    Add a curved slot of varying width defined by center length, and start, end, inner, and outer radii.

    Args:
        arc (Curve | Edge | Wire): reference arc
        start_height (float): height of start circle
        end_height (float): height of end circle
        width_factor (float): 
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    def __init__(self,
                 arc: Curve | Edge | Wire,
                 start_height: float,
                 end_height: float,
                 width_factor: float,
                 mode = Mode.ADD):

        start_arc = CenterArc(arc @ 0, start_height / 2, start_angle=0, arc_size=360)
        end_arc = CenterArc(arc @ 1, end_height / 2, start_angle=0, arc_size=360)
        midline = arc @ 1 - arc @ 0

        # factor = width_factor * (1.888 - .666) + .666
        # inner_radius = midline.length / factor - (start_height + end_height) / 4
        # outer_radius = midline.length / factor + (start_height + end_height) / 4

        inner_radius = arc.radius - width_factor
        outer_radius = arc.radius + width_factor

        inner_arc = DoubleArcTangentArc(start_arc, end_arc, inner_radius, side=Side.LEFT, keep=Keep.INSIDE)
        outer_arc = DoubleArcTangentArc(start_arc, end_arc, outer_radius, side=Side.LEFT, keep=Keep.OUTSIDE)
        start_arc = TangentArc([inner_arc @ 0, outer_arc @ 0], tangent=-(inner_arc % 0))
        end_arc = TangentArc([inner_arc @ 1, outer_arc @ 1], tangent=inner_arc % 1)

        face = make_face([start_arc, end_arc, inner_arc, outer_arc])
        super().__init__(obj=face, mode=mode)