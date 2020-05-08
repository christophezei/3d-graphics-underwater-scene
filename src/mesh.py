#!/usr/bin/env python3
# External, non built-in modules
from itertools import cycle

import OpenGL.GL as GL  # standard Python OpenGL wrapper
import numpy as np
from vertex_array import VertexArray


class Mesh:

    def __init__(self, shader, attributes, index=None):
        self.shader = shader
        names = ['view', 'projection', 'model']
        self.loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.vertex_array = VertexArray(attributes, index)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)

        GL.glUniformMatrix4fv(self.loc['view'], 1, True, view)
        GL.glUniformMatrix4fv(self.loc['projection'], 1, True, projection)
        GL.glUniformMatrix4fv(self.loc['model'], 1, True, model)

        # draw triangle as GL_TRIANGLE vertex array, draw array call
        self.vertex_array.execute(primitives)


class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """

    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, [pos, col])

    def draw(self, projection, view, model, primitives=GL.GL_LINES):
        super().draw(projection, view, model, primitives)


class TexturedMesh(Mesh):
    """ Simple first textured object """

    def __init__(self, shader, texture, attributes, index=None):
        super().__init__(shader, attributes, index)

        loc = GL.glGetUniformLocation(shader.glid, 'diffuse_map')
        self.loc['diffuse_map'] = loc
        # setup texture and upload it to GPU
        self.texture = texture
        loc = GL.glGetUniformLocation(shader.glid, 'waterColor')
        self.loc['waterColor'] = loc

        loc = GL.glGetUniformLocation(shader.glid, 'shineDamper')
        self.loc['shineDamper'] = loc

        loc = GL.glGetUniformLocation(shader.glid, 'reflectivity')
        self.loc['reflectivity'] = loc

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)
        # texture access setups
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(self.loc['diffuse_map'], 0)

        waterColor = np.array(((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)), 'f')
        GL.glUniform3fv(self.loc['waterColor'], 1, waterColor)

        shineDamper = 10
        GL.glUniform1f(self.loc['shineDamper'], shineDamper)

        reflectivity = 1
        GL.glUniform1f(self.loc['reflectivity'], reflectivity)

        super().draw(projection, view, model, primitives)

        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)


class SkinnedMesh(TexturedMesh):
    """class of skinned mesh nodes in scene graph """

    def __init__(self, shader, texture, attributes, bone_nodes, bone_offsets, index=None):
        super().__init__(shader, texture, attributes, index)
        # store skinning.vert data
        self.bone_nodes = bone_nodes
        self.bone_offsets = bone_offsets

        loc = GL.glGetUniformLocation(shader.glid, 'lightPosition')
        self.loc['lightPosition'] = loc

        loc = GL.glGetUniformLocation(shader.glid, 'lightColor')
        self.loc['lightColor'] = loc

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        """ skinning.vert object draw method """
        shid = self.shader.glid
        GL.glUseProgram(shid)

        # bone world transform matrices need to be passed for skinning.vert
        for bone_id, node in enumerate(self.bone_nodes):
            bone_matrix = node.world_transform @ self.bone_offsets[bone_id]

            bone_loc = GL.glGetUniformLocation(shid, 'boneMatrix[%d]' % bone_id)
            GL.glUniformMatrix4fv(bone_loc, 1, True, bone_matrix)

        lightPosition = np.array(((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)), 'f')
        GL.glUniform3fv(self.loc['lightPosition'], 1, lightPosition)

        lightColor = np.array(((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)), 'f')
        GL.glUniform3fv(self.loc['lightColor'], 1, lightColor)
        super().draw(projection, view, model, primitives)

        # leave clean state for easier debugging
        GL.glUseProgram(0)
