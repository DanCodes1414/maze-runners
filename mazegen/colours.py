from pydantic import BaseModel

# in the format BGRA (more refined palette)
CHARCOAL = (50, 50, 50, 255)       # Dark, professional wall color
CREAM = (230, 230, 200, 255)       # Warm, easy on the eyes
SLATE = (110, 90, 80, 255)         # Cool grey-blue tone
LIGHT_BLUE = (230, 216, 173, 255)  # Soft, muted blue
DEEP_TEAL = (102, 102, 0, 255)     # Rich teal (darker than pure cyan)
MINT = (152, 251, 152, 255)        # Soft, pale green
NAVY = (139, 100, 64, 255)         # Deep blue
SANDY = (210, 180, 140, 255)       # Warm tan
DARK_PURPLE = (130, 0, 75, 255)    # Rich purple (refined)
PALE_LAVENDER = (250, 230, 230, 255)  # Light, cool complement
FOREST_GREEN = (34, 139, 34, 255)  # Deep green (not neon)
GOLD = (215, 215, 0, 255)          # Muted gold/yellow


class ColourPair(BaseModel):
    walls: tuple[int, int, int, int]
    path: tuple[int, int, int, int]


COLOUR_PAIRS = [
    # Classic professional looks
    ColourPair(walls=CHARCOAL, path=CREAM),           # Dark/light - best contrast
    ColourPair(walls=SLATE, path=LIGHT_BLUE),        # Cool tones
    
    # Nature-inspired
    ColourPair(walls=FOREST_GREEN, path=SANDY),      # Earthy
    ColourPair(walls=DEEP_TEAL, path=MINT),          # Fresh
    
    # Sophisticated contrasts
    ColourPair(walls=NAVY, path=GOLD),               # Elegant
    ColourPair(walls=DARK_PURPLE, path=PALE_LAVENDER),  # Refined
]
