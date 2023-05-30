attribute vec3 pos;
attribute vec2 texcoord;
varying vec2 v_texcoord;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main() {
    gl_Position = projection * view * model * vec4(pos, 1);
    v_texcoord = texcoord;
}
