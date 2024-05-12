from .base_route import BaseRoute
from .field import Cell, Field, PositionError


class Route1(BaseRoute):
    """
    First demo implementation of route calculation algorithm.
    """

    def __init__(self, field: Field, start: Cell, finish: Cell, name: str = "Demo route implementation"):
        super().__init__(field=field, start=start, finish=finish, name=name)

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
            # if we made no step forwards, add current and previous cells to blacklist and make step backwards:
            if previous_cell is current_cell:
                blacklist.add(current_cell)
                blacklist.add(path.pop())
                current_cell = path[-1]
