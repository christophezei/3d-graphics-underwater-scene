#!/usr/bin/env python3

import glfw  # lean window system wrapper for OpenGL
from viewer import Viewer
from skybox import Skybox
from project.src.fish import BarracuddaFish, SeaSnake, BlueStarFishLoader, ReefFish0, ReefFish1
from project.src.shader import Shader

# -------------- Linear Blend Skinning : TP7 ---------------------------------
from project.src.transform import translate, vec, rotate

MAX_VERTEX_BONES = 4
MAX_BONES = 128

# new shader for skinned meshes, fully compatible with previous color fragment

SKINNING_VERT = """#version 330 core
// ---- camera geometry
uniform mat4 projection, view,model;

// ---- skinning globals and attributes
const int MAX_VERTEX_BONES=%d, MAX_BONES=%d;
uniform mat4 boneMatrix[MAX_BONES];
uniform vec3 lightPosition;
out float visibility;
const float density = 0.3;
const float gradient = 1.5;
out vec3 surfaceNormal;
out vec3 toLightVec;
out vec3 toCameraVector;


// ---- vertex attributes
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoord;
layout(location = 2) in vec4 bone_ids;
layout(location = 3) in vec4 bone_weights;
layout(location = 4) in vec3 normals;

// ----- interpolated attribute variables to be passed to fragment shader
out vec2 frag_tex_coords;

void main() {

    mat4 skinMatrix = mat4(0);
    for (int b=0; b < MAX_VERTEX_BONES; b++)
    skinMatrix +=  bone_weights[b] * boneMatrix[int(bone_ids[b])];
      
      
    // ------ compute world and normalized eye coordinates of our vertex
    vec4 wPosition4 = skinMatrix * vec4(position, 1.0);
    vec4 wordPosition = model * vec4(position, 1.0);
    vec4 positionRelativeToCam = view * wordPosition;
    gl_Position = projection * view * wPosition4;
    frag_tex_coords = textCoord;
    
    surfaceNormal = transpose(inverse(mat3(view * model))) * normals;
    toLightVec = lightPosition - wordPosition.xyz;
    toCameraVector = (inverse(view) * vec4(0.0, 0.0, 0.0, 1.0)).xyz - wordPosition.xyz;
    float distance = length(positionRelativeToCam.xyz);
    visibility = exp(-pow((distance*density),gradient));
    visibility = clamp(visibility,0.0, 1.0);
   
}
""" % (MAX_VERTEX_BONES, MAX_BONES)

SKINNING_FRAG = """
#version 330 core

uniform sampler2D diffuse_map;
uniform vec3 waterColor;
uniform vec3 lightColor;
uniform float shineDamper;
uniform float reflectivity;

in vec2 frag_tex_coords;
in vec3 surfaceNormal;
in vec3 toLightVec;
in float visibility;
in vec3 toCameraVector;
out vec4 out_color;



void main() {
  vec3 unitNormal = normalize(surfaceNormal);
  vec3 unitLight = normalize(toLightVec);
  vec4 textureColor = texture(diffuse_map, frag_tex_coords);
  float nDot1 = dot(unitNormal, unitLight);
  float brightness = max(nDot1,0.0);
  vec3 diffuse = brightness * lightColor;
  vec3 unitVectorToCamera = normalize(toCameraVector);
  vec3 lightDirection = -unitLight;
  vec3 reflectedLightDirection =  reflect(lightDirection, unitNormal);
  float specularFactor = dot(reflectedLightDirection, unitVectorToCamera);
  specularFactor = max(specularFactor, 0.0); 
  float dampedFactor = pow(specularFactor, shineDamper);
  vec3 finalSpecularFactor = dampedFactor * reflectivity * lightColor;
  
  out_color = vec4(diffuse, 1.0) * textureColor + vec4(finalSpecularFactor, 1.0);
  out_color = mix(vec4(waterColor,1.0),out_color,visibility);

}

"""


def init_BaracuddaFish():
    shader = Shader(SKINNING_VERT, SKINNING_FRAG)
    fish = BarracuddaFish(shader)
    return fish


def init_BlueStarFish():
    shader_texture = Shader("src/shaders/texture.vert", "src/shaders/texture.frag")
    fish = BlueStarFishLoader(shader_texture).get_BlueStarFish()
    return fish


def init_SeaSnake():
    shader_texture = Shader("src/shaders/texture.vert", "src/shaders/texture.frag")
    snake = SeaSnake(shader_texture)
    return snake


def init_ReefFish0():
    shader_texture = Shader("src/shaders/texture.vert", "src/shaders/texture.frag")
    fish = ReefFish0(shader_texture)
    return fish


def init_ReefFish1():
    shader_texture = Shader("src/shaders/texture.vert", "src/shaders/texture.frag")
    fish = ReefFish1(shader_texture)
    return fish


def main():
    """ create a window, add scene objects, then run rendering loop """

    viewer = Viewer(1900, 1200)
    viewer.add((init_BaracuddaFish()))
    viewer.add(init_BlueStarFish())
    viewer.add(init_SeaSnake())
    viewer.add_movable(init_ReefFish0())
    viewer.add_movable(init_ReefFish1())

    under_water = [
        'res/skybox/underwater/uw_lf.jpg',
        'res/skybox/underwater/uw_rt.jpg',
        'res/skybox/underwater/uw_up.jpg',
        'res/skybox/underwater/uw_dn.jpg',
        'res/skybox/underwater/uw_ft.jpg',
        'res/skybox/underwater/uw_bk.jpg']
    viewer.add(Skybox(under_water))

    viewer.run()


if __name__ == '__main__':
    glfw.init()  # initialize window system glfw
    main()  # main function keeps variables locally scoped
    glfw.terminate()  # destroy all glfw windows and GL contexts
