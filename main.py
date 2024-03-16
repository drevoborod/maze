#!/usr/bin/env python3.12

from field import Field, CellCondition
from output import draw_field


if __name__ == "__main__":
    f = Field().build(20, 20)
    for x in range(3, 6):
        f.set_cell_state(x, 5, CellCondition.blocked)
    f.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)

    # print(f(12, 5).state)
    draw_field(f)
