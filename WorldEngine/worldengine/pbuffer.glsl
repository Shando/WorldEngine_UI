#version 130

uniform vec2 pbuffer_size;

out vec4 color;

void main(void)
{
    vec2 FragCoord = vec2(gl_FragCoord.x / pbuffer_size.x - 0.5, gl_FragCoord.y / pbuffer_size.y - 0.5);
    float radius = sqrt(FragCoord.x * FragCoord.x + FragCoord.y * FragCoord.y);
    float gray = sin(radius * 200.0);

    color = vec4(FragCoord.x * gray, FragCoord.y * gray, 0.0, 1.0);
}
