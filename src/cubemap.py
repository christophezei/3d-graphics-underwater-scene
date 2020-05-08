#!/usr/bin/env python3
# External, non built-in modules
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import numpy as np  # all matrix manipulations & OpenGL args
from PIL import Image  # load images for textures


class Cubemap:

    def __init__(self, file):
        self.glid = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.glid)
        try:
            self.__load(file)
            GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE)
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % file)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)

    def __load(self, files):
        # helper array stores texture format for every pixel size 1..4
        i = 0
        for file in files:
            # imports image as a numpy array in exactly right format
            tex = np.array(Image.open(file))
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL.GL_RGB, tex.shape[1],
                            tex.shape[0], 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, tex)
            i += 1
            message = 'Loaded texture %s\t(%s)'
            print(message % (file, tex.shape))

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)
