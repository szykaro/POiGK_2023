import sys
from vispy import app, scene
from vispy.visuals.transforms import MatrixTransform
import numpy as np

# Create a canvas with a 3D viewport
canvas = scene.SceneCanvas(keys='interactive')
view = canvas.central_widget.add_view()

# Create three spheres: big, medium, small
big_sphere = scene.visuals.Sphere(radius=1, color='blue',
                                  parent=view.scene,
                                  shading='smooth')
medium_sphere = scene.visuals.Sphere(radius=0.5, color='green',
                                     parent=view.scene,
                                     shading='smooth')
small_sphere = scene.visuals.Sphere(radius=0.25, color='red',
                                    parent=medium_sphere,
                                    shading='smooth')

# Apply a transform to the medium sphere to move it away from the big sphere
medium_transform = MatrixTransform()
medium_transform.translate((2, 0, 0))
medium_sphere.transform = medium_transform

# Apply a transform to the small sphere to move it away from the medium sphere
small_transform = MatrixTransform()
small_transform.translate((0.75, 0, 0))
small_sphere.transform = small_transform

# Create a camera to view the scene
cam = scene.TurntableCamera(up='z', fov=60)
view.camera = cam

def update(ev):

    angle_update = 1

    # Update the position of medium_sphere (orbiting around big sphere)
    medium_transform.rotate(angle_update, (0, 0, 1))

    # Update the position of small_sphere (orbiting around medium sphere)
    small_transform.rotate(angle_update, (0, 0, 1))

timer = app.Timer()
timer.connect(update)
timer.start()

canvas.show()

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()