"""Exception hierarchy for A-Maze-ing parser errors.

Every error raised while parsing or validating a configuration
derives from MazeParserError, so callers can catch the base class.
"""


class MazeParserError(Exception):
    """Base class for all configuration parsing and validation errors."""


class LineSyntaxError(MazeParserError):
    """Raise when a configuration file line has invalid syntax.

    A line is invalid if it is not a comment and contains no '=' sign,
    or if it assigns an empty value to a recognised key. For example,
    'pot', 'width' and 'width=' are all invalid, whereas 'pot=' is not,
    because 'pot' is not a recognised key.
    """
    def __init__(self, line: str) -> None:
        super().__init__(f"The following line has invalid syntax: {line}")


class MissingKeyError(MazeParserError):
    """Raise when one or more mandatory keys are absent from the file."""
    def __init__(self, missing_keys: list[str]) -> None:
        super().__init__(f"The following mandatory keys "
                         f"are missing: {missing_keys}")


class FlagError(MazeParserError):
    """Raise when a boolean flag is assigned a non-boolean value.

    For example, 'PERFECT=fish' triggers this error.
    """
    def __init__(self, flag: str, flag_name: str) -> None:
        super().__init__(f"Invalid {flag_name} flag provided: {flag}.")


class TupleError(MazeParserError):
    """Raise when ENTRY or EXIT does not contain exactly two coordinates."""
    def __init__(self, point_name: str) -> None:
        super().__init__("Wrong number of coordinates"
                         f" provided for {point_name}")


class OutputFilenameError(MazeParserError):
    """Raise when the value assigned to OUTPUT_FILE is not acceptable."""
