from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, translate, perspective
from vispy.geometry.generation import create_box, create_sphere, create_cone, create_cylinder, create_arrow


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title="Hello world!", size=(800, 800))
        gloo.set_state(depth_test=True)

        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        self.shapes = []
        self.translations = []
        self.gen_scene()
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.timer.start()

        self.view = translate((0, 0, -6))
        self.projection = perspective(60, 1, 2, 10)
        self.model = np.eye(4, dtype=np.float32)

    def gen_scene(self):
        self.shapes.append(self.gen_cube())
        self.translations.append((0, 0, 0))
        self.shapes.append(self.gen_sphere())
        self.translations.append((0, 2, 0))
        self.shapes.append(self.gen_cone())
        self.translations.append((0, -2, 0))
        self.shapes.append(self.gen_cylinder())
        self.translations.append((2, 0, 0))
        self.shapes.append(self.gen_arrow())
        self.translations.append((-2, 0, 0))

    def gen_cube(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)

        V, I, L = create_box()
        shape['program']['pos'] = V['position']
        shape['program']['color'] = V['color']

        shape['triangle_indices'] = gloo.IndexBuffer(I)
        shape['line_indices'] = gloo.IndexBuffer(L)
        return shape

    def gen_sphere(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)

        sphere = create_sphere(20, 20, 20)
        print(help(sphere))
        vertices = sphere.get_vertices()
        shape['program']['pos'] = vertices

        colors = np.concatenate((vertices, np.ones((vertices.shape[0], 1), dtype=np.float32)), axis=1)
        shape['program']['color'] = colors

        shape['triangle_indices'] = gloo.IndexBuffer(sphere.get_faces())
        shape['line_indices'] = gloo.IndexBuffer(sphere.get_edges())
        return shape

    def gen_cone(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)

        cone = create_cone(20)
        vertices = cone.get_vertices()
        shape['program']['pos'] = vertices

        colors = np.concatenate((vertices, np.ones((vertices.shape[0], 1), dtype=np.float32)), axis=1)
        shape['program']['color'] = colors

        shape['triangle_indices'] = gloo.IndexBuffer(cone.get_faces())
        shape['line_indices'] = gloo.IndexBuffer(cone.get_edges())
        return shape

    def gen_cylinder(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)

        cylinder = create_cylinder(10, 20)
        vertices = cylinder.get_vertices()
        shape['program']['pos'] = vertices

        colors = np.concatenate((vertices, np.ones((vertices.shape[0], 1), dtype=np.float32)), axis=1)
        shape['program']['color'] = colors

        shape['triangle_indices'] = gloo.IndexBuffer(cylinder.get_faces())
        shape['line_indices'] = gloo.IndexBuffer(cylinder.get_edges())
        return shape

    def gen_arrow(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)

        arrow = create_arrow(10, 20, 0.5, 1.5)
        vertices = arrow.get_vertices().astype(np.float32)
        shape['program']['pos'] = vertices

        colors = np.concatenate((vertices * 2, np.ones((vertices.shape[0], 1), dtype=np.float32)), axis=1)
        shape['program']['color'] = colors

        shape['triangle_indices'] = gloo.IndexBuffer(arrow.get_faces())
        shape['line_indices'] = gloo.IndexBuffer(arrow.get_edges())
        return shape

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        for shape, trans in zip(self.shapes, self.translations):
            self.draw_shape(shape, trans)

    def draw_shape(self, shape, translation=(0, 0, 0)):
        shape['program']['view'] = self.view
        shape['program']['projection'] = self.projection
        shape['program']['model'] = self.model.dot(translate(translation))
        shape['program']['mask'] = 1
        shape['program'].draw("triangles", shape['triangle_indices'])
        shape['program']['mask'] = 0
        shape['program'].draw("lines", shape['line_indices'])


    def on_timer(self, event):
        self.time += 1 / 60
        self.model = rotate(self.time * 180 / np.pi, (0, 0, 1)).dot(
            rotate(0.4 * self.time * 180 / np.pi, (0, 1, 0))
        )
        self.show()


apka = Apka()
app.run()
