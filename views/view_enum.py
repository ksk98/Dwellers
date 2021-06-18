from enum import Enum


# Enum of existing views
class Views(Enum):
    MENU = 0
    LOBBY = 1
    JOIN = 2
    JOINING = 3
    ERROR = 4
    SETTINGS = 5
    HOST_PASSWORD = 6
    PLAY = 7
    CHARACTERS = 20
    CHARACTER_POINTS = 21
    CHARACTER_OVERWRITE = 22
    ROOM = 23
    COMBAT = 24

