from field import CellCondition, Field


FIELD_CELLS = {
    CellCondition.passable: "[ ]",
    CellCondition.blocked: "[▇]"
}


def draw_field(f: Field):
    for row in f:
        for cell in row:
            print(FIELD_CELLS[cell.state], end="")
        print()
