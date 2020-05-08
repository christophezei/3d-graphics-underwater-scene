#version 330 core

uniform sampler2D diffuse_map;
uniform vec3 waterColor;

in vec2 frag_tex_coords;
in float visibility;
out vec4 out_color;

void main() {
  vec4 textureColor = texture(diffuse_map, frag_tex_coords);
  out_color = textureColor;
  out_color = mix(vec4(waterColor,1.0),out_color,visibility);

}
