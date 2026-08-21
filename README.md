*This project has been created as part of the 42 curriculum by dmgeorgi, dqureshi.*

# A-Maze-ing

## Description



## Instructions

`a_maze_ing.py` takes exactly one argument: the path to a configuration file.
Any configuration error stops the program with a message on `stderr` and a
non-zero exit code.

## Configuration file

A default configuration is provided in `config.txt` at the root of the
repository.

### Format

- One `KEY=VALUE` pair per line, with exactly one `=` per line.
- Lines whose first non-whitespace character is `#` are comments.
- Blank lines are ignored.
- Whitespace around keys and values is ignored, so `WIDTH = 20` is fine.
- Keys are case-insensitive (`width=20` and `WIDTH=20` are equivalent).
- Keys that are not listed below are silently ignored.
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
  itself.
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


### Why this algorithm


## Reusable code



## Parsing and validation (dmgeorgi)

Configuration handling lives in `maze_config.py`, which is independent of the
generator and the display.

- `MazeConfig.get_config_from_file(path)` reads, parses and validates a
  configuration file and returns a `MazeConfig` instance. This is the entry
  point used by `a_maze_ing.py`.
- `MazeConfig(...)` can also be constructed directly with already-parsed values,
  in which case only the validation step runs. All eight arguments are
  positional and required: `output_filename, width, height, entry_coords,
  exit_coords, perfect_flag, braided_flag, seed`. Pass `None` for
  `braided_flag` or `seed` to leave them unset.

```python
from maze_config import MazeConfig, MazeConfigError

try:
    maze_config = MazeConfig.get_config_from_file("config.txt")
except (MazeConfigError, ValueError, OSError) as e:
    print(f"Error: {e}")
```

Every validation failure is a subclass of `MazeConfigError`, so callers can
catch one base class. The specific conditions are documented in the docstrings
of each exception class (`python3 -c "import maze_config; help(maze_config)"`).

## Team and project management

### Roles

- **dmgeorgi**: configuration parsing and validation (`maze_config.py`).
- **<login2>**: <generator / display / packaging>.

### Planning and how it evolved


### What worked and what could be improved


### Tools


## Resources

- PEP 8, PEP 257, PEP 484 (style, docstrings, type hints).
- Python documentation for `random`, `argparse`, and packaging
  (`https://packaging.python.org`).

### How AI was used

