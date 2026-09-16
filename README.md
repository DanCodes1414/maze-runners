*This project has been created as part of the 42 curriculum by dmgeorgi, dqureshi.*

# A-Maze-ing

## Description

A-Maze-ing generates a maze from a plain-text configuration file, writes it to
disk using hexadecimal wall encoding, and displays it graphically.

Depending on the configuration, the generated maze can be:

- A perfect maze with exactly one path between the entry and exit.
- A playable Pac-Man-style board containing loops and alternative routes.
- A braided maze with no dead ends.

The reusable generation logic lives in `mazegen`, a standalone Python package
that can be built as a wheel and installed into another project.

## Instructions

### Requirements

- Python 3.10 or later
- A Linux graphical environment
- The Python `venv` module
- MiniLibX

The MiniLibX installation files required by the visualizer are included in
`vis_src`:

```text
vis_src/
├── fedora/
│   └── mlx-2.2-py3-none-any.whl
├── mlx-2.2.tgz
├── src/
│   └── mlx_CLXV-2.2.tgz
└── ubuntu/
    └── mlx-2.2-py3-none-any.whl
```

### Setting up MiniLibX

Run the following commands from the root of the repository.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the MiniLibX wheel matching your Linux distribution.

On Ubuntu:

```bash
python -m pip install vis_src/ubuntu/mlx-2.2-py3-none-any.whl
```

On Fedora:

```bash
python -m pip install vis_src/fedora/mlx-2.2-py3-none-any.whl
```

The source archives are also included in `vis_src` for reference or for systems
where MiniLibX needs to be rebuilt.

Confirm that the Python package can be imported:

```bash
python -c "from mlx import Mlx; print('MiniLibX import successful')"
```

To check whether MiniLibX can connect to the graphical display:

```bash
python -c "from mlx import Mlx; print(Mlx().mlx_init())"
```

A non-`None` pointer means that MiniLibX initialized successfully.

This second command must be run from a graphical session. It may return `None`
when run through SSH, a headless terminal, or an environment without access to
the display, even if the package was installed correctly.

The virtual environment must be activated again whenever a new terminal is
opened:

```bash
source .venv/bin/activate
```

The `.venv` directory is machine-specific and must not be submitted. It should
be included in `.gitignore`.

### MiniLibX Set-up on Mac

MiniLibX must be run on a UTM virtual machine. Follow these steps only if running on a MacOS:

1. Download UTM: https://mac.getutm.app/
2. Open UTM and create a new `Virtualise -> Linux` VM with the Debian iso (https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/) and 25GB drive size
3. Run `Graphical Install`
4. Don't create a root user account
5. Create a user account with your intra name as the username and choose a short simple password
6. Choose the first Guided partition option
7. Add the Debian Desktop env and GNOME packages to be installed
8. Once installed, press continue and then close the page
9. On the main UTM page, stop the VM, clear the iso image for the VM, and then start the VM again
10. Login with the account password set earlier
11. Open the terminal inside the VM and run `ssh-keygen -t ed25519 -C "YOUR_EMAIL"`
12. Run `cat .ssh/id_ed25519.pub` and copy the value (Shift -> Control -> C)
13. Paste the value in intra SSH settings (https://profile.intra.42.fr/gitlab_users)
14. Run `sudo apt install libxcb1-dev libxcb-keysyms1-dev libvulkan-dev zlib1g-dev libbsd-dev glslc pip clang git`
15. Now clone the repo: `git clone REPO_NAME a_maze_ing && cd a_maze_ing`
16. Run `python3 -m venv .venv && source .venv/bin/activate`
17. Run `git clone https://github.com/42school/mlx_CLXV.git && cd mlx_CLXV && ./configure.sh && make && cd ..`
18. Run `make install-mac` and finally `make run`


### Running the program

Run the program from the root of the repository:

```bash
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` takes exactly one argument: the path to a configuration file.

A configuration error stops the program, prints an error message to `stderr`,
and exits with status code 1. A successful run exits with status code 0.

### Visualizer controls

| Key | Action |
| --- | --- |
| `1` | Generate and display a new maze |
| `2` | Show or hide the shortest path |
| `3` | Change the maze colours |
| `4` | Quit the program |

The visualizer can also be closed using the window's close button.

Pressing `Ctrl-Z` suspends the process. If this happens, return it to the
foreground by entering the following command in the terminal:

```bash
fg
```


## Configuration file

A default configuration file is provided as `config.txt` at the root of the
repository.

### Format

- Each setting uses one `KEY=VALUE` pair per line.
- The key is everything before the first `=`.
- Blank lines are ignored.
- Lines whose first non-whitespace character is `#` are comments.
- Inline comments are not supported.
- Whitespace around keys and values is ignored.
- Keys are case-insensitive.
- Unknown keys are ignored, but their lines must still contain an `=`.
- A recognised key with an empty value is a syntax error.
- If a recognised key appears more than once, the first value is kept and a
  warning is printed to `stderr`.

For example:

```ini
WIDTH = 20
```

is valid, while:

```ini
WIDTH=20 # cells
```

is not. Because inline comments are not supported, the value is interpreted as
`20 # cells` and cannot be converted to an integer.

### Mandatory keys

| Key | Meaning | Value format | Example |
| --- | --- | --- | --- |
| `WIDTH` | Maze width in cells | Integer | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | Integer | `HEIGHT=15` |
| `ENTRY` | Entry cell | Zero-based `x,y` coordinates | `ENTRY=0,0` |
| `EXIT` | Exit cell | Zero-based `x,y` coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | File where the maze is written | Filename without a directory | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to generate a perfect maze | `True` or `False`, case-insensitive | `PERFECT=True` |

### Optional keys

| Key | Meaning | Value format | Default |
| --- | --- | --- | --- |
| `SEED` | Seed used for reproducible generation | Non-negative integer | A random seed |
| `BRAIDED` | Whether to remove all dead ends | `True` or `False`, case-insensitive | `False` |

### Validity rules

- A perfect maze requires both dimensions to be at least 1 and its total area
  to be at least 2.
- An imperfect maze requires both dimensions to be at least 2 and its total
  area to be at least 6.
- `ENTRY` and `EXIT` must be inside the maze.
- `ENTRY` and `EXIT` must refer to different cells.
- `OUTPUT_FILE` may not contain `/`.
- `OUTPUT_FILE` may not refer to the configuration file itself.
- `PERFECT` and `BRAIDED` cannot both be `True`, because a braided maze contains
  loops by definition.

An imperfect grid must support at least two independent loops. A grid containing
W by H cells can hold at most `(W - 1)(H - 1)` independent loops, making 2 by 3
the smallest supported imperfect maze.

### Example configuration

```ini
# Default A-Maze-ing configuration

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
BRAIDED=False
```

### Example errors

| Invalid configuration | Result |
| --- | --- |
| `WIDTH=abc` | `Error: ValueError on WIDTH. WIDTH value in configuration file: 'abc'` |
| Entry and exit both set to `0,0` | `Error: Entry and exit points cannot be the same.` |
| `HEIGHT` is missing | `Error: The following mandatory keys are missing: ['HEIGHT']` |

## Maze generation algorithm

The generator uses a cellular automaton. Each cell has one of three states:

- `FREE`
- `SEED`
- `BLOCKED`

The algorithm repeatedly processes the `SEED` cells. Each seed attempts to
connect to neighbouring `FREE` cells. A newly connected cell can become a new
`SEED`, causing the maze to grow and branch.

Generation stops when no `FREE` cells remain. At this point, every cell has
either been connected to the maze or marked as blocked.

This initial generation produces a perfect maze. The configuration flags can
then modify it:

- With `PERFECT=True`, no additional walls are removed, so exactly one route
  exists between any two connected cells.
- With `PERFECT=False`, eligible walls are selected randomly and removed. This
  creates loops and independent routes suitable for a Pac-Man-style board.
- With `BRAIDED=True`, the remaining dead ends are removed.

The visible `42` pattern is represented using `BLOCKED` cells. These cells are
fully enclosed and excluded from the connected maze structure.

### Why this algorithm

The cellular automaton was chosen because it builds the maze incrementally
while keeping the state of every cell explicit. The `FREE`, `SEED`, and
`BLOCKED` states make it possible to control how the maze expands and to reserve
cells for the `42` pattern.

The branching probability introduces randomness without requiring recursive
function calls. Starting with a connected perfect maze also provides a useful
foundation for both required generation modes: it can be kept unchanged for a
perfect maze or modified by removing walls to produce a board with loops.

## Output file

Each maze cell is represented by one hexadecimal digit. The four least
significant bits describe its walls:

| Bit | Direction |
| --- | --- |
| `0` | North |
| `1` | East |
| `2` | South |
| `3` | West |

A set bit means that the wall is closed. A cleared bit means that the wall is
open.

The maze is written row by row, with one output line for each row of cells.

After the maze grid, the file contains an empty line followed by:

1. The entry coordinates.
2. The exit coordinates.
3. The shortest valid path using the letters `N`, `E`, `S`, and `W`.

Every line ends with a newline character.

## Visualizer

The graphical visualizer is implemented with MiniLibX. The maze is drawn into
an image buffer before the complete image is copied to the window.

The visualizer is divided into three classes:

| Class | Responsibility |
| --- | --- |
| `Canvas` | Writes individual pixels and filled rectangles into an MLX image |
| `MazePainter` | Calculates maze dimensions and draws cells, walls, blocked cells, and colours |
| `MazeRender` | Manages the MLX window, keyboard callbacks, regeneration, refreshing, and cleanup |

This separation keeps raw image-buffer operations out of the maze drawing code.
It also keeps MiniLibX window management separate from the rules used to draw
the maze.

The maze generator does not import or depend on the visualizer.

## Reusable code

The reusable part of the project is the `mazegen` package. It contains the
classes needed to configure, generate, solve, and export a maze.

It does not depend on the configuration-file parser or the graphical
visualizer, allowing it to be installed and reused in another project.

### Building the package

Build the package from the root of the repository:

```bash
python -m build
```

This produces a source distribution and a wheel with names similar to:

```text
mazegen-1.0.0.tar.gz
mazegen-1.0.0-py3-none-any.whl
```

### Installing the package

Install the wheel with:

```bash
python -m pip install mazegen-1.0.0-py3-none-any.whl
```

Alternatively, install the source distribution:

```bash
python -m pip install mazegen-1.0.0.tar.gz
```

After installation, `mazegen` can be imported from any Python program using
that environment.

### Basic example

```python
from mazegen.config import MazeConfig
from mazegen.maze import Maze

maze_config = MazeConfig(
    width=25,
    height=20,
    entry=(0, 0),
    exit=(18, 13),
    perfect=False,
    braid=False,
    seed=42,
    output_file="output.txt",
)

maze = Maze(config=maze_config)
maze.generate()
maze.solve()
maze.export()
```

### Custom parameters

All generation parameters are passed through `MazeConfig`:

| Parameter | Meaning |
| --- | --- |
| `width` | Maze width in cells |
| `height` | Maze height in cells |
| `entry` | Entry-cell coordinates |
| `exit` | Exit-cell coordinates |
| `perfect` | Whether the maze must contain exactly one route |
| `braid` | Whether all dead ends should be removed |
| `seed` | Optional seed for reproducible generation |
| `output_file` | Name of the file written by `export()` |

Using the same dimensions and seed produces the same maze:

```python
config = MazeConfig(
    width=25,
    height=20,
    entry=(0, 0),
    exit=(18, 13),
    perfect=True,
    braid=False,
    seed=42,
    output_file="output.txt",
)
```

### Accessing the generated maze

The generated cell structure is available through:

```python
maze.grid
```

Each item in the grid is a `Cell` containing its coordinates, state, and wall
data.

Generate and solve the maze with:

```python
maze.generate()
maze.solve()
```

The solution is the shortest valid route from the configured entry to the
configured exit.

### Main classes

- **`Cell`** represents one cell and stores its position, state, and walls.
- **`MazeConfig`** stores and validates the generation parameters.
- **`Maze`** generates, solves, and exports the maze.

The package includes its own documentation so it remains usable independently
of the main repository.

## Parsing and validation

Configuration parsing and validation are divided between four modules:

| Module | Responsibility |
| --- | --- |
| `mazegen/errors.py` | Defines the `MazeConfigError` exception hierarchy |
| `mazegen/config.py` | Defines `MazeConfig` and validates typed configuration values |
| `parser_errors.py` | Defines errors relating to configuration-file syntax |
| `config_parser.py` | Reads the file, converts its values, and creates a `MazeConfig` |

`mazegen/errors.py` and `mazegen/config.py` are included in the reusable
package. The file parser remains at the repository root because it belongs to
the A-Maze-ing command-line program rather than the reusable generator.

The dependencies point in one direction:

```text
config_parser -> mazegen.config -> mazegen.errors
config_parser -> parser_errors
```

`MazeParsing.parse_config_from_file(path)` reads a configuration file and
returns a validated `MazeConfig`.

`MazeParsing` does not hold state and is not instantiated. Its parsing steps are
implemented using static methods and class methods so they can be tested
independently.

A `MazeConfig` can also be created directly from values that have already been
converted to the correct Python types.

### Error handling

Configuration failures can come from four sources:

- `MazeParserError` subclasses for invalid configuration-file syntax.
- `ValueError` when a dimension, seed, or coordinate is not an integer.
- `MazeConfigError` subclasses when validly formatted values describe an
  impossible maze.
- `OSError` when the configuration file cannot be opened.

Example:

```python
from config_parser import MazeParsing
from mazegen.errors import MazeConfigError
from parser_errors import MazeParserError

try:
    maze_config = MazeParsing.parse_config_from_file("config.txt")
except (MazeConfigError, MazeParserError, ValueError, OSError) as error:
    print(f"Error: {error}")
```

Values are converted in the following order:

1. `OUTPUT_FILE`
2. `PERFECT`
3. `BRAIDED`
4. `WIDTH`
5. `HEIGHT`
6. `SEED`
7. `ENTRY`
8. `EXIT`

Parsing stops when the first error is found.

The exception classes contain further documentation in their docstrings:

```bash
python3 -c "import parser_errors; help(parser_errors)"
python3 -c "import mazegen.errors; help(mazegen.errors)"
```

## Team and project management

### Roles

- **dmgeorgi:** configuration parsing and validation, including
  `config_parser.py`, `parser_errors.py`, `mazegen/config.py`, and
  `mazegen/errors.py`.
- **dqureshi:** maze generation, graphical visualization, and packaging of the
  reusable `mazegen` module.

### Planning and how it evolved

dmgeorgi was new to learning Python in a structured way. Before starting
A-Maze-ing, he completed and submitted Python modules 0 through 4.

These modules introduced classes, inheritance, exceptions, error handling, and
context managers. The project provided an opportunity to apply those concepts
to a larger program.

He did not study modules 5 through 10 before or during the project. This was
partly due to time constraints and partly a conscious choice to avoid getting
stuck in tutorial material without applying the concepts already learned.

During the project, the team reviewed the implementation and found places where
knowledge of additional Python libraries could have reduced the amount of code.
For example, discovering Pydantic later showed that some parts of configuration
validation could have been implemented differently.

### What worked well

- Dividing the project into generation, parsing, validation, visualization, and
  packaging responsibilities allowed the team members to work independently.
- Separating `MazeConfig` validation from file parsing made the reusable package
  independent of the main program.
- Starting from a connected perfect maze made it possible to support perfect,
  imperfect, and braided generation modes.
- Keeping MiniLibX inside a virtual environment made its installation
  reproducible without modifying the system Python installation.

### What could be improved

- Some design decisions were made before the complete interaction between the
  generator, parser, and visualizer was known.
- More integration tests could have been written earlier.
- Earlier research into Python packaging and validation libraries could have
  reduced repeated work.

### Tools

- Python virtual environments for dependency isolation.
- MiniLibX for the graphical visualizer.
- `pytest` or `unittest` for testing.
- `flake8` for style checking.
- `mypy` for static type checking.
- Python's `build` package for producing the reusable distribution files.
- Git for version control and team collaboration.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [MiniLibX Python Manual](https://github.com/noradefitero/42_MiniLibX_Python_Manual)
- [Official MiniLibX repository](https://github.com/42school/mlx_CLXV)

### How AI was used

AI assistants were used to support review and discussion rather than to replace
understanding of the implementation.

They were used to:

- Suggest tests and edge cases for configuration parsing.
- Review MiniLibX image-buffer and callback handling.
- Discuss how to separate drawing, maze rendering, and window management.
- Review and improve project documentation.
- Suggest colour values and colour combinations for the visualizer.

AI was used to generate initial colour combinations for the visualizer.
The suggestions were reviewed and adapted before being included in the project.

All AI-generated suggestions were checked against the subject, tested where
appropriate, and reviewed by the team before use.