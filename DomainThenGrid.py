import numpy.typing as npt
from manim import *

from Grid2D import Grid2D
from GridSelector import Grid2DFuncs, Grid2DItems


class My2DGridAnim(MovingCameraScene):
    def construct(self):
        grid_carrier: npt.NDArray[Grid2D] = np.zeros((3, 3), dtype=Grid2D)

        # self.camera.frame.scale(3)

        spacing = 0.3

        for j in range(3):
            for i in range(3):
                new_grid = Grid2D((7, 7), 1)
                grid_carrier[j, i] = new_grid
                new_grid.move_to([i * (7.2 + spacing), j * (-7.2 - spacing), 0])

        #
        big_square = Square(7.2)
        #
        self.add(big_square)
        self.camera.frame.scale(1.1)
        domain_text = Text("Domain")
        domain_text.next_to(big_square, UP)
        #
        self.play(DrawBorderThenFill(VGroup(big_square, domain_text)))
        top_left_grid: Grid2D = grid_carrier[0, 0]
        cell_brace = Brace(top_left_grid.squares[0, 3], LEFT)
        cell_text = Text("Cell")
        cell_text.next_to(cell_brace, LEFT)
        for grid in grid_carrier.flatten():
            real = VGroup(*grid.squares[1:-1, 1:-1].flatten())
            real.set_fill(GREEN, opacity=1)
            exterior = Grid2DFuncs.get_edge_vgroup(grid.squares, Grid2DItems.EXTERIOR)
            exterior.set_fill(RED, opacity=1)
        self.play(DrawBorderThenFill(top_left_grid))
        self.play(FadeIn(cell_brace), FadeIn(cell_text))
        ghost_text_mv = domain_text.copy()
        ghost_text_mv.move_to(domain_text, ORIGIN)

        self.play(
            domain_text.animate.shift(3 * LEFT), ghost_text_mv.animate.shift(3 * RIGHT)
        )
        real_domain_text = Text("Real Domain")

        ghost_domain_text = Text("Ghost Domain")
        ghost_domain_text.set_fill(RED, opacity=1)

        real_domain_text.set_fill(GREEN, opacity=1)
        real_domain_text.move_to(domain_text)
        ghost_domain_text.move_to(ghost_text_mv)
        self.play(
            Transform(domain_text, real_domain_text),
            Transform(ghost_text_mv, ghost_domain_text),
        )
        # self.add(ghost_text_mv)

        self.wait(3)
        self.add(VGroup(*grid_carrier.flatten()))
        self.play(
            self.camera.frame.animate.scale(3).move_to(grid_carrier[1, 1]),
            Uncreate(VGroup(cell_brace, cell_text, domain_text, ghost_text_mv)),
        )
        middle: Grid2D = grid_carrier[1, 1]

        self.play(self.camera.frame.animate.scale(0.6).move_to(middle.get_top()))
        self.wait(3)
