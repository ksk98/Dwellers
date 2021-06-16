from enum import Enum


# Used to distinguish the room counts.
class RoomType(Enum):
    NONE = 0
    EMPTY = 1
    ENEMY = 2
    TREASURE = 3
