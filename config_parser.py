"""Parse A-Maze-ing configuration files into MazeConfig instances.

Reads a KEY=VALUE text file, converts each value to its expected type,
and hands the result to MazeConfig, which validates it.

Every key in MANDATORY_KEYS must be present. The keys in
ADDITIONAL_KEYS are optional and fall back to a default. Any other key
found in the file is ignored.

The entry point is MazeParsing.parse_config_from_file; the other methods
are the steps it is built from.
"""

import parser_errors as errors
import sys
import os
from mazegen.config import MazeConfig


class MazeParsing:
    MANDATORY_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    ADDITIONAL_KEYS = ["SEED", "BRAID"]
    """Namespace holding the parsing steps for a configuration file.

    The class keeps no state and is never instantiated: every method is
    a staticmethod or a classmethod. Call parse_config_from_file to go
    from a filename to a validated MazeConfig; the other methods are
    exposed mainly so each step can be read and tested on its own.
    """

    @staticmethod
    def remove_comments_and_whitespace(content: str) -> list[str]:
        """Return the usable lines of a configuration file.

        Each line is stripped of its surrounding whitespace, then blank
        lines and comment lines are dropped. A line is a comment when
        its first non-whitespace character is '#', so a '#' further
        along a line is kept and ends up inside the value.

        Args:
            content: The whole configuration file, as a single string.

        Returns:
            non_comment_or_whitespace_lines: The stripped lines that are neither empty nor comments, in \
            the order they appear in the file.
        """
        lines = content.split('\n')
        non_comment_or_whitespace_lines: list[str] = []
        for line in lines:
            line = line.strip()
            if line and line[0] != '#':
                non_comment_or_whitespace_lines.append(line)
        return non_comment_or_whitespace_lines

    @classmethod
    def find_missing_keys(cls, kv_dictionary: dict[str, str]) -> list[str]:
        """Return the mandatory keys missing from a parsed config.

        Args:
            kv_dictionary: The keys found in the file, as returned by
                create_kv_dictionary.

        Returns:
            missing_keys: The keys of MANDATORY_KEYS that are absent from \
            kv_dictionary, in the order they are declared there. Empty \
            if none are missing.
        """
        missing_keys = []
        for mandatory_key in cls.MANDATORY_KEYS:
            if mandatory_key not in kv_dictionary.keys():
                missing_keys.append(mandatory_key)
        return missing_keys

    @classmethod
    def create_kv_dictionary(cls, non_comment_lines: list[str]) -> dict[str, str]:
        """Map the recognised keys of a config file to their values.

        Each line is split on its first '='. The key is upper-cased and
        stripped, so keys match case-insensitively and may be padded
        with spaces; the value is stripped too. Lines whose key is in
        neither MANDATORY_KEYS nor ADDITIONAL_KEYS are skipped without
        error. When a recognised key appears more than once, the first
        value is kept and a warning is printed on stderr.

        Args:
            non_comment_lines: Stripped lines, as returned by
                remove_comments_and_whitespace.

        Returns:
            kv_dictionary: The recognised keys, upper-cased, mapped to their raw string \
            values. Converting those values to their expected types is \
            left to the other methods.

        Raises:
            errors.LineSyntaxError: If a line holds no '=' at all, or if
                a recognised key is given an empty value.
        """
        kv_dictionary: dict[str, str] = {}
        recognised_keys = cls.MANDATORY_KEYS + cls.ADDITIONAL_KEYS
        for line in non_comment_lines:
            kv_pair = line.split('=', 1)
            key = kv_pair[0].upper().strip()
            if len(kv_pair) < 2:
                raise errors.LineSyntaxError(kv_pair[0])
            if key in recognised_keys:
                value = kv_pair[1].strip()
                if not value:
                    raise errors.LineSyntaxError(line)
                if key in kv_dictionary:
                    print(f"Duplicate key for {key} in configuration file: '{kv_pair[0]}'. "
                          "Discarding duplicate and continuing.", file=sys.stderr)
                else:
                    kv_dictionary[key] = value
        return kv_dictionary

    @staticmethod
    def parse_dimension(dimension_str: str, dimension_name: str) -> int:
        """Convert a configuration value to an int.

        Args:
            dimension_str: The value to convert. Surrounding whitespace
                and a leading sign are accepted, as by int().
            dimension_name: The name used to identify the value in the
                error message. It has no effect on the conversion.

        Returns:
            dimension_str: dimension as an int. Nothing else is checked here. Negative \
            or unreasonably large values are rejected later by \
            MazeConfig.

        Raises:
            ValueError: If dimension_str is not a valid integer. The
                message names dimension_name and quotes the value.
        """
        try:
            dimension_int = int(dimension_str)
        except ValueError:
            raise ValueError(f"ValueError on {dimension_name}. {dimension_name} "
                             f"value in configuration file: '{dimension_str}'")
        return dimension_int

    @classmethod
    def parse_point(cls, kv_dictionary: dict[str, str],
                    point_name: str) -> tuple[int, int]:
        """Read a pair of coordinates from a parsed configuration.

        The value is split on ',' and both halves go through
        parse_dimension, so "0,0" and " 0 , 0 " are equally accepted.
        Whether the point falls inside the maze is checked later by
        MazeConfig.

        Args:
            kv_dictionary: The parsed configuration.
            point_name: The key to read, e.g. "ENTRY" or "EXIT". It is
                also used in the error messages, and must be present in
                kv_dictionary.

        Returns:
            x_coord, y_coord: The coordinates as an (x, y) tuple of ints.

        Raises:
            errors.TupleError: If the value does not hold exactly two
                comma-separated fields.
            ValueError: If either coordinate is not a valid integer.
            KeyError: If point_name is absent from kv_dictionary.
        """
        point_str = kv_dictionary[point_name]
        coords = point_str.split(',')
        if len(coords) != 2:
            raise errors.TupleError(point_name)
        x_coord = cls.parse_dimension(coords[0], f"{point_name} x-coordinate")
        y_coord = cls.parse_dimension(coords[1], f"{point_name} y-coordinate")
        return (x_coord, y_coord)

    @staticmethod
    def parse_flag(kv_dictionary: dict[str, str], flag_name: str) -> bool:
        """Read a boolean flag from a parsed configuration.

        The value is compared using str.capitalize, which upper-cases
        the first character and lower-cases the rest, so "TRUE", "true"
        and "tRuE" are all accepted.

        Args:
            kv_dictionary: The parsed configuration.
            flag_name: The key to read, e.g. "PERFECT" or "BRAID". It
                is also used in the error message, and must be present
                in kv_dictionary.

        Returns:
            The boolean the value stands for.

        Raises:
            errors.FlagError: If the value is neither "True" nor
                "False", ignoring case.
            KeyError: If flag_name is absent from kv_dictionary.
        """
        flag = kv_dictionary[flag_name]
        if flag.capitalize() == "True":
            return True
        elif flag.capitalize() == "False":
            return False
        raise errors.FlagError(flag, flag_name)

    @staticmethod
    def check_output_filename(output_filename: str, config_filename: str) -> str:
        """Check that the output will not overwrite the config file.

        Both names are resolved with os.path.realpath, so symbolic links
        and different relative paths leading to the same file are
        caught. Nothing else is verified: the target directory may not
        exist and the file may not be writable.

        Args:
            output_filename: The value of OUTPUT_FILE.
            config_filename: The path the configuration was read from.

        Returns:
            output_filename: unchanged, so the check can be used inline.

        Raises:
            errors.OutputFilenameError: If both names resolve to the
                same path.
        """
        output_filename_path = os.path.realpath(output_filename)
        config_filename_path = os.path.realpath(config_filename)
        if output_filename_path == config_filename_path:
            raise errors.OutputFilenameError("OUTPUT_FILE can't be the same as config filename.")
        return output_filename

    @classmethod
    def parse_config_from_file(cls, config_filename: str) -> MazeConfig:
        """Build a MazeConfig from a configuration file.

        Reads the file, strips comments, collects the KEY=VALUE pairs,
        converts each value to its expected type and passes them to
        MazeConfig, which validates them. This is the intended way to
        create a MazeConfig from a file.

        The optional keys fall back to a default when absent: BRAID to
        False and SEED to None. BRAID is passed to MazeConfig as its
        braid argument.

        Values are converted in a fixed order (OUTPUT_FILE, PERFECT,
        BRAID, WIDTH, HEIGHT, SEED, ENTRY, EXIT) and the first failure
        stops the parsing, so a file with several problems only reports
        the first one in that order.

        Args:
            config_filename: Path to the configuration file.

        Returns:
            A MazeConfig built from the file and validated by MazeConfig
            itself. Values that are individually well-formed but
            describe an impossible maze are rejected there, not here.

        Raises:
            OSError: If the file cannot be opened or read, for instance
                FileNotFoundError or PermissionError.
            UnicodeDecodeError: If the file is not text in the default
                encoding.
            errors.MissingKeyError: If any key of MANDATORY_KEYS is
                absent from the file.
            errors.LineSyntaxError: On a line without '=' or with an
                empty value for a recognised key.
            errors.OutputFilenameError: If OUTPUT_FILE points at the
                configuration file itself.
            errors.FlagError: On a PERFECT or BRAID value that is not
                a boolean.
            errors.TupleError: If ENTRY or EXIT does not hold exactly
                two coordinates.
            ValueError: If WIDTH, HEIGHT, SEED or a coordinate is not a
                valid integer.
        """
        with open(config_filename) as f:
            content = f.read()
        non_comment_lines = cls.remove_comments_and_whitespace(content)
        kv_dictionary = cls.create_kv_dictionary(non_comment_lines)
        missing_keys = cls.find_missing_keys(kv_dictionary)
        if missing_keys:
            raise errors.MissingKeyError(missing_keys)
        output_filename = cls.check_output_filename(kv_dictionary["OUTPUT_FILE"], config_filename)
        perfect = cls.parse_flag(kv_dictionary, "PERFECT")
        if "BRAID" in kv_dictionary:
            braid = cls.parse_flag(kv_dictionary, "BRAID")
        else:
            braid = False
        width = cls.parse_dimension(kv_dictionary["WIDTH"], "WIDTH")
        height = cls.parse_dimension(kv_dictionary["HEIGHT"], "HEIGHT")
        if "SEED" in kv_dictionary:
            seed = cls.parse_dimension(kv_dictionary["SEED"], "SEED")
        else:
            seed = None
        entry_point = cls.parse_point(kv_dictionary, "ENTRY")
        exit_point = cls.parse_point(kv_dictionary, "EXIT")
        maze_config = MazeConfig(
            width=width,
            height=height,
            entry=entry_point,
            exit=exit_point,
            perfect=perfect,
            braid=braid,
            seed=seed,
            output_file=output_filename
        )
        maze_config.validation_rules() # type: ignore[operator]
        return maze_config
