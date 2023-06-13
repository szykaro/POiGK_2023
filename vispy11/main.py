from vispy.scene import SceneCanvas
from vispy.scene.visuals import Box
from vispy.scene.cameras import TurntableCamera


canvas = SceneCanvas(keys='interactive', size=(800, 600), show=True)

view = canvas.central_widget.add_view(bgcolor='#efefef')
cube = Box(1, 1, 1, color='blue',
           edge_color="black",
           parent=view.scene)
# view.camera = 'turntable'
camera = TurntableCamera(parent=view.scene, fov=60, distance=3.0)
view.camera = camera

canvas.app.run()
