"""Solution for https://www.reddit.com/r/openscad/comments/1lzkjen/how_to_code_selfcutting_movable_letters/"""

# %%
from build123d import *
from ocp_vscode import *

# %%
# https://www.dafont.com/cute-dino-2.font
font = "Cute Dino.ttf"
string = "BUILD123D"
height = 10
overlap = 1.5
gap = .2
base = 1
boss = 1


text = Text(string, 10, font_path=font)
widths = [f.bounding_box().size.X for f in text.faces()]
text_f = text.faces()
working = ShapeList()
for i in range(len(widths)):
    if i == 0:
        x = 0
    else:
        x = sum(widths[:i]) - i * overlap

    working.append(text_f[i].located(Location((x, 0, 0))))

try:
    bosses = ShapeList([working[0]])
    for i in reversed(range(1, len(working))):
        bosses.append(working[i] - offset(working[i - 1], gap))

except:
    print("Warning : offset method failed, switching to scale")
    bosses = ShapeList([working[0]])
    for i in reversed(range(1, len(working))):
        dif = working[i - 1].location.position - working[i - 1].center()
        cut = scale(working[i - 1].translate(dif), (widths[i - 1] + gap * 2) / widths[i - 1]).translate(-dif)
        bosses.append(working[i] - cut)

show(working, bosses)
result = (extrude(working, base) + extrude(bosses, boss + base)).clean()
result = scale(result, height / result.bounding_box().size.Y)
show(result)


# %%
