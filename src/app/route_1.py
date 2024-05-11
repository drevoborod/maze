from .base_route import BaseRoute
from .field import Cell, PositionError


class Route1(BaseRoute):
    """
    First demo implementation of route calculation algorithm.
    """
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