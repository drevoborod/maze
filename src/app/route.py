import time

from .field import Cell, Field, PositionError


class Route:
    def __init__(self, field: Field, start: Cell, finish: Cell):
        self._field = field
        self._path: list[Cell] = []
        # stores path steps numbers accessible by tuple of coordinates: {(x1, y1): n1, (x1, y2): n2, (x2, y1): n2,...}
        self._enumerated_path: dict[tuple[int, int], int] = {}
        self._start: Cell = start
        self._finish: Cell = finish
        # stores information about how many times every cell has been called:
        self._cell_call_statistics: dict[tuple[int, int], int] = {}
        # how long a path has been calculated:
        self._calculation_time: int = 0

    @property        
    def start(self):
        return self._start
    
    @start.setter
    def start(self, new: tuple[int, int] | Cell):
        self.reset()
        if isinstance(new, Cell):
            self._start = new
        else:
            self._start = self.field(*new)

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, new: tuple[int, int] | Cell):
        self.reset()
        if isinstance(new, Cell):
            self._finish = new
        else:
            self._finish = self.field(*new)

    @property
    def path(self) -> list[Cell]:
        """
        Calculates and returns a path from the start to the finish.
        The path will be represented as a list of cells.

        :return: a list of cells representing calculated path to the finish.
        """
        if not self._path:
            self.reset()
            timestamp = time.time()
            self._path = self._calculate_path()
            self._calculation_time = time.time() - timestamp
        return self._path

    @property
    def enumerated_path(self) -> dict[tuple[int, int], int]:
        """
        Calculates and returns a path from the start to the finish.
        The path will be represented as a dict of position tuples.
        Position in path can be obtained by subscribing using (x, y):
            position_in_path = enumerated_path[(x, y)]
        Position numbers begin from 1.

        """
        if not self._enumerated_path:
            self._enumerated_path = self._cells_list_to_dict(self.path)
        return self._enumerated_path

    @property
    def field(self) -> Field:
        return self._field

    @property
    def calculation_time(self):
        return self._calculation_time

    @property
    def cell_call_statistics(self):
        return self._cell_call_statistics

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Returns field cell by coordinates.
        Proxy function for statistics calculation purposes.
        """
        self._cell_call_statistics[(x, y)] = self._cell_call_statistics.get((x, y), 0) + 1
        return self.field(x, y)

    def path_position(self, x: int, y: int) -> int | bool:
        """
        Returns position number in path by coordinates. Position numbers should begin from 1.
        If no such coordinates exist in path, returns False.

        """
        try:
            return self.enumerated_path[(x, y)]
        except KeyError:
            return False

    def reset(self):
        """
        Reset all path-related information.

        """
        self._path = []
        self._enumerated_path = {}
        self._cell_call_statistics = {}
        self._calculation_time = 0

    @staticmethod
    def _cells_list_to_dict(path: list[Cell]) -> dict[tuple[int, int], int]:
        return {(cell.x, cell.y): number for number, cell in enumerate(path, 1)}

    def _calculate_path(self) -> list[Cell]:
        current_cell = self.start
        path = [current_cell]
        blacklist = set()

        while True:
            if self.finish == current_cell:
                return path
            # saving current sell state to check later if it was changed:
            previous_cell = current_cell
            for new_coords in (
                (current_cell.x + 1, current_cell.y),
                (current_cell.x, current_cell.y + 1),
                (current_cell.x - 1, current_cell.y),
                (current_cell.x, current_cell.y - 1)
            ):
                if self._cell_can_be_used(new_coords, path, blacklist):
                    if path[-1] != current_cell:    # to avoid duplicates when returning to previously visited cell
                        path.append(current_cell)
                    current_cell = self.get_cell(*new_coords)
                    break
                else:
                    try:
                        blacklist.add(self.get_cell(*new_coords))
                    except PositionError:
                        pass
            # if we made no step forward, add current and previous cell to blacklist and make step backwards:
            if previous_cell is current_cell:
                blacklist.add(current_cell)
                blacklist.add(path.pop())
                current_cell = path[-1]

    def _cell_can_be_used(self, coords: tuple[int, int], path: list[Cell], blacklist: set[Cell]) -> bool:
        # check that we are not out of bounds:
        try:
            cell = self.get_cell(*coords)
        except PositionError:
            return False

        if cell == self.finish:
            return True
        if cell in path:
            return False
        # check whether this cell has been checked already or not:
        if cell in blacklist:
            return False
        if cell.passable:
            return True

