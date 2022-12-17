import cadquery as cq

# Seal dimensions
seal_length = 2.0  # seal length in meters
seal_height = 0.5  # seal height in meters
seal_width = 0.8  # seal width in meters

# Create a 3D box representing the body of the seal
seal_body = cq.Workplane("XY").box(seal_length, seal_width, seal_height)

# Add the head to the seal
head_radius = 0.4  # head radius in meters
head_offset = seal_length / 2 - head_radius  # head offset from the body
seal_head = cq.Workplane("XY").sphere(head_radius)
seal_head = seal_head.translate((head_offset, 0, 0))

# Add the flippers to the seal
flipper_length = 0.4  # flipper length in meters
flipper_radius = 0.1  # flipper radius in meters
flipper_offset = seal_width / 2 - flipper_radius  # flipper offset from the body

# Create the left flipper
left_flipper = cq.Workplane("XY").cylinder(flipper_radius, flipper_length)
#left_flipper = left_flipper.rotate((0, 0, 0), (0, 0, 1), 90)
left_flipper = left_flipper.translate((0, flipper_offset, 0))

# Create the right flipper
right_flipper = cq.Workplane("XY").cylinder(flipper_radius, flipper_length)
#right_flipper = right_flipper.rotate((0, 0, 0), (0, 0, 1), 90)
right_flipper = right_flipper.translate((0, -flipper_offset, 0))

# Add the flippers to the seal
seal = seal_body.union(seal_head).union(left_flipper).union(right_flipper)

# Triangulate the seal surface
#seal = seal.triangulate()

# Render the final model
show_object(seal)