# Config related to room contents
# Specifies ranges of RNG
from dungeon.room_type_enum import RoomType

config = {
    RoomType.EMPTY: {
        "enemies_min": 0,
        "enemies_max": 1,
        "gold_min": 0,
        "gold_max": 5
    },
    RoomType.TREASURE: {
        "enemies_min": 0,
        "enemies_max": 2,
        "gold_min": 50,
        "gold_max": 100
    },
    RoomType.ENEMY: {
        "enemies_min": 3,
        "enemies_max": 4,
        "gold_min": 5,
        "gold_max": 20
    }
}
