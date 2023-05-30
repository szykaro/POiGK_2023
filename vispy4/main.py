from vispy import app, gloo
import numpy as np


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title="Hello world!", size=(800, 800))
        self.program = None
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.draw_square()
        self.timer.start()

    def draw_square(self):
        vertex_shader = self.load_shader("vertex_shader.glsl")
        fragment_shader = self.load_shader("fragment_shader.glsl")
        self.program = gloo.Program(vertex_shader, fragment_shader, 4)
        self.program["pos"] = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]]) * 0.25
        self.program["color"] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]])
        self.program["time"] = self.time
        self.show()

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        self.program.draw("triangle_fan")

    def on_key_press(self, event):
        if event.key == " ":
            self.program["color"] = None
            self.program["color"] = np.random.rand(4, 3).astype(np.float32)
            self.show()

    def on_timer(self, event):
        self.time += 1 / 60
        self.program["time"] = self.time
        self.show()


apka = Apka()
app.run()
