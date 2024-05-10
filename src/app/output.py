from .field import CellCondition, Field
from .route import Route


CELL_TEMPLATE = "[{:<3}]"
FIELD_CELLS = {
    CellCondition.passable: CELL_TEMPLATE.format(" "),
    CellCondition.blocked: CELL_TEMPLATE.format("▇")
}
X_NUMBER = "|{:<3}|"
INDENT = 4
Y_NUMBER = f"{{:<{INDENT}}}"
WAYPOINT_CHAR = "*"
START_CHAR = "S"
FINISH_CHAR = "F"


def _draw_x_coordinates_row(f: Field):
    print(f"{' ' * INDENT}", end="")
    for number in range(1, len(f) + 1):
        print(X_NUMBER.format(number), end="")
    print()


def draw_field(f: Field):
    _draw_x_coordinates_row(f)
    for number, row in enumerate(f, 1):
        print(Y_NUMBER.format(number), end="")
        for cell in row:
            print(FIELD_CELLS[cell.state], end="")
        print()


def draw_route(route: Route):
    _draw_x_coordinates_row(route.field)
    for number, row in enumerate(route.field, 1):
        print(Y_NUMBER.format(number), end="")
        for cell in row:
            if cell == route.start:
                point = CELL_TEMPLATE.format(START_CHAR)
            elif cell == route.finish:
                point = CELL_TEMPLATE.format(FINISH_CHAR)
            elif position := route.path_position(cell.x, cell.y):
                point = CELL_TEMPLATE.format(position)
            else:
                point = FIELD_CELLS[cell.state]
            print(point, end="")
        print()
