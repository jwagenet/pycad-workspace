"""Demo method to align and fuse part using joints for bfly2000

Joints are created on each part and connected. One of the parts (carriage) gets parameters
for mating alignment. This method seems best to implement if the parts might need to be split
and assembled differently in the future. In this case the joints are placed in natural part 
pivots, but using locations where bolt holes or other mating features might go makes sense."""

import copy
from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


## Mate position parameters with some limits
# keep height +/- < 30 or so for the defined box size
mate_angle = 10
mate_height = -5


## Arm Side
arm_l = 200
arm_w = 50
arm_t = 5
hole_r = 3.5/2
hole_bcr = 35/2
with BuildPart() as side:
    with BuildSketch() as s:
        SlotArc(Line((0, 0), (arm_l, 0)), arm_w)
        with PolarLocations(hole_bcr, 4) as l1:
            Circle(hole_r, mode=Mode.SUBTRACT)
    extrude(amount=arm_t)

arm_side = side.part
RigidJoint("carriage-mount", arm_side, Location((200, 0, 0), (0, 0, 0)))


## Carriage representation
motor_h = 60
motor_w = 50
motor_d = 80
carriage_t = 5
with BuildPart() as carriage:
    Box(motor_d, motor_w, motor_h)
    yz_faces = carriage.faces().filter_by(Plane.YZ).sort_by(Axis.X)
    offset(amount=-carriage_t, openings=carriage.faces().sort_by(Axis.Z)[-1])

carriage = carriage.part

## Assign mate height and angle relative to carriage center
# using faces flips normals for free
for i, face in enumerate(yz_faces):
    with Locations(face.move(Location((0, 0, mate_height), (-90 + mate_angle, 0, 0)))) as l:
        RigidJoint(f"arm-mount{i}", carriage, l.locations[0])

arm_sides = [arm_side, copy.copy(arm_side)]
for i, side in enumerate(arm_sides):
    carriage.joints[f"arm-mount{i}"].connect_to(side.joints[f"carriage-mount"])


## Combined part
with BuildPart() as combined:
    add(carriage)
    for side in arm_sides:
        add(side)

show(combined)