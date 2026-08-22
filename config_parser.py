import config_errors
import sys
import os

MANDATORY_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

ADDITIONAL_KEYS = ["SEED", "BRAIDED"]


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


def parse_missing_keys(kv_dictionary: dict[str, str]) -> list[str]:
    """Return the mandatory keys that are absent from kv_dictionary."""
    missing_keys = []
    for mandatory_key in MANDATORY_KEYS:
        if mandatory_key not in kv_dictionary.keys():
            missing_keys.append(mandatory_key)
    return missing_keys


def create_kv_dictionary(non_comment_lines: list[str]) -> dict[str, str]:
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
    recognised_keys = MANDATORY_KEYS + ADDITIONAL_KEYS
    for line in non_comment_lines:
        kv_pair = line.split('=', 1)
        key = kv_pair[0].upper().strip()
        if len(kv_pair) < 2:
            raise config_errors.LineSyntaxError(kv_pair[0])
        if key in recognised_keys:
            value = kv_pair[1].strip()
            if not value:
                raise config_errors.LineSyntaxError(line)
            if key in kv_dictionary:
                print(f"Duplicate key for {key} in configuration file: "
                      f"'{kv_pair[0]}'. Discarding duplicate "
                      "and continuing.", file=sys.stderr)
            else:
                kv_dictionary[key] = value
    return kv_dictionary


def parse_dimension(dimension_str: str, dimension_name: str) -> int:
    """Return dimension_str converted to an int.

    dimension_name is used only in the error message.

    Raise ValueError if dimension_str is not a valid integer.
    """
    try:
        dimension_int = int(dimension_str)
    except ValueError:
        raise ValueError(f"ValueError on {dimension_name}. {dimension_name} "
                         f"value in configuration file: '{dimension_str}'")
    return dimension_int


def parse_point(kv_dictionary: dict[str, str],
                point_name: str) -> tuple[int, int]:
    """Return the (x, y) pair stored under point_name in kv_dictionary.

    The value must be two comma-separated integers.

    Raise TupleError if there are not exactly two coordinates.
    Raise ValueError if either coordinate is not an integer.
    """
    point_str = kv_dictionary[point_name]
    coords = point_str.split(',')
    if len(coords) != 2:
        raise config_errors.TupleError(point_name)
    x_coord = parse_dimension(coords[0], f"{point_name} x-coordinate")
    y_coord = parse_dimension(coords[1], f"{point_name} y-coordinate")
    return (x_coord, y_coord)


def parse_flag(kv_dictionary: dict[str, str], flag_name: str) -> bool:
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
    raise config_errors.FlagError(flag, flag_name)


def parse_file(output_filename: str, config_filename: str) -> str:
    """Return output_filename if it is an acceptable output target.

    Raise OutputFilenameError if output_filename contains a path
    separator or resolves to the same file as config_filename.
    """
    output_filename_path = os.path.realpath(output_filename)
    config_filename_path = os.path.realpath(config_filename)
    if '/' in output_filename:
        raise config_errors.OutputFilenameError("OUTPUT_FILE does "
                                                "not accept paths.")
    if output_filename_path == config_filename_path:
        raise config_errors.OutputFilenameError("OUTPUT_FILE can't be the"
                                                " same as config filename.")
    return output_filename
