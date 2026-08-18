#!/usr/bin/env python3


class MazeConfigError(Exception):
    pass


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
        super().__init__(f"The following keys are missing: {missing_keys}")


class PointError(MazeConfigError):
    def __init__(self) -> None:
        super().__init__("Entry and exit points cannot be the same.")


class FlagError(MazeConfigError):
    def __init__(self, flag: str) -> None:
        super().__init__(f"Invalid flag provided: {flag}.")


class TupleError(MazeConfigError):
    def __init__(self, point_name: str) -> None:
        super().__init__("Wrong number of coordinates"
                         f" provided for {point_name}")


class MazeTooSmallError(MazeConfigError):
    def __init__(self, maze_dimension: str, num: int) -> None:
        super().__init__(f"The {maze_dimension} of the maze is too small."
                         f" {maze_dimension.capitalize()} must"
                         f" be at least {num}.")


class MazeConfig:

    mandatory_keys = ["WIDTH", "HEIGHT",
                      "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    # additional_keys = ["SEED", "ALGORITHM", "DISPLAY_MODE"]

    @staticmethod
    def validate_dimension(dimension: int, dimension_name: str) -> int:
        if dimension < 0:
            raise InvalidCoordinateError(dimension, dimension_name)
        return dimension

    @staticmethod
    def validate_maze_size(width: int, height: int) -> tuple[int, int]:
        if width < 1:
            raise MazeTooSmallError("width", 1)
        if height < 1:
            raise MazeTooSmallError("height", 1)
        if width * height < 2:
            raise MazeTooSmallError("area", 2)
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
                 perfect_flag: bool) -> None:
        self.output_filename = output_filename
        self.width, self.height = MazeConfig.validate_maze_size(width, height)
        maze_dimensions = (self.width, self.height)
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
    def get_missing_keys(cls, kv_dictionary: dict[str, str]) -> list[str]:
        missing_keys = []
        for mandatory_key in cls.mandatory_keys:
            if mandatory_key not in kv_dictionary.keys():
                missing_keys.append(mandatory_key)
        return missing_keys

    @staticmethod
    def create_kv_dictionary(non_comment_lines: list[str]) -> dict[str, str]:
        kv_dictionary: dict[str, str] = {}
        for line in non_comment_lines:
            kv_pair = line.split('=', 1)
            key = kv_pair[0].upper().strip()
            if len(kv_pair) < 2:
                raise LineSyntaxError(kv_pair[0])
            if key not in kv_dictionary.keys():
                kv_dictionary[key] = kv_pair[1].strip()
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
    def get_flag(flag: str) -> bool:
        if flag.capitalize() == "True":
            return True
        elif flag.capitalize() == "False":
            return False
        raise FlagError(flag)

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
        perfect_flag = cls.get_flag(kv_dictionary["PERFECT"])
        width = cls.get_dimension(kv_dictionary["WIDTH"], "WIDTH") #min width and min height are both contingent on the perfect flag if flag==false min size is a 2x2 because it needs multiple routes.
        height = cls.get_dimension(kv_dictionary["HEIGHT"], "HEIGHT")
        entry_point = cls.get_point(kv_dictionary, "ENTRY")
        exit_point = cls.get_point(kv_dictionary, "EXIT")
        return cls(output_filename, width, height, entry_point,
                   exit_point, perfect_flag)
