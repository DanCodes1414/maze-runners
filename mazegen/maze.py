import random
from pydantic import BaseModel, Field
from .cell import Cell
from .generator import MazeGenerator
from .solver import MazeSolver
from .colours import ColourPair, COLOUR_PAIRS
from .config import MazeConfig


class Maze(BaseModel):
    """
    Represents a maze with a grid of cells, start and end positions, and the generated path.

    Attributes:
        config (MazeConfig): The configuration for generating the maze.
        colours (str): Color codes for rendering the maze.
        grid (list[list[Cell]]): A 2D list representing the maze grid with Cell objects.
        path (list[tuple[int, int]]): A list of coordinates representing the generated path from entry to exit.
        generated (bool): A flag indicating whether the maze has been generated.
    """
    config: MazeConfig
    colours: ColourPair = Field(default=COLOUR_PAIRS[0])
    show_path: bool = Field(default=False)
    grid: list[list['Cell']] = Field(default_factory=list[list['Cell']])
    path: list[tuple[int, int]] = Field(default_factory=list) # TODO: Perhaps change to this -> path: list[str] = Field(default_factory=list)
    generated: bool = Field(default=False, exclude=True)

    def generate(self) -> None:
        """
        Generates the maze using a maze generation algorithm and updates the grid attribute.
        """
        try:
            generator = MazeGenerator(self.config)
            self.grid = generator.generate()
            self.generated = True
        except Exception as e:
            print(f"Unexpected error: {e}")

    def solve(self) -> None:
        """
        Solves the maze using a pathfinding algorithm (e.g., A* or BFS) and updates the path attribute.
        """
        if not self.generated:
            raise RuntimeError("Maze grid is not generated. Call generate() before solving.")
        try:
            solver = MazeSolver(self.config)
            self.path = solver.solve()
        except Exception as e:
            print(f"Unexpected error: {e}")

    # TODO: Remove this method?
    def render(self) -> None:
        """
        Renders the maze visually in the console or a graphical interface.
        """
        if not self.generated:
            raise RuntimeError("Maze grid is not generated. Call generate() before rendering.")
        pass

    def switch_colours(self) -> None:
        """
        Switches the colour for rendering the maze.
        """
        new_colour_pair = self.colours
        while new_colour_pair == self.colours:
            new_colour_pair = random.Random().choice(COLOUR_PAIRS)
        self.colours = new_colour_pair

    def export(self) -> None:
        """
        Exports the maze to a template file.
        """
        if not self.generated:
            raise RuntimeError("Maze grid is not generated. Call generate() before exporting.")

        grid_lines = []
        for r in range(self.config.height):
            row_chars = []
            for c in range(self.config.width):
                cell = self.grid[r][c]
                row_chars.append(cell.hex_representation())
            grid_lines.append("".join(row_chars))

        if not len(self.path):
            self.solve()
        direction_vectors = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "W": (0, -1)
        }
        shortest_path = ""
        for i in range(len(self.path) - 1):
            current_r, current_c = self.path[i]
            next_r, next_c = self.path[i + 1]
            dr = next_r - current_r
            dc = next_c - current_c
            direction = None
            for dir_key, (dir_r, dir_c) in direction_vectors.items():
                if (dr, dc) == (dir_r, dir_c):
                    direction = dir_key
                    break
            shortest_path += direction

        try:
            with open(self.config.output_file, 'w') as f:
                for line in grid_lines:
                    f.write(line + "\n")
                f.write(f"\n{self.config.entry[1]},{self.config.entry[0]}\n")
                f.write(f"{self.config.exit[1]},{self.config.exit[0]}\n")
                f.write(f"{shortest_path}\n")
        except Exception as e:
            print(f"Error exporting maze to file: {e}")
