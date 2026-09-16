#!/usr/bin/env python3
"""Provide a graphical visualizer for generated mazes using MiniLibX.

The module provides low-level image drawing through ``Canvas``, maze-specific
drawing through ``MazePainter``, and window and event management through
``MazeRender``.

The visualizer can be closed by pressing 4 or using the window's close button.
Pressing Ctrl-Z suspends the process instead of closing it. A suspended process
can be resumed from the terminal using the ``fg`` command.
"""
import random
from mlx import Mlx  # type: ignore[import-untyped]
from mazegen.colours import ColourPair, COLOUR_PAIRS
from mazegen.maze import Maze
from mazegen.config import MazeConfig


class Canvas:
    """Provide basic drawing operations for an MLX image buffer."""

    def __init__(self, image: memoryview, line_len_in_pix: int, bytes_per_pixel: int) -> None:
        """Initialize the canvas.

        Args:
            image: Writable buffer containing the image data.
            line_len_in_pix: Number of pixels in each image row.
            bytes_per_pixel: Number of bytes used by each pixel.
        """
        self.image = image
        self.line_len_in_pix = line_len_in_pix
        self.bytes_per_pixel = bytes_per_pixel

    def colour_pixel(self, coordinates: tuple[int, int], colour: tuple[int, int, int, int]) -> None:
        """Colour one pixel in the image.

        Args:
            coordinates: Pixel position as an ``(x, y)`` tuple.
            colour: Four colour-channel values in MLX byte order.
        """
        x_coord, y_coord = coordinates[0], coordinates[1]
        self.image[self.bytes_per_pixel * (self.line_len_in_pix * y_coord + x_coord)] = colour[0]
        self.image[self.bytes_per_pixel * (self.line_len_in_pix * y_coord + x_coord) + 1] = colour[1]
        self.image[self.bytes_per_pixel * (self.line_len_in_pix * y_coord + x_coord) + 2] = colour[2]
        self.image[self.bytes_per_pixel * (self.line_len_in_pix * y_coord + x_coord) + 3] = colour[3]

    def fill_rect(self, x: int, y: int, width: int, height: int, colour: tuple[int, int, int, int]) -> None:
        """Fill a rectangular area with one colour.

        Args:
            x: Horizontal coordinate of the rectangle's top-left corner.
            y: Vertical coordinate of the rectangle's top-left corner.
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.
            colour: Four colour-channel values in MLX byte order.
        """
        for row in range(y, y + height):
            for col in range(x, x + width):
                self.colour_pixel((col, row), colour)


class MazePainter:
    ENTRY_COLOUR = (60, 170, 20, 255)
    EXIT_COLOUR = (40, 40, 230, 255)
    SOLUTION_COLOUR = (230, 70, 20, 255)
    """Draw a maze and manage its visual properties."""

    def __init__(self, config: MazeConfig) -> None:
        """Initialize the maze painter.

        Args:
            config: Maze configuration containing its dimensions and seed.
        """
        self.width_in_cells = config.width
        self.height_in_cells = config.height
        self.cell_thick = 15
        self.wall_thick = 3
        cell_size = self.cell_thick + 2 * self.wall_thick
        self.maze_width_in_pixels = self.width_in_cells * cell_size + 2 * self.wall_thick
        self.maze_height_in_pixels = self.height_in_cells * cell_size + 2 * self.wall_thick
        self.rng = random.Random(config.seed)
        self.colour_pair = self.rng.choice(COLOUR_PAIRS)

    def choose_another_colour_pair(self) -> ColourPair:
        """Choose a colour pair different from the current pair.

        Returns:
            A randomly selected colour pair. If multiple pairs are available,
            the returned pair differs from the current pair.
        """
        new_colour_pair = self.rng.choice(COLOUR_PAIRS)

        if len(COLOUR_PAIRS) > 1:
            while new_colour_pair == self.colour_pair:
                new_colour_pair = self.rng.choice(COLOUR_PAIRS)

        return new_colour_pair

    def change_colour_pair(self) -> None:
        """Replace the current colour pair with another pair."""
        self.colour_pair = self.choose_another_colour_pair()

    def draw_cell(self, top_left: tuple[int, int], bottom_right: tuple[int, int], walls: int, canvas: Canvas) -> None:
        """Draw one maze cell and its walls.

        Args:
            top_left: Pixel coordinates of the cell's top-left corner.
            bottom_right: Pixel coordinates of the cell's bottom-right corner.
            walls: Bit mask representing the cell's closed walls.
            canvas: Canvas on which to draw the cell.
        """
        tlx, tly = top_left
        brx, bry = bottom_right
        cell_w, cell_h = brx - tlx, bry - tly
        w = self.wall_thick
        wall_colour = self.colour_pair.walls

        if walls == 15:
            blocked_cells_constant = 2 / 3
            r, g, b, a = self.colour_pair.path
            scaled_r = int(r * blocked_cells_constant)
            scaled_g = int(g * blocked_cells_constant)
            scaled_b = int(b * blocked_cells_constant)
            path_colour = (scaled_r, scaled_g, scaled_b, a)
        else:
            path_colour = self.colour_pair.path

        canvas.fill_rect(tlx, tly, cell_w, cell_h, path_colour)

        if walls & 1:
            canvas.fill_rect(tlx, tly, cell_w, w, wall_colour)
        if walls & 2:
            canvas.fill_rect(brx - w, tly, w, cell_h, wall_colour)
        if walls & 4:
            canvas.fill_rect(tlx, bry - w, cell_w, w, wall_colour)
        if walls & 8:
            canvas.fill_rect(tlx, tly, w, cell_h, wall_colour)

    def draw_endpoints(self, maze: Maze, canvas: Canvas) -> None:
        """Colour the entry and exit cell interiors."""
        cell_size = self.cell_thick + 2 * self.wall_thick

        endpoints = (
            (maze.config.entry, self.ENTRY_COLOUR),
            (maze.config.exit, self.EXIT_COLOUR),
        )

        for (row, col), colour in endpoints:
            x = 2 * self.wall_thick + col * cell_size
            y = 2 * self.wall_thick + row * cell_size

            canvas.fill_rect(x, y, self.cell_thick, self.cell_thick, colour)

    def draw_path(self, path: list[tuple[int, int]], canvas: Canvas) -> None:
        """Connect the centres of adjacent path cells, supplied as (x, y)."""
        if not path:
            return

        cell_size = self.cell_thick + 2 * self.wall_thick
        thickness = max(1, self.cell_thick // 3)
        half = thickness // 2
        colour = self.SOLUTION_COLOUR

        previous: tuple[int, int] | None = None
        for row, col in path:
            cx = self.wall_thick + col * cell_size + cell_size // 2
            cy = self.wall_thick + row * cell_size + cell_size // 2
            if previous is None:
                canvas.fill_rect(cx - half, cy - half,
                                 thickness, thickness, colour)
            else:
                px, py = previous
                canvas.fill_rect(min(px, cx) - half, min(py, cy) - half, abs(cx - px) + thickness,
                                 abs(cy - py) + thickness, colour)
            previous = (cx, cy)

    def draw_maze(self, maze: Maze, canvas: Canvas) -> None:
        """Draw every cell in a maze.

        Args:
            maze: Maze containing the grid to draw.
            canvas: Canvas on which to draw the maze.
        """
        canvas.fill_rect(0, 0, self.maze_width_in_pixels, self.maze_height_in_pixels, self.colour_pair.walls)

        cell_size = self.cell_thick + 2 * self.wall_thick

        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                top_left = (self.wall_thick + x * cell_size, self.wall_thick + y * cell_size)
                bottom_right = (self.wall_thick + (x + 1) * cell_size, self.wall_thick + (y + 1) * cell_size)
                self.draw_cell(top_left, bottom_right, maze.grid[y][x].walls, canvas)


class MazeRender:
    """Manage the MiniLibX window and visualizer interactions."""

    REGEN_KEY, PATH_KEY, COLOUR_KEY, EXIT_KEY = 49, 50, 51, 52
    CLOSE_BUTTON = 33

    def __init__(self, config: MazeConfig, maze: Maze) -> None:
        """Initialize the maze renderer.

        Args:
            config: Configuration used to prepare the maze painter.
            maze: Maze to display and regenerate.
        """
        self.m = Mlx()
        self.mlx_ptr = None
        self.win_ptr = None
        self.img_ptr = None
        self.canvas: Canvas | None = None
        self.generator = maze
        self.painter = MazePainter(config)

    def free_and_quit(self) -> None:
        """Destroy the allocated MLX resources."""
        if self.img_ptr:
            self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        if self.win_ptr:
            self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        if self.mlx_ptr:
            self.m.mlx_release(self.mlx_ptr)

    def myclose(self, _param: object) -> None:
        """Handle a request to close the window.

        Args:
            _param: Unused callback parameter supplied by MiniLibX.
        """
        self.m.mlx_loop_exit(self.mlx_ptr)

    def mykey(self, keynum: int, _param: object) -> None:
        """Handle a keyboard event.

        Args:
            keynum: Numeric code of the pressed key.
            _param: Unused callback parameter supplied by MiniLibX.
        """
        if keynum == self.EXIT_KEY:
            self.m.mlx_loop_exit(self.mlx_ptr)
        elif keynum == self.REGEN_KEY:
            self.generator.path.clear()
            self.generator.generate()
            self.generator.solve()
            self.refresh()
        elif keynum == self.PATH_KEY:
            self.toggle_path()
        elif keynum == self.COLOUR_KEY:
            self.painter.change_colour_pair()
            self.refresh()

    def toggle_path(self) -> None:
        """Show or hide the stored solution and redraw the window."""
        self.generator.show_path = not self.generator.show_path
        self.refresh()

    def draw_menu(self) -> None:
        """Draw the visualizer controls below the maze."""
        text_string = "1: regen  2: path  3: colour  4: quit"
        self.m.mlx_string_put(self.mlx_ptr, self.win_ptr, 0, self.painter.maze_height_in_pixels, 0xFFFFFF, text_string)

    def refresh(self) -> None:
        """Redraw the maze, optional solution, endpoints, and menu."""
        if self.canvas is None:
            raise RuntimeError("Cannot refresh before the canvas is initialized.")

        self.painter.draw_maze(self.generator, self.canvas)

        if self.generator.show_path:
            self.painter.draw_path(self.generator.path, self.canvas)

        self.painter.draw_endpoints(self.generator, self.canvas)

        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )
        self.draw_menu()

    def run_window(self) -> None:
        """Create the MLX window and run its event loop."""
        text_height = 25
        win_width = self.painter.maze_width_in_pixels
        win_height = self.painter.maze_height_in_pixels + text_height

        self.mlx_ptr = self.m.mlx_init()
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, win_width, win_height, "A-Maze-ing")
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        self.img_ptr = self.m.mlx_new_image(self.mlx_ptr, win_width, win_height)
        mem = self.m.mlx_get_data_addr(self.img_ptr)

        image_in_bytes = mem[0]
        bits_per_pixel = mem[1]
        bytes_per_pixel = bits_per_pixel // 8
        line_len_in_pix = mem[2] // bytes_per_pixel

        self.canvas = Canvas(image_in_bytes, line_len_in_pix, bytes_per_pixel)
        self.refresh()
        self.m.mlx_hook(self.win_ptr, self.CLOSE_BUTTON, 0, self.myclose, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_loop(self.mlx_ptr)
        self.free_and_quit()
