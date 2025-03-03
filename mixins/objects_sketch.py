import copy
from build123d import *
from ocp_vscode import show, show_object, set_viewer_config, set_port, set_defaults, get_defaults
set_port(3939)

# geometric solution reference https://www.youtube.com/watch?v=-STj2SSv6TU for tangent arcs

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


show(AubergineSlot(length=20,
                      start_radius=10,
                      end_radius=1,
                      inner_radius=15,
                      outer_radius=30,
                      side=Side.RIGHT,
                      rotation=0))

# todo: AubergineArc. use x/y ratio of arc angle to determine inner/outer radii