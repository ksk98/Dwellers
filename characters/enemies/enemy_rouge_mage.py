import random

from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_fist import AttackFist
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type


class RogueMage(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Rogue Mage"
        self.type = Type.HUMAN
        self.base_hp = 20
        self.base_energy = 30
        self.strength = 3
        self.attacks = [AttackFire(), AttackFist()]

        self.refresh()

    def act(self, targets: list[Character]) -> str:
        # Smart enough to finish off hurt players, but if none are present the attacks are random
        # Not smart enough to rest often to keep fire damage high
        target_ind = self.get_index_of_weakest_target(targets)
        if targets[target_ind].hp <= 8:
            outcome = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                outcome = self.use_skill_on(self.attacks[1], targets[target_ind])
                if outcome == "":
                    return self.refresh()
        else:
            target_ind = self.get_index_of_random_target(targets)
            outcome = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                outcome = self.use_skill_on(self.attacks[1], targets[target_ind])
                if outcome == "":
                    return self.refresh()

        return outcome
