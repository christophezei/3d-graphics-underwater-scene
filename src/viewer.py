#!/usr/bin/env python3
"""
Viewer class & window management
"""
# Python built-in modules
from itertools import cycle

# External, non built-in modules
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
from nodeModule import *
from trackball import GLFWTrackball
from transform import identity, translate, rotate, vec


class Viewer(Node):
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):
        super().__init__()

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)
        self.drawables = []
        self.movables = []

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        # initialize trackball
        self.trackball = GLFWTrackball(self.win)

        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])
        self.model = identity()

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            # draw our scene objects
            # self.draw(projection, view, identity())

            for movable in self.movables:
                movable.draw(projection, view, self.model)

                # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(projection, view, identity())

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def add_movable(self, movable):
        self.movables.append(movable)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_D:
                self.model = self.model @ translate(0.01, 0, 0)
            if key == glfw.KEY_A:
                self.model = self.model @ translate(-0.01, 0, 0)
            if key == glfw.KEY_W:
                self.model = self.model @ translate(0, 0, 0.01)
            if key == glfw.KEY_S:
                self.model = self.model @ translate(0, 0, -0.01)
            if key == glfw.KEY_E:
                self.model = self.model @ translate(0, 0.01, 0)
            if key == glfw.KEY_F:
                self.model = self.model @ translate(0, -0.01, 0)
            if key == glfw.KEY_Z:
                self.model = self.model @ rotate(vec(1, 0, 0), 10)
            if key == glfw.KEY_X:
                self.model = self.model @ rotate(vec(0, 1, 0), 10)
            if key == glfw.KEY_C:
                self.model = self.model @ rotate(vec(0, 0, 1), 10)
            if key == glfw.KEY_SPACE:
                glfw.set_time(0)
