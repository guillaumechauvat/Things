import cadquery as cq
from cadquery import exporters

spacing = 30
blades_thickess = 4
blades_width = [30, 50]
blades_length = [130, 170]
x_padding = 0.4 * spacing
y_padding = 0.25 * spacing
z_padding = 0.4 * spacing
wall_padding = 0.5 * spacing
fillet_sides = 15
fillet_top = 4
fillet_under = 1
fillet_blades_top = 1
fillet_blades_bottom = 1
fillet_blades_inside = 0.5
fillet_wall = 1

nblades = len(blades_width)
lx = max(blades_width) + 2 * y_padding
ly = (nblades - 1) * spacing + 2 * x_padding + wall_padding
lz = max(blades_length) + z_padding

# make a box
holder = (
    cq.Workplane("XY")
    .box(lx, ly, lz)
    #.faces(">Z")
    #.fillet(fillet_outside)
    .edges("|Z and <Y")
    .fillet(fillet_sides)
    .edges(">Z and (not >Y)")
    .fillet(fillet_top)
    .edges("<Z and (not >Y)")
    .fillet(fillet_under)
    .edges(">Y")
    .fillet(fillet_wall)
)

# make holes in it
for blade in range(nblades):
    y_offset = (blade - (nblades - 1) / 2) * spacing - wall_padding / 2
    holder = (
        holder
        .faces(">Z")
        .moveTo(0, y_offset)
        .rect(blades_width[blade], blades_thickess)
        .cutThruAll()
    )

# round the edges of the blade slits
holder = holder.edges("|Z").fillet(fillet_blades_inside)
holder = holder.edges("<Z").fillet(fillet_blades_bottom)
holder = holder.edges(">Z").fillet(fillet_blades_top)



exporters.export(holder, 'knife_block.stl', tolerance=0.01, angularTolerance=0.07)