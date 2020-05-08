#!/usr/bin/env python3
# Python built-in modules
from bisect import bisect_left  # search sorted keyframe lists

# External, non built-in modules
import glfw  # lean window system wrapper for OpenGL

from nodeModule import *
from transform import translate, scale, lerp, quaternion_slerp, quaternion_matrix

# -------------- Interpolator class -----------------------------------------
from project.src.transform import identity


class KeyFrames:
    """ Stores keyframe pairs for any value type with interpolation_function"""

    def __init__(self, time_value_pairs, interpolation_function=lerp):
        if isinstance(time_value_pairs, dict):  # convert to list of pairs
            time_value_pairs = time_value_pairs.items()
        keyframes = sorted(((key[0], key[1]) for key in time_value_pairs))
        self.times, self.values = zip(*keyframes)  # pairs list -> 2 lists
        self.interpolate = interpolation_function

    def value(self, time):
        """ Computes interpolated value from keyframes, for a given time """

        # 1. ensure time is within bounds else return boundary keyframe
        if time <= self.times[0]:
            return self.values[0]  # i need to return the values not the time
        if time >= self.times[-1]:
            return self.values[-1]
        # 2. search for closest index entry in self.times, using bisect_left function
        index_entry = bisect_left(self.times, time)
        # 3. using the retrieved index, interpolate between the two neighboring values
        # in self.values, using the initially stored self.interpolate function
        fraction = (time - self.times[index_entry - 1]) / (self.times[index_entry] - self.times[index_entry - 1])
        return self.interpolate(self.values[index_entry - 1], self.values[index_entry], fraction)


class TransformKeyFrames:
    """ KeyFrames-like object dedicated to 3D transforms """

    def __init__(self, translate_keys, rotate_keys, scale_keys):
        """ stores 3 keyframe sets for translation, rotation, scale """
        self.translate_keys = KeyFrames(translate_keys)
        self.rotate_keys = KeyFrames(rotate_keys, quaternion_slerp)
        self.scale_keys = KeyFrames(scale_keys)

    def value(self, time):
        """ Compute each component's interpolation and compose TRS matrix """
        translate_mat = translate(self.translate_keys.value(time))
        rotate_mat = quaternion_matrix(self.rotate_keys.value(time))
        scale_mat = scale(self.scale_keys.value(time))
        return translate_mat @ rotate_mat @ scale_mat


class KeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """

    def __init__(self, translate_keys, rotate_keys, scale_keys, **kwargs):
        super().__init__(**kwargs)
        self.keyframes = TransformKeyFrames(translate_keys, rotate_keys, scale_keys)

    def draw(self, projection, view, model, **param):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())
        super().draw(projection, view, model, **param)


# -------- Skinning Control for Keyframing Skinning Mesh Bone Transforms ------
class SkinningControlNode(Node):
    """ Place node with transfoshaderrm keys above a controlled subtree """

    def __init__(self, *keys, transform=identity()):
        super().__init__(transform=transform)
        self.keyframes = TransformKeyFrames(*keys) if keys[0] else None
        self.world_transform = identity()

    def draw(self, projection, view, model):
        """ When redraw requested, interpolate our node transform from keys """
        if self.keyframes:  # no keyframe update should happens if no keyframes
            self.transform = self.keyframes.value(glfw.get_time())

        # store world transform for skinned meshes using this node as bone
        self.world_transform = model @ self.transform

        # default node behaviour (call children's draw method)
        super().draw(projection, view, model)
