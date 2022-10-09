import numpy.typing as npt
from manim import *


class Grid2D(VGroup):
    def __init__(self, grid_size: tuple[int, int], side_length: float):
        self.squares: npt.NDArray[Square] = np.zeros(grid_size, dtype=Square)
        super().__init__()
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                square = Square(side_length=side_length)
                self.squares[i, j] = square
                square.move_to((i * (side_length + 0.03), j * (side_length + 0.03), 0))

        self.add(*self.squares.flatten())
