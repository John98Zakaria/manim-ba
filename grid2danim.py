import numpy as np
from manim import *

from Grid2D import Grid2D
from GridSelector import Grid2DFuncs, Grid2DItems


class My2DGridAnim(Scene):

    def construct(self):
        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))
        top_middle_grid = Grid2D((7, 7), 1)
        print(top_middle_grid.squares)
        top_middle_grid.move_to([-3, 0, 0])
        real = VGroup(*top_middle_grid.squares[1:-1, 1:-1].flatten())
        real.set_fill(GREEN, opacity=1)
        exterior = Grid2DFuncs.get_edge_vgroup(top_middle_grid.squares, Grid2DItems.EXTERIOR)

        exterior.set_fill(RED, opacity=1)
        top_middle_grid.scale(0.5)
        self.add(top_middle_grid)
        top_left_grid = top_middle_grid.copy()
        top_middle_grid.next_to(top_middle_grid, RIGHT)
        top_left_grid.set_fill(BLUE, opacity=1)
        self.add(top_left_grid)
        top_right_grid = top_middle_grid.copy()
        top_right_grid.next_to(top_middle_grid,RIGHT)
        self.add(top_right_grid)
        # self.play(Indicate(top_middle_grid.squares[0, 0]))
