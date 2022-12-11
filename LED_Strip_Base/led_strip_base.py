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
wire_width = 5

# Calculated parameters
total_length = acrylic_length + base_padding
total_width = led_width + 2 * walls
inner_length = total_length - 2 * walls
inner_width = led_width
base_extra_thickness = base_thickness - base_side_thickness

# outer part
base = (
    cq.Workplane('XY')
    .tag('base')
    .rect(total_length, total_width)
    .extrude(base_side_thickness)
)
# fillets
base = (
    base
    .edges('|Z')
    .fillet(fillet)
    .faces('<Z')
    .fillet(bottom_fillet)
)
# inner part
base = (
    base
    .faces('>Z').workplane()
    .tag('lid')
    .rect(inner_length, inner_width)
    .extrude(base_extra_thickness)
    # extra bit for the wire hole
    .workplaneFromTagged('lid')
    .transformed(offset=cq.Vector(inner_length / 2, 0, 0))
    .rect(2 * walls, wire_width)
    .extrude(base_extra_thickness)
)
