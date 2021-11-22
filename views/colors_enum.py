from enum import Enum


class Color(bytes, Enum):
    """
    Enum for text colors. Holds:
     * name (e.g. BLUE)
     * value ('\033[34m')
     * label ('b' for usage with §)

    Available colors and their labels:
    §0 - reset
    §1 - bold
    §4 - underline
    §5  - gray
    §r - red
    §g - green
    §y - yellow
    §b - blue
    §m - magenta
    §c - cyan
    §R - light red
    §G - light green
    §Y - light yellow
    §B - light blue
    §M - light magenta
    §C - light cyan
    """

    def __new__(cls, indx, value, label):
        obj = bytes.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    """
    """
    RESET =     (0, '\033[0m', "0")
    BOLD =      (1, '\033[1m', "1")
    ITALIC =    (2, '\033[3m', "3")
    UNDERLINE = (3, '\033[4m', "4")
    GRAY =      (4, '\033[90m', "5")
    RED =       (5, '\033[31m', "r")
    GREEN =     (6, '\033[32m', "g")
    YELLOW =    (7, '\033[33m', "y")
    BLUE =      (8, '\033[34m', "b")
    MAGENTA =   (9, '\033[35m', "m")
    CYAN =      (10, '\033[36m', "c")
    WHITE =     (11, '\033[37m', "w")
    LIGHT_RED =     (12, '\033[91m', "R")
    LIGHT_GREEN =   (13, '\033[92m', "G")
    LIGHT_YELLOW =  (14, '\033[93m', "Y")
    LIGHT_BLUE =    (15, '\033[94m', "B")
    LIGHT_MAGENTA = (16, '\033[95m', "M")
    LIGHT_CYAN =    (17, '\033[96m', "C")
    LIGHT_WHITE =   (18, '\033[97m', "W")

    @staticmethod
    def get_value(label: str) -> str:
        # label = label.lower()
        for color in Color:
            if color.label == label:
                return color.value
