from enum import Enum, auto

import numpy as np


class CubeFace(Enum):
    BOTTOM_FACE = auto()
    BOTTOM_LOWER_EDGE = auto()
    BOTTOM_LEFT_EDGE = auto()
    BOTTOM_UPPER_EDGE = auto()
    BOTTOM_RIGHT_EDGE = auto()
    TOP_FACE = auto()
    TOP_LOWER_EDGE = auto()
    TOP_LEFT_EDGE = auto()
    TOP_UPPER_EDGE = auto()
    TOP_RIGHT_EDGE = auto()
    LEFT_FACE = auto()
    LEFT_LOWER_EDGE = auto()
    LEFT_LEFT_EDGE = auto()
    LEFT_UPPER_EDGE = auto()
    LEFT_RIGHT_EDGE = auto()
    RIGHT_FACE = auto()
    RIGHT_LOWER_EDGE = auto()
    RIGHT_LEFT_EDGE = auto()
    RIGHT_UPPER_EDGE = auto()
    RIGHT_RIGHT_EDGE = auto()
    FRONT_FACE = auto()
    FRONT_LOWER_EDGE = auto()
    FRONT_LEFT_EDGE = auto()
    FRONT_UPPER_EDGE = auto()
    FRONT_RIGHT_EDGE = auto()
    BACK_FACE = auto()
    BACK_LOWER_EDGE = auto()
    BACK_LEFT_EDGE = auto()
    BACK_UPPER_EDGE = auto()
    BACK_RIGHT_EDGE = auto()
    BOTTOM_LOWER_LEFT_CORNER = auto()
    BOTTOM_LOWER_RIGHT_CORNER = auto()
    BOTTOM_UPPER_LEFT_CORNER = auto()
    BOTTOM_UPPER_RIGHT_CORNER = auto()
    TOP_LOWER_LEFT_CORNER = auto()
    TOP_LOWER_RIGHT_CORNER = auto()
    TOP_UPPER_LEFT_CORNER = auto()
    TOP_UPPER_RIGHT_CORNER = auto()


class DomainDecomposer:

    @staticmethod
    def select_attribute(cubies: np.ndarray, face: CubeFace, flatten=True):
        selected_object = np.zeros(0)
        x, y, z = cubies.shape
        match face:
            case CubeFace.LEFT_FACE:
                selected_object = cubies[:, y - 1, :]
            case CubeFace.RIGHT_FACE:
                selected_object = cubies[:, 0, :]
            case CubeFace.TOP_FACE:
                selected_object = cubies[:, :, z - 1]
            case CubeFace.BOTTOM_FACE:
                selected_object = cubies[:, :, 0]
            case CubeFace.TOP_LEFT_EDGE:
                selected_object = cubies[:, y - 1, z - 1]
            case CubeFace.TOP_UPPER_LEFT_CORNER:
                selected_object = np.array(cubies[0, y - 1, z - 1])

        if flatten:
            selected_object = selected_object.flatten()
        return selected_object
