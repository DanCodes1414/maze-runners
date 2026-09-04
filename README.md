*This project has been created as part of the 42 curriculum by dmgeorgi, dqureshi.*

# A-Maze-ing

## Description

A-Maze-ing generates a maze from a plain-text configuration file, writes it to
disk using a hexadecimal wall encoding, and displays it. The maze can either be
perfect (exactly one path between entry and exit) or a playable board with
loops and no dead ends, depending on the configuration.

The generation logic itself lives in `mazegen`, a standalone Python package that
can be built as a wheel and installed into another project with `pip`. See
[Reusable code](#reusable-code).

`<rewrite this in your own words — it is the first thing a peer reads>`

## Instructions

```
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` takes exactly one argument: the path to a configuration file.
Any configuration error stops the program with a message on `stderr` and exit
code 1; a successful run exits with 0.

## Configuration file

A default configuration is provided in `config.txt` at the root of the
repository.

### Format

- One `KEY=VALUE` pair per line. The key is everything before the first `=`,
  so a value may itself contain further `=` characters.
- Lines whose first non-whitespace character is `#` are comments. There are no
  inline comments: `WIDTH=20 # cells` sets `WIDTH` to `20 # cells`, which then
  fails to convert to an integer.
- Blank lines are ignored.
- Whitespace around keys and values is ignored, so `WIDTH = 20` is fine.
- Keys are case-insensitive (`width=20` and `WIDTH=20` are equivalent).
- Keys that are not listed below are ignored, but every line still has to
  contain an `=`: a line without one is a syntax error whether or not its key
  is recognised.
- A recognised key with an empty value is a syntax error.
- If a recognised key appears twice, the first value is kept and a warning is
  printed to `stderr`.

### Mandatory keys

| Key           | Meaning                        | Value format                 | Example                |
|---------------|--------------------------------|------------------------------|------------------------|
| `WIDTH`       | Maze width in cells            | integer                      | `WIDTH=20`             |
| `HEIGHT`      | Maze height in cells           | integer                      | `HEIGHT=15`            |
| `ENTRY`       | Entry cell                     | `x,y`, zero-based            | `ENTRY=0,0`            |
| `EXIT`        | Exit cell                      | `x,y`, zero-based            | `EXIT=19,14`           |
| `OUTPUT_FILE` | Where the maze is written      | bare filename, no directory  | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Generate a perfect maze?       | `True` or `False`, any case  | `PERFECT=True`         |

### Optional keys

| Key       | Meaning                                  | Value format                | Default when absent                |
|-----------|------------------------------------------|-----------------------------|------------------------------------|
| `SEED`    | Seed for reproducible generation         | non-negative integer        | a random seed is used              |
| `BRAIDED` | Generate a board with no dead ends at all | `True` or `False`, any case | `False` (dead ends are tolerated)  |

### Validity rules

- A perfect maze needs both dimensions to be at least 1 and an area of at
  least 2.
- An imperfect maze needs both dimensions to be at least 2 and an area of at
  least 6. A grid of W×H cells can hold at most (W−1)(H−1) independent loops,
  and the subject requires at least two, so 2×3 is the smallest playable board.
- `ENTRY` and `EXIT` must lie inside the grid (0 ≤ x < WIDTH, 0 ≤ y < HEIGHT)
  and must be different cells.
- `OUTPUT_FILE` may not contain `/` and may not be the configuration file
  itself. The second check resolves both paths, so a symbolic link or a
  different relative path leading back to the configuration file is caught too.
- `PERFECT` and `BRAIDED` cannot both be `True`: a braided board contains loops
  by definition.

### Example

```ini
# Default A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

### Example errors

| Line               | Message                                                              |
|--------------------|----------------------------------------------------------------------|
| `WIDTH=abc`        | `Error: ValueError on WIDTH. WIDTH value in configuration file: 'abc'` |
| `EXIT=0,0` (same as entry) | `Error: Entry and exit points cannot be the same.`           |
| `HEIGHT` missing   | `Error: The following mandatory keys are missing: ['HEIGHT']`        |

## Maze generation algorithm

The generator uses a cellular automaton. Each cell of the grid holds a state:
`FREE`, `SEED` or `BLOCKED`. The algorithm repeatedly processes the `SEED`
cells; each one invites its neighbouring `FREE` cells to connect to it, and a
newly connected cell becomes a `SEED` itself with a fixed probability, which is
what makes the maze branch. It stops when no `FREE` cell is left, so every cell
ends up either connected or blocked.

That pass produces a perfect maze. The configuration flags then modify it:

- With `PERFECT=False`, eligible walls are chosen at random and broken down.
  This adds the loops and independent routes a Pac-Man-style board needs.
- With `BRAIDED=True`, dead ends are removed as well, so the board has none at
  all.

`<how the "42" pattern is placed, and how it relates to the BLOCKED state>`

### Why this algorithm

`<your reasoning — what made the cellular automaton the right choice for you>`

## Reusable code

The `mazegen` package is the reusable part of this project. It contains the
classes needed to generate, solve and export a maze, and nothing that depends
on the rest of the repository, so it can be installed into any other project.

### Installing the package

The package is built from the root of the repository with:

```
python -m build
```

This produces a `.tar.gz` and a `.whl` file named `mazegen-*`. To use the
package in another project:

1. Copy the `.tar.gz` or `.whl` file into your project directory.
2. From that directory, run `pip install mazegen-1.0.0-py3-none-any.whl`
   (or the `.tar.gz` equivalent).
3. `import mazegen` now works from anywhere in that project.

### Basic example

```python
from mazegen.maze import Maze
from mazegen.config import MazeConfig

maze_config = MazeConfig(
    width=25,
    height=20,
    entry=(0, 0),
    exit=(18, 13),
    perfect=False,
    braid=False,
    output_file="output.txt",
)
maze = Maze(config=maze_config)
maze.generate()
maze.solve()
maze.export()
```

### Custom parameters

All generation parameters are passed through `MazeConfig`:

| Parameter     | Meaning                                                                 |
|---------------|-------------------------------------------------------------------------|
| `width`       | Maze width in cells.                                                    |
| `height`      | Maze height in cells.                                                   |
| `entry`       | Coordinates of the entry cell.                                          |
| `exit`        | Coordinates of the exit cell.                                           |
| `seed`        | Optional. Seed for random generation, for reproducible mazes. A random seed is used when omitted. |
| `perfect`     | `True` generates a perfect maze (no loops).                             |
| `braid`       | `True` generates a braided maze: loops, and no dead ends.               |
| `output_file` | Name of the file `export()` writes to.                                  |

Passing the same `seed` with the same dimensions produces the same maze every
time:

```python
config = MazeConfig(width=25, height=20, entry=(0, 0), exit=(18, 13),
                    perfect=True, braid=False, seed=42,
                    output_file="output.txt")
```

### Accessing the structure and the solution

`<how a user reads the grid out of a Maze object, and how they read the
solution — attribute names and what the values look like>`

### Classes

- **`Cell`** — the position and walls of a single cell of the maze.
- **`MazeConfig`** — the configuration a maze is generated from, and the
  validation of those values. See the table above.
- **`Maze`** — the maze itself, with `generate()`, `solve()` and `export()`.

The same documentation ships inside the package, so anyone who installs the
wheel has it without visiting this repository.

## Parsing and validation (dmgeorgi)

Configuration handling is split across four modules so that the validation
logic can be packaged without the file-parsing code:

| Module              | Responsibility                                                    |
|---------------------|-------------------------------------------------------------------|
| `mazegen/errors.py` | The `MazeConfigError` exception hierarchy. Imports nothing from the project. |
| `mazegen/config.py` | The `MazeConfig` class: takes raw, already-typed values and validates them. |
| `parser_errors.py`  | The `MazeParserError` exception hierarchy, for failures that belong to the file rather than to the maze. |
| `config_parser.py`  | The `MazeParsing` class: reads a configuration file, converts each value to its type, and builds a `MazeConfig`. |

The first two live inside the `mazegen` package, so a project that installs the
package gets the validation without the file parsing. The other two stay at the
root of the repository: they exist to serve `a_maze_ing.py` and are not part of
the reusable module.

Dependencies point one way only: `config_parser` → `mazegen.config` →
`mazegen.errors`, and `config_parser` → `parser_errors`.

- `MazeParsing.parse_config_from_file(path)` reads and parses a configuration
  file and returns a validated `MazeConfig`. This is the entry point used by
  `a_maze_ing.py`. `MazeParsing` holds no state and is never instantiated;
  every method on it is a `staticmethod` or a `classmethod`, so the individual
  steps can be called and tested on their own.
- `MazeConfig(...)` can also be constructed directly from already-typed values,
  in which case only validation runs. Its keyword arguments are `width`,
  `height`, `entry`, `exit`, `perfect`, `braid`, `seed` and `output_file`;
  `seed` and `braid` are the optional ones.

Failures come from three places, which is why the caller catches four things:

- `MazeParserError` subclasses, raised while reading the file: a line without
  an `=`, an empty value, a missing mandatory key, an `ENTRY` or `EXIT` that is
  not a pair, a flag that is not a boolean, or an `OUTPUT_FILE` pointing at the
  configuration file.
- `ValueError`, raised directly by `MazeParsing.parse_dimension` when `WIDTH`,
  `HEIGHT`, `SEED` or a coordinate is not an integer. It belongs to neither
  hierarchy.
- `MazeConfigError` subclasses, raised by `MazeConfig` when the values are
  well-formed but describe an impossible maze.
- `OSError` from opening the file itself: missing file, no read permission,
  a directory given instead of a file.

```python
from config_parser import MazeParsing
from mazegen.errors import MazeConfigError
from parser_errors import MazeParserError

try:
    maze_config = MazeParsing.parse_config_from_file("config.txt")
except (MazeConfigError, MazeParserError, ValueError, OSError) as e:
    print(f"Error: {e}")
```

Values are converted in a fixed order (`OUTPUT_FILE`, `PERFECT`, `BRAIDED`,
`WIDTH`, `HEIGHT`, `SEED`, `ENTRY`, `EXIT`) and the first failure stops the
parsing, so a file with several problems reports only the first one in that
order.

The specific conditions behind each exception are documented in the docstrings
of the exception classes
(`python3 -c "import parser_errors; help(parser_errors)"` and
`python3 -c "import mazegen.errors; help(mazegen.errors)"`).

## Team and project management

### Roles

- **dmgeorgi**: configuration parsing and validation (`config_parser.py`,
  `parser_errors.py`, `mazegen/config.py`, `mazegen/errors.py`).
- **dqureshi**: `<generator / display / packaging>`.

### Planning and how it evolved

Personal note: dmgeorgi is new to python, or at least new to learning about it
in a structured way. So, before tackling A-maze-ing, he completed and submitted py0-py4.
The concepts he learned in those were classes, inheritance, exceptions and error handling and context
managers, which he has used in his work.

However, he did not look into py5-py10 before or during the project.
This was partly due to time constraints, and wanting to get through
A-Maze-ing with his partner before either were black-holed.
However, it was also partly a conscious choice, since dmgeorgi has a tendency
to get stuck in tutorial hell; He wanted to make sure that he tackled real problems
using the concepts he learned before learnng new concepts.

He does not regret this choice but during the project he did a
lot of post-mortems with Claude and found that there were definitely ways he
could've done less work had he known more. One example of this was learning about pydantic
after reviewing dqureshi's work, and finding that it could've saved him a lot of time
when he was writing the validation section. Oh, well.

### What worked and what could be improved

`<...>`

### Tools

`<...>`

## Resources

- PEP 8, PEP 257, PEP 484 (style, docstrings, type hints).
- Python documentation for `random`, `argparse`, and packaging
  (`https://packaging.python.org`).

### How AI was used

`<...>`

So, for the visualiser we need a virtual environment but the setup is simple.
Here's what I did to make it work on my machine (I have included only the most necessary steps).

Run all these commands from root (maze-runners):

1) mkdir vis (create a vis folder - where visualisation lives)
2) download mlx-2.2.tgz off intra project page
3) copy mlx-2.2.tgz from downloads to maze-runners/vis
4) tar -xvf vis/mlx-2.2.tgz (unzip the folder - you will see src and fedora folder, do not touch those)
5) python3 -m venv .venv (create the virtual environment)
6) source .venv/bin/activate (activate the virtual environment)
7) pip install vis/ubuntu/mlx-2.2-py3-none-any.whl
8) Confirm success with python -c "from mlx import Mlx; print(Mlx().mlx_init())"

I need to talk with Dan about what stuff we keep in vis and whether we include the .venv, 
since the mlx stuff doesn't work without the venv