import random

from characters.attacks.attack_bite import AttackBite
from characters.attacks.attack_spit import AttackSpit
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type


class BuglingSpitter(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bugling Spitter"
        self.type = Type.INSECT
        self.base_hp = 25
        self.base_energy = 25
        self.strength = 4
        self.attacks = [AttackBite(), AttackSpit()]

        self.refresh()

    def act(self, targets: list[Character]) -> str:
        # Bugling spitters spit acid that saps energy
        # Their behavior is pretty random
        target_ind = self.get_index_of_random_target(targets)
        attack = random.randint(0, len(self.attacks))
        outcome = self.use_skill_on(self.attacks[attack], targets[target_ind])
        if outcome == "":
            return self.rest()

        return outcome
