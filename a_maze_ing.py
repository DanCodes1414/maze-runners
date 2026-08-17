#!/usr/bin/env python3

from maze_config import MazeConfig
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Error: wrong number of args.\n"
              "Usage: python3 a_maze_ing.py <config_file/config.txt>",
              file=sys.stderr)
        return 1
    try:
        maze_config = MazeConfig.get_config_from_file(sys.argv[1])
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    else:
        print(maze_config.width)
        print(maze_config.height)
        print(maze_config.entry_point)
        print(maze_config.exit_point)
        print(maze_config.output_filename)
        print(maze_config.perfect_flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
