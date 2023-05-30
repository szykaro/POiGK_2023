from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, scale, translate, ortho, perspective
from utils import generate_triangles, generate_lines


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Hello world!',
                         size=(800, 800))
        gloo.set_state(depth_test=True)
        self.program = None
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.draw_cube()
        self.draw_lines()
        self.timer.start()

    def draw_cube(self):
        vertex_shader = self.load_shader('vertex_shader.glsl')
        fragment_shader = self.load_shader('fragment_shader.glsl')
        self.program = gloo.Program(vertex_shader, fragment_shader, 36)
        triangles = generate_triangles()
        colors = (triangles + 1) / 2
        self.program['pos'] = triangles
        self.program['color'] = colors

    def draw_lines(self):
        vertex_shader = self.load_shader('vertex_shader.glsl')
        fragment_shader = self.load_shader('fragment_shader.glsl')
        self.lines = gloo.Program(vertex_shader, fragment_shader, 24)
        lines = generate_lines()
        colors = np.zeros_like(lines)
        self.lines['pos'] = lines
        self.lines['color'] = colors

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, 'r') as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('triangles')
        self.lines.draw('lines')

    def on_timer(self, event):
        self.time += 1 / 60
        # self.program['projection'] = ortho(-2, 2, -2, 2, -2, 2)
        self.program['view'] = translate((0, 0, -6))
        self.program['projection'] = perspective(45, 1, 2, 10)
        self.program['model'] = rotate(self.time * 180 / np.pi, (0, 0, 1)).dot(
            rotate(0.4 * self.time * 180 / np.pi, (0, 1, 0))
        )
        self.lines['view'] = self.program['view']
        self.lines['projection'] = self.program['projection']
        self.lines['model'] = self.program['model']
        self.show()


apka = Apka()
app.run()
