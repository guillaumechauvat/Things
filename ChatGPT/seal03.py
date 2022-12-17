import cadquery
from cadquery import Solid

# Set the dimensions for the seal
body_length = 100.0
body_height = 50.0
body_width = 30.0
flipper_length = 20.0
flipper_width = 10.0
flipper_thickness = 5.0
eye_radius = 5.0
nose_length = 20.0
nose_width = 10.0

# Create the body of the seal using a cuboid
body = Solid.makeBox(body_length, body_width, body_height)

# Create the left and right flippers using a cuboid
left_flipper = Solid.makeBox(flipper_length, flipper_width, flipper_thickness)
right_flipper = Solid.makeBox(flipper_length, flipper_width, flipper_thickness)

# Create the eyes using spheres
left_eye = Solid.makeSphere(eye_radius)
right_eye = Solid.makeSphere(eye_radius)

# Create the nose using a cuboid
nose = Solid.makeBox(nose_length, nose_width, body_height)

# Add the flippers and eyes to the body using boolean operations
body = body.cut(left_flipper.translate((-body_length / 2 + flipper_length / 2, 0, 0))
                .rotate((0,0,0), (0,0,1), -45))
body = body.cut(right_flipper.translate((body_length / 2 - flipper_length / 2, 0, 0))
                .rotate((0,0,0), (0,0,1), 45))
body = body.cut(left_eye.translate((-body_length / 2 + eye_radius, body_width / 2, body_height / 2)))
body = body.cut(right_eye.translate((body_length / 2 - eye_radius, body_width / 2, body_height / 2)))

# Add the nose to the body using a boolean operation
body = body.cut(nose.translate((0, body_width / 2, 0)))

# Display the resulting model
show_object(body)