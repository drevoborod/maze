from .field import Cell, Field, PositionError


class Route:
    def __init__(self, field: Field, start: Cell, finish: Cell):
        self._field = field
        self._path: list[Cell] = []
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
    def path(self) -> list[Cell]:
        """
        Calculates and returns a path from the start to the finish.

        :return: a list of cells representing calculated path to the finish.
        """
        if not self._path:
            self._path = self._calculate_path()
        return self._path

    @property
    def field(self) -> Field:
        return self._field

    def reset(self):
        self._path = set()

    def _calculate_path(self) -> list[Cell]:
        current_cell = self.start
        path = [current_cell]
        blacklist = set()

        while True:
            if self.finish == current_cell:
                return path
            # saving current sell state to check later if it changed:
            previous_cell = current_cell
            for new_coords in (
                (current_cell.x + 1, current_cell.y),
                (current_cell.x, current_cell.y + 1),
                (current_cell.x - 1, current_cell.y),
                (current_cell.x, current_cell.y - 1)
            ):
                if self._check_cell(new_coords, path, blacklist):
                    path.append(current_cell)
                    current_cell = self._field(*new_coords)
                    ### Debug:
                    # draw_route(self, path, current_cell)
                    # print()
                    ###
                    break
                else:
                    try:
                        blacklist.add(self._field(*new_coords))
                    except PositionError:
                        pass
            # if we made no step forward, add current cell to blacklist and make step backwards:
            if previous_cell is current_cell:
                blacklist.add(path.pop())
                current_cell = path[-1]

    def _check_cell(self, coords: tuple[int, int], path: list[Cell], blacklist: set[Cell]) -> bool:
        # check that we are not out of bounds:
        try:
            cell = self._field(*coords)
        except PositionError:
            return False
        if cell == self.finish:
            return True
        # # check that the cell is not previous cell in the path:
        # if cell == path[-1]:
        #     return False
        if cell in path:
            return False

        # check whether this cell has been checked already or not:
        if cell in blacklist:
            return False
        if cell.passable:
            return True

