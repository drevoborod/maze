from .base_route import BaseRoute
from .field import Cell, PositionError


class Route2(BaseRoute):
    """
    Second optimised implementation of route calculation algorithm.
    """
    def __init__(self, *args):
        super().__init__(*args, name="Second algorithm implementation")

    def _calculate_path(self) -> list[Cell]:
        current_cell = self.start
        path = [current_cell]
        blacklist = set()

        while True:
            if self.finish == current_cell:
                return path
            # saving current sell state to check later if it was changed:
            previous_cell = current_cell

            # find out in which direction the closest path to the finish lays:
            x_diff = current_cell.x - self.finish.x
            y_diff = current_cell.y - self.finish.y
            if x_diff == 0:
                if y_diff > 0:
                    new_coords = (current_cell.x, current_cell.y - 1)
                else:
                    new_coords = (current_cell.x, current_cell.y + 1)
            elif y_diff == 0:
                if x_diff > 0:
                    new_coords = (current_cell.x - 1, current_cell.y)
                else:
                    new_coords = (current_cell.x + 1, current_cell.y)
            elif abs(x_diff) > abs(y_diff):
                if x_diff > 0:
                    new_coords = (current_cell.x - 1, current_cell.y)
                else:
                    new_coords = (current_cell.x + 1, current_cell.y)
            else:
                if y_diff > 0:
                    new_coords = (current_cell.x, current_cell.y - 1)
                else:
                    new_coords = (current_cell.x, current_cell.y + 1)

            if self._cell_can_be_used(new_coords, path, blacklist):
                if path[-1] != current_cell:    # to avoid duplicates when returning to previously visited cell
                    path.append(current_cell)
                current_cell = self.get_cell(*new_coords)
            else:
                try:
                    blacklist.add(self.get_cell(*new_coords))
                except PositionError:
                    pass
            # if we made no step forwards, add current and previous cells to blacklist and make step backwards:
            if previous_cell is current_cell:
                blacklist.add(current_cell)
                blacklist.add(path.pop())
                current_cell = path[-1]

