from enum import auto

import numpy.typing as npt
from manim import *

from Grid2D import Grid2D
from GridSelector import Grid2DFuncs, Grid2DItems


class Direction(Enum):
    TOP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def build_right_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x - 1):
        for j in range(y):
            left_square: Grid2D = grid_carrier[j, i]
            right_square: Grid2D = grid_carrier[j, i + 1]
            left_to_right_start = left_square.squares[-2, 3].get_center()
            left_to_right_end = right_square.squares[0, 3].get_center()
            arrows.append(CurvedArrow(left_to_right_start, left_to_right_end))

    return arrows


def build_left_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x - 1, 0, -1):
        for j in range(y):
            right_square: Grid2D = grid_carrier[j, i]
            left_square: Grid2D = grid_carrier[j, i - 1]
            right_to_left_start = right_square.squares[1, 3].get_center()
            right_to_left_end = left_square.squares[-1, 3].get_center()
            arrows.append(CurvedArrow(right_to_left_start, right_to_left_end))

    return arrows


def build_down_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x):
        for j in range(y - 1):
            top_square: Grid2D = grid_carrier[j, i]
            lower_square: Grid2D = grid_carrier[j + 1, i]
            top_down_start = top_square.squares[3, 1].get_center()
            top_down_end = lower_square.squares[3, -1].get_center()
            arrows.append(CurvedArrow(top_down_start, top_down_end))

    return arrows


def build_up_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x):
        for j in range(y - 1):
            top_square: Grid2D = grid_carrier[j, i]
            lower_square: Grid2D = grid_carrier[j + 1, i]
            top_down_start = top_square.squares[3, 0].get_center()
            top_down_end = lower_square.squares[3, -2].get_center()
            arrows.append(CurvedArrow(top_down_end, top_down_start))

    return arrows


def build_grid_items(grid_carrier: npt.NDArray[Grid2D], side1: Grid2DItems):
    sides_grid = np.zeros_like(grid_carrier)
    y, x = grid_carrier.shape
    for i in range(x):
        for j in range(y):
            sides_grid[j, i] = Grid2DFuncs.get_edge_vgroup(
                grid_carrier[j, i].squares, side1
            )
    return sides_grid


def make_dots_across_path(path: Mobject):
    three_dots = [Dot(color=YELLOW), Dot(color=YELLOW), Dot(color=YELLOW)]
    animations = [MoveAlongPath(dot, path) for dot in three_dots]
    return LaggedStart(*animations), three_dots


def flatten_n(iterable, index):
    for item in iterable:
        yield item[index]


class SyncComm(MovingCameraScene):
    def construct(self):
        grid_carrier = np.zeros((2, 3), dtype=Grid2D)

        # self.camera.frame.scale(3)

        spacing_x = 1
        spacing_y = 2
        rank_counter = 0
        grid_texts: list[Text] = []
        state_texts: list[Text] = []
        for j in range(2):
            for i in range(3):
                new_grid = Grid2D((7, 7), 1)
                grid_carrier[j, i] = new_grid
                new_grid.move_to([i * (7.2 + spacing_x), j * (-7.2 - spacing_y), 0])
                rank_text = Text(f"Rank {rank_counter}")
                rank_counter += 1
                state_text = Text(f"INTEGRATE1", color=BLUE)
                state_text.next_to(new_grid, UP)
                rank_text.next_to(state_text, UP)
                state_texts.append(state_text)
                grid_texts.append(rank_text)

        for grid in grid_carrier.flatten():
            real = VGroup(*grid.squares[1:-1, 1:-1].flatten())
            real.set_fill(GREEN, opacity=1)
            exterior = Grid2DFuncs.get_edge_vgroup(grid.squares, Grid2DItems.EXTERIOR)
            exterior.set_fill(RED, opacity=1)
        lower_middle: Grid2D = grid_carrier[1, 1]

        self.camera.frame.scale(2.7).move_to(lower_middle.get_top() + [0, 2, 0])

        self.add(*grid_carrier.flatten(), *grid_texts, *state_texts)

        self.play(
            *[
                Transform(state, Text("COMM1", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )
        self.play(
            *[
                Transform(state, Text("FORCE", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )
        self.play(
            *[
                Transform(state, Text("COMM2", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )
        self.play(
            *[
                Transform(state, Text("INTEGRATE2", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )
        self.play(
            *[
                Transform(state, Text("COMM2", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )
        self.play(
            *[
                Transform(state, Text("COMM1", color=BLUE).move_to(state))
                for state in state_texts
            ]
        )

        self.play(
            Transform(
                state_texts[2], Text("COMM1: RIGHT", color=BLUE).move_to(state_texts[2])
            ),
            Transform(
                state_texts[1], Text("COMM1: RIGHT", color=BLUE).move_to(state_texts[1])
            ),
            Transform(
                state_texts[0], Text("COMM1: RIGHT", color=BLUE).move_to(state_texts[0])
            ),
            Transform(
                state_texts[4], Text("COMM1: DOWN", color=BLUE).move_to(state_texts[4])
            ),
        )
        down_arrows = build_down_arrows(grid_carrier)
        up_arrows = build_up_arrows(grid_carrier)
        right_arrows = build_right_arrows(grid_carrier)
        left_arrows = build_left_arrows(grid_carrier)
        left_arrows[0].get_center()
        left_arrow_free = CurvedArrow(
            grid_carrier[0, -1].squares[-1, 3].get_center() + [3, 0, 0],
            grid_carrier[0, -1].squares[-1, 3].get_center(),
        )

        self.play(Create(left_arrow_free.set_color(BLUE)))
        self.wait(1)
        self.play(Create(down_arrows[1].set_color(BLUE)))
        self.wait(1)
        self.play(Create(right_arrows[0]))
        dots_animation, dots = make_dots_across_path(right_arrows[0])
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(right_arrows[0])

        self.play(Transform(
            state_texts[0], Text("COMM1: LEFT", color=BLUE).move_to(state_texts[0])
        ), )

        self.play(Create(right_arrows[2]))
        self.wait(1)
        dots_animation, dots = make_dots_across_path(right_arrows[2])
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(right_arrows[2])



        self.wait(1)
        dots_animation, dots = make_dots_across_path(left_arrow_free)
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(left_arrow_free)

        self.play(
            Transform(
                state_texts[2], Text("COMM1: LEFT", color=BLUE).move_to(state_texts[2])
            ),
            Transform(
                state_texts[1], Text("COMM1: LEFT", color=BLUE).move_to(state_texts[1])
            ),

        )

        self.wait(1)

        self.play(Create(left_arrows[2]))
        dots_animation, dots = make_dots_across_path(left_arrows[2])
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(left_arrows[2])

        self.play(Transform(
                state_texts[0], Text("COMM1: DOWN", color=BLUE).move_to(state_texts[0])
            ),)

        self.play(Create(left_arrows[0]))
        dots_animation, dots = make_dots_across_path(left_arrows[0])
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(left_arrows[0])

        self.play(
            Transform(
                state_texts[2], Text("COMM1: DOWN", color=BLUE).move_to(state_texts[2])
            ),
            Transform(
                state_texts[1], Text("COMM1: DOWN", color=BLUE).move_to(state_texts[1])
            ),

        )

        dots_animation, dots = make_dots_across_path(down_arrows[1])
        self.play(dots_animation, run_time=1)
        self.remove(*dots)
        self.remove(down_arrows[1])

        self.wait(3)
