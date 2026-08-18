GREY = '\u001b[90m'
WHITE = '\u001b[37m'
GREEN = '\u001b[32m'
RED = '\u001b[31m'
BLUE = '\u001b[34m'
INDIGO = '\u001b[35m'
YELLOW = '\u001b[33m'
RESET = '\u001b[0m'


class ColourPair:
    def __init__(self, walls: str, path: str):
        self.walls = walls
        self.path = path


COLOUR_PAIRS = [
    ColourPair(WHITE, BLUE),
    ColourPair(YELLOW, INDIGO),
]
