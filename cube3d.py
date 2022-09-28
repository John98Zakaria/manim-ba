from manim import *
from manim_rubikscube import *

from CubeSelector import DomainDecomposer, CubeFace


class TenDimensionalExample(ThreeDScene):
    def construct(self):
        left = RubiksCube(7).scale(0.3)
        right = RubiksCube(7).scale(0.3)

        left.move_to([1, -4, 0])
        # right.move_to(left, RIGHT)
        right.move_to([1, -4, -2])
        # left.rotate_about_origin(45,Z_AXIS)
        # self.move_camera(phi=50*DEGREES, theta=160*DEGREES)
        # self.begin_ambient_camera_rotation(rate=0.3)
        # self.set_camera_orientation(phi=-60 * DEGREES,theta=5 *DEGREES, zoom=-0.5)
        self.set_camera_orientation(zoom=-0.5)
        # left.rotate_about_origin(-180 * DEGREES, Z_AXIS)
        self.play(
            FadeIn(left), FadeIn(right)
        )
        self.wait()

        # Because get_face() returns an array of Cubie objects, they must
        # be added to a VGroup before an animation can be called on all
        # of them simultaneously

        # interior = VGroup(*(left.cubies[1:-1,1:-1,1:-1]).flatten())
        face = VGroup(*DomainDecomposer.select_attribute(left.cubies, CubeFace.TOP_UPPER_LEFT_CORNER))

        self.play(
            Indicate(face)
        )
        face.set_opacity(0.3, )

        self.wait()
