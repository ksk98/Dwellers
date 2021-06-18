# Config related to the characters. This includes base stats, upgrade costs etc.
from characters.enums.stats_enum import Stat

config = {
    # PLAYER
    "base": {
        Stat.HEALTH: 50,
        Stat.ENERGY: 20,
        Stat.STRENGTH: 5,
        "points": 10,
        "attack_cost": 5,
        #"rest_efficiency": 10
    },
    "upgrades": {
        Stat.HEALTH: 10,
        Stat.STRENGTH: 1,
        Stat.ENERGY: 2
    }
}
