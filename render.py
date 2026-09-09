#!/usr/bin/env python3
"""
so, to quit the programme a user can press '4' or click the x on the window.
Pressing ctrl-Z suspends the process, putting it in the background (the same as sending the SIGTSTP signal).
The window becomes unresponsive, type 'fg' (foreground) in the terminal to resolve.

"""
import random
from mlx import Mlx
from mazegen.config import MazeConfig
from mazegen.cell import Cell
from mazegen.colours import ColourPair, COLOUR_PAIRS


class MazeRender:

    REGEN_KEY, PATH_KEY, COLOUR_KEY, EXIT_KEY = 49, 50, 51, 52
    EXIT_BUTTON = 33

    def __init__(self, config: MazeConfig, grid: list[list['Cell']], c_thick: int = 10, w_thick: int = 1) -> None:
        self.m = Mlx()
        self.mlx_ptr = None
        self.win_width = None
        self.win_height = None
        self.win_ptr = None
        self.img_ptr = None
        self.height_in_cells = config.height
        self.width_in_cells = config.width
        self.cell_thick = c_thick
        self.wall_thick = w_thick
        self.maze_in_image_height = None
        self.maze_in_image_width = None
        self.colour = random.Random().choice(COLOUR_PAIRS)
        self.grid = grid

    def calculate_maze_in_image_size(self) -> None:
        self.maze_in_image_height = self.height_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2
        self.maze_in_image_width = self.width_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2

    def free_and_quit(self) -> None:
        self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)

    # def switch_colours(self) -> None:
    #     """
    #     Switches the colour for rendering the maze.
    #     """
    #     new_colour_pair = self.colours
    #     while new_colour_pair == self.colours:
    #         new_colour_pair = random.Random().choice(COLOUR_PAIRS)
    #     self.colours = new_colour_pair
    
    def myclose(self, param) -> None:
        self.m.mlx_loop_exit(self.mlx_ptr)

    def mykey(self, keynum, mystuff) -> None:
        if keynum == self.EXIT_KEY:
            self.m.mlx_loop_exit(self.mlx_ptr)
        elif keynum == self.REGEN_KEY:
            ...
        elif keynum == self.PATH_KEY:
            ...
        elif keynum == self.COLOUR_KEY:
            ...

    def draw_maze(self, tup: tuple[memoryview, int, int, int], grid: list[list['Cell']], colour: ColourPair) -> None:
        screen = tup[0] # in bytes
        pixel_size = tup[1] / 8 # also in bytes
        line_len = tup[2] # in bytes
        #self.draw_border()

    def run_window(self) -> None:
        self.mlx_ptr = self.m.mlx_init()        
        self.calculate_maze_in_image_size()
        self.win_width, self.win_height = self.maze_in_image_width, self.maze_in_image_height #+ text_height
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.img_ptr = self.m.mlx_new_image(self.mlx_ptr, self.win_width, self.win_height)
        tup = self.m.mlx_get_data_addr(self.img_ptr)
        self.draw_maze(tup, self.grid, self.colour)
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        self.m.mlx_hook(self.win_ptr, self.EXIT_BUTTON, 0, self.myclose, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_loop(self.mlx_ptr)
        self.free_and_quit()
