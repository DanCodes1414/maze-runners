#!/usr/bin/env python3

from config_parser import MazeParsing
from mazegen.errors import MazeConfigError
from mazegen.maze import Maze
from render import MazeRender
from parser_errors import MazeParserError
import sys



def main() -> int:
    if len(sys.argv) != 2:
        print("Error: wrong number of args.\n"
              "Usage: python3 a_maze_ing.py <config_file/config.txt>",
              file=sys.stderr)
        return 1
    try:
        maze_config = MazeParsing.parse_config_from_file(sys.argv[1])
    except (MazeConfigError, MazeParserError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected Error in Parsing and Validation: {e}", file=sys.stderr)
        return 1
    maze = Maze(config=maze_config)
    maze.generate()
    renderer = MazeRender(maze_config, maze.grid, w_thick=5)
    renderer.run_window()
    return 0


if __name__ == "__main__":
    sys.exit(main())
