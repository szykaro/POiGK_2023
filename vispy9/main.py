from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, translate, perspective
from vispy.geometry.generation import create_box, cre
import cv2


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title="Hello world!", size=(800, 800))
        gloo.set_state(depth_test=True)
        self.program = None
        self.triangle_indices = None
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.draw_cube()
        self.timer.start()

    def draw_cube(self):
        vertex_shader = self.load_shader("vertex_shader.glsl")
        fragment_shader = self.load_shader("fragment_shader.glsl")
        self.program = gloo.Program(vertex_shader, fragment_shader)

        V, I, L = create_box()

        self.program['pos'] = V['position']
        self.program['texcoord'] = V['texcoord']

        image = cv2.imread('texture.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.program['texture'] = image

        self.triangle_indices = gloo.IndexBuffer(I)


    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        self.program.draw("triangles", self.triangle_indices)

    def on_timer(self, event):
        self.time += 1 / 60
        self.program["view"] = translate((0, 0, -6))
        self.program["projection"] = perspective(45, 1, 2, 10)
        self.program["model"] = rotate(self.time * 180 / np.pi, (0, 0, 1)).dot(
            rotate(0.4 * self.time * 180 / np.pi, (0, 1, 0))
        )
        self.show()


apka = Apka()
app.run()
