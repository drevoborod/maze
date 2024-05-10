#!/usr/bin/env python3.12

### Debug
from app import GLOBAL_CELL_CALL_COUNTER
###
from app.field import Field, CellCondition
from app.output import draw_field, draw_route
from app.route import Route


if __name__ == "__main__":
    f = Field().build(20, 20)
    f.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)
    for x in range(3, 6):
        f.set_cell_state(x, 5, CellCondition.blocked)
    for y in range(7, 18):
        f.set_cell_state(8, y, CellCondition.blocked)

    # Increase complexity:
    # for x in range(8, 21):
    #     f.set_cell_state(x, 6, CellCondition.blocked)

    # Increase complexity 2:
    # for x in range(8, 19):
    #     f.set_cell_state(x, 6, CellCondition.blocked)

    # ToDo: fix bug in "Complexity 3" configuration: continue on the other side of field.
    ## Increase complexity 3:
    for x in range(8, 21):
        f.set_cell_state(x, 6, CellCondition.blocked)
    for x in range(2, 6):
        f.set_cell_state(x, 12, CellCondition.blocked)
    for y in range(7, 12):
        f.set_cell_state(4, y, CellCondition.blocked)
    for y in range(1, 5):
        f.set_cell_state(13, y, CellCondition.blocked)

    draw_field(f)   # draw just a field with obstacles
    print()

    # Regular route:
    r = Route(f, f(4, 4), f(16, 12))
    # Regular route 2:
    # r = Route(f, f(4, 4), f(6, 12))
    # Reversed route:
    # r = Route(f, f(16, 12), f(4, 4))
    # Reversed route 2:
    # r = Route(f, f(6, 12), f(4, 4))

    draw_route(r)   # draw a field with route on it

    ### Debug
    print()
    for key, value in sorted(GLOBAL_CELL_CALL_COUNTER.items()):
        print(f"{key}: {value}")
    print()
    draw_route(r)
    print()

    # ToDo: Fix bug: why some steps are duplicated? Maybe it's ok?
    # Locating duplicated cells in route:
    excl_dict = {}
    for number, cell in enumerate(r.path, 1):
        excl_dict[cell] = excl_dict.get(cell, []) + [number]
    for key, value in excl_dict.items():
        if len(value) > 1:
            print(f"Cell: {key}, Positions in path: {', '.join(map(str, value))}")
    ###


