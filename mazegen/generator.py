from random import Random
from .config import MazeConfig
from .cell import Cell, AutomatonCell, CellState


TURN_PROB = 12
BRANCH_PROB = 5
directions = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}


class MazeConfigError(Exception):
    """Custom exception for invalid maze configurations."""
    pass


def wall_direction(direction: str) -> int:
    """Returns the wall bit corresponding to the given direction."""
    if direction == "N": return 1
    elif direction == "E": return 2
    elif direction == "S": return 4
    else: return 8


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


def branching(cell: 'AutomatonCell', rand: Random) -> None:
    """
    Determines whether the current cell should turn into a new seed cell based on BRANCH_PROB.
    This allows for branching in the maze generation process, creating more complex paths.
    """
    if rand.randint(0, 100) > BRANCH_PROB:
        cell.state = CellState.CONNECTED
    else:
        cell.state = CellState.SEED


def reverse_direction(direction: str) -> str:
    """Returns the opposite direction of the given direction."""
    if direction == "N": return "S"
    elif direction == "E": return "W"
    elif direction == "S": return "N"
    else: return "E"


def turn_direction(cell: AutomatonCell, rand: Random) -> str | None:
    """
    Determines the next direction for the maze path.

    With probability TURN_PROB, randomly selects a direction. Otherwise,
    goes in the opposite direction to the parent cell.
    If the chosen direction has no free neighbours, selects a random free neighbour direction instead.

    Args:
        cell: The current cell.
        rand: Random instance for probability-based decisions.

    Returns:
        A direction string ('N', 'S', 'E', 'W') or None if no free neighbours.
    """
    if rand.randint(0, 100) <= TURN_PROB:
        direction = rand.choice(["N", "E", "S", "W"])
    else:
        direction = reverse_direction(cell.parent)

    if cell.free_neighbours == []:
        return None
    if direction not in cell.free_neighbours:
        direction = rand.choice(cell.free_neighbours)
    return direction


def update_free_neighbours(cell: 'AutomatonCell', grid: list[list['AutomatonCell']]) -> None:
    """
    Updates the free_neighbours attribute of the given cell based on its current state
    and the states of its neighbouring cells.
    """
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


def initialise_grid(config:MazeConfig) -> list[list['AutomatonCell']]:
    """
    Initialises a grid of AutomatonCells with the specified dimensions.
    """
    grid = [[AutomatonCell(row=r, col=c) for c in range(config.width)] for r in range(config.height)]
    blocked_cells = get_blocked_cells(config.height, config.width)
    for r in range(config.height):
        for c in range(config.width):
            if (r, c) in blocked_cells:
                grid[r][c].state = CellState.BLOCKED
            if (r, c) == config.entry:
                grid[r][c].state = CellState.SEED
    for r in range(config.height):
        for c in range(config.width):
            update_free_neighbours(grid[r][c], grid)
    return grid


def any_free_cells(grid: list[list['AutomatonCell']]) -> bool:
    """
    Checks if there are any FREE cells in the grid.
    """
    for row in grid:
        for cell in row:
            if cell.state == CellState.FREE:
                return True
    return False


def algorithm_step(grid: list[list['AutomatonCell']], rand: Random) -> list[list['AutomatonCell']]:
    """
    Uses the Cell Automaton algorithm to generate the maze.
    The algorithm iteratively processes seed cells, inviting neighbouring free cells to connect
    and potentially become new seed cells for branching.
    The process continues until there are no more FREE cells left in the grid
    (i.e., all cells are either CONNECTED or BLOCKED).
    """
    while any_free_cells(grid):
        seed_cells = [cell for row in grid for cell in row if cell.state == CellState.SEED]
        if not seed_cells:
            connected_cells = [
                cell for row in grid for cell in row
                if cell.state == CellState.CONNECTED and cell.free_neighbours
            ]
            rand.choice(connected_cells).state = CellState.SEED
        for seed_cell in seed_cells:
            direction = turn_direction(seed_cell, rand)
            if direction is None:
                seed_cell.state = CellState.CONNECTED
                continue
            drv, dcv = directions[direction]
            neighbour_cell = grid[seed_cell.row + drv][seed_cell.col + dcv]
            neighbour_cell.state = CellState.INVITE
            neighbour_cell.parent = reverse_direction(direction)
            update_free_neighbours(neighbour_cell, grid)
            update_free_neighbours(seed_cell, grid)
            branching(seed_cell, rand)
        invite_cells = [cell for row in grid for cell in row if cell.state == CellState.INVITE]
        for invite_cell in invite_cells:
            invite_cell.state = CellState.SEED
    cells = [cell for row in grid for cell in row if (cell.state != CellState.BLOCKED and cell.parent)]
    for cell in cells:
        cell.walls -= wall_direction(cell.parent)
        parent_cell = grid[cell.row + directions[cell.parent][0]][cell.col + directions[cell.parent][1]]
        parent_cell.walls -= wall_direction(reverse_direction(cell.parent))
    return grid


def imperfect_maze(grid: list[list['AutomatonCell']], rand: Random) -> list[list['AutomatonCell']]:
    """
    Introduces loops into a perfect maze by knocking down shared walls.
    """
    removal_rate = rand.randint(5, 25) / 100
    rows = len(grid)
    cols = len(grid[0])

    WALL_N, WALL_E, WALL_S, WALL_W = 1, 2, 4, 8
    wall_directions = [
        (WALL_E, WALL_W, 0, 1),
        (WALL_S, WALL_N, 1, 0)
    ]

    eligible_walls = []
    for r in range(rows):
        for c in range(cols):
            current_cell = grid[r][c]
            if current_cell.state == CellState.BLOCKED:
                continue

            for wall_bit, opp_bit, dr, dc in wall_directions:
                if (current_cell.walls & wall_bit) != 0:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_cell = grid[nr][nc]
                        if neighbor_cell.state != CellState.BLOCKED:
                            eligible_walls.append((current_cell, neighbor_cell, wall_bit, opp_bit))

    num_to_remove = int(len(eligible_walls) * removal_rate)
    walls_to_remove = rand.sample(eligible_walls, num_to_remove)

    for current_cell, neighbor_cell, wall_bit, opp_bit in walls_to_remove:
        current_cell.walls &= ~wall_bit
        neighbor_cell.walls &= ~opp_bit

    return grid


def perfectly_braided_maze(grid: list[list['AutomatonCell']], rand: Random) -> list[list['AutomatonCell']]:
    """
    Braids the maze by removing all dead ends.
    """
    rows = len(grid)
    cols = len(grid[0])

    WALL_N, WALL_E, WALL_S, WALL_W = 1, 2, 4, 8
    wall_directions = [
        (WALL_E, WALL_W, 0, 1),
        (WALL_S, WALL_N, 1, 0)
    ]

    for r in range(rows):
        for c in range(cols):
            current_cell = grid[r][c]
            if current_cell.state == CellState.BLOCKED:
                continue

            wall_count = bin(current_cell.walls).count('1')
            if wall_count == 3:
                for wall_bit, opp_bit, dr, dc in wall_directions:
                    if (current_cell.walls & wall_bit) != 0:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor_cell = grid[nr][nc]
                            if neighbor_cell.state != CellState.BLOCKED:
                                current_cell.walls &= ~wall_bit
                                neighbor_cell.walls &= ~opp_bit
                                break
    return grid


def create_simple_grid(grid: list[list['AutomatonCell']]) -> list[list['Cell']]:
    """Converts the grid of AutomatonCells into a simpler grid of Cells."""
    rows = len(grid)
    cols = len(grid[0])
    simple_grid = [[Cell(row=r, col=c) for c in range(cols)] for r in range(rows)]
    for r in range(rows):
        for c in range(cols):
            simple_grid[r][c].walls = grid[r][c].walls

    return simple_grid


class MazeGenerator:
    """
    A class to generate mazes using the Cell Automaton algorithm.

    Attributes:
        config (MazeConfig): The configuration for generating the maze.
        grid (list[list[AutomatonCell]]): A 2D list representing the maze grid with AutomatonCell objects.
    """
    def __init__(self, config: MazeConfig):
        self.config = config
        self.grid: list[list['AutomatonCell']] = []

    def generate(self) -> list[list['Cell']]:
        """
        Generates a maze based on the provided configuration.

        Returns:
            list[list[Cell]]: A 2D list representing the generated maze grid with Cell objects.
        """
        self.grid = initialise_grid(self.config)
        rand = Random(self.config.seed)
        self.grid = algorithm_step(self.grid, rand)
        if not self.config.perfect:
            self.grid = imperfect_maze(self.grid, rand)
        if self.config.braid:
            self.grid = perfectly_braided_maze(self.grid, rand)
        simple_grid = create_simple_grid(self.grid)
        return simple_grid
