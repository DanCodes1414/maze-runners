#!/usr/bin/env python3

"""Validated maze parameters for the A-Maze-ing generator.

Exposes the MazeConfig class, which checks that a set of maze
parameters (dimensions, entry and exit points, flags, seed) describe
a maze that can be generated. Parsing a configuration file into those
parameters is handled separately by config_parser.
"""

import config_errors as errors


class MazeConfig:
    """Validated maze parameters.

    The constructor validates raw values directly. To build an instance
    from a configuration file, use config_parser.parse_config_from_file.
    """

    def __init__(self, output_filename: str, width: int, height: int,
                 entry_coords: tuple[int, int], exit_coords: tuple[int, int],
                 perfect_flag: bool, braided_flag: bool | None = None,
                 seed: int | None = None) -> None:
        """Validate the given parameters and store them as attributes.

        output_filename is stored as given. width and height are checked
        with validate_maze, entry_coords and exit_coords with
        validate_point, and seed (when not None) with validate_dimension;
        any error those raise is propagated.

        Raise PointError if entry_coords and exit_coords are equal.
        Raise ContradictionError if perfect_flag and braided_flag are
        both True.
        """
        self.output_filename = output_filename
        self.perfect_flag = perfect_flag
        self.width, self.height = MazeConfig.validate_maze(width,
                                                           height,
                                                           self.perfect_flag)
        maze_dimensions = (self.width, self.height)
        self.entry_point = MazeConfig.validate_point(
            "ENTRY", entry_coords, maze_dimensions)
        self.exit_point = MazeConfig.validate_point(
            "EXIT", exit_coords, maze_dimensions)
        if (self.entry_point == self.exit_point):
            raise errors.PointError()
        self.braided_flag = braided_flag
        if self.braided_flag and self.perfect_flag:
            raise errors.ContradictionError()
        self.seed: int | None
        if seed is not None:
            self.seed = self.validate_dimension(seed, "SEED")
        else:
            self.seed = seed

    @staticmethod
    def validate_dimension(dimension_value: int, dimension_name: str) -> int:
        """Return dimension_value unchanged if it is non-negative.

        Raise InvalidDimensionError otherwise, using dimension_name in
        the error message.
        """
        if dimension_value < 0:
            raise errors.InvalidDimensionError(dimension_value, dimension_name)
        return dimension_value

    @staticmethod
    def validate_maze(width: int, height: int,
                      perfect_flag: bool) -> tuple[int, int]:
        """Return (width, height) if the maze is large enough.

        The minimum depends on perfect_flag. A perfect maze needs both
        dimensions to be at least 1 and an area of at least 2. An
        imperfect maze needs both dimensions to be at least 2 and an
        area of at least 6, the smallest board that can hold two
        independent loops.

        Raise MazeTooSmallError if either requirement is not met.
        """
        if perfect_flag:
            if width < 1:
                raise errors.MazeTooSmallError("width", 1, "perfect")
            if height < 1:
                raise errors.MazeTooSmallError("height", 1, "perfect")
            if width * height < 2:
                raise errors.MazeTooSmallError("area", 2, "perfect")
        else:
            if width < 2:
                raise errors.MazeTooSmallError("width", 2, "imperfect")
            if height < 2:
                raise errors.MazeTooSmallError("height", 2, "imperfect")
            if width * height < 6:
                raise errors.MazeTooSmallError("area", 6, "imperfect")
        return (width, height)

    @staticmethod
    def validate_point(point_name: str, point_coords: tuple[int, int],
                       maze_dimensions: tuple[int, int]) -> tuple[int, int]:
        """Return point_coords unchanged if they lie inside the maze.

        point_name is a label such as "ENTRY" or "EXIT", used only in
        error messages. maze_dimensions is the (width, height) pair the
        coordinates are checked against.

        Raise InvalidDimensionError if either coordinate is negative.
        Raise PointOutOfBoundsError if either coordinate is beyond the
        corresponding maze dimension.
        """
        MazeConfig.validate_dimension(point_coords[0],
                                      f"{point_name} x-coordinate")
        MazeConfig.validate_dimension(point_coords[1],
                                      f"{point_name} y-coordinate")
        if point_coords[0] >= maze_dimensions[0]:
            raise errors.PointOutOfBoundsError(point_coords, point_name,
                                               "x-coordinate",
                                               maze_dimensions[0] - 1)
        if point_coords[1] >= maze_dimensions[1]:
            raise errors.PointOutOfBoundsError(point_coords, point_name,
                                               "y-coordinate",
                                               maze_dimensions[1] - 1)
        return point_coords
