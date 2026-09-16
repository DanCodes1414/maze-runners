from pydantic import BaseModel

# in the format BGRA
CHARCOAL = (50, 50, 50, 255)
CREAM = (230, 230, 200, 255)
SLATE = (110, 90, 80, 255)
LIGHT_BLUE = (230, 216, 173, 255)
DEEP_TEAL = (102, 102, 0, 255)
MINT = (152, 251, 152, 255)
NAVY = (139, 100, 64, 255)
SANDY = (210, 180, 140, 255)
DARK_PURPLE = (130, 0, 75, 255)
PALE_LAVENDER = (250, 230, 230, 255)
FOREST_GREEN = (34, 139, 34, 255)
GOLD = (215, 215, 0, 255)


class ColourPair(BaseModel):
    walls: tuple[int, int, int, int]
    path: tuple[int, int, int, int]


COLOUR_PAIRS = [
    ColourPair(walls=CHARCOAL, path=CREAM),
    ColourPair(walls=SLATE, path=LIGHT_BLUE),
    ColourPair(walls=FOREST_GREEN, path=SANDY),
    ColourPair(walls=DEEP_TEAL, path=MINT),
    ColourPair(walls=NAVY, path=GOLD),
    ColourPair(walls=DARK_PURPLE, path=PALE_LAVENDER)
]
