from .config import MazeConfig
from .cell import Cell, BreadCell
from .generator import direction_vectors
import time # needd to remove this 

class Queue:
    """A class to keep track of stuff
    """
    def __init__(self) -> None:
        self.queue: list[tuple[int, int]] = []

    def dequeue(self) -> tuple[int, int]:
        # remove element from the beginning of the queue
        return (self.queue.pop(0))

    def enqueue(self, element: tuple[int, int]) -> None:
        # add element to the end of the queue
        self.queue.append(element)

    def is_empty(self) -> bool:
        return len(self.queue) == 0


class MazeSolver:
    """
    A class to solve a maze using the BFS (Breadth-First Search) algorithm.

    Attributes:
        config (MazeConfig): The configuration for generating the maze.
        grid (list[list[Cell]]): A 2D list representing the maze grid with Cell objects.
    """  
    def __init__(self, grid: list[list['Cell']], config: MazeConfig) -> None:
        self.config = config
        self.grid = grid
        self.bfs_grid : list[list['BreadCell']] = []
        self.queue = Queue()

    @staticmethod
    def create_bread_grid(grid: list[list['Cell']]) -> list[list['BreadCell']]:
        """Converts the grid of Cells into Bread(th First Search)Cells."""
        rows = len(grid)
        cols = len(grid[0])
        bread_grid = [[BreadCell(row=r, col=c) for c in range(cols)] for r in range(rows)]
        for r in range(rows):
            for c in range(cols):
                bread_grid[r][c].walls = grid[r][c].walls
        return bread_grid
        
    def find_valid_directions(self, point: tuple[int, int], direction_vectors: dict[str, tuple[int, int]]) -> dict[str, tuple[int, int]]:
        valid_directions = {key:direction_vectors[key] for key in direction_vectors}
        walls = self.grid[point[0]][point[1]].walls
        if walls & 1:
            valid_directions.pop("N")
        if walls & 2:
            valid_directions.pop("E")
        if walls & 4:
            valid_directions.pop("S")
        if walls & 8:
            valid_directions.pop("W")
        return valid_directions

    def explore_neighbours(self, point: tuple[int, int]) -> None:
        """Explore and enqueue valid neighbours
        """
        valid_directions: dict[str, tuple[int, int]] = self.find_valid_directions(point, direction_vectors)
        for (drv, drc) in valid_directions.values():
            neighbour_row = point[0] + drv
            neighbour_col = point[1] + drc
            if 0 <= neighbour_row < self.config.height and 0 <= neighbour_col < self.config.width:
                if not self.bfs_grid[neighbour_row][neighbour_col].visited:
                    self.queue.enqueue((neighbour_row, neighbour_col))
                    self.bfs_grid[neighbour_row][neighbour_col].visited = True
                    self.bfs_grid[neighbour_row][neighbour_col].parent_cell = self.bfs_grid[point[0]][point[1]]

    def reverse_path(self, cell: BreadCell, entry_point: tuple[int, int], exit_point: tuple[int, int]) -> list[tuple[int, int]]:
        shortest_path = []
        point = (cell.row, cell.col)
        shortest_path.append(point)
        while point != entry_point:
            cell = cell.parent_cell
            point = (cell.row, cell.col)
            shortest_path.append(point)
        shortest_path.reverse() 
        return shortest_path

    def solve(self) -> list[tuple[int, int]]:
        """
        Solves the maze using the BFS algorithm and returns the path as a list of coordinates.
        """
        entry_point = self.config.entry
        exit_point = self.config.exit
        self.bfs_grid = self.create_bread_grid(self.grid)
        self.queue.enqueue(entry_point)
        self.bfs_grid[entry_point[0]][entry_point[1]].visited = True
        while not self.queue.is_empty():
            point = self.queue.dequeue()
            if point == exit_point:
                break
            self.explore_neighbours(point)
        shortest_path = self.reverse_path(self.bfs_grid[point[0]][point[1]], entry_point, exit_point)
        return shortest_path
