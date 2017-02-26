#version 130

in vec4 vertex;
in vec4 normal;
in vec2 texture_coordonnees;

out float color_factor;
out vec4 texture_color;

uniform mat4 matrixpmv;
uniform vec4 light_direction;
uniform sampler2D texture2d;

void main(void)
{
    color_factor = max(dot(normal, light_direction), 0.0);

    texture_color = texture(texture2d, texture_coordonnees.st);

    gl_Position = matrixpmv * vertex;
}
