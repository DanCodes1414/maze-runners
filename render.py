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
from mazegen.maze import Maze


class MazeRender:

    REGEN_KEY, PATH_KEY, COLOUR_KEY, EXIT_KEY = 49, 50, 51, 52
    EXIT_BUTTON = 33

    def __init__(self, maze_dimensions: tuple[int, int], maze: Maze, c_thick: int = 10, w_thick: int = 1) -> None:
        self.m = Mlx()
        self.mlx_ptr = None
        self.win_width = None
        self.win_height = None
        self.win_ptr = None
        self.img_ptr = None
        self.generator = maze
        self.width_in_cells = maze_dimensions[0]
        self.height_in_cells = maze_dimensions[1]
        self.cell_thick = c_thick
        self.wall_thick = w_thick
        self.maze_in_image_height = None
        self.maze_in_image_width = None
        self.colour_pair = random.Random().choice(COLOUR_PAIRS)
        self.screen = None
        self.grid = maze.grid
        self.mem = None

    def calculate_maze_in_image_size(self) -> None:
        self.maze_in_image_height = self.height_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2 * self.wall_thick # in pixels
        self.maze_in_image_width = self.width_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2 * self.wall_thick # in pixels

    def free_and_quit(self) -> None:
        self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)
    
    def myclose(self, param) -> None:
        self.m.mlx_loop_exit(self.mlx_ptr)

    def choose_another_colour_pair(self) -> ColourPair:
        new_colour_pair = random.Random().choice(COLOUR_PAIRS)
        while (new_colour_pair == self.colour_pair):
            new_colour_pair = random.Random().choice(COLOUR_PAIRS)
        return new_colour_pair           

    def mykey(self, keynum, mystuff) -> None:
        if keynum == self.EXIT_KEY:
            self.m.mlx_loop_exit(self.mlx_ptr)
        elif keynum == self.REGEN_KEY:
            self.generator.generate()
            self.grid = self.generator.grid
            self.draw_maze(self.mem)
            self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        elif keynum == self.PATH_KEY:
            ...
        elif keynum == self.COLOUR_KEY:
            self.colour_pair = self.choose_another_colour_pair() 
            self.draw_maze(self.mem)
            self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def colour_pixel(self, coordinates: tuple[int, int], colour: tuple[int, int, int, int], line_len_in_pix: int) -> None:
        x_coord, y_coord =  coordinates[0], coordinates[1]
        self.screen[4 * (line_len_in_pix * y_coord + x_coord)] = colour[0]
        self.screen[4 * (line_len_in_pix * y_coord + x_coord) + 1] = colour[1]
        self.screen[4 * (line_len_in_pix * y_coord + x_coord) + 2] = colour[2]
        self.screen[4 * (line_len_in_pix * y_coord + x_coord) + 3] = colour[3]

    def colour_top_edge(self, top_left: tuple[int, int], bottom_right: tuple[int, int], line_len_in_pix: int) -> None:
        top_left_x, top_left_y = top_left[0], top_left[1]
        bottom_right_x = bottom_right[0]
        for i in range(self.wall_thick):
            for x in range(top_left_x, bottom_right_x):
                self.colour_pixel((x, top_left_y + i), self.colour_pair.walls, line_len_in_pix)

    def colour_bottom_edge(self, top_left: tuple[int, int], bottom_right: tuple[int, int], line_len_in_pix: int) -> None:
        top_left_x = top_left[0]
        bottom_right_x, bottom_right_y = bottom_right[0], bottom_right[1]
        for i in range(self.wall_thick):
            for x in range(top_left_x, bottom_right_x):
                self.colour_pixel((x, bottom_right_y - i - 1), self.colour_pair.walls, line_len_in_pix)

    def colour_right_edge(self, top_left: tuple[int, int], bottom_right: tuple[int, int], line_len_in_pix: int) -> None:
        top_left_y = top_left[1]
        bottom_right_x, bottom_right_y = bottom_right[0], bottom_right[1]
        for i in range(self.wall_thick):
            for y in range(top_left_y, bottom_right_y):
                self.colour_pixel((bottom_right_x - i - 1, y), self.colour_pair.walls, line_len_in_pix)

    def colour_left_edge(self, top_left: tuple[int, int], bottom_right: tuple[int, int], line_len_in_pix: int) -> None:
        top_left_x, top_left_y = top_left[0], top_left[1]
        bottom_right_y = bottom_right[1]
        for i in range(self.wall_thick):
            for y in range(top_left_y, bottom_right_y):
                self.colour_pixel((top_left_x + i, y), self.colour_pair.walls, line_len_in_pix)       

    def draw_cell(self, top_left: tuple[int, int], bottom_right: tuple[int, int], line_len_in_pix: int, walls: int) -> None:
        top_left_x, top_left_y = top_left[0], top_left[1]
        bottom_right_x, bottom_right_y = bottom_right[0], bottom_right[1]
        for y in range(top_left_y, bottom_right_y):
            for x in range(top_left_x, bottom_right_x):
                self.colour_pixel((x, y), self.colour_pair.path, line_len_in_pix)
        if walls % 2 == 1:
            self.colour_top_edge(top_left, bottom_right, line_len_in_pix)
        if int(walls / 2) % 2 == 1:
            self.colour_right_edge(top_left, bottom_right, line_len_in_pix)
        if int(walls / 4) % 2 == 1:
            self.colour_bottom_edge(top_left, bottom_right, line_len_in_pix)
        if int(walls / 8) % 2 == 1:
            self.colour_left_edge(top_left, bottom_right, line_len_in_pix)
        
    def draw_maze(self, mem: tuple[memoryview, int, int, int]) -> None:
        self.screen = mem[0] # in bytes
        self.draw_cell((0,0), (self.maze_in_image_width, self.maze_in_image_height), self.maze_in_image_width, 15)
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                top_left = (self.wall_thick + x * (self.cell_thick + 2 * self.wall_thick),
                            self.wall_thick + y * (self.cell_thick + 2 * self.wall_thick))
                bottom_right = (self.wall_thick + (x + 1) * (self.cell_thick + 2 * self.wall_thick),
                            self.wall_thick + (y + 1) * (self.cell_thick + 2 * self.wall_thick))
                self.draw_cell(top_left, bottom_right, self.maze_in_image_width, ((self.grid)[y][x]).walls)
        self.m.mlx_string_put(self.mlx_ptr, self.win_ptr, 2, self.maze_in_image_height + 2, 400, "1: regen  2: path  3: colour  4: walls")

    def run_window(self) -> None:
        self.mlx_ptr = self.m.mlx_init()        
        self.calculate_maze_in_image_size()
        self.win_width, self.win_height = self.maze_in_image_width, self.maze_in_image_height + 25 # for text at the bottom
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.img_ptr = self.m.mlx_new_image(self.mlx_ptr, self.win_width, self.win_height)
        self.mem = self.m.mlx_get_data_addr(self.img_ptr)
        self.draw_maze(self.mem)
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        self.m.mlx_hook(self.win_ptr, self.EXIT_BUTTON, 0, self.myclose, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_loop(self.mlx_ptr)
        self.free_and_quit()
