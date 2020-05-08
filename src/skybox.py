#!/usr/bin/env python3

# External, non built-in modules
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import numpy as np

from cubemap import Cubemap
from shader import Shader
from vertex_array import VertexArray

vertex_shad = """#version 330 core
layout (location = 0) in vec3 position;

out vec3 fragTextureCoord;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out float visibility;
const float density = 0.3;
const float gradient = 1.5;

void main() {
    fragTextureCoord = position;
    vec4 positionRelativeToCam = view * model * vec4(position, 1.0);
    gl_Position = projection * positionRelativeToCam;
    float distance = length(positionRelativeToCam.xyz);
    visibility = exp(-pow((distance*density),gradient));
    visibility = clamp(visibility,0.0, 1.0);
   
}
"""

frag_shad = """#version 330 core
out vec4 color;
in float visibility;
uniform vec3 waterColor;
in vec3 fragTextureCoord;

uniform samplerCube skybox;

void main() {
    color = texture(skybox, fragTextureCoord);
    color = mix(vec4(waterColor,1.0),color,visibility);
}
"""

def_vertices = np.array((
    (-1.0, 1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),

    (-1.0, -1.0, 1.0),
    (-1.0, -1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, 1.0, 1.0),
    (-1.0, -1.0, 1.0),

    (1.0, -1.0, -1.0),
    (1.0, -1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, -1.0),
    (1.0, -1.0, -1.0),

    (-1.0, -1.0, 1.0),
    (-1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, -1.0, 1.0),
    (-1.0, -1.0, 1.0),

    (-1.0, 1.0, -1.0),
    (1.0, 1.0, -1.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 1.0, 1.0),
    (-1.0, 1.0, -1.0),

    (-1.0, -1.0, -1.0),
    (-1.0, -1.0, 1.0),
    (1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (-1.0, -1.0, 1.0),
    (1.0, -1.0, 1.0)), 'f')


class Skybox:
    def __init__(self, files, attributes=[def_vertices]):
        self.shader = Shader(vertex_shad, frag_shad)
        self.vertex_array = VertexArray(attributes)
        self.cubemap = Cubemap(files)

    def draw(self, projection, view, model):
        """ Draw object """
        GL.glDepthFunc(GL.GL_LEQUAL)

        GL.glUseProgram(self.shader.glid)

        # projection geometry
        loc = GL.glGetUniformLocation(self.shader.glid, 'model')
        np.resize(view, (3, 3))
        np.resize(view, (4, 4))
        #  GL.glUniformMatrix4fv(loc, 1, True, projection @ view @ np.identity(4, 'f'))
        GL.glUniformMatrix4fv(loc, 1, True, model)
        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)
        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)

        loc = GL.glGetUniformLocation(self.shader.glid, 'waterColor')
        waterColor = np.array(((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)), 'f')
        GL.glUniform3fv(loc, 1, waterColor)

        loc = GL.glGetUniformLocation(self.shader.glid, 'skybox')
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.cubemap.glid)
        GL.glUniform1i(loc, 0)

        self.vertex_array.execute(GL.GL_TRIANGLES)

        GL.glDepthFunc(GL.GL_LESS)

        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)
        GL.glUseProgram(0)
