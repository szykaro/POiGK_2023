attribute vec2 pos;
attribute vec3 color;
varying vec3 v_color;
uniform float time;

void main() {
    float scale = cos(time);
    float pos_x = pos.x * scale + 0.5;
    float pos_y = pos.y * scale;
    float pos_x2 = pos_x * cos(time) - pos_y * sin(time);
    float pos_y2 = pos_x * sin(time) + pos_y * cos(time);
    gl_Position = vec4(pos_x2, pos_y2, 0, 1);
    v_color = color;
}
