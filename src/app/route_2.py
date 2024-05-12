import random

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

            # potential new cells ranged by priority:
            new_coords_prioritized: list[tuple[int, int]] = []

            # find out in which direction the closest path to the finish lays:
            x_diff = current_cell.x - self.finish.x
            y_diff = current_cell.y - self.finish.y
            if x_diff == 0:
                if y_diff > 0:
                    new_coords_prioritized.append((current_cell.x, current_cell.y - 1))
                    new_coords_prioritized.append((current_cell.x, current_cell.y + 1))
                else:
                    new_coords_prioritized.append((current_cell.x, current_cell.y + 1))
                    new_coords_prioritized.append((current_cell.x, current_cell.y - 1))
                additional = [current_cell.x + 1, current_cell.x - 1]
                random.shuffle(additional)  # let the fate decide :)
                new_coords_prioritized.append((additional[0], current_cell.y))
                new_coords_prioritized.append((additional[1], current_cell.y))
            elif y_diff == 0:
                if x_diff > 0:
                    new_coords_prioritized.append((current_cell.x - 1, current_cell.y))
                    new_coords_prioritized.append((current_cell.x + 1, current_cell.y))
                else:
                    new_coords_prioritized.append((current_cell.x + 1, current_cell.y))
                    new_coords_prioritized.append((current_cell.x - 1, current_cell.y))
                additional = [current_cell.y + 1, current_cell.y - 1]
                random.shuffle(additional)
                new_coords_prioritized.append((current_cell.x, additional[0]))
                new_coords_prioritized.append((current_cell.x, additional[1]))
            elif abs(x_diff) > abs(y_diff):
                if x_diff > 0:
                    new_coords_prioritized.append((current_cell.x - 1, current_cell.y))
                    additional = [(current_cell.x + 1, current_cell.y)]
                else:
                    new_coords_prioritized.append((current_cell.x + 1, current_cell.y))
                    additional = [(current_cell.x - 1, current_cell.y)]
                if y_diff > 0:
                    new_coords_prioritized.append((current_cell.x, current_cell.y - 1))
                    additional.append((current_cell.x, current_cell.y + 1))
                else:
                    new_coords_prioritized.append((current_cell.x, current_cell.y + 1))
                    additional.append((current_cell.x, current_cell.y - 1))
                random.shuffle(additional)
                new_coords_prioritized.append(additional[0])
                new_coords_prioritized.append(additional[1])
            else:
                if y_diff > 0:
                    new_coords_prioritized.append((current_cell.x, current_cell.y - 1))
                    additional = [(current_cell.x, current_cell.y + 1)]
                else:
                    new_coords_prioritized.append((current_cell.x, current_cell.y + 1))
                    additional = [(current_cell.x, current_cell.y - 1)]
                if x_diff > 0:
                    new_coords_prioritized.append((current_cell.x - 1, current_cell.y))
                    additional.append((current_cell.x + 1, current_cell.y + 1))
                else:
                    new_coords_prioritized.append((current_cell.x + 1, current_cell.y))
                    additional.append((current_cell.x - 1, current_cell.y))
                random.shuffle(additional)
                new_coords_prioritized.append(additional[0])
                new_coords_prioritized.append(additional[1])

            for new_coords in new_coords_prioritized:
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
            else:
                # if we made no step forwards, add current and previous cells to blacklist and make step backwards:
                blacklist.add(current_cell)
                blacklist.add(path.pop())
                current_cell = path[-1]

