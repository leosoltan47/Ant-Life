from enum import Enum

class Directions(Enum):
    Left = (-1.0, 0)
    Right = (1.0, 0)
    Up = (0, -1.0)
    Down = (0, 1.0)

class Ant: 
    _position_x: float
    _position_y: float
    _is_alive: bool

    def __init__(self, x: float, y: float) -> None:
        self._position_x = x
        self._position_y = y
        self._is_alive = True

    def move(self, action: Directions) -> None:
        x, y = action.value
        self._position_x += x
        self._position_y += y

class Fruit():
    pass

