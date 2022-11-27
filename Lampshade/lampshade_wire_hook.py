import cadquery as cq
from math import *
from cadquery import exporters


# parameters
r_out = 24.5
r_in = 6.5
thickness = 3
hc = 35
fillet = thickness / 3
d_slit = 6
r_holes = 5.5
r_holes_centre = 15
r_holes_2 = 2
r_holes_2_centre = 20
n_holes = 6
d_support = 15
hook_thickness = 2.5
r_hook_support = 16
hook_support_width = 8
hook_r_in = 3.5
hook_width = 3
hook_neck = 1

###

hook_r_out = hook_r_in + hook_width

base = (
    cq.Workplane("XY").circle(r_out)
    .transformed(offset=(0, 0, thickness)).circle(r_out)
    .loft()
    .faces(">Z").tag("baseplane")
    .polygon(nSides=n_holes, diameter=2*r_holes_centre, forConstruction=True)
    .vertices()
    .hole(2 * r_holes)
    .workplaneFromTagged("baseplane")
    .transformed(rotate=(0, 0, 180 / n_holes))
    .polygon(nSides=n_holes, diameter=2*r_holes_2_centre, forConstruction=True)
    .vertices()
    .hole(2 * r_holes_2)
    .union(
        cq.Workplane("XZ")
        .transformed(offset=(0, thickness / 2, 0.95 * r_out))
        .rect(d_support / 2, thickness)
        .transformed(offset=(0, 0, -1.9 * r_out))
        .rect(d_support / 2, thickness)
        .loft()
    )
    .cut(
        cq.Workplane("YZ")
        .rect(d_slit / 2, 3 * thickness)
        .transformed(offset=(0, 0, 2 * r_out))
        .rect(d_slit / 2, 3 * thickness)
        .loft()
    )
    .workplaneFromTagged("baseplane")
    .hole(2 * r_in)
    .edges("|Z").fillet(fillet)
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(0, r_hook_support, -thickness))
        .rect(hook_thickness, hook_support_width)
        .transformed(offset=(0, 0, 3 * thickness))
        .rect(hook_thickness, hook_support_width)
        .loft()
    )
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(0, -r_hook_support, -thickness))
        .rect(hook_thickness, hook_support_width)
        .transformed(offset=(0, 0, 3 * thickness))
        .rect(hook_thickness, hook_support_width)
        .loft()
    )
    .edges(">Z").fillet(fillet)
)

hook_holes_dist = 2 * hook_r_in + hook_width
hook_neck_width = 2 * hook_r_out - 2 * hook_neck
hook = (
    cq.Workplane("XY")
    .transformed(offset=(2 * r_out, 0, 0))
    .tag("hook1")
    .circle(hook_r_out)
    .extrude(hook_thickness)
    .transformed(offset=(hook_holes_dist, 0, 0))
    .tag("hook2")
    .circle(hook_r_out)
    .extrude(hook_thickness)
    .workplaneFromTagged("hook1")
    .transformed(offset=(hook_holes_dist / 2, 0, 0))
    .rect(hook_holes_dist, hook_neck_width)
    .extrude(hook_thickness)
    .workplaneFromTagged("hook1")
    .circle(hook_r_in)
    .cutThruAll()
    .workplaneFromTagged("hook2")
    .circle(hook_r_in)
    .cutThruAll()
)

show_object(base)
show_object(hook)