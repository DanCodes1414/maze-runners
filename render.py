#!/usr/bin/env python3
"""
so, to quit the programme a user can press '4' or click the x on the window.
Pressing ctrl-Z suspends the process, putting it in the background (the same as sending the SIGTSTP signal).
The window becomes unresponsive, type 'fg' (foreground) in the terminal to resolve.

"""
import random
from mlx import Mlx
from mazegen.colours import ColourPair, COLOUR_PAIRS
from mazegen.maze import Maze


class Cell:
    def __init__(self, screen: memoryview, line_len_in_pix: int) -> None:
        self.screen = screen
        self.line_len_in_pix = line_len_in_pix

    def colour_pixel(self, coordinates: tuple[int, int], colour: tuple[int, int, int, int]) -> None:
        x_coord, y_coord =  coordinates[0], coordinates[1]
        self.screen[4 * (self.line_len_in_pix * y_coord + x_coord)] = colour[0]
        self.screen[4 * (self.line_len_in_pix * y_coord + x_coord) + 1] = colour[1]
        self.screen[4 * (self.line_len_in_pix * y_coord + x_coord) + 2] = colour[2]
        self.screen[4 * (self.line_len_in_pix * y_coord + x_coord) + 3] = colour[3]

    def fill_rect(self, x: int, y: int, width: int, height: int,
                        colour: tuple[int, int, int, int]) -> None:
        for row in range(y, y + height):
            for col in range(x, x + width):
                self.colour_pixel((col, row), colour)

class MazeRender:

    REGEN_KEY, PATH_KEY, COLOUR_KEY, EXIT_KEY = 49, 50, 51, 52
    EXIT_BUTTON = 33

    def __init__(self, maze_dimensions: tuple[int, int], maze: Maze) -> None:
        self.m = Mlx()
        self.mlx_ptr = None
        self.win_width = None
        self.win_height = None
        self.win_ptr = None
        self.img_ptr = None
        self.generator = maze
        self.width_in_cells = maze_dimensions[0]
        self.height_in_cells = maze_dimensions[1]
        self.cell_thick, self.wall_thick = self.calculate_thickness()
        self.maze_height_in_pixels = None
        self.maze_width_in_pixels = None
        self.colour_pair = random.Random().choice(COLOUR_PAIRS)
        self.screen = None
        self.grid = maze.grid
        self.mem = None
        self.line_len_in_pix = None

    def calculate_thickness(self) -> tuple[int, int]:
        if self.width_in_cells < 6 or self.height_in_cells < 6:
            cell_thick = 50
            wall_thick = 10
        else:
            cell_thick = 10
            wall_thick = 2
        return(cell_thick, wall_thick)

    def calculate_maze_in_image_size(self) -> None:
        self.maze_height_in_pixels = self.height_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2 * self.wall_thick
        self.maze_width_in_pixels = self.width_in_cells * (self.cell_thick + 2 * self.wall_thick) + 2 * self.wall_thick

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

    def draw_cell(self, top_left, bottom_right, walls) -> None:
        tlx, tly = top_left
        brx, bry = bottom_right
        cell_w, cell_h = brx - tlx, bry - tly
        w = self.wall_thick
        wall_colour = self.colour_pair.walls

        if top_left != (0, 0) and walls == 15:
            path_colour = tuple(int((c * 2) / 3) for c in self.colour_pair.path)
        else:
            path_colour = self.colour_pair.path

        cell = Cell(self.screen, self.line_len_in_pix)
        cell.fill_rect(tlx, tly, cell_w, cell_h, path_colour)
        if walls & 1:
            cell.fill_rect(tlx, tly, cell_w, w, wall_colour)
        if walls & 2:
            cell.fill_rect(brx - w, tly, w, cell_h, wall_colour)
        if walls & 4:
            cell.fill_rect(tlx, bry - w, cell_w, w, wall_colour)
        if walls & 8:
            cell.fill_rect(tlx, tly, w, cell_h, wall_colour)
        
    def draw_maze(self, mem: tuple[memoryview, int, int, int]) -> None:
        self.screen = mem[0] # in bytes
        self.line_len_in_pix = int(mem[2] / 4)
        self.draw_cell((0,0), (self.maze_width_in_pixels, self.maze_height_in_pixels), 15)
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                top_left = (self.wall_thick + x * (self.cell_thick + 2 * self.wall_thick),
                            self.wall_thick + y * (self.cell_thick + 2 * self.wall_thick))
                bottom_right = (self.wall_thick + (x + 1) * (self.cell_thick + 2 * self.wall_thick),
                            self.wall_thick + (y + 1) * (self.cell_thick + 2 * self.wall_thick))
                self.draw_cell(top_left, bottom_right, ((self.grid)[y][x]).walls)
        text_string = "1: regen  2: path  3: colour  4: quit"
        self.m.mlx_string_put(self.mlx_ptr, self.win_ptr, 0, self.maze_height_in_pixels, 0xFFFFFF, text_string)

    def run_window(self) -> None:
        self.mlx_ptr = self.m.mlx_init()        
        self.calculate_maze_in_image_size()
        text_height = 25
        self.win_width = self.maze_width_in_pixels
        self.win_height = self.maze_height_in_pixels + text_height
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
