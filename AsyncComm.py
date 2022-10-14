import itertools
import random
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
            start = top_square.squares[3, 1].get_center()
            end = lower_square.squares[3, -1].get_center()
            arrows.append(CurvedArrow(start, end))

    return arrows


def build_up_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x):
        for j in range(y - 1):
            top_square: Grid2D = grid_carrier[j, i]
            lower_square: Grid2D = grid_carrier[j + 1, i]
            start = top_square.squares[3, 0].get_center()
            end = lower_square.squares[3, -2].get_center()
            arrows.append(CurvedArrow(end, start))

    return arrows


def build_down_right_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x - 1):
        for j in range(y - 1):
            top_square: Grid2D = grid_carrier[j, i]
            lower_square: Grid2D = grid_carrier[j + 1, i + 1]
            start = top_square.squares[-2, 1].get_center()
            end = lower_square.squares[0, -1].get_center()
            arrows.append(CurvedArrow(start, end))

    return arrows


def build_down_left_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(1, x):
        for j in range(y - 1):
            top_square: Grid2D = grid_carrier[j, i]
            lower_square: Grid2D = grid_carrier[j + 1, i - 1]
            start = top_square.squares[1, 1].get_center()
            end = lower_square.squares[-1, -1].get_center()
            arrows.append(CurvedArrow(start, end))

    return arrows


def build_up_left_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(1, x):
        for j in range(1, y):
            top_square: Grid2D = grid_carrier[j - 1, i - 1]
            lower_square: Grid2D = grid_carrier[j, i]
            start = lower_square.squares[1, -2].get_center()
            end = top_square.squares[-1, 0].get_center()
            arrows.append(CurvedArrow(start, end))

    return arrows


def build_up_right_arrows(grid_carrier: npt.NDArray[Grid2D]):
    y, x = grid_carrier.shape
    arrows: list[CurvedArrow] = []
    for i in range(x - 1):
        for j in range(1, y):
            top_square: Grid2D = grid_carrier[j - 1, i + 1]
            lower_square: Grid2D = grid_carrier[j, i]
            start = lower_square.squares[-2, -2].get_center()
            end = top_square.squares[0, 0].get_center()
            arrows.append(CurvedArrow(start, end))

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
    return LaggedStart(*animations), three_dots, path


def flatten_n(iterable, index):
    for item in iterable:
        yield item[index]


class AsyncComm(MovingCameraScene):
    def construct(self):
        grid_carrier = np.zeros((2, 3), dtype=Grid2D)

        spacing_x = 1
        spacing_y = 1.5
        rank_counter = 0
        grid_texts: list[Text] = []
        state_texts: list[Text] = []
        for j in range(2):
            for i in range(3):
                new_grid = Grid2D((7, 7), 1)
                grid_carrier[j, i] = new_grid
                new_grid.move_to([i * (7.2 + spacing_x), j * (-7.2 - spacing_y), 0])
                rank_text = Text(f"Rank {rank_counter}").scale(1.2)
                rank_counter += 1
                rank_text.next_to(new_grid, UP)
                grid_texts.append(rank_text)

        for grid in grid_carrier.flatten():
            real = VGroup(*grid.squares[1:-1, 1:-1].flatten())
            real.set_fill(GREEN, opacity=1)
            exterior = Grid2DFuncs.get_edge_vgroup(grid.squares, Grid2DItems.EXTERIOR)
            exterior.set_fill(RED, opacity=1)
        lower_middle: Grid2D = grid_carrier[1, 1]

        self.camera.frame.scale(2.7).move_to(lower_middle.get_top() + [0, 1, 0])

        self.add(*grid_carrier.flatten(), *grid_texts)

        down_arrows = build_down_arrows(grid_carrier)
        down_right_arrows = build_down_right_arrows(grid_carrier)
        down_left_arrows = build_down_left_arrows(grid_carrier)
        up_arrows = build_up_arrows(grid_carrier)
        up_left = build_up_left_arrows(grid_carrier)
        up_right = build_up_right_arrows(grid_carrier)
        left_arrows = build_left_arrows(grid_carrier)
        right_arrows = build_right_arrows(grid_carrier)

        animation_down_arrows_dots = [make_dots_across_path(arrow) for arrow in down_arrows]
        animation_up_arrows_dots = [make_dots_across_path(arrow) for arrow in up_arrows]
        animation_up_right_dots = [make_dots_across_path(arrow) for arrow in up_right]
        animation_up_left_dots = [make_dots_across_path(arrow) for arrow in up_left]
        animation_down_left_arrows_dots = [make_dots_across_path(arrow) for arrow in down_left_arrows]
        animation_down_right_arrows_dots = [make_dots_across_path(arrow) for arrow in down_right_arrows]
        animation_left_arrows_dots = [make_dots_across_path(arrow) for arrow in left_arrows]
        animation_right_arrows_dots = [make_dots_across_path(arrow) for arrow in right_arrows]

        self.wait(2)

        random.seed(13)

        everything = list(
            itertools.chain(animation_down_arrows_dots,
                            animation_up_arrows_dots,
                            animation_up_right_dots,
                            animation_up_left_dots,
                            animation_down_left_arrows_dots,
                            animation_down_right_arrows_dots,
                            animation_left_arrows_dots,
                            animation_right_arrows_dots))

        random.shuffle(everything)

        arrow1_group = list(flatten_n(everything[:5], 2))
        animation1_group = list(flatten_n(everything[:5], 0))
        dots1_group = list(flatten_n(everything[:5], 1))
        arrow2_group = list(flatten_n(everything[5:13], 2))
        animation2_group = list(flatten_n(everything[5:13], 0))
        dots2_group = list(flatten_n(everything[5:13], 1))
        arrow3_group = list(flatten_n(everything[13:], 2))
        animation3_group = list(flatten_n(everything[13:], 0))
        dots3_group = list(flatten_n(everything[13:], 1))

        self.orechstare_animation(animation1_group, arrow1_group, dots1_group)
        self.orechstare_animation(animation2_group, arrow2_group, dots2_group)
        self.orechstare_animation(animation3_group, arrow3_group, dots3_group)

        self.wait(3)


    def orechstare_animation(self, animation1_group, arrow1_group, dots1_group):
        self.play(*(Create(arrow) for arrow in arrow1_group))
        self.play(LaggedStart(*animation1_group,lag_ratio=0.4))
        for dots_group in dots1_group:
            self.remove(*dots_group)
        self.remove(*arrow1_group)
