#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoord;

out vec2 frag_tex_coords;
out float visibility;
const float density = 0.3;
const float gradient = 1.5;


void main() {
    vec4 wordPosition = model * vec4(position, 1.0);
    vec4 positionRelativeToCam = view * wordPosition;
    gl_Position = projection * positionRelativeToCam;
    frag_tex_coords = textCoord;

    float distance = length(positionRelativeToCam.xyz);
    visibility = exp(-pow((distance*density),gradient));
    visibility = clamp(visibility,0.0, 1.0);
}
