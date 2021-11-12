import random

from characters.enemies.enemy_base import EnemyBase
from characters.enemies.enemy_blind_bloodbeast import BlindBloodbeast
from characters.enemies.enemy_bloodsucker import Bloodsucker
from characters.enemies.enemy_bugling import Bugling
from characters.enemies.enemy_bugling_spitter import BuglingSpitter
from characters.enemies.enemy_dweller import Dweller
from characters.enemies.enemy_ghoul import Ghoul
from characters.enemies.enemy_rouge_mage import RogueMage
from characters.enemies.enemy_skeleton import Skeleton
from characters.enemies.enemy_skeleton_hunter import SkeletonHunter
from characters.enemies.enemy_skeleton_lazy import SkeletonLazy
from characters.enemies.enemy_worshipper import Worshipper
from characters.enums.difficulty_enum import Difficulty, EnemyTier


def roll_an_enemy_party(difficulty, players: int) -> list[EnemyBase]:
    enemies = []

    chance_roll = random.randint(0, 99)
    for i in range(players):
        if difficulty == Difficulty.EASY:
            if chance_roll < 60:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.WEAK))
            elif chance_roll < 85:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
            else:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.WEAK))
                enemies.append(roll_an_enemy_of_tier(EnemyTier.WEAK))

        elif difficulty == Difficulty.MEDIUM:
            if chance_roll < 50:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
            elif chance_roll < 80:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.WEAK))
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
            elif chance_roll < 95:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
            else:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.STRONG))

        else:
            if chance_roll < 45:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.STRONG))
            elif chance_roll < 75:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.REGULAR))
                enemies.append(roll_an_enemy_of_tier(EnemyTier.STRONG))
            elif chance_roll < 92:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.STRONG))
                enemies.append(roll_an_enemy_of_tier(EnemyTier.STRONG))
            else:
                enemies.append(roll_an_enemy_of_tier(EnemyTier.VERY_STRONG))

    return enemies


# Deprecated
def roll_an_enemy(difficulty) -> EnemyBase:
    # Chances to roll enemy of a certain difficulty:
    # Easy      20%
    # Medium    45%
    # Hard      30%
    # Very Hard 5%
    chance_roll = random.randint(0, 99)
    if chance_roll in range(0, 20):
        return roll_an_enemy_of_tier(EnemyTier.WEAK)
    elif chance_roll in range(20, 65):
        return roll_an_enemy_of_tier(EnemyTier.REGULAR)
    elif chance_roll in range(65, 95):
        return roll_an_enemy_of_tier(EnemyTier.STRONG)
    else:
        return roll_an_enemy_of_tier(EnemyTier.VERY_STRONG)


def roll_an_enemy_of_tier(tier: EnemyTier) -> EnemyBase:
    if tier == EnemyTier.WEAK:
        pool = [SkeletonLazy(), Dweller()]
    elif tier == EnemyTier.REGULAR:
        pool = [Skeleton(), RogueMage(), Bugling(), Bloodsucker()]
    elif tier == EnemyTier.STRONG:
        pool = [SkeletonHunter(), Worshipper(), BuglingSpitter()]
    else:
        pool = [BlindBloodbeast(), Ghoul()]

    ind = random.randint(0, len(pool)-1)
    return pool[ind]
