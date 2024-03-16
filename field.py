from enum import Enum
from typing import overload


class CellCondition(Enum):
    passable = 1
    blocked = 2


class Cell:
    def __init__(self, x, y, state=CellCondition.passable):
        self.x = x
        self.y = y
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: CellCondition):
        self._state = state


class Field:
    def __init__(self):
        self.x = 0
        self.y = 0
        self._grid: list[list[Cell]] = []

    def build(self, x=100, y=100):
        self.x = x
        self.y = y
        self._grid = [[Cell(x + 1, y + 1) for x in range(self.x)] for y in range(self.y)]
        return self

    @overload
    def set_cell_state(self, x: int, y: int, state: CellCondition): ...

    @overload
    def set_cell_state(self, *args: tuple[int, int] | CellCondition): ...

    @overload
    def set_cell_state(self, *args: tuple[int, int], state: CellCondition): ...

    def set_cell_state(self, *args, state=None):
        error_message = "Incorrect signature"
        match args:
            case int(x), int(y), CellCondition() as state:
                self(x, y).state = state
            case (int(), int()), *_, CellCondition() as state:
                for x, y in args[:-1]:
                    self(x, y).state = state
            case (int(), int()), *_:
                if not state:
                    raise TypeError(error_message)
                for x, y in args:
                    self(x, y).state = state
            case _:
                raise TypeError(error_message)

    def is_cell_accessible(self, x, y):
        if self(x, y).state == CellCondition.passable:
            return True
        return False

    def __call__(self, x, y):
        try:
            return self._grid[y-1][x-1]
        except IndexError:
            raise ValueError(f"Cell coordinates ({x=}, {y=}) are out of bounds")

    def __iter__(self):
        return iter(self._grid)

