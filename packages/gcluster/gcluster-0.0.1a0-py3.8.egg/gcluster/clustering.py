from enum import Enum
from .graph import Graph


class Mode(Enum):
    STRONG = 1
    UNION = 2


def clustering(mode: Mode):
    if mode == Mode.STRONG:
        return 1
    elif mode == Mode.UNION:
        return 2
