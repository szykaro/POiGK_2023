attribute vec2 pos;
attribute vec3 color;
varying vec3 v_color;
uniform mat4 M;

void main() {
    gl_Position = M * vec4(pos, 0, 1);
    v_color = color;
}
