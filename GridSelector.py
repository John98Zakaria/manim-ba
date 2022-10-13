from enum import Enum, auto

import numpy as np
from manim import VGroup


class Grid2DItems(Enum):
    GHOST_LEFT_EDGE = auto()
    REAL_LEFT_EDGE = auto()
    GHOST_RIGHT_EDGE = auto()
    REAL_RIGHT_EDGE = auto()
    GHOST_TOP_EDGE = auto()
    REAL_TOP_EDGE = auto()
    GHOST_BOTTOM_EDGE = auto()
    REAL_BOTTOM_EDGE = auto()
    INTERIOR = auto()
    EXTERIOR = auto()
    LOWER_REAL_GHOST = auto()
    LOWER_REAL_BOTH = auto()
    TOP_GHOST_BOTH = auto()


class Grid2DFuncs:
    @staticmethod
    def get_edge(squares: np.ndarray, item: Grid2DItems):
        selection = np.zeros(0)
        match item:
            case Grid2DItems.GHOST_LEFT_EDGE:
                selection = squares[0, 1:-1]
            case Grid2DItems.GHOST_RIGHT_EDGE:
                selection = squares[-1, 1:-1]
            case Grid2DItems.GHOST_TOP_EDGE:
                selection = squares[1:-1, -1]
            case Grid2DItems.GHOST_BOTTOM_EDGE:
                selection = squares[1:-1, 0]
            case Grid2DItems.REAL_LEFT_EDGE:
                selection = squares[1, 1:-1]
            case Grid2DItems.REAL_RIGHT_EDGE:
                selection = squares[-2, 1:-1]
            case Grid2DItems.REAL_TOP_EDGE:
                selection = squares[1:-1, -2]
            case Grid2DItems.REAL_BOTTOM_EDGE:
                selection = squares[1:-1, 1]
            case Grid2DItems.INTERIOR:
                selection = squares[1:-1, 1:-1]
            case Grid2DItems.EXTERIOR:
                mask = np.ones(squares.shape, dtype=bool)
                mask[1:-1, 1:-1] = False
                selection = squares[mask]
            case Grid2DItems.LOWER_REAL_BOTH:
                selection = squares[:, 1]
            case Grid2DItems.TOP_GHOST_BOTH:
                selection = squares[:, -1]
        return selection

    @staticmethod
    def get_edge_vgroup(squares: np.ndarray, item: Grid2DItems):
        return VGroup(*Grid2DFuncs.get_edge(squares, item).flatten())
