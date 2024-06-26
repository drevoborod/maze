from enum import Enum
from typing import overload, Self


class PositionError(Exception): pass


class CellCondition(Enum):
    passable = 1
    blocked = 2


class Cell:
    def __init__(self, x: int, y: int, state=CellCondition.passable):
        self._x = x
        self._y = y
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: CellCondition):
        self._state = state

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def passable(self) -> bool:
        return self.state == CellCondition.passable

    def __eq__(self, other: tuple[int, int] | Self):
        if isinstance(other, Cell):
            return self() == other()
        else:
            return self() == other

    def __call__(self, *args, **kwargs) -> tuple[int, int]:
        return self.x, self.y

    def __hash__(self):
        return hash(self())

    def __str__(self):
        return str(self())


class Field:
    """
    Playing field consistent of Cell instances. X and Y indexes (width and height) start with 1.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self._grid: list[list[Cell]] = []

    def build(self, x: int = 100, y: int = 100) -> Self:
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
        """
        Change state of one or many cells.

        :param args:
        :param state:
        """
        error = TypeError("Incorrect signature")
        match args:
            case int(x), int(y), CellCondition() as state:
                self(x, y).state = state
            case (int(), int()), *_, CellCondition() as state:
                for x, y in args[:-1]:
                    self(x, y).state = state
            case (int(), int()), *_:
                if not state:
                    raise error
                for x, y in args:
                    self(x, y).state = state
            case _:
                raise error

    def __call__(self, x: int, y: int) -> Cell:
        """
        Get specific cell from the field by coordinates.

        """
        error = PositionError(f"Cell coordinates ({x=}, {y=}) are out of bounds")
        if x < 1 or y < 1:
            raise error
        try:
            return self._grid[y-1][x-1]
        except IndexError:
            raise error

    def __iter__(self):
        return iter(self._grid)

    def __len__(self):
        return len(self._grid)
