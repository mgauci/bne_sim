# Definitions of constants.

# 'Hack' to creates an enum-like class in Python.
# See: http://stackoverflow.com/questions/36932/
def enum(**enums):
    return type('Enum', (), enums)

# RGB color definitions.
COLORS = enum(
    red   = (255,   0,   0),
    green = (  0, 255,   0),
    blue  = (  0,   0, 255),
    black = (  0,   0,   0),
    white = (255, 255, 255),
)

# 1080 pixels, screen height = 0.28 meters 
# for 23" screen with 16:9 display ratio.
SCALE   = 1080/0.286258
