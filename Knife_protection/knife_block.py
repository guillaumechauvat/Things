import cadquery as cq
from cadquery import exporters
from math import *

# knife block for two knives with custom sizes

# some dimesnions
blade_width = 3
shell_thickness = 1
guard_angle = 5  # in degrees
fillet = 0.4  # this is the largest possible


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
    (19, 170),
    (24, 170),
    (40, 140),
    (50, 70),
    (53, -53 * tan(guard_angle * pi / 180)),
]

knife01_hole01 = [
    (5, 10),
    (5, 43),
    (30, 86),
    (34, 68),
    (34, 10),
]

knife01_hole02 = [
    (5, 57),
    (5, 125),
    (8, 137),
    (26, 96),
]

knife01_hole03 = [
    (13, 145),
    (20, 156),
    (21, 156),
    (29, 132),
    (33, 111),
    (28, 111),
]

knife01 = (
    cq.Workplane("XZ")
    .polyline(knife01_outline)
    .close()
    .extrude(blade_width)
    .faces("<Z")
    .shell(shell_thickness)
    .faces("<Y")
    .polyline(knife01_hole01)
    .close()
    .polyline(knife01_hole02)
    .close()
    .polyline(knife01_hole03)
    .close()
    .cutThruAll()
    .fillet(fillet)
)


# rotate to make sure the bottom surface is aligned with the Z plane
knife01 = knife01.rotate((0, 0, 0), (0,1,0), -guard_angle)
