import random

from characters.attacks.attack_bite import AttackBite
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type


class Bugling(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bugling"
        self.type = Type.INSECT
        self.base_hp = 20
        self.base_energy = 15
        self.strength = 3
        self.attacks = [AttackBite()]

        self.refresh()

    def act(self, targets: list[Character]) -> str:
        # Buglings are regular workers of the insect hive
        # Their behavior is pretty random
        target_ind = self.get_index_of_random_target(targets)
        roll = random.randint(0, 1)
        if roll == 0:
            if self.energy < self.base_energy:
                return self.rest()
            else:
                return self.use_skill_on(self.attacks[0], targets[target_ind])
        else:
            outcome = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()
            else:
                return outcome
