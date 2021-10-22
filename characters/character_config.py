# Config related to the characters. This includes base stats, upgrade costs etc.
from characters.enums.stats_enum import Stat

config = {
    # PLAYER
    "base": {
        Stat.HEALTH: 50,
        Stat.ENERGY: 20,
        Stat.STRENGTH: 5,
        "points": 5,
    },
    "upgrades": {
        Stat.HEALTH: 8,
        Stat.STRENGTH: 1,
        Stat.ENERGY: 5
    }
}
