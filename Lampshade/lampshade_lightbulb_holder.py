import cadquery as cq
from math import *
from cadquery import exporters


# parameters
r_in = 21.5
thickness = 2.5  # r_in + thickness = 24 mm, max is 25 mm
h = 12
fillet = thickness / 3
fillet_in = 0.3
r_wire = 7
r_holes = 10
n_holes = 6
slit_width = 8

###

r_out = r_in + thickness
hodler = (
    cq.Workplane("XY").circle(r_out)
    .transformed(offset=(0, 0, h)).circle(r_out)
    .loft()
    .faces(">Z").shell(-thickness)
    .faces(">Z[-2]").fillet(fillet_in)
)

holder_with_main_hole = (
    hodler.hole(r_wire)
)

r_hole_centre = (r_in + r_wire / 2 + fillet - fillet_in) / 2
holder_with_holes = (
    holder_with_main_hole
    .polygon(nSides=n_holes, diameter=2*r_hole_centre, forConstruction=True)
    .vertices()
    .hole(r_holes)
)

slit = (
    cq.Workplane("YZ").rect(slit_width / 2, 3 * h)
    .transformed(offset=(0, 0, 2 * r_in)).rect(slit_width / 2, 3 * h)
    .loft()
)

holder_with_holes = holder_with_holes.cut(slit)

holder_filleted = (
    holder_with_holes
    .edges(">X").fillet(fillet)
    .faces(">Z[-2]").fillet(fillet)
    .faces(">Z").fillet(fillet)
)

#show_object(slit)
show_object(holder_filleted)
exporters.export(holder_filleted, 'lightbulb_holder.step')
exporters.export(holder_filleted, 'lightbulb_holder.stl', tolerance=0.01, angularTolerance=0.07)