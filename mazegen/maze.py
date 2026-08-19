import random
from pydantic import BaseModel, Field
from .cell import Cell
from .generator import MazeGenerator, MazeConfigError
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
    """
    config: MazeConfig
    colours: ColourPair = Field(default=COLOUR_PAIRS[0])
    show_path: bool = Field(default=False)
    grid: list[list['Cell']] = Field(default_factory=list[list['Cell']])
    path: list[tuple[int, int]] = Field(default_factory=list)
    # TODO: Perhaps change to this -> path: list[str] = Field(default_factory=list)

    def generate(self) -> None:
        """
        Generates the maze using a maze generation algorithm and updates the grid attribute.
        """
        try:
            generator = MazeGenerator(self.config)
            self.grid = generator.generate()
        except MazeConfigError as ce:
            print(f"Configuration error: {ce}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def solve(self) -> None:
        """
        Solves the maze using a pathfinding algorithm (e.g., A* or BFS) and updates the path attribute.
        """
        if not self.grid:
            raise RuntimeError("Maze grid is not generated. Call generate() before solving.")
        pass

    # TODO: Remove this method?
    def render(self) -> None:
        """
        Renders the maze visually in the console or a graphical interface.
        """
        if not self.grid:
            raise RuntimeError("Maze grid is not generated. Call generate() before solving.")
        pass

    def switch_colours(self) -> None:
        """
        Switches the colour for rendering the maze.
        """
        new_colour_pair = self.colours
        while new_colour_pair == self.colours:
            new_colour_pair = random.Random().choice(COLOUR_PAIRS)
        self.colours = new_colour_pair

    def export(self, filename: str = "output_file.txt") -> None:
        """
        Exports the maze to a template file.
        """
        if not self.grid:
            raise RuntimeError("Maze grid is not generated. Call generate() before solving.")

        rows = len(self.grid)
        cols = len(self.grid[0])

        grid_lines = []
        for r in range(rows):
            row_chars = []
            for c in range(cols):
                cell = self.grid[r][c]
                row_chars.append(format(cell.walls, 'x'))
            grid_lines.append("".join(row_chars))

        shortest_path = ""
        # TODO: Implement pathfinding algorithm to find the shortest path and update the shortest_path variable.

        with open(filename, 'w') as f:
            for line in grid_lines:
                f.write(line + "\n")
            f.write(f"\n{self.config.entry[0] + 1},{self.config.entry[1] + 1}\n")
            f.write(f"{self.config.exit[0] + 1},{self.config.exit[1] + 1}\n")
            f.write(f"{shortest_path}\n")


if __name__ == "__main__":
    maze_config = MazeConfig(width=25, height=20, entry=(0, 0), exit=(18, 13), perfect=False, braid=True)
    maze = Maze(config=maze_config)
    maze.generate()
    maze.export(filename="output_file.txt")
