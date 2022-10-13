from enum import auto

import numpy as np
import numpy.typing as npt
from manim import *

from Grid2D import Grid2D
from GridSelector import Grid2DFuncs, Grid2DItems


class Direction(Enum):
    TOP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def build_left_arrows(grid_carrier: npt.NDArray[Grid2D]):
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


def build_right_arrows(grid_carrier: npt.NDArray[Grid2D]):
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
        spacing_y = 1.5
        rank_counter = 0
        grid_text: list[Text] = []
        for j in range(2):
            for i in range(3):
                new_grid = Grid2D((7, 7), 1)
                grid_carrier[j, i] = new_grid
                new_grid.move_to([i * (7.2 + spacing_x), j * (-7.2 - spacing_y), 0])
                rank_text = Text(f"Rank {rank_counter}")
                grid_text.append(rank_text)
                rank_counter += 1
                rank_text.next_to(new_grid, UP)

        for grid in grid_carrier.flatten():
            real = VGroup(*grid.squares[1:-1, 1:-1].flatten())
            real.set_fill(GREEN, opacity=1)
            exterior = Grid2DFuncs.get_edge_vgroup(grid.squares, Grid2DItems.EXTERIOR)
            exterior.set_fill(RED, opacity=1)
        lower_middle: Grid2D = grid_carrier[1, 1]

        top_right: Grid2D = grid_carrier[0, -1]
        current_direction_text = Text("Direction:", weight=BOLD).scale(1.3)
        current_direction = Text("RIGHT", color=YELLOW)  # Inverted lists names

        current_direction_text.next_to(top_right.get_right() + [2, 3, 0], RIGHT)
        current_direction.next_to(current_direction_text, DOWN, 7)

        self.add(current_direction_text, current_direction)

        self.camera.frame.scale(2.7).move_to(lower_middle.get_top() + [5, 2, 0])

        self.add(*grid_carrier.flatten(), *grid_text)

        # RIGHT SIDE

        # left_arrows = build_left_arrows(grid_carrier)
        # left_sides = build_grid_items(grid_carrier, Grid2DItems.REAL_RIGHT_EDGE)
        # right_sides = build_grid_items(grid_carrier, Grid2DItems.GHOST_LEFT_EDGE)
        # self.play(*[Indicate(edge) for edge in left_sides[:, ::2].flatten()], run_time=2)
        # self.wait(1)
        # self.play(*(Create(arrow) for arrow in left_arrows[:2]))
        # self.absolute_front(left_arrows[:2])
        # self.wait(1)
        # self.play(
        #     *[Indicate(edge) for edge in right_sides[:, 1].flatten()], run_time=2
        # )
        # self.wait(1)
        # dots_animations = [make_dots_across_path(arrow) for arrow in left_arrows[:2]]
        #
        # self.play(*flatten_n(dots_animations, 0), run_time=1)
        # self.remove(*left_arrows[:2])
        # self.remove_dots(dots_animations)
        # self.play(*(Create(arrow) for arrow in left_arrows[2:]))
        #
        # dots_animations = [make_dots_across_path(arrow) for arrow in left_arrows[2:]]
        #
        # self.play(*flatten_n(dots_animations, 0), run_time=1)
        # self.remove_dots(dots_animations)
        # self.remove(*left_arrows[2:])

        # LEFT SIDE

        right_sides = build_grid_items(grid_carrier, Grid2DItems.GHOST_RIGHT_EDGE)
        left_sides = build_grid_items(grid_carrier, Grid2DItems.REAL_LEFT_EDGE)
        self.play(
            Transform(
                current_direction, Text("LEFT", color=YELLOW).move_to(current_direction)
            )
        )
        self.play(*[Indicate(edge) for edge in left_sides[:, 1].flatten()], run_time=2)
        right_arrows = build_right_arrows(grid_carrier)
        self.absolute_front(right_arrows[2:])
        self.play(*((Create(arrow) for arrow in right_arrows[2:])))
        self.play(*[Indicate(edge) for edge in right_sides[:, 0].flatten()], run_time=2)
        dots_animations = [make_dots_across_path(arrow) for arrow in right_arrows[2:]]
        self.play(*flatten_n(dots_animations, 0), run_time=1)
        for dots in flatten_n(dots_animations, 1):
            self.remove(*dots)
        self.remove(*right_arrows)

        self.play(*[Indicate(edge) for edge in left_sides[:, 2].flatten()], run_time=2)
        right_arrows = build_right_arrows(grid_carrier)
        self.play(*((Create(arrow) for arrow in right_arrows[:2])))
        self.absolute_front(right_arrows[:2])
        self.play(*[Indicate(edge) for edge in right_sides[:, 1].flatten()], run_time=2)
        dots_animations = [make_dots_across_path(arrow) for arrow in right_arrows[:2]]
        self.play(*flatten_n(dots_animations, 0), run_time=1)
        for dots in flatten_n(dots_animations, 1):
            self.remove(*dots)
        self.remove(*right_arrows)

        self.play(
            Transform(
                current_direction, Text("DOWN", color=YELLOW).move_to(current_direction)
            )
        )

        down_arrows = build_down_arrows(grid_carrier)
        lower_sides = build_grid_items(grid_carrier, Grid2DItems.LOWER_REAL_BOTH)
        top_sides = build_grid_items(grid_carrier, Grid2DItems.TOP_GHOST_BOTH)
        self.play(
            Transform(
                current_direction, Text("DOWN", color=YELLOW).move_to(current_direction)
            )
        )
        self.play(
            *[Indicate(edge, scale_factor=1.1) for edge in lower_sides[0, :].flatten()],
            run_time=2,
        )
        self.play(*((Create(arrow) for arrow in down_arrows)))
        self.absolute_front(down_arrows)
        self.play(
            *[
                Indicate(edge, scale_factor=1.1)
                for edge in top_sides[
                    1:,
                ].flatten()
            ],
            run_time=2,
        )

        dots_animations = [make_dots_across_path(arrow) for arrow in down_arrows]
        self.play(*flatten_n(dots_animations, 0), run_time=1)
        for dots in flatten_n(dots_animations, 1):
            self.remove(*dots)
        self.remove(*down_arrows)
        self.wait(3)

    def remove_dots(self, dots_animations):
        for dots in flatten_n(dots_animations, 1):
            self.remove(*dots)

    def absolute_front(self, arrows_list):
        for arrow in arrows_list:
            self.add_foreground_mobject(arrow)
