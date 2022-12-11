import cadquery as cq
from cadquery import exporters
from math import *

# Dimensions

acrylic_length = 198
acrylic_width = 6
led_width = 10
led_height = 4
base_thickness = 1.5
base_side_thickness = 1
base_padding = 5
top_thickness = 8
walls = 1
fillet = 1
bottom_fillet = 0.5

# Calculated parameters
total_length = acrylic_length + base_padding
total_width = led_width + 2 * walls
inner_length = total_length - 2 * walls
inner_width = led_width

# outer part
base = (
    cq.Workplane('XY')
    .tag('base')
    .rect(total_length, total_width)
    .extrude(base_side_thickness)
    .edges('|Z')
    .fillet(fillet)
    .faces('<Z')
    .fillet(bottom_fillet)
    .workplaneFromTagged('base')
    .rect(inner_length, inner_width)
    .extrude(base_thickness)
)
