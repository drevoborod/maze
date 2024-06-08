from ..core.base_route import BaseRoute, UnreachableFinishError
from ..core.field import Cell, Field, PositionError


class Route1(BaseRoute):
    """
    First demo implementation of route calculation algorithm.
    """

    def __init__(self, field: Field, start: Cell, finish: Cell, name: str = "Demo route implementation",
                 calculation_callback=None):
        super().__init__(field=field, start=start, finish=finish, name=name, calculation_callback=calculation_callback)

    def _calculate_path(self, callback=None) -> list[Cell]:
        current_cell = self.start
        path = [current_cell]
        blacklist = set()

        while True:
            if self.finish == current_cell:
                return path
            if callback:
                callback(path)
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
                try:
                    current_cell = path[-1]
                except IndexError:
                    raise UnreachableFinishError
