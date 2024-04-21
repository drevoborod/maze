#!/usr/bin/env python3.12

### Debug
from app.field import GLOBAL_COUNTER
###
from app.field import Field, CellCondition
from app.output import draw_field, draw_route
from app.route import Route


if __name__ == "__main__":
    f = Field().build(20, 20)
    for x in range(3, 6):
        f.set_cell_state(x, 5, CellCondition.blocked)
    for y in range(7, 18):
        f.set_cell_state(8, y, CellCondition.blocked)

    # ToDo: fix bug here with increased complexity and reversed route (from down-right to top-left):
    # Increase complexity:
    # for x in range(8, 21):
    #     f.set_cell_state(x, 6, CellCondition.blocked)

    # ToDo: fix bug here with increased complexity and regular route:
    # Increase complexity 2:
    # for x in range(8, 19):
    #     f.set_cell_state(x, 6, CellCondition.blocked)

    f.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)
    draw_field(f)   # draw just a field with obstacles
    print()

    # Regular route:
    r = Route(f, f(4, 4), f(16, 12))
    # Reversed route:
    # r = Route(f, f(16, 12), f(4, 4))

    # ToDo: fix a bug here (with "increased complexity" field configuration):
    # r = Route(f, f(4, 4), f(6, 12))

    draw_route(r)   # draw a field with route on it

    ### Debug
    print()
    for key, value in GLOBAL_COUNTER.items():
        print(f"{key}: {value}")
    ###
    print()
    draw_route(r)

