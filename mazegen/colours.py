from pydantic import BaseModel

# in the format BGRA
GREY = (128, 128, 128, 255)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (0, 0, 255, 255)
BLUE = (255, 0, 0, 255)
INDIGO = (130, 0, 75, 255)
YELLOW = (0, 255, 255, 255)


class ColourPair(BaseModel):
    walls: tuple[int, int, int, int]
    path: tuple[int, int, int, int]


COLOUR_PAIRS = [
    ColourPair(walls=WHITE, path=BLUE),
    ColourPair(walls=YELLOW, path=INDIGO),
]
