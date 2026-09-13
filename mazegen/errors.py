"""Exception hierarchy for A-Maze-ing configuration errors.

Every error raised while parsing or validating a configuration
derives from MazeConfigError, so callers can catch the base class.
"""


class MazeConfigError(Exception):
    """Base class for all configuration parsing and validation errors."""


class InvalidDimensionError(MazeConfigError):
    """Raise when a value that must be non-negative is negative.

    Applies to maze width and height, point coordinates and the seed.
    """
    def __init__(self, dimension: int, dimension_name: str) -> None:
        super().__init__(f"{dimension_name} is {dimension}. {dimension_name} cannot be negative.")


class PointOutOfBoundsError(MazeConfigError):
    """Raise when a point's coordinates fall outside the maze."""
    def __init__(self, point_coords: tuple[int, int], point_name: str, dimension: str, max_dimension: int) -> None:
        super().__init__(
            f"{point_name} point {point_coords} is not in the maze. Maximum {dimension} is {max_dimension}."
        )


class PointError(MazeConfigError):
    """Raise when the entry and exit points share the same coordinates."""
    def __init__(self) -> None:
        super().__init__("Entry and exit points cannot be the same.")


class MazeTooSmallError(MazeConfigError):
    """Raise when the maze dimensions are below the minimum allowed size."""
    def __init__(self, maze_dimension: str, num: int) -> None:
        super().__init__(
            f"The {maze_dimension} of the maze is too small. "
            f"{maze_dimension.capitalize()} must be at least {num}."
        )


class MazeTooBigError(MazeConfigError):
    """Raise when the maze dimensions are above the minimum allowed size."""
    def __init__(self, maze_dimension: str, num: int) -> None:
        super().__init__(
            f"The {maze_dimension} of the maze is too big. "
            f"{maze_dimension.capitalize()} must be at most {num}."
        )


class ContradictionError(MazeConfigError):
    """Raise when both the BRAID and PERFECT flags are set.

    A braided maze contains loops by definition, so it can never be perfect.
    """
    def __init__(self) -> None:
        super().__init__("Maze cannot be both perfect and braided")


class OutputFilenameError(MazeConfigError):
    """Raise when the value assigned to OUTPUT_FILE is not acceptable."""


class BlockedCellsError(MazeConfigError):
    """Raise when ENTRY/EXIT point is in blocked (by 42 logo) cells."""
    def __init__(self, point_name: str) -> None:
        super().__init__(f"{point_name} point cannot be in blocked cells.")
