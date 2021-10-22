import random

from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.hit import Hit


class Skeleton(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Skeleton"
        self.type = Type.UNDEAD
        self.base_hp = 25
        self.base_energy = 15
        self.strength = 3
        self.attacks = [AttackSlash()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Regular skeleton, likes to casually rest sometimes
        # Picks targets at random
        target_ind = self.get_index_of_random_target(targets)
        roll = random.randint(0, 1)
        if roll == 0:
            if self.energy < self.base_energy:
                return self.rest()
            else:
                return self.use_skill_on(self.attacks[0], targets[target_ind])
        else:
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()
            else:
                return outcome, hit
