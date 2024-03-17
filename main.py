#!/usr/bin/env python3.12

from field import Field, CellCondition
from output import draw_field, draw_route
from route import Route


if __name__ == "__main__":
    f = Field().build(20, 20)
    for x in range(3, 6):
        f.set_cell_state(x, 5, CellCondition.blocked)
    for y in range(7, 18):
        f.set_cell_state(8, y, CellCondition.blocked)

    # ToDo: fix a bug here:
    # for x in range(8, 21):
    #     f.set_cell_state(x, 6, CellCondition.blocked)

    f.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)
    draw_field(f)   # draw just a field with obstacles
    print()
    r = Route(f, f(4, 4), f(16, 12))

    # ToDo: fix a bug here:
    # r = Route(f, f(4, 4), f(6, 12))

    draw_route(r)   # draw a field with route on it
