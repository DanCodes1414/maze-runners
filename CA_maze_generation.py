from enum import Enum
from pydantic import BaseModel, Field
import random


GREY = '\u001b[90m'
GREEN = '\u001b[32m'
RED = '\u001b[31m'
END = '\u001b[0m'
TURN_PROB = 12
BRANCH_PROB = 5
SEED = 42
rand = random.Random(SEED)
directions = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

#class MazeGenerationError(Exception):
#    pass
class MazeConfigError(Exception):
    pass

class CellState(Enum):
    """
        FREE: The cell is not connected to any other cell.
        SEED: The cell is a seed cell, which can be used to start the maze and to invite other cells to connect to it.
        INVITE: The cell is invited to connect to a seed cell and become the new seed cell.
        CONNECTED: The cell is connected to at least one other cell.
        BLOCKED: The cell is blocked and cannot be connected to any other cell. Used for 42 logo.
    """
    FREE = 0
    SEED = 1
    INVITE = 2
    CONNECTED = 3,
    BLOCKED = 4


class Cell(BaseModel):
    row: int
    col: int
    state: CellState = Field(default=CellState.FREE)
    #is_blocked: bool = Field(default=False) # Possibly add is_blocked to CellState enum.
    walls: int = Field(default=15, ge=1, le=15) # 4 bits for walls: N=8, E=4, S=2, W=1 (3=0011 means S and W walls). Should be between 1 and 15
    parent: str = Field(default=None) # directions of parent cell (N, E, S, W)
    free_neighbours: list[str] = Field(default_factory=list) # directions of free neighbours (N, E, S, W)

    def __str__(self):
        return f"Cell({self.row}, {self.col}, {self.state.name}, walls={self.walls}, parent={self.parent}, free_neighbours={self.free_neighbours})\n"


def branching(cell: Cell):
    if rand.randint(0, 100) > BRANCH_PROB:
        cell.state = CellState.CONNECTED
    else:
        cell.state = CellState.SEED


def reverse_direction(direction: str) -> str:
    if direction == 'N': return 'S'
    elif direction == 'E': return 'W'
    elif direction == 'S': return 'N'
    elif direction == 'W': return 'E'


def turn_direction(cell: Cell) -> str:
    if rand.randint(0, 100) <= TURN_PROB:
        direction = rand.choice(['N', 'E', 'S', 'W'])
    else:
        direction = reverse_direction(cell.parent)

    if cell.free_neighbours == []:
        return None
    if direction not in cell.free_neighbours:
        direction = rand.choice(cell.free_neighbours)
    return direction


def update_free_neighbours(cell: Cell, grid: list[list[Cell]]):
    cell.free_neighbours = []
    if cell.state == CellState.BLOCKED:
        return
    for direction, (drv, drc) in directions.items():
        neighbour_row = cell.row + drv
        neighbour_col = cell.col + drc
        if 0 <= neighbour_row < len(grid) and 0 <= neighbour_col < len(grid[0]):
            neighbour_cell = grid[neighbour_row][neighbour_col]
            if neighbour_cell.state == CellState.FREE:
                cell.free_neighbours.append(direction)


def initialise_grid(rows: int, cols: int, start: tuple[int, int], end: tuple[int, int]) -> list[list[Cell]]:
    if rows < 5 or cols < 7:
        raise MazeConfigError("Maze dimensions must be at least 5x7.")
    grid = [[Cell(row=r, col=c) for c in range(cols)] for r in range(rows)]
    blocked_cells = get_blocked_cells(rows, cols)
    if start in blocked_cells or end in blocked_cells:
        raise MazeConfigError("Start and end cells cannot be in blocked cells.")
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked_cells:
                grid[r][c].state = CellState.BLOCKED
            if (r, c) == start:
                grid[r][c].state = CellState.SEED
    for r in range(rows):
        for c in range(cols):
            update_free_neighbours(grid[r][c], grid)
    return grid


def any_free_cells(grid: list[list[Cell]]) -> bool:
    for row in grid:
        for cell in row:
            if cell.state == CellState.FREE:
                return True
    return False


def any_seed_cells(grid: list[list[Cell]]) -> bool:
    for row in grid:
        for cell in row:
            if cell.state == CellState.SEED:
                return True
    return False


def algorithm_step(grid: list[list[Cell]]) -> list[list[Cell]]:
    while any_free_cells(grid):
        seed_cells = [cell for row in grid for cell in row if cell.state == CellState.SEED]
        if not seed_cells:
            connected_cells = [cell for row in grid for cell in row if cell.state == CellState.CONNECTED and cell.free_neighbours]
            rand.choice(connected_cells).state = CellState.SEED
        for seed_cell in seed_cells:
            direction = turn_direction(seed_cell)
            if direction is None:
                seed_cell.state = CellState.CONNECTED
                continue
            drv, dcv = directions[direction]
            neighbour_cell = grid[seed_cell.row + drv][seed_cell.col + dcv]
            neighbour_cell.state = CellState.INVITE
            neighbour_cell.parent = reverse_direction(direction)
            update_free_neighbours(neighbour_cell, grid)
            update_free_neighbours(seed_cell, grid)
            branching(seed_cell)
        invite_cells = [cell for row in grid for cell in row if cell.state == CellState.INVITE]
        for invite_cell in invite_cells:
            invite_cell.state = CellState.SEED
    cells = [cell for row in grid for cell in row if (cell.state != CellState.BLOCKED and cell.parent is not None)]
    for cell in cells:
        cell.walls -= wall_direction(cell.parent)
        parent_cell = grid[cell.row + directions[cell.parent][0]][cell.col + directions[cell.parent][1]]
        parent_cell.walls -= wall_direction(reverse_direction(cell.parent))
    return grid


def wall_direction(direction: str) -> int:
    if direction == 'N': return 8
    elif direction == 'E': return 4
    elif direction == 'S': return 2
    elif direction == 'W': return 1


def get_blocked_cells(rows: int, cols: int) -> set[tuple[int, int]]:
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

# ▌ (U+258C) – Left half block (Default)
# ▋ (U+258B) – Left five-eighths block
# ▊ (U+258A) – Left three-quarters block
# ▉ (U+2589) – Left seven-eighths block

# ▐ (U+2590A) - Right Half Block

# █ (U+2588) - Full Block

# ■ (U+25A0) - Black Square

def render_maze(grid: list[list[Cell]], start: tuple[int, int], end: tuple[int, int]):
    for r in range(len(grid)):
        for c1 in range(len(grid[0])):
            cell = grid[r][c1]
            if (c1 == 0 or c1 == len(grid[0]) - 1) and r > 0:
                print("▋", end="")
            else:
                print("▋", end="")
            if cell.walls & 8: # N wall
                print("▋", end="")
            else:
                print(" ", end="")
        print("▋")
        for c2 in range(len(grid[0])):
            cell = grid[r][c2]
            cell_left = grid[r][c2 - 1] if c2 > 0 else None
            if cell.walls & 1 and (cell_left is None or not cell_left.walls & 4): # W wall
                print("▋", end="")
            if cell.state == CellState.BLOCKED:
                print(f"{GREY}█{END}", end="")
            elif (cell.row, cell.col) == start:
                print(f"{GREEN}█{END}", end="")
            elif (cell.row, cell.col) == end:
                print(f"{RED}█{END}", end="")
            else:
                print(" ", end="")
            if cell.walls & 4: # E wall
                print("▋", end="")
            else:
                print(" ", end="")
        print()
    for c3 in range(len(grid[0])):
        cell = grid[r][c3]
        print("▋", end="")
        if cell.walls & 2: # S wall
            print("▋", end="")
        else:
            print(" ", end="")
    print("▋")


grid = initialise_grid(15, 15, (1, 1), (12, 12))
grid = algorithm_step(grid)

render_maze(grid, (1, 1), (12, 12))