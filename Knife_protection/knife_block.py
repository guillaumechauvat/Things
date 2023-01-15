import cadquery as cq
from cadquery import exporters
from math import *

# knife block for two knives with custom sizes

# some dimesnions
blade_width = 3
shell_thickness = 1
guard_angle = 5  # in degrees
fillet = 0.4  # this is the largest possible
base_fillet = 0.3
final_fillet = 0.4
connection_fillet = 0.4
spacing = 30
wall_spacing = 30
connection_width = 1.2
connection_height = 5
connection_height_top = 3
wall_connection_thickness = 1

# Outline of the first knife, seen from the side
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
)

################
# second knife #
################

knife02_outline = [
    (0, 0),
    (0, 85),
    (5, 115),
    (9, 120),
    (14, 120),
    (23, 100),
    (29, 65),
    (34, -34 * tan(guard_angle * pi / 180)),
]

knife02_hole01 = [
    (5, 10),
    (5, 85),
    (7, 90),
    (10, 85),
    (22, 45),
    (24, 10)
]

knife02_hole02 = [
    (8, 103),
    (10, 110),
    (11, 110),
    (17, 99),
    (21, 79),
    (19, 80),
]

knife02 = (
    cq.Workplane("XZ")
    #.transformed(offset=(0, spacing, 0))
    .polyline(knife02_outline)
    .close()
    .extrude(blade_width)
    .faces("<Z")
    .shell(shell_thickness)
    .faces("<Y")
    .polyline(knife02_hole01)
    .close()
    .polyline(knife02_hole02)
    .close()
    .cutThruAll()
)

# rotate to make sure the bottom surface is aligned with the Z plane
knife01 = knife01.rotate((0, 0, 0), (0,1,0), -guard_angle)
knife02 = knife02.rotate((0, 0, 0), (0,1,0), -guard_angle)


# space the knife holders
knife02 = knife02.translate((0, spacing, 0))
knives = knife01.union(knife02)

# add connections
x0 = 0
y0 = shell_thickness / 2
x1 = 32
y1 = spacing - blade_width - shell_thickness / 2
x2 = 51.5

# dx offsets to get a constant width of beams
dx1 = connection_width * sqrt(1 + (x1 - x0)**2 / (y1 - y0)**2)
dx2 = connection_width
dx3 = connection_width * sqrt(1 + (x2 - x1)**2 / (y1 - y0)**2)
dx4 = connection_width * sqrt(1 + (x2 - x0)**2 / (y1 - y0)**2)
base_connection = (
    cq.Workplane("XY")
    .polyline([
        (x0, y0),
        (x1 - dx1, y1),
        (x1, y1),
        (x0 + dx1, y0),
    ])
    .close()
    .polyline([
        (x0, y0),
        (x0, y1),
        (x0 + dx2, y1),
        (x0 + dx2, y0),
    ])
    .close()
    .polyline([
        (x2 - dx3, y0),
        (x1 - dx3, y1),
        (x1, y1),
        (x2, y0),
    ])
    .close()
    .polyline([
        (x0, y1),
        (x0 + dx4, y1),
        (x2, y0),
        (x2 - dx4, y0),
    ])
    .close()
    .extrude(connection_height)
    .fillet(base_fillet)
)

# extra connection between the tips
x0 = 8
z0 = 167
x1 = 2
z1 = 115
dx = connection_width * sqrt(1 + (x1 - x0)**2 / (y1 - y0)**2)
dz = connection_height_top * sqrt(1 + (z1 - z0)**2 / (y1 - y0)**2)
beam = (
    cq.Workplane("XZ")
    .polyline([
        (x0 - dx / 2, z0 - dz / 2),
        (x0 - dx / 2, z0 + dz / 2),
        (x0 + dx / 2, z0 + dz / 2),
        (x0 + dx / 2, z0 - dz / 2),
    ])
    .close()
    .workplane(offset=(y0 - y1))
    .polyline([
        (x1 - dx / 2, z1 - dz / 2),
        (x1 - dx / 2, z1 + dz / 2),
        (x1 + dx / 2, z1 + dz / 2),
        (x1 + dx / 2, z1 - dz / 2),
    ])
    .close()
    .loft()
)
###################
# Wall Connection #
###################

wall_connection_1 = (
    cq.Workplane("XZ")
    .workplane(offset=blade_width)
    .polyline([
        (1, 0),
        (-10, 125),
        (-8, 125),
        (3, 0),
    ])
    .close()
    .extrude(wall_spacing)
    .cut(
        cq.Workplane("YZ")
        .workplane(offset=15)
        .polyline([
            (-5, 5),
            (-5, 110),
            (-wall_spacing + 5, 5)
        ])
        .close()
        .polyline([
            (-wall_spacing, 15),
            (-wall_spacing, 120),
            (-10, 120)
        ])
        .close()
        .extrude(-30)
    )
)

wall_connection_2 = (
    cq.Workplane("XZ")
    .workplane(offset=blade_width)
    .polyline([
        (52, 0),
        (42.5, 73.5),
        (30, 125),
        (28, 125),
        (40.5, 73),
        (50, 0),
    ])
    .close()
    .extrude(wall_spacing)
    .cut(
        cq.Workplane("YZ")
        .workplane(offset=55)
        .polyline([
            (-5, 15),
            (-5, 120),
            (-wall_spacing + 5, 120)
        ])
        .close()
        .polyline([
            (-10, 5),
            (-wall_spacing, 5),
            (-wall_spacing, 110)
        ])
        .close()
        .extrude(-30)
    )
)

wall_connection = (
    cq.Workplane("XZ")
    .workplane(offset=blade_width + wall_spacing)
    .polyline([
        (1, 0),
        (52, 0),
        (42.5, 73.5),
        (30, 125),
        (-10, 125),
    ])
    .close()
    .extrude(wall_connection_thickness)
    .translate((0, wall_connection_thickness, 0))
    .union(wall_connection_1)
    .union(wall_connection_2)
    .fillet(connection_fillet)
)

knives = knives.fillet(fillet)
knives = (
    knives
    .union(base_connection)
    .union(beam)
    .union(wall_connection)
    .fillet(final_fillet)
)

show_object(knives)
