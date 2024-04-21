from .field import CellCondition, Field
from .route import Route


FIELD_CELLS = {
    CellCondition.passable: "[ ]",
    CellCondition.blocked: "[▇]"
}
WAYPOINT = "[*]"
START = "[S]"
FINISH = "[F]"


def draw_field(f: Field):
    for row in f:
        for cell in row:
            print(FIELD_CELLS[cell.state], end="")
        print()


def draw_route(route: Route):
    for row in route.field:
        for cell in row:
            if cell == route.start:
                point = START
            elif cell == route.finish:
                point = FINISH
            elif cell in route.path:
                point = WAYPOINT
            else:
                point = FIELD_CELLS[cell.state]
            print(point, end="")
        print()
