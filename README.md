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
 
Configuration handling is split across three modules so that the validation
logic can be packaged without the file-parsing code:
 
| Module             | Responsibility                                                    |
|--------------------|-------------------------------------------------------------------|
| `config_errors.py` | The `MazeConfigError` exception hierarchy. Imports nothing from the project. |
| `maze_config.py`   | The `MazeConfig` class: takes raw values and validates them.       |
| `config_parser.py` | Reads a configuration file, converts each value to its type, and builds a `MazeConfig`. |
 
Dependencies point one way only: `config_parser` → `maze_config` →
`config_errors`. Only the last two are needed by a project that already has
its parameters and wants them checked.
 
- `config_parser.parse_config_from_file(path)` reads and parses a configuration
  file and returns a validated `MazeConfig`. This is the entry point used by
  `a_maze_ing.py`.
- `MazeConfig(...)` can also be constructed directly from already-typed values,
  in which case only validation runs. The arguments, in order, are
  `output_filename, width, height, entry_coords, exit_coords, perfect_flag,
  braided_flag, seed`; the last two are optional and default to `None`.
```python
from config_errors import MazeConfigError
from config_parser import parse_config_from_file
 
try:
    maze_config = parse_config_from_file("config.txt")
except (MazeConfigError, ValueError, OSError) as e:
    print(f"Error: {e}")
```
 
Every parsing or validation failure is a subclass of `MazeConfigError`, so
callers can catch one base class. The specific conditions are documented in
the docstrings of each exception class
(`python3 -c "import config_errors; help(config_errors)"`).
 
## Team and project management
 
### Roles
 
- **dmgeorgi**: configuration parsing and validation (`maze_config.py`,
  `config_parser.py`, `config_errors.py`).
- **dqureshi**: <generator / display / packaging>.
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
could've done lesss work had he known more. One example of this was learning about pydantic
after reviewing dqureshi's work, and finding that it could've saved him a lot of time 
when he was writing the validation section. Oh, well.

### What worked and what could be improved
 
 
### Tools
 
 
## Resources
 
- PEP 8, PEP 257, PEP 484 (style, docstrings, type hints).
- Python documentation for `random`, `argparse`, and packaging
  (`https://packaging.python.org`).
### How AI was used