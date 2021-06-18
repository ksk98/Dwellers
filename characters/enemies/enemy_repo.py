import random

from characters.enemies.enemy_base import EnemyBase
from characters.enemies.enemy_blind_bloodbeast import BlindBloodbeast
from characters.enemies.enemy_bugling import Bugling
from characters.enemies.enemy_bugling_spitter import BuglingSpitter
from characters.enemies.enemy_dweller import Dweller
from characters.enemies.enemy_ghoul import Ghoul
from characters.enemies.enemy_rouge_mage import RogueMage
from characters.enemies.enemy_skeleton import Skeleton
from characters.enemies.enemy_skeleton_hunter import SkeletonHunter
from characters.enemies.enemy_skeleton_lazy import SkeletonLazy
from characters.enemies.enemy_worshipper import Worshipper


def roll_an_enemy() -> EnemyBase:
    # Chances to roll enemy of a certain difficulty:
    # Easy      20%
    # Medium    45%
    # Hard      30%
    # Very Hard 5%
    chance_roll = random.randint(0, 99)
    if chance_roll in range(0, 20):
        pool = [SkeletonLazy(), Dweller()]
    elif chance_roll in range(20, 65):
        pool = [Skeleton(), RogueMage(), Bugling()]
    elif chance_roll in range(65, 95):
        pool = [SkeletonHunter(), Worshipper(), Ghoul(), BuglingSpitter()]
    else:
        pool = [BlindBloodbeast()]

    ind = random.randint(0, len(pool)-1)
    return pool[ind]


if __name__ == '__main__':
    print(roll_an_enemy().name)
