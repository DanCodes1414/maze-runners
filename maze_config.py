#!/usr/bin/env python3


class BadDimensionError(Exception):
    def __init__(self, dimension: str) -> None:
        super().__init__(f"{dimension} cannot be negative.")


class PointOutOfBoundsError(Exception):
    def __init__(self, point_coords: tuple[int, int],
                 point_name: str, dimension: str, max_dimension: int) -> None:
        super().__init__(f"{point_name} point {point_coords}"
                         "is not in the maze."
                         f" Maximum {dimension} is {max_dimension}.")


class KeyError(Exception):
    def __init__(self, missing_keys: list[str]) -> None:
        super().__init__(f"Check the existance and syntax "
                         f"of the following: {missing_keys}")


class PointError(Exception):
    def __init__(self) -> None:
        super().__init__("Entry and exit points cannot be the same.")


class FlagError(Exception):
    def __init__(self, flag: str) -> None:
        super().__init__(f"Invalid flag provided: {flag}.")


class TupleError(Exception):
    def __init__(self, point_name: str, num: int) -> None:
        super().__init__(f"{point_name} takes exactly 2 coordinates,"
                         f" but {num} was provided")


class MazeConfig:

    mandatory_keys = ["WIDTH", "HEIGHT",
                      "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    @staticmethod
    def validate_dimension(dimension: int, dimension_name: str) -> int:
        if dimension < 0:
            raise BadDimensionError(dimension_name.capitalize())
        return dimension

    @staticmethod
    def validate_point(point_name: str, point_coords: tuple[int, int],
                       maze_dimensions: tuple[int, int]) -> tuple[int, int]:
        MazeConfig.validate_dimension(point_coords[0], "width")
        MazeConfig.validate_dimension(point_coords[1], "height")
        if point_coords[0] > maze_dimensions[0]:
            raise PointOutOfBoundsError(point_coords, point_name,
                                        "width", maze_dimensions[0])
        if point_coords[1] > maze_dimensions[1]:
            raise PointOutOfBoundsError(point_coords, point_name,
                                        "height", maze_dimensions[1])
        return point_coords

    def __init__(self, output_filename: str, width: int, height: int,
                 entry_coords: tuple[int, int], exit_coords: tuple[int, int],
                 perfect_flag: bool) -> None:
        self.output_filename = output_filename
        self.width = MazeConfig.validate_dimension(width, "width")
        self.height = MazeConfig.validate_dimension(height, "height")
        maze_dimensions = (width, height)
        self.entry_point = MazeConfig.validate_point(
            "entry", entry_coords, maze_dimensions)
        self.exit_point = MazeConfig.validate_point(
            "exit", exit_coords, maze_dimensions)
        if (self.entry_point == self.exit_point):
            raise PointError()
        self.perfect_flag = perfect_flag

    @staticmethod
    def remove_comments_and_whitespace(content: str) -> list[str]:
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            if not lines[i].strip() or ((lines[i]).strip())[0] == '#':
                lines.remove(lines[i])
            else:
                i += 1
        return [line.strip() for line in lines]

    @classmethod
    def has_mandatory_keys(cls, kv_dictionary: dict[str, str]) -> list[str]:
        missing_keys = []
        for mandatory_key in cls.mandatory_keys:
            if mandatory_key not in kv_dictionary.keys():
                missing_keys.append(mandatory_key)
        return missing_keys

    @staticmethod
    def create_kv_dictionary(non_comment_lines: list[str]) -> dict[str, str]:
        kv_dictionary: dict[str, str] = {}
        for line in non_comment_lines:
            kv_pair = line.split('=')
            kv_pair[0] = kv_pair[0].upper().strip()
            if len(kv_pair) == 2 and kv_pair[0] not in kv_dictionary.keys():
                kv_dictionary[kv_pair[0]] = kv_pair[1].strip()
        return kv_dictionary

    @staticmethod
    def get_point(kv_dictionary: dict[str, str],
                  point_name: str) -> tuple[int, int]:
        point_str = kv_dictionary[point_name]
        coords = point_str.split(',')
        if len(coords) != 2:
            raise TupleError(point_name, len(coords))
        try:
            x_coord = int(coords[0])
            y_coord = int(coords[1])
        except ValueError:
            raise ValueError(f"Non-numerical coordnates detected."
                             f"Check {point_name}: {coords}")
        return (x_coord, y_coord)

    @staticmethod
    def get_flag(flag: str) -> bool:
        if flag.capitalize() == "True":
            return True
        elif flag.capitalize() == "False":
            return False
        raise FlagError(flag)

    @classmethod
    def get_config_from_file(cls, filename: str) -> "MazeConfig":
        with open(filename) as f:
            content = f.read()
        non_comment_lines = cls.remove_comments_and_whitespace(content)
        kv_dictionary = cls.create_kv_dictionary(non_comment_lines)
        bad_lines = cls.has_mandatory_keys(kv_dictionary)
        if bad_lines:
            raise KeyError(bad_lines)
        output_filename = kv_dictionary["OUTPUT_FILE"]
        width = int(kv_dictionary["WIDTH"])
        height = int(kv_dictionary["HEIGHT"])
        entry_point = cls.get_point(kv_dictionary, "ENTRY")
        exit_point = cls.get_point(kv_dictionary, "EXIT")
        perfect_flag = cls.get_flag(kv_dictionary["PERFECT"])
        return cls(output_filename, width, height,
                   entry_point, exit_point, perfect_flag)
