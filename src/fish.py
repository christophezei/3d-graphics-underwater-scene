from transform import scale, rotate
from nodeModule import *

from project.src.keyframe import KeyFrameControlNode, TransformKeyFrames
from project.src.loaders import load_skinned, load_textured
from project.src.transform import translate, vec, quaternion_from_euler, identity


class BarracuddaFish(Node):
    """Barracudda Fish"""

    def __init__(self, shader):
        super().__init__(transform=(scale(0.0007) @ rotate((0.0, 1.0, 0.0), -80)))
        barraccuda_object_text = "res/Fish/Barracuda/Barracuda_Base Color.png"
        barraccuda_object = 'res/Fish/Barracuda/Barracuda2anim.fbx'
        self.add(*load_skinned(barraccuda_object, shader, barraccuda_object_text))


class BlueStarFish(Node):
    """Star Fish"""

    def __init__(self, shader):
        super().__init__(transform=(scale(0.12) @ translate(-5, -0.3, -5.5) @ rotate((1.0, 0.2, 0.0), 80)))
        bluestarfish_object_text = "res/Fish/BlueStarfish/BlueStarfish_Normal_DirectX.png"
        bluestarfish_object = 'res/Fish/BlueStarfish/BluieStarfish.obj'
        self.add(*load_textured(bluestarfish_object, shader, bluestarfish_object_text))


class BlueStarFishLoader():
    def __init__(self, shader_text):
        self.starFish = BlueStarFish(shader_text)
        translate_BlueFish = {0: vec(0, 0, 0), 20: vec(0.8, 1, -.85)}

        rotate_BlueFish = {0: quaternion_from_euler(0, 0, 0), 4: quaternion_from_euler(0, 0, 10),
                           10: quaternion_from_euler(0, 65, 0), 20: quaternion_from_euler(0, 180, 0)}

        keynode = KeyFrameControlNode(translate_BlueFish, rotate_BlueFish, {0: 1, 15: 0.7})
        keynode.add(self.starFish)
        self.starFish = keynode

    def get_BlueStarFish(self):
        return self.starFish


class SeaSnake(Node):
    """Sea snake"""

    def __init__(self, shader):
        super().__init__(transform=(scale(0.07) @ translate(-5, -0.3, 8.5) @ rotate((1.0, 1.0, 0.0), 90)))
        sea_snake_object_text = "res/Fish/SeaSnake/SeaSnake_Base_Color.png"
        sea_snake_object = 'res/Fish/SeaSnake/seasnake.obj'
        self.add(*load_textured(sea_snake_object, shader, sea_snake_object_text))


class ReefFish0(Node):
    def __init__(self, shader):
        super().__init__(transform=(scale(0.05) @ translate(-6.5, -6.5, -20.0) @rotate((0.0, 1.0, 0.0), 80)))
        reef_fish_0_object_text = "res/Fish/ReefFish0/reefFish0_Normal.png"
        reef_fish_0_object = 'res/Fish/ReefFish0/ReefFish0.obj'
        self.add(*load_textured(reef_fish_0_object, shader, reef_fish_0_object_text))


class ReefFish1(Node):
    def __init__(self, shader):
        super().__init__(transform=(scale(0.05) @ translate(-12, -6.5, -20.0) @rotate((0.0, 1.0, 0.0), 80)))
        reef_fish_1_object_text = "res/Fish/ReefFish3/ReefFish3_Base_Color.png"
        reef_fish_1_object = 'res/Fish/ReefFish3/ReefFish3.obj'
        self.add(*load_textured(reef_fish_1_object, shader, reef_fish_1_object_text))
