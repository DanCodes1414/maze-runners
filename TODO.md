# TODO List

## General (dqureshi)
- [ ] Flake8 passing?
- [ ] `mypy --strict .` passing?
- [ ] Runtime errors handled?
- [ ] Docstrings included?
- [x] .gitignore included?
- [x] LICENSE.md included?
- [ ] Use venv/pyenv for dependency isolation 
- [ ] `a_maze_ing.py` as main project file
- [ ] Both evaluatees fully understand the project and our code?


## Config txt validation and parsing (dmgeorgi)
- [x] Handle invalid/missing file
- [x] `a_maze_ing.py` as main project file
- [x] Default config file included in Git repo?
- [x] Handle missing parameters
- [x] Handle entry/exit out of range or the same
- [x] Ignore lines starting with # (comments)
- [x] Define minimum maze size (depending on Perfect flag)
- [x] Check that config.txt is a plain text file
- [x] BONUS: parsing for the SEED flag
- [x] Check that the output_filename is valid (write parsing in MazeConfig.get_file)
- [x] Write doctrings
- [ ] Write check for valid starting and exit points if 42 logo is present

## Maze Generation (dqureshi)
- [x] External walls are fully covered (no escaping via the edge of the maze!)
- [x] No blocked off or isolated cells (except for the 42 logo)
- [x] Neighbouring cells must have walls touching each other (i.e, if there is a wall on the east for Cell 1, there must be a wall on the west for Cell 2)
- [ ] There cannot be a 3x3 open area
- [x] 42 logo displayed with fully closed cells
- [x] If the PERFECT flag is activated, the maze contains exactly 1 path between the entry and exit?
- [x] Reproducibility via a seed


## Maze Solver (dmgeorgi)
- [ ] Use an algorithm to find the shortest path between entry and exit cells


## Output file (dqureshi)
- [x] 1 hexa number for each cell (when viewed in binary, 1 means wall (closed) and 0 is no-wall (open))
- [x] The hexa number viewed in binary represent the directions
    * **North**: 2^0 place
    * **East**: 2^1 place
    * **South**: 2^2 place
    * **West**: 2^3 place
- [x] Cells are stored row by row, one row per line.
- [x] Empty line bewteen maze cells and entry/exit coords
- [x] the entry coordinates and the exit coordinates on seperate lines
- [x] the shortest valid path from entry to exit, using the four letters N, E, S, W 
- [x] File ends with `\n`
- [x] File is created in root and saved properly


## Terminal ASCII rendering (dmgeorgi)
- [ ] Generated maze appears when running code.
- [ ] Option to: Generate a new maze
- [ ] Option to: Show/Hide a valid shortest path from the entrance to the exit.
- [ ] Option to: Change maze wall colours
- [ ] Entry/Exit cells should be clearly shown (with different colours)
- [ ] The program will be constantly waiting for user input, so there should be an option to Quit
- [ ] Indication of which cell is the Entry cell and which cell is the Exit cell.


## Standalone module (dqureshi)
- [x] Documentation on how to use and import the module
    * Instantiate and use the generator, with some basic example.
    * Pass custom parameters (e.g., size, seed).
    * Access the generated structure, and access at least a solution.
- [ ] mazegen-* package exists in root and can be used with pip/uv? (Example of filename: `mazegen-1.0.0-py3.whl`)


## Makefile (dqureshi)
- [x] **install**: Install dependencies with pip
- [x] **run**: Execute the main script
- [x] **debug**: Run while debugging
- [x] **clean**: Remove temporary files (__pycache__, .mypy_cache)
- [x] **lint**: `flake8 .` and `mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs`
- [x] **lint-strict**: `flake8 .` and `mypy --strict .


## Testing (dqureshi)
- [x] Test stand-alone module in a virtual-env.


## README (dmgeorgi)
- [ ] Include intra names at the top
- [ ] Add Description, Instructions, and Resources
- [ ] Structure of config file
- [ ] Maze algorithm/s chosen and why?
- [ ] What part of code is reusable
- [ ] The roles of each team member
- [ ] Anticipated planning and how it evolved until the end
- [ ] What worked well and what could be improved?
- [ ] Any specific tools used?
- [ ] Bonus features


## Bonuses?
- [ ] Animations
- [ ] Another maze algorithm
- [x] Maze with 0 dead-ends
