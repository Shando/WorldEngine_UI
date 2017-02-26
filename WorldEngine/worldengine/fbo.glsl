#version 130

uniform vec2 fbo_size;

out vec4 color;

void main(void)
{
    vec2 FragCoord = vec2(gl_FragCoord.x / fbo_size.x - 0.5, gl_FragCoord.y / fbo_size.y - 0.5);
    float radius = sqrt(FragCoord.x * FragCoord.x + FragCoord.y * FragCoord.y);
    float gray = sin(radius * 200.0);

    color = vec4(0.0, FragCoord.x * gray, FragCoord.y * gray, 1.0);
}
