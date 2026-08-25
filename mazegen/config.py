from pydantic import BaseModel, Field


class MazeConfig(BaseModel):
    """
    Represents the configuration for generating a maze.

    Attributes:
        width (int): The width of the maze. Must be between 1 and 50.
        height (int): The height of the maze. Must be between 1 and 50.
        entry (tuple[int, int]): The coordinates of the maze entry point (row, col).
        exit (tuple[int, int]): The coordinates of the maze exit point (row, col).
        seed (int): An optional seed for random number generation. If not provided, a random seed will be used.
        perfect (bool): If True, generates a perfect maze (no loops).
        braid (bool): If True, generates a braided maze (a maze with loops and no dead ends).
        output_file (str): The name of the output file where the maze will be exported.
    """
    width: int = Field(ge=1, le=50)
    height: int = Field(ge=1, le=50)
    entry: tuple[int, int]
    exit: tuple[int, int]
    seed: int | None = Field(default=None)
    perfect: bool = Field(default=False)
    braid: bool = Field(default=False)
    output_file: str
