attribute vec3 pos;
attribute vec3 color;
varying vec3 v_color;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main() {
    gl_Position = projection * view * model * vec4(pos, 1);
    v_color = color;
}
