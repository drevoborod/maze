from field import Cell, Field, PositionError


class Route:
    def __init__(self, field: Field, start: Cell, finish: Cell):
        self._field = field
        self._path: set[Cell] = set()
        self._start: Cell = start
        self._finish: Cell = finish

    @property        
    def start(self):
        return self._start
    
    @start.setter
    def start(self, new: tuple[int, int] | Cell):
        if isinstance(new, Cell):
            self._start = new
        else:
            self._start = self._field(*new)

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, new: tuple[int, int] | Cell):
        if isinstance(new, Cell):
            self._finish = new
        else:
            self._finish = self._field(*new)

    @property
    def path(self) -> set[Cell]:
        if not self._path:
            self._path = self._calculate_path()
        return self._path

    @property
    def field(self) -> Field:
        return self._field

    def reset(self):
        self._path = set()

    def _calculate_path(self, current_cell: Cell = None, path: set[Cell] = None) -> set[Cell]:
        if not current_cell:
            current_cell = self.start
        if path is None:
            path = set()
        if self.finish == current_cell:
            return path
        new_path = path.copy()
        new_path.add(current_cell)
        if self._check_cell(new_coords := (current_cell.x + 1, current_cell.y), new_path):
            new_path.update(self._calculate_path(self._field(*new_coords), new_path))
        elif self._check_cell(new_coords := (current_cell.x - 1, current_cell.y), new_path):
            new_path.update(self._calculate_path(self._field(*new_coords), new_path))
        elif self._check_cell(new_coords := (current_cell.x, current_cell.y + 1), new_path):
            new_path.update(self._calculate_path(self._field(*new_coords), new_path))
        elif self._check_cell(new_coords := (current_cell.x, current_cell.y - 1), new_path):
            new_path.update(self._calculate_path(self._field(*new_coords), new_path))
        return new_path

    def _check_cell(self, coords: tuple[int, int], path: set[Cell]) -> bool:
        try:
            cell = self._field(*coords)
        except PositionError:
            return False
        if cell == self.finish:
            return True
        if cell in path:
            return False
        if cell.passable:
            return True

