#version 130

in float color_factor;
in vec4 texture_color;

out vec4 color;

uniform float ratio_shadow = 0.2;
uniform float ratio_texture = 0.6;
uniform vec4 ambiant_color;

const vec4 blanc = vec4(1.0, 1.0, 1.0, 1.0);

void main(void)
{
    color = ambiant_color
        + (blanc * ratio_shadow * color_factor)
        + (blanc * ratio_texture * texture_color);
}
