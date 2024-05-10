from .field import Cell, Field, PositionError


class Route:
    def __init__(self, field: Field, start: Cell, finish: Cell):
        self._field = field
        self._path: list[Cell] = []
        # path represented like this: {x: {y: position_in_path_list}}:
        self._subscriptable_path: dict[int, dict[int, int]] = {}
        self._start: Cell = start
        self._finish: Cell = finish

    @property        
    def start(self):
        return self._start
    
    @start.setter
    def start(self, new: tuple[int, int] | Cell):
        self.reset()
        if isinstance(new, Cell):
            self._start = new
        else:
            self._start = self._field(*new)

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, new: tuple[int, int] | Cell):
        self.reset()
        if isinstance(new, Cell):
            self._finish = new
        else:
            self._finish = self._field(*new)

    @property
    def path(self) -> list[Cell]:
        """
        Calculates and returns a path from the start to the finish.

        :return: a list of cells representing calculated path to the finish.
        """
        if not self._path:
            self._path = self._calculate_path()
        return self._path

    @property
    def subscriptable_path(self) -> dict[int, dict[int, int]]:
        """
        Position in path can be obtained by subscripting using [x][y]:
        position = subscriptable_path()[5][10]
        Position numbers should begin from 1.

        """
        if not self._subscriptable_path:
            self._subscriptable_path = self._cells_list_to_dict(self.path)
        return self._subscriptable_path

    @property
    def field(self) -> Field:
        return self._field

    def path_position(self, x: int, y: int) -> int | bool:
        """
        Returns position number in path by coordinates. Position numbers should begin from 1.
        If no such coordinates exist in path, returns False.

        """
        try:
            return self.subscriptable_path[x][y]
        except KeyError:
            return False

    def reset(self):
        self._path = []
        self._subscriptable_path = {}

    @staticmethod
    def _cells_list_to_dict(path: list[Cell]) -> dict[int, dict[int, int]]:
        result = {}
        for number, cell in enumerate(path, 1):
            result[cell.x] = result.get(cell.x, {})
            result[cell.x][cell.y] = number
        return result

    def _calculate_path(self) -> list[Cell]:
        current_cell = self.start
        path = [current_cell]
        blacklist = set()

        while True:
            if self.finish == current_cell:
                return path
            # saving current sell state to check later if it was changed:
            previous_cell = current_cell
            if current_cell == (12, 5):
                pass
            for new_coords in (
                (current_cell.x + 1, current_cell.y),
                (current_cell.x, current_cell.y + 1),
                (current_cell.x - 1, current_cell.y),
                (current_cell.x, current_cell.y - 1)
            ):
                if self._cell_can_be_used(new_coords, path, blacklist):
                    if path[-1] != current_cell:    # to avoid duplicates when returning to previously visited cell
                        path.append(current_cell)
                    current_cell = self._field(*new_coords)
                    break
                else:
                    try:
                        blacklist.add(self._field(*new_coords))
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
            cell = self.field(*coords)
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

