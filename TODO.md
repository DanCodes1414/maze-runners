# TODO List

## General (dqureshi)
- [ ] Flake8 passing?
- [ ] `mypy --strict .` passing?
- [ ] Runtime errors handled?
- [ ] Docstrings included?
- [ ] .gitignore included?
- [ ] Use venv for dependency isolation 
- [ ] `a_maze_ing.py` as main project file
- [ ] Both evaluatees fully understand the project and our code??


## Config txt validation and parsing (dmgeorgi)
- [ ] Handle invalid/missing file
- [ ] Handle maze too small for 42 logo
- [ ] Handle missing parameters
- [ ] Handle entry/exit out of range or the same
- [ ] Ignore lines starting with # (comments)
- [ ] output-file is a txt file (must end with .txt extension, otherwise rejected)
- [ ] `a_maze_ing.py` as main project file
- [ ] BONUS: Seed/Algorithm/Display parameters included?
- [ ] Default config file included in Git repo?


## Maze Generation (dqureshi)
- [ ] External walls are fully covered (no escaping via the edge of the maze!)
- [ ] No blocked off or isolated cells (except for the 42 logo)
- [ ] Neighbouring cells must have walls touching each other (i.e, if there is a wall on the east for Cell 1, there must be a wall on the west for Cell 2)
- [ ] There cannot be a 3x3 open area
- [ ] 42 logo displayed with fully closed cells
- [ ] If the PERFECT flag is activated, the maze contains exactly 1 path between the entry and exit?
- [ ] Reproducibility via a seed
- [ ] BONUS: Is the second algorithm implemented?


## Output file (dqureshi)
- [ ] 1 hexa number for each cell (when viewed in binary, 1 means wall (closed) and 0 is no-wall (open))
- [ ] The hexa number viewed in binary represent the directions
    * **North**: 2^0 place
    * **East**: 2^1 place
    * **South**: 2^2 place
    * **West**: 2^3 place
- [ ] Cells are stored row by row, one row per line.
- [ ] Empty line bewteen maze cells and entry/exit coords
- [ ] the entry coordinates and the exit coordinates on seperate lines
- [ ] the shortest valid path from entry to exit, using the four letters N, E, S, W 
- [ ] File ends with `\n`
- [ ] File is created in root and saved properly


## Terminal ASCII rendering (dmgeorgi)
- [ ] Generated maze appears when running code.
- [ ] Option to: Generate a new maze
- [ ] Option to: Show/Hide a valid shortest path from the entrance to the exit.
- [ ] Option to: Change maze wall colours
- [ ] Entry/Exit cells should be clearly shown (with different colours)
- [ ] The program will be constantly waiting for user input, so there should be an option to Quit
- [ ] Indication of which cell is the Entry cell and which cell is the Exit cell.


## Standalone module (dqureshi)
- [ ] Documentation on how to use and import the module
    * Instantiate and use the generator, with some basic example.
    * Pass custom parameters (e.g., size, seed).
    * Access the generated structure, and access at least a solution.
- [ ] mazegen-* package exists in root and can be used with pip/uv? (Example of filename: `mazegen-1.0.0-py3.whl`)


## Makefile (dmgeorgi)
- [ ] **install**: Install dependencies with pip/uv (dqureshi)
- [ ] **run**: Execute the main script
- [ ] **debug**: Run while debugging
- [ ] **clean**: Remove temporary files (__pycache__, .mypy_cache)
- [ ] **lint**: `flake8 .` and `mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs`
- [ ] **lint-strict**: `flake8 .` and `mypy --strict .


## Testing (dqureshi)
- [ ] Write basic unittests for the maze algorithm
- [ ] Write basic unittests for the output file
- [ ] Write unittests for edge-cases (e.g. maze too small, invalid config file).
- [ ] Test stand-alone module in a virtual-env.


## README
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
