import copy

from build123d import *
from ocp_vscode import show, show_object, set_viewer_config, set_port, set_defaults, get_defaults
set_port(3939)



drum_type = "plain" # [plain]
drum_t = 1.5
drum_id = 20
drum_od = drum_id + drum_t*2
drum_w = 10
drum_eye = True

flange_od = 65
flange_t = 1.5

thread_l = 4
thread_pitch = 2
thread_od = 24
thread_id = 25

window_type = "web" # [circle, web, none]
window_margin = 5
window_web_r = 3
window_count = 6

eyelet_count = 2
eyelet_sets = 3
eyelet_od = 2
eyelet_spacing = 5
eyelet_margin = 3

class Flange(BasePartObject):
    def __init__(self):
        with BuildPart() as p:
            with BuildSketch() as s:
                Circle(flange_od/2)
                Circle(drum_id/2, mode=Mode.SUBTRACT)

                # eyelets
                with PolarLocations(flange_od/2 - eyelet_margin, eyelet_sets, start_angle=90):
                    total_width = eyelet_spacing * (eyelet_count - 1)
                    locs = [Vertex(Y=i * eyelet_spacing - total_width/2) for i in range(eyelet_count)]
                    with Locations(locs):
                        Circle(eyelet_od/2, mode=Mode.SUBTRACT)

            extrude(amount=flange_t)

            # windows
            with BuildSketch() as s:
                if window_type.lower() == "none":
                    pass

                elif window_type.lower() == "circle":
                    with PolarLocations((flange_od + drum_od)/4, window_count, 60):
                        Circle(((flange_od + drum_od)/4 - window_margin*2)/2)

                elif window_type.lower() == "web":
                    Circle(flange_od/2 - window_margin)
                    Circle(drum_od/2 + window_margin, mode=Mode.SUBTRACT)
                    with PolarLocations(drum_od/2, window_count, -30):
                        Rectangle(window_margin, (flange_od - drum_od)/2, align=(Align.CENTER, Align.MIN), mode=Mode.SUBTRACT, rotation=-90)
                    fillet(s.vertices(), window_web_r)
                        # with BuildLine() as line:
                        #     a1 = CenterArc((0,0), flange_diameter/2 - window_border_width, start_angle=-angle/2, arc_size=angle)
                        #     a2 = CenterArc((0,0), drum_diameter/2 + window_border_width, start_angle=-angle/2, arc_size=angle)
                        #     c1 = Line(a1 @ 0, a2 @ 0)
                        #     c2 = Line(a1 @ 1, a2 @ 1)
                        #     o1 = offset(c1, window_border_width/2, side=Side.RIGHT, mode=Mode.ADD)
                        #     o2 = offset(c2, window_border_width/2, side=Side.RIGHT, mode=Mode.ADD)

                else:
                    raise NotImplementedError

            extrude(amount=flange_t, mode=Mode.SUBTRACT)

            super().__init__(p.part)
            RigidJoint("flange", self, Location((0, 0, flange_t)))


class Drum(BasePartObject):
    def __init__(self):
        with BuildPart() as p:
            if drum_type == "plain":
                Cylinder(drum_od/2, drum_w, align=(Align.CENTER, Align.CENTER, Align.MIN))
                Cylinder(drum_id/2, drum_w, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

            else:
                raise NotImplementedError



            if drum_eye:
                Cylinder(eyelet_od/2, drum_od/2, rotation=(90, 0, 0), align=(Align.CENTER, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)


        super().__init__(p.part)
        RigidJoint("bottom", self, Location((0, 0, 0)))
        if drum_type in ["plain"]:
            RigidJoint("top", self, Location((0, 0, drum_w), (180, 0, 180)))

f = Flange()
f2 = copy.copy(f)
d = Drum()
f.joints["flange"].connect_to(d.joints["bottom"])
d.joints["top"].connect_to(f2.joints["flange"])

show(f,f2,d)