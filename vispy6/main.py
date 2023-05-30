from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, scale, translate, perspective
from utils import generate_triangles


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Hello world!',
                         size=(800, 800))
        gloo.set_state(depth_test=True)
        self.program = None
        self.time = 0
        self.timer = app.Timer(1/60, connect=self.on_timer)
        self.draw_cube()
        self.timer.start()

    def draw_cube(self):
        vertex_shader = self.load_shader('vertex_shader.glsl')
        fragment_shader = self.load_shader('fragment_shader.glsl')
        triangles = generate_triangles()
        # colors = np.zeros_like(triangles)
        # colors[:18, 0] = 1
        # colors[18:, 2] = 1
        colors = (triangles + 1) / 2
        self.program = gloo.Program(vertex_shader, fragment_shader, 36)
        self.program['pos'] = triangles * 0.5
        self.program['color'] = colors

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, 'r') as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('triangles')

    def on_timer(self, event):
        self.time += 1/60
        self.program['model'] = rotate(self.time * 100, (0, 0, 1)).dot(
            rotate(self.time * 40, (0, 1, 0))
        )
        self.program['view'] = translate((0, 0, -4))
        self.program['projection'] = perspective(45, 1, 2, 6)
        self.show()


apka = Apka()
app.run()
