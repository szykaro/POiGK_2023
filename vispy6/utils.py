import numpy as np


def generate_triangles():
    triangles = []
    initial_vertices = [[1] * 3, [-1] * 3]
    for first in initial_vertices:
        for i in range(3):
            second = first.copy()
            second[i] = -first[i]
            for j in range(3):
                if i == j:
                    continue
                third = second.copy()
                third[j] = -second[j]
                triangle = [first, second, third]
                triangles.extend(triangle)
    triangles = np.array(triangles, dtype=np.float32)
    return triangles


def generate_lines():
    lines = []
    initial_lines = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    for first in initial_lines:
        for i in range(3):
            second = first.copy()
            second[i] = -first[i]
            line = [first, second]
            lines.extend(line)
    lines = np.array(lines, dtype=np.float32)
    return lines
