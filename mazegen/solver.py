from .config import MazeConfig
from .cell import Cell


class MazeSolver:
    """
    A class to solve a maze using the BFS (Breadth-First Search) algorithm.

    Attributes:
        config (MazeConfig): The configuration for generating the maze.
        grid (list[list[AutomatonCell]]): A 2D list representing the maze grid with AutomatonCell objects.
    """
    def __init__(self, config: MazeConfig):
        self.config = config
        self.grid: list[list['Cell']] = []

    def solve(self) -> list[tuple[int, int]]:
        """
        Solves the maze using the BFS algorithm and returns the path as a list of coordinates.
        """
        # TODO: Implement the BFS algorithm to find the shortest path from entry to exit in the maze.
        entry = self.config.entry
        return [self.config.entry, (entry[0], entry[1] + 1)]
