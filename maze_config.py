#!/usr/bin/env python3

"""Parse and validate A-Maze-ing configuration files.

Exposes the MazeConfig class, which reads a KEY=VALUE configuration
file and produces a validated set of maze parameters, plus the
MazeConfigError hierarchy used to report every validation failure.
"""

import sys
import os


class MazeConfigError(Exception):
    """Base class for all configuration parsing and validation errors."""


class InvalidDimensionError(MazeConfigError):
    """Raise when a value that must be non-negative is negative.

    Applies to maze width and height, point coordinates and the seed.
    """
    def __init__(self, dimension: int, dimension_name: str) -> None:
        super().__init__(f"{dimension_name} is {dimension}."
                         f" {dimension_name} cannot be negative.")


class PointOutOfBoundsError(MazeConfigError):
    """Raise when a point's coordinates fall outside the maze."""
    def __init__(self, point_coords: tuple[int, int],
                 point_name: str, dimension: str, max_dimension: int) -> None:
        super().__init__(f"{point_name} point {point_coords}"
                         f" is not in the maze. Maximum {dimension}"
                         f" is {max_dimension}.")


class LineSyntaxError(MazeConfigError):
    """Raise when a configuration file line has invalid syntax.

    A line is invalid if it is not a comment and contains no '=' sign,
    or if it assigns an empty value to a recognised key. For example,
    'pot', 'width' and 'width=' are all invalid, whereas 'pot=' is not,
    because 'pot' is not a recognised key.
    """
    def __init__(self, line: str) -> None:
        super().__init__(f"The following line has invalid syntax: {line}")


class MissingKeyError(MazeConfigError):
    """Raise when one or more mandatory keys are absent from the file."""
    def __init__(self, missing_keys: list[str]) -> None:
        super().__init__(f"The following mandatory keys "
                         f"are missing: {missing_keys}")


class PointError(MazeConfigError):
    """Raise when the entry and exit points share the same coordinates."""
    def __init__(self) -> None:
        super().__init__("Entry and exit points cannot be the same.")


class FlagError(MazeConfigError):
    """Raise when a boolean flag is assigned a non-boolean value.

    For example, 'PERFECT=fish' triggers this error.
    """
    def __init__(self, flag: str, flag_name: str) -> None:
        super().__init__(f"Invalid {flag_name} flag provided: {flag}.")


class TupleError(MazeConfigError):
    """Raise when ENTRY or EXIT does not contain exactly two coordinates."""
    def __init__(self, point_name: str) -> None:
        super().__init__("Wrong number of coordinates"
                         f" provided for {point_name}")


class MazeTooSmallError(MazeConfigError):
    """Raise when the maze dimensions are below the minimum allowed size."""
    def __init__(self, maze_dimension: str, num: int, maze_type: str) -> None:
        super().__init__(f"The {maze_dimension} of the maze is too small."
                         f" {maze_dimension.capitalize()} must"
                         f" be at least {num} in a {maze_type} maze.")


class OutputFilenameError(MazeConfigError):
    """Raise when the value assigned to OUTPUT_FILE is not acceptable."""


class ContradictionError(MazeConfigError):
    """Raise when both the BRAIDED and PERFECT flags are set.

    A braided maze contains loops by definition, so it can never be
    perfect.
    """
    def __init__(self) -> None:
        super().__init__("Maze cannot be both perfect and braided")


class MazeConfig:
    """Validated maze parameters read from a configuration file.

    Instances are normally created through get_config_from_file rather
    than the constructor directly.
    """
    mandatory_keys = ["WIDTH", "HEIGHT",
                      "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    additional_keys = ["SEED", "BRAIDED"]

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
                raise MazeTooSmallError("width", 1, "perfect")
            if height < 1:
                raise MazeTooSmallError("height", 1, "perfect")
            if width * height < 2:
                raise MazeTooSmallError("area", 2, "perfect")
        else:
            if width < 2:
                raise MazeTooSmallError("width", 2, "imperfect")
            if height < 2:
                raise MazeTooSmallError("height", 2, "imperfect")
            if width * height < 6:
                raise MazeTooSmallError("area", 6, "imperfect")
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
            raise PointOutOfBoundsError(point_coords, point_name,
                                        "x-coordinate", maze_dimensions[0] - 1)
        if point_coords[1] >= maze_dimensions[1]:
            raise PointOutOfBoundsError(point_coords, point_name,
                                        "y-coordinate", maze_dimensions[1] - 1)
        return point_coords

    def __init__(self, output_filename: str, width: int, height: int,
                 entry_coords: tuple[int, int], exit_coords: tuple[int, int],
                 perfect_flag: bool, braided_flag: bool | None,
                 seed: int | None) -> None:
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
            raise PointError()
        self.braided_flag = braided_flag
        if self.braided_flag and self.perfect_flag:
            raise ContradictionError()
        self.seed: int | None
        if seed is not None:
            self.seed = self.validate_dimension(seed, "SEED")
        else:
            self.seed = seed

    @staticmethod
    def remove_comments_and_whitespace(content: str) -> list[str]:
        """Return the stripped, non-empty, non-comment lines of content.

        A line is a comment if its first non-whitespace character is '#'.
        """
        lines = content.split('\n')
        non_comment_or_whitespace_lines: list[str] = []
        for line in lines:
            line = line.strip()
            if line and line[0] != '#':
                non_comment_or_whitespace_lines.append(line)
        return non_comment_or_whitespace_lines

    @classmethod
    def get_missing_keys(cls, kv_dictionary: dict[str, str]) -> list[str]:
        """Return the mandatory keys that are absent from kv_dictionary."""
        missing_keys = []
        for mandatory_key in cls.mandatory_keys:
            if mandatory_key not in kv_dictionary.keys():
                missing_keys.append(mandatory_key)
        return missing_keys

    @classmethod
    def create_kv_dictionary(cls,
                             non_comment_lines: list[str]) -> dict[str, str]:
        """Return a dict of recognised keys to their values.

        non_comment_lines is the output of remove_comments_and_whitespace.
        Keys are matched case-insensitively and stored in upper case;
        lines with unrecognised keys are ignored. If a recognised key
        appears more than once, the first value is kept and a warning is
        printed to stderr.

        Raise LineSyntaxError if a line has no '=' or a recognised key
        has an empty value.
        """
        kv_dictionary: dict[str, str] = {}
        recognised_keys = cls.mandatory_keys + cls.additional_keys
        for line in non_comment_lines:
            kv_pair = line.split('=', 1)
            key = kv_pair[0].upper().strip()
            if len(kv_pair) < 2:
                raise LineSyntaxError(kv_pair[0])
            if key in recognised_keys:
                value = kv_pair[1].strip()
                if not value:
                    raise LineSyntaxError(line)
                if key in kv_dictionary:
                    print(f"Duplicate key for {key} in configuration file: "
                          f"'{kv_pair[0]}'. Discarding duplicate "
                          "and continuing.", file=sys.stderr)
                else:
                    kv_dictionary[key] = value
        return kv_dictionary

    @staticmethod
    def get_dimension(dimension_str: str, dimension_name: str) -> int:
        """Return dimension_str converted to an int.

        dimension_name is used only in the error message.

        Raise ValueError if dimension_str is not a valid integer.
        """
        try:
            dimension_int = int(dimension_str)
        except ValueError:
            raise ValueError(f"ValueError on {dimension_name}. "
                             f"{dimension_name} value in configuration file:"
                             f" '{dimension_str}'")
        return dimension_int

    @classmethod
    def get_point(cls, kv_dictionary: dict[str, str],
                  point_name: str) -> tuple[int, int]:
        """Return the (x, y) pair stored under point_name in kv_dictionary.

        The value must be two comma-separated integers.

        Raise TupleError if there are not exactly two coordinates.
        Raise ValueError if either coordinate is not an integer.
        """
        point_str = kv_dictionary[point_name]
        coords = point_str.split(',')
        if len(coords) != 2:
            raise TupleError(point_name)
        x_coord = cls.get_dimension(coords[0], f"{point_name} x-coordinate")
        y_coord = cls.get_dimension(coords[1], f"{point_name} y-coordinate")
        return (x_coord, y_coord)

    @staticmethod
    def get_flag(kv_dictionary: dict[str, str], flag_name: str) -> bool:
        """Return the boolean stored under flag_name in kv_dictionary.

        The value is matched case-insensitively against "True" and
        "False".

        Raise FlagError if the value is neither.
        """
        flag = kv_dictionary[flag_name]
        if flag.capitalize() == "True":
            return True
        elif flag.capitalize() == "False":
            return False
        raise FlagError(flag, flag_name)

    @staticmethod
    def get_file(output_filename: str, config_filename: str) -> str:
        """Return output_filename if it is an acceptable output target.

        Raise OutputFilenameError if output_filename contains a path
        separator or resolves to the same file as config_filename.
        """
        output_filename_path = os.path.realpath(output_filename)
        config_filename_path = os.path.realpath(config_filename)
        if '/' in output_filename:
            raise OutputFilenameError("OUTPUT_FILE does not accept paths.")
        if output_filename_path == config_filename_path:
            raise OutputFilenameError("OUTPUT_FILE can't"
                                      " be the same as config filename.")
        return output_filename

    @classmethod
    def get_config_from_file(cls, config_filename: str) -> "MazeConfig":
        """Return a MazeConfig built from the file at config_filename.

        Read the file, strip comments, parse KEY=VALUE lines and
        validate the result. This is the intended way to create a
        MazeConfig.

        Raise OSError if the file cannot be read.
        Raise ValueError if a numeric value cannot be parsed.
        Raise a MazeConfigError subclass if the file is malformed or
        describes an impossible maze; see the individual exception
        classes for the specific conditions.
        """
        with open(config_filename) as f:
            content = f.read()
        non_comment_lines = cls.remove_comments_and_whitespace(content)
        kv_dictionary = cls.create_kv_dictionary(non_comment_lines)
        missing_keys = cls.get_missing_keys(kv_dictionary)
        if missing_keys:
            raise MissingKeyError(missing_keys)
        output_filename = cls.get_file(kv_dictionary["OUTPUT_FILE"],
                                       config_filename)
        perfect_flag = cls.get_flag(kv_dictionary, "PERFECT")
        if "BRAIDED" in kv_dictionary:
            braided_flag = cls.get_flag(kv_dictionary, "BRAIDED")
        else:
            braided_flag = None
        width = cls.get_dimension(kv_dictionary["WIDTH"], "WIDTH")
        height = cls.get_dimension(kv_dictionary["HEIGHT"], "HEIGHT")
        if "SEED" in kv_dictionary:
            seed = cls.get_dimension(kv_dictionary["SEED"], "SEED")
        else:
            seed = None
        entry_point = cls.get_point(kv_dictionary, "ENTRY")
        exit_point = cls.get_point(kv_dictionary, "EXIT")
        return cls(output_filename, width, height, entry_point,
                   exit_point, perfect_flag, braided_flag, seed)
