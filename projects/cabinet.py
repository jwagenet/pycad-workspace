import copy
import math

from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


## Parameters
ply_shrink = 1/16
ply_nom_t = .75
ply_t = ply_nom_t - ply_shrink
back_nom_t = 1
back_t = back_nom_t - ply_shrink

frame_h = 28
frame_d = 18.5
frame_w = 53.5 * 2
cabinet_sections = 6
frame_sec_max = 3
frame_top_d = 5
frame_section_w = frame_w / cabinet_sections

pin_d = .5
holes = 12
pin_dia = .25
pin_spacing = 32 / 25.4
pin_offset_back = 1
pin_start = 6.375
pin_offset_front = 2


## Part Classes
class Shelf(BasePartObject):
    def __init__(
        self,
        type = "single",
    ):
        shelf_gap = 1/16

        if type == "end":
            wall_overlap = 1
            label = "Shelf End"
        elif type == "mid":
            wall_overlap = 1.5
            label = "Shelf Mid"
        else:
            wall_overlap = 2
            label = "Shelf Single"

        shelf_d = frame_d - shelf_gap
        wide_w = frame_section_w - (ply_t * wall_overlap) - shelf_gap

        with BuildPart() as shelf:
            Box(wide_w, shelf_d, ply_t, align=Align.MIN)

        super().__init__(part=shelf.part)
        self.label = label

        RigidJoint("pin", self, Location((-shelf_gap/2, pin_offset_front - shelf_gap, 0), (0, 0, 0)))


class Door(BasePartObject):
    def __init__(
        self,
        type = "left",
    ):
        door_top = .25
        door_gap = .125
        door_handle_dia = 1.5
        door_handle_pos = 2
        door_h = frame_h - door_top
        door_w = frame_section_w - door_gap

        with BuildPart() as door:
            with BuildSketch() as profile:
                Rectangle(door_w, door_h, align=(Align.MIN, Align.MIN))
                with Locations((door_w - door_handle_pos, door_h - door_handle_pos)):
                    Circle(door_handle_dia/2, mode=Mode.SUBTRACT)

            extrude(amount=ply_t)

            if type == "left":
                mirror(about=Plane.YZ, mode=Mode.REPLACE)

        super().__init__(part=door.part)

        if type == "right":
            self.label = "Door Right"
            RigidJoint("left", self, Location((door_w + door_gap/2, 0, ply_t), (90, 180, 0)))

        elif type == "left":
            self.label = "Door Left"
            RigidJoint("left", self, Location((door_gap/2, 0, ply_t), (90, 180, 0)))


class FrameBack(BasePartObject):
    def __init__(
        self,
        width,
        thickness = ply_t,
        type = "back",
    ):
        with BuildPart() as back:
            Box(width, frame_h, thickness, align=Align.MIN)

        super().__init__(part=back.part)
        self.label = "Frame Back"
        RigidJoint("back", self, Location((thickness, 0, thickness), (-90, 0, 0)))


class FrameCap(BasePartObject):
    def __init__(
        self,
        type = "left",
    ):
        with BuildPart() as frame_cap:
            with BuildSketch():
                Rectangle(frame_d, frame_h, align=(Align.MIN, Align.MIN))

            extrude(amount=ply_t)
            extrude(PinGrid().move(Location((0, ply_t, ply_t))), -pin_d, mode=Mode.SUBTRACT)

            if type == "right":
                mirror(about=Plane.YZ, mode=Mode.REPLACE)

        super().__init__(part=frame_cap.part)

        if type == "left":
            self.label = "Frame Left"
            RigidJoint("back", self, Location((frame_d, 0, ply_t), (-90, 0, -90)))
            RigidJoint("top", self, Location((frame_d, frame_h, ply_t), (-90, 0, -90)))
            RigidJoint("front", self, Location((0, frame_h, ply_t), (-90, 0, -90)))

            RigidJoint("pin0", self, Location((2, ply_t + pin_start + 3 * pin_spacing, ply_t), (-90, 0, -90)))
            RigidJoint("pin1", self, Location((2, ply_t + pin_start + 9 * pin_spacing, ply_t), (-90, 0, -90)))

        else:
            self.label = "Frame Right"
            RigidJoint("back", self, Location((-frame_d, 0, ply_t), (-90, 0, 90)))


class FrameDivider(BasePartObject):
    def __init__(
        self,
        type = "divider",
    ):

        divider_h = frame_h - ply_t * 2
        tab_h = .5
        tab_f = .25
        tab_w = frame_d - (frame_top_d + .5) * 2

        with BuildPart() as frame_divider:
            with BuildSketch() as profile:
                Rectangle(frame_d, divider_h, align=(Align.MIN, Align.MIN))
                with Locations((frame_d/2, divider_h)):
                    tab = Rectangle(tab_w, tab_h, align=(Align.CENTER, Align.MIN))

                fillet(tab.vertices().sort_by(Axis.Y)[:2], tab_f)

            extrude(amount=ply_t)
            extrude(PinGrid().move(Location((0, ply_t, ply_t))), -ply_t, mode=Mode.SUBTRACT)

        super().__init__(part=frame_divider.part)
        self.label = "Divider"
        RigidJoint("back", self, Location((frame_d, 0, ply_t/2), (-90, 0, -90)))
        RigidJoint("pin0", self, Location((2, pin_start + 3 * pin_spacing, ply_t), (-90, 0, -90)))
        RigidJoint("pin1", self, Location((2, pin_start + 9 * pin_spacing, ply_t), (-90, 0, -90)))


class FrameBase(BasePartObject):
    def __init__(
        self,
        width,
        depth,
        thickness,
        type = "bottom",
    ):

        with BuildPart() as base:
            Box(width, depth, thickness, align=Align.MIN)

        super().__init__(part=base.part)
        if type == "bottom":
            self.label = "Frame Base"
            RigidJoint("left", self, Location((0, depth, 0), (0, 0, 0)))
            RigidJoint("right", self, Location((width, depth, 0), (0, 0, 0)))

        elif type == "top":
            self.label = "Frame Top"
            RigidJoint("back", self, Location((0, depth, thickness), (0, 0, 0)))
            RigidJoint("front", self, Location((0, 0, thickness), (0, 0, 0)))


class EndShelf(BasePartObject):
    def __init__(
        self,
        width,
        thickness,
        type = "end",
    ):

        with BuildPart() as end_shelf:
            with BuildSketch() as profile:
                Triangle(a=width, c=width, B=90, align=Align.MIN)

            extrude(amount=thickness)

        super().__init__(part=end_shelf.part)
        self.label = "End Shelf"
        RigidJoint("bottom", self, Location((0, 0, 0), (0, 0, 0)))
        RigidJoint("top", self, Location((0, 0, thickness), (0, 0, 0)))



class PinGrid(BaseSketchObject):
    def __init__(
        self,
    ):
        with BuildSketch() as pin_grid:
            with Locations((pin_offset_front, pin_start, 0)):
                with GridLocations(frame_d - pin_offset_front - pin_offset_back, pin_spacing, 2, holes, align=Align.MIN):
                    Circle(pin_dia/2)

        super().__init__(obj=pin_grid.sketch)


## Assembly Components
shelf_end = Shelf("end")
shelf_mid = Shelf("mid")
shelf_single = Shelf("single")

door_left = Door("left")
door_right = Door("right")

frame_cap_left = FrameCap("left")
frame_cap_right = FrameCap("right")
frame_divider = FrameDivider()

cabinet = []

# todo

frames = [3, 3]


for s, n_sections in enumerate(frames):

    ## Frame
    frame_back_w = frame_section_w * n_sections
    frame_back = FrameBack(frame_back_w, back_t)

    horiz_w = n_sections * frame_section_w - ply_t * 2
    frame_base = FrameBase(horiz_w, frame_d, ply_t, "bottom")
    frame_top_back = FrameBase(horiz_w, frame_top_d, ply_t, "top")
    frame_top_front = copy.copy(frame_top_back)

    ## Joints
    frame_base.joints["left"].connect_to(frame_cap_left.joints["back"])
    frame_base.joints["right"].connect_to(frame_cap_right.joints["back"])
    frame_base.joints["left"].connect_to(frame_back.joints["back"])
    frame_cap_left.joints["top"].connect_to(frame_top_back.joints["back"])
    frame_cap_left.joints["front"].connect_to(frame_top_front.joints["front"])
    frame = [frame_base, frame_cap_left, frame_cap_right, frame_back, frame_top_back, frame_top_front]

    frame_section = Compound(frame)

    dividers = []
    doors = []
    shelves = []
    for i in range(n_sections):
        ## Doors
        if len(frames) > 1:
            door_interior = True
            if s % 2 == 0:
                door_solo_side = 1
            else:
                door_solo_side = 0

        point = frame_section_w * i - ply_t
        RigidJoint(f"door{i}", frame_base, Location((point, 0, 0), (0, 0, 0)))

        # single
        if door_solo_side and n_sections == 1:
            door_copy = copy.copy(door_right)

        # multi
        elif door_solo_side:
            if i == n_sections - 1 and door_interior:
                door_copy = copy.copy(door_left)
            elif i % 2 == 0:
                door_copy = copy.copy(door_left)
            else:
                door_copy = copy.copy(door_right)
        else:
            if i == 0 and door_interior:
                door_copy = copy.copy(door_right)
            elif i % 2 == 0:
                door_copy = copy.copy(door_right)
            else:
                door_copy = copy.copy(door_left)

        frame_base.joints[f"door{i}"].connect_to(door_copy.joints["left"])
        doors.append(door_copy)

        ## Dividers
        if i != 0:
            point = frame_section_w * i - ply_t
            RigidJoint(f"div{i}", frame_base, Location((point, frame_d, ply_t), (0, 0, 0)))
            divider_copy = copy.copy(frame_divider)
            frame_base.joints[f"div{i}"].connect_to(divider_copy.joints["back"])
            dividers.append(divider_copy)

        ## Shelves
        if n_sections == 1:
            shelf = shelf_single
        elif i == 0 or i == n_sections - 1:
            shelf = shelf_mid
        else:
            shelf = shelf_end

        if i == 0:
            target = frame_cap_left
        else:
            target = dividers[i-1]

        for j in range(2):
            shelf_copy = copy.copy(shelf)
            target.joints[f"pin{j}"].connect_to(shelf_copy.joints["pin"])
            shelves.append(shelf_copy)

    frame_section += dividers + doors + shelves
    frame_section.label = f"Frame Section {s}"
    RigidJoint(f"left", frame_section, Location((0, 0, 0), (0, 0, 0)))
    RigidJoint(f"right", frame_section, Location((frame_back_w, 0, 0), (0, 0, 0)))

    cabinet.append(frame_section)



show_object(cabinet[0], options={"color": (200, 150, 200)}, render_joints=True)
for i in range(1, len(cabinet)):
    color = (200, 150, 200) if i % 2 == 0 else (150, 200, 200)

    cabinet[i].joints["left"].connect_to(cabinet[i-1].joints["right"])
    show_object(cabinet[i], options={"color": color}, render_joints=True)

show(EndShelf(frame_d, ply_t), render_joints=True)



