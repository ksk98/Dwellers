import random

from characters.character import Character
from characters.enums.character_type_enum import Type


class EnemyBase(Character):
    def __init__(self):
        super().__init__()
        self.name = "???"
        self.type = Type.HUMAN
        self.base_hp = 1
        self.base_energy = 1
        self.strength = 1

        self.restore()

    @staticmethod
    def get_index_of_weakest_target(targets: list[Character]) -> int:
        target_ind = 0
        for ind in range(len(targets)):
            if targets[ind].hp < targets[target_ind].hp:
                target_ind = ind

        return target_ind

    @staticmethod
    def get_index_of_strongest_target(targets: list[Character]) -> int:
        target_ind = 0
        for ind in range(len(targets)):
            if targets[ind].hp > targets[target_ind].hp:
                target_ind = ind

        return target_ind

    @staticmethod
    def get_index_of_random_target(targets: list[Character]) -> int:
        return random.randint(0, len(targets) - 1)
