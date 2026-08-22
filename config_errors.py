"""Exception hierarchy for A-Maze-ing configuration errors.

Every error raised while parsing or validating a configuration
derives from MazeConfigError, so callers can catch the base class.
This module imports nothing from the project so that both
config_parser and maze_config can depend on it freely.
"""


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
