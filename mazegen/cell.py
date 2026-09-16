from enum import Enum
from pydantic import BaseModel, Field


class CellState(Enum):
    """
        FREE: The cell is not connected to any other cell.\n
        SEED: The cell is a seed cell, which can be used to start the maze
        and to invite other cells to connect to it.\n
        INVITE: The cell is invited to connect to a seed cell and become the new seed cell.\n
        CONNECTED: The cell is connected to at least one other cell.\n
        BLOCKED: The cell is blocked and cannot be connected to any other cell. Used for 42 logo.
    """
    FREE = 0
    SEED = 1
    INVITE = 2
    CONNECTED = 3,
    BLOCKED = 4


class Cell(BaseModel):
    """
    Represents a cell in the maze grid.

    Attributes:
        row (int): The row index of the cell in the grid.
        col (int): The column index of the cell in the grid.
        walls (int): A bitmask representing the walls of the cell (4 bits for walls: N=1, E=2, S=4, W=8).
    """
    row: int
    col: int
    walls: int = Field(default=15, ge=0, le=15)

    def is_blocked(self) -> bool:
        """Checks if the cell is blocked."""
        return self.walls == 15

    def hex_representation(self) -> str:
        """Returns the hexadecimal representation of the cell's walls."""
        return format(self.walls, 'x')


class AutomatonCell(Cell, BaseModel):
    """
    Represents a cell in the maze grid for the Cell Automaton algorithm.

    Attributes:
        row (int): The row index of the cell in the grid.
        col (int): The column index of the cell in the grid.
        state (CellState): The current state of the cell.
        walls (int): A bitmask representing the walls of the cell (4 bits for walls: N=1, E=2, S=4, W=8).
        parent (str): The direction of the parent cell (N, E, S, W) if the cell is connected.
        free_neighbours (list[str]): A list of directions (N, E, S, W) representing the free neighbouring cells.
    """
    state: CellState = Field(default=CellState.FREE)
    parent: str = Field(default="")
    free_neighbours: list[str] = Field(default_factory=list)


class BreadCell(Cell, BaseModel):
    visited: bool = Field(default=False)
    parent_cell: 'BreadCell' = Field(default=None)


def get_blocked_cells(rows: int, cols: int) -> set[tuple[int, int]]:
    """
    Returns a set of coordinates for cells that should be blocked in the maze.
    The blocked cells are determined based on the maze dimensions
    and are designed to create a 42 pattern at the centre of the maze.\n
    If the maze dimensions are too small for the 42 pattern, no cells will be blocked.
    """
    if rows < 6 or cols < 8:
        return set()

    middle_row = (rows - 1) // 2
    middle_col = (cols - 1) // 2
    blocked_cells = {
        (middle_row - 2, middle_col - 3),
        (middle_row - 2, middle_col + 1),
        (middle_row - 2, middle_col + 2),
        (middle_row - 2, middle_col + 3),
        (middle_row - 1, middle_col - 3),
        (middle_row - 1, middle_col + 3),
        (middle_row, middle_col - 3),
        (middle_row, middle_col - 2),
        (middle_row, middle_col - 1),
        (middle_row, middle_col + 1),
        (middle_row, middle_col + 2),
        (middle_row, middle_col + 3),
        (middle_row + 1, middle_col - 1),
        (middle_row + 1, middle_col + 1),
        (middle_row + 2, middle_col - 1),
        (middle_row + 2, middle_col + 1),
        (middle_row + 2, middle_col + 2),
        (middle_row + 2, middle_col + 3),
    }
    return blocked_cells
