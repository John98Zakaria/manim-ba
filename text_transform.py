import numpy as np
from manim import *

from Grid2D import Grid2D
from GridSelector import Grid2DFuncs, Grid2DItems


class TextTransform(MovingCameraScene):

    def construct(self):

        self.camera.frame.scale(1.1)
        domain_text = Text("Domain")

        real_domain_text = Text("Real Domain")
        real_domain_text.set_fill(GREEN,opacity=1)
        transform = Transform(domain_text, real_domain_text)
        self.play(transform)
        self.play(domain_text.animate.shift(LEFT))
        # right_grid = Grid2D((7, 7), 1)
        # right_grid.move_to((7.5, 0, 0))
        #
        # self.play(Create(right_grid))
        self.wait(3)
