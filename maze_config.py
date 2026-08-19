#!/usr/bin/env python3

import sys


class MazeConfigError(Exception):
    pass


class NegativeSeedError(MazeConfigError):
    def __init__(self, seed_value: int) -> None:
        super().__init__(f"Seed value is {seed_value}."
                          "Seed value can't be negative")


class InvalidCoordinateError(MazeConfigError):
    def __init__(self, dimension: int, dimension_name: str) -> None:
        super().__init__(f"{dimension_name} is {dimension}."
                         f" {dimension_name} cannot be negative.")


class PointOutOfBoundsError(MazeConfigError):
    def __init__(self, point_coords: tuple[int, int],
                 point_name: str, dimension: str, max_dimension: int) -> None:
        super().__init__(f"{point_name} point {point_coords}"
                         f" is not in the maze. Maximum {dimension}"
                         f" is {max_dimension}.")


class LineSyntaxError(MazeConfigError):
    def __init__(self, line: str) -> None:
        super().__init__(f"The following line has invalid syntax: {line}")


class MissingKeyError(MazeConfigError):
    def __init__(self, missing_keys: list[str]) -> None:
        super().__init__(f"The following mandatory keys "
                         f"are missing: {missing_keys}")


class PointError(MazeConfigError):
    def __init__(self) -> None:
        super().__init__("Entry and exit points cannot be the same.")


class FlagError(MazeConfigError):
    def __init__(self, flag: str, flag_name: str) -> None:
        super().__init__(f"Invalid {flag_name} flag provided: {flag}.")


class TupleError(MazeConfigError):
    def __init__(self, point_name: str) -> None:
        super().__init__("Wrong number of coordinates"
                         f" provided for {point_name}")


class MazeTooSmallError(MazeConfigError):
    def __init__(self, maze_dimension: str, num: int, maze_type: str) -> None:
        super().__init__(f"The {maze_dimension} of the maze is too small."
                         f" {maze_dimension.capitalize()} must"
                         f" be at least {num} in a {maze_type} maze.")

class ContradictionError(MazeConfigError):
    def __init__(self) -> None:
        super().__init__("Maze cannot be both perfect and braided")

class MazeConfig:

    mandatory_keys = ["WIDTH", "HEIGHT",
                      "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    additional_keys = ["SEED", "BRAIDED"]

    @staticmethod
    def validate_dimension(dimension: int, dimension_name: str) -> int:
        if dimension < 0:
            raise InvalidCoordinateError(dimension, dimension_name)
        return dimension

    @staticmethod
    def validate_maze(width: int, height: int,
                      perfect_flag: bool) -> tuple[int, int]:
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
        return (width, height)

    @staticmethod
    def validate_point(point_name: str, point_coords: tuple[int, int],
                       maze_dimensions: tuple[int, int]) -> tuple[int, int]:
        MazeConfig.validate_dimension(point_coords[0],
                                      f"{point_name.upper()} x-coordinate")
        MazeConfig.validate_dimension(point_coords[1],
                                      f"{point_name.upper()} y-coordinate")
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
        self.output_filename = output_filename
        self.perfect_flag = perfect_flag
        self.width, self.height = MazeConfig.validate_maze(width,
                                                           height,
                                                           self.perfect_flag)
        maze_dimensions = (self.width, self.height)
        self.entry_point = MazeConfig.validate_point(
            "entry", entry_coords, maze_dimensions)
        self.exit_point = MazeConfig.validate_point(
            "exit", exit_coords, maze_dimensions)
        if (self.entry_point == self.exit_point):
            raise PointError()
        self.braided_flag = braided_flag
        if self.braided_flag and self.perfect_flag:
            raise ContradictionError()
        if seed and seed < 0:
            raise NegativeSeedError(seed)
        self.seed = seed

    @staticmethod
    def remove_comments_and_whitespace(content: str) -> list[str]:
        lines = content.split('\n')
        non_comment_or_whitespace_lines: list[str] = []
        for line in lines:
            line = line.strip()
            if line and line[0] != '#':
                non_comment_or_whitespace_lines.append(line)
        return non_comment_or_whitespace_lines

    @classmethod
    def get_missing_keys(cls, kv_dictionary: dict[str, str]) -> list[str]:
        missing_keys = []
        for mandatory_key in cls.mandatory_keys:
            if mandatory_key not in kv_dictionary.keys():
                missing_keys.append(mandatory_key)
        return missing_keys

    @classmethod
    def create_kv_dictionary(cls,
                             non_comment_lines: list[str]) -> dict[str, str]:
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
        point_str = kv_dictionary[point_name]
        coords = point_str.split(',')
        if len(coords) != 2:
            raise TupleError(point_name)
        x_coord = cls.get_dimension(coords[0], f"{point_name} x-coordinate")
        y_coord = cls.get_dimension(coords[1], f"{point_name} y-coordinate")
        return (x_coord, y_coord)

    @staticmethod
    def get_flag(kv_dictionary: dict[str, str], flag_name: str) -> bool:
        flag = kv_dictionary[flag_name]
        if flag.capitalize() == "True":
            return True
        elif flag.capitalize() == "False":
            return False
        raise FlagError(flag, flag_name)

    @staticmethod
    def get_file(file_name: str) -> str:
        ...
        return file_name

    @classmethod
    def get_config_from_file(cls, filename: str) -> "MazeConfig":
        with open(filename) as f:
            content = f.read()
        non_comment_lines = cls.remove_comments_and_whitespace(content)
        kv_dictionary = cls.create_kv_dictionary(non_comment_lines)
        missing_keys = cls.get_missing_keys(kv_dictionary)
        if missing_keys:
            raise MissingKeyError(missing_keys)
        output_filename = cls.get_file(kv_dictionary["OUTPUT_FILE"]) #I still haven't written this 
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
