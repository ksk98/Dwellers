import random

from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type


class Skeleton(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Skeleton"
        self.type = Type.UNDEAD
        self.base_hp = 25
        self.base_energy = 15
        self.strength = 3
        self.attacks = [AttackSlash()]

        self.refresh()

    def act(self, targets: list[Character]) -> str:
        # Regular skeleton, likes to causaly rest sometimes
        # Picks targets at random
        target_ind = self.get_index_of_random_target(targets)
        roll = random.randint(0, 1)
        if roll == 0:
            if self.energy < self.base_energy:
                return self.refresh()
            else:
                return self.use_skill_on(self.attacks[0], targets[target_ind])
        else:
            outcome = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.refresh()
            else:
                return outcome
