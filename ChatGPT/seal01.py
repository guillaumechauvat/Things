import cadquery as cq

# Create the base shape for the seal using a series of curves
curve1 = cq.Workplane("XY").circle(10).extrude(5)
curve2 = cq.Workplane("XY").circle(5).extrude(10)
curve3 = cq.Workplane("XY").circle(2).extrude(10)

# Combine the curves to create the overall shape of the seal
seal = curve1.union(curve2).union(curve3)

# Add the head and flippers to the seal using simple geometric shapes
head = cq.Workplane("XY").circle(5).extrude(5)
flipper1 = cq.Workplane("XY").rect(2, 5).extrude(2)
flipper2 = cq.Workplane("XY").rect(2, 5).extrude(2)

# Place the head and flippers in the appropriate locations on the seal
seal = seal.union(head.translate((10, 0, 0)))
seal = seal.union(flipper1.translate((-6, -6, 0)))
seal = seal.union(flipper2.translate((-6, 6, 0)))

# Render the final model
show_object(seal)
