import cadquery as cq
import random

# Set the size and number of shapes to create
size = 20
num_shapes = 10

# Create a 3D model to hold the shapes
model = cq.Workplane("XY").box(size, size, size)

# Create the shapes and add them to the model
for i in range(num_shapes):
    # Generate random parameters for the shape
    shape_size = size * random.random()
    shape_x = size * (random.random() - 0.5)
    shape_y = size * (random.random() - 0.5)
    shape_z = size * (random.random() - 0.5)
    shape_rotation = 360 * random.random()
    shape_twist = 360 * random.random()
    shape_slices = int(10 * random.random()) + 3
    
    # Create a random shape using the parameters
    shape = cq.Workplane("XY").box(shape_size, shape_size, shape_size).rotate((0,0,0), (0,0,1), shape_rotation).twistAtPoint((0,0,0), shape_twist, (0,0,1)).slices(shape_slices)
    
    # Add the shape to the model
    model = model.union(shape.translate((shape_x, shape_y, shape_z)))

# Render the model
show_object(model)
