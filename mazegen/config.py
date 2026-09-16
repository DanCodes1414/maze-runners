from pydantic import BaseModel, Field, model_validator
from typing import Self
from .errors import (
    OutputFilenameError, PointError, ContradictionError, InvalidDimensionError,
    MazeTooSmallError, MazeTooBigError, BlockedCellsError, PointOutOfBoundsError)
from .cell import get_blocked_cells


class MazeConfig(BaseModel):
    """
    Represents the configuration for generating a maze.

    Attributes:
        width (int): The width of the maze. Must be between 1 and 50.
        height (int): The height of the maze. Must be between 1 and 50.
        entry (tuple[int, int]): The coordinates of the maze entry point (row, col).
        exit (tuple[int, int]): The coordinates of the maze exit point (row, col).
        seed (int): An optional seed for random number generation. If not provided, a random seed will be used.
        perfect (bool): If True, generates a perfect maze (no loops).
        braid (bool): If True, generates a braided maze (a maze with loops and no dead ends).
        output_file (str): The name of the output file where the maze will be exported.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    seed: int | None = Field(default=None)
    perfect: bool = Field(default=False)
    braid: bool = Field(default=False)
    output_file: str

    @model_validator(mode="after")
    def validation_rules(self) -> Self:
        """Validate the given parameters.

        output_filename is stored as given. width and height are checked
        with validate_maze, entry and exit coords with
        validate_point, and seed (when not None) with validate_dimension;
        any error those raise is propagated.

        Raise OutputFilenameError if output filename contains paths.
        Raise PointError if entry and exit coords are equal.
        Raise ContradictionError if perfect and braid flags are both True.
        """
        if '/' in self.output_file:
            raise OutputFilenameError("OUTPUT_FILE does not accept paths.")
        self.width, self.height = MazeConfig.validate_maze(self.width, self.height)
        maze_dimensions = (self.width, self.height)
        self.entry = MazeConfig.validate_point("ENTRY", self.entry, maze_dimensions)
        self.exit = MazeConfig.validate_point("EXIT", self.exit, maze_dimensions)
        if (self.entry == self.exit):
            raise PointError()
        if self.braid and self.perfect:
            raise ContradictionError()
        if self.seed is not None:
            MazeConfig.validate_dimension(self.seed, "SEED")
        return self

    @staticmethod
    def validate_dimension(dimension_value: int, dimension_name: str) -> int:
        """Return dimension_value unchanged if it is non-negative.

        Raise InvalidDimensionError otherwise, using dimension_name in
        the error message.
        """
        if dimension_value < 0:
            raise InvalidDimensionError(dimension_value, dimension_name)
        return dimension_value

    @staticmethod
    def validate_maze(width: int, height: int) -> tuple[int, int]:
        """Return (width, height) if the maze is large enough.

        The minimum depends on perfect_flag. A perfect maze needs both
        dimensions to be at least 1 and an area of at least 2. An
        imperfect maze needs both dimensions to be at least 2 and an
        area of at least 6, the smallest board that can hold two
        independent loops.

        Raise MazeTooSmallError if either requirement is not met.
        """
        min_width = 4
        min_height = 4
        max_height = 50
        max_width = 50
        if width < min_width:
            raise MazeTooSmallError("width", min_width)
        if height < min_height:
            raise MazeTooSmallError("height", min_height)
        if width > max_width:
            raise MazeTooBigError("width", max_width)
        if height > max_height:
            raise MazeTooBigError("height", max_height)
        return (width, height)

    @staticmethod
    def validate_point(
        point_name: str, point_coords: tuple[int, int], maze_dimensions: tuple[int, int]
    ) -> tuple[int, int]:
        """Return point_coords unchanged if they lie inside the maze
        and aren't in the blocked cells.

        point_name is a label such as "ENTRY" or "EXIT", used only in
        error messages. maze_dimensions is the (width, height) pair the
        coordinates are checked against.

        Raise InvalidDimensionError if either coordinate is negative.
        Raise PointOutOfBoundsError if either coordinate is beyond the
        corresponding maze dimension.
        Raise BlockedCellsError if either coordinate is in the blocked cells.
        """
        MazeConfig.validate_dimension(point_coords[0], f"{point_name} x-coordinate")
        MazeConfig.validate_dimension(point_coords[1], f"{point_name} y-coordinate")
        if point_coords[0] >= maze_dimensions[0]:
            raise PointOutOfBoundsError(point_coords, point_name, "x-coordinate", maze_dimensions[0] - 1)
        if point_coords[1] >= maze_dimensions[1]:
            raise PointOutOfBoundsError(point_coords, point_name, "y-coordinate", maze_dimensions[1] - 1)
        point_coords = (point_coords[1], point_coords[0])
        blocked_cells = get_blocked_cells(maze_dimensions[1], maze_dimensions[0])
        if point_coords in blocked_cells:
            raise BlockedCellsError(point_name)
        return point_coords
