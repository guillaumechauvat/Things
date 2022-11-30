import cadquery as cq
from math import *
from cadquery import exporters


# parameters
r_in = 22  # 43.2
wall_thickness = 2.5  # r_in + thickness = 24 mm, max is 25 mm
base_thickness = 2.0
walls_h = 4
fillet = 0.8
fillet_in = 0.3
r_wire = 6.8  # 13.1
r_holes = 9
n_holes = 8
slit_width = 5.5

###

r_out = r_in + wall_thickness
h_tot = walls_h + base_thickness
holder = (
    cq.Workplane("XY")
    .circle(r_out)
    .transformed(offset=(0, 0, walls_h + base_thickness))
    .circle(r_out)
    .loft()
    .faces(">Z")
    .tag("baseplane")
    .hole(2 * r_in, depth=walls_h , clean=True)
    #.faces(">Z").shell(-thickness)
    #.faces(">Z[-2]").fillet(fillet_in)
)

slit = (
    cq.Workplane("YZ").rect(slit_width, 3 * h_tot)
    .transformed(offset=(0, 0, 2 * r_in)).rect(slit_width, 3 * h_tot)
    .loft()
)

holder = holder.cut(slit)

holder = (
    holder
    .workplaneFromTagged("baseplane")
    .hole(2 * r_wire)
)

r_hole_centre = (r_in + r_wire + fillet - fillet_in) / 2
holder = (
    holder
    .workplaneFromTagged("baseplane")
    .polygon(nSides=n_holes, diameter=2*r_hole_centre, forConstruction=True)
    .vertices()
    .hole(r_holes)
)

holder = (
    holder
    .edges(">X").fillet(fillet)
    .faces(">Z[-2]").fillet(fillet)
    .faces(">Z").fillet(fillet)
)

show_object(holder)
#exporters.export(holder, 'lightbulb_holder.step')
exporters.export(holder, 'lightbulb_holder.stl', tolerance=0.01, angularTolerance=0.07)
