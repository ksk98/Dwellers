from enum import Enum


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class EnemyTier:
    WEAK = 0
    REGULAR = 1
    STRONG = 2
    VERY_STRONG = 3
