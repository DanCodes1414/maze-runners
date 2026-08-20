# Reusable Standalone Module
This module contains the classes required to generate, solve, and export a maze. This module can be imported into your own personal projects!

---

The module was packaged from the root directory using:
```python -m build```

---

## Instructions
To import this module into your own project, follow these steps:
1. Copy the tar.gz or whl file into your project directory. Let's say your project directory is `my-project`.
2. Inside the `my-project` directory, run ```pip install file_name.tar.gz``` or ```pip install file_name.whl```
3. You can now use the module in your project!

---

## Example Usage
```python
from mazegen.maze import Maze
from mazegen.config import MazeConfig

maze_config = MazeConfig(
    width=25, height=20, entry=(0, 0), exit=(18, 13), perfect=False, braid=False, output_file="output.txt"
)
maze = Maze(config=maze_config)
maze.generate()
maze.solve()
maze.export()
```

---

## Code Classes

### Cell Class
The `Cell` class contains the position and walls for each individual cell in the maze.

### MazeConfig Class
The `MazeConfig` class contains the configuration required to generate a maze.
- width: The width of the maze.
- height: The height of the maze.
- entry: The coordinates of the maze entry point (row, col).
- exit: The coordinates of the maze exit point (row, col).
- seed: An optional seed for random number generation for maze reproducibility. If not provided, a random seed will be used.
- perfect: If True, generates a perfect maze (no loops). This set to True will override the braid option.
- braid: If True, generates a braided maze (a maze with loops and no dead ends).
- output_file: The name of the output file where the maze will be exported.

### Maze Class
The `Maze` class stores the maze details and has functions to generate, solve and export the maze.

---

## Maze Generation Algorithm
This program uses the Cell Automaton algorithm to generate a maze.
The algorithm iteratively processes SEED cells, inviting neighbouring FREE cells to connect and potentially (based on a set probability) become new SEED cells for branching. The process continues until there are no more FREE cells left in the grid (i.e., all cells are either CONNECTED or BLOCKED).

If the `perfect` config option is set to False, the maze will have multiple paths and loops. A non-perfect maze is generated from a perfect maze by randomly breaking down eligible walls.

If the `braid` config option is set to True, the maze will have no dead ends.