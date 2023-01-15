import cadquery as cq
from cadquery import exporters

# knife block for two knives with custom sizes

# some dimesnions
blade_width = 3
shell_thickness = 1

# Outline of the knife holes, seen from the side
# The shape is reversed, in the direction it's intended to be printed,
#the tip of the knife up.
knife01_outline = [
    (0, 0),
    (0, 125),
    #(5, 147),
    #(20, 164),
    #(25, 164),
    #(30, 162),
    (5, 150),
    (22, 170),
    (40, 140),
    (50, 70),
    (53, 0),
]

knife01_hole01 = [
    (5, 10),
    (5, 43),
    (30, 86),
    (34, 68),
    (34, 10),
]

knife01 = (
    cq.Workplane("XZ")
    .polyline(knife01_outline)
    .close()
    .extrude(blade_width)
    .faces("<Z")
    .shell(shell_thickness)
)