from vispy import app, scene, geometry
from vispy.scene.cameras import TurntableCamera
from vispy.geometry.generation import create_cylinder, create_cone
from vispy.visuals.filters import ShadingFilter, TextureFilter

canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
view = canvas.central_widget.add_view()

cylinder = create_cylinder(20, 50, (0.5, 0.5), 1.5)
tower = scene.visuals.Mesh(meshdata=cylinder, parent=view.scene,
                           color=(0.5, 0.5, 0.5, 1))

cone = create_cone(20, 0.7, 0.5)
cap = scene.visuals.Mesh(meshdata=cone, parent=view.scene,
                         color=(1, 0, 0, 1))
cap.transform = scene.transforms.STTransform(translate=(0, 0, 1.5))

plane = scene.visuals.Plane(width=2, height=2, parent=view.scene, color=(0, 1, 0, 1))

# Ustawienie kamery
camera = TurntableCamera(parent=view.scene, fov=60, distance=3.0)
view.camera = camera

shading = ShadingFilter(shading='smooth', light_dir=(1, 0, 0))
tower.attach(shading)
shading = ShadingFilter(shading='smooth', light_dir=(1, 0, 0))
cap.attach(shading)
shading = ShadingFilter(shading='smooth', light_dir=(1, 0, 0))
plane.attach(shading)

app.run()
