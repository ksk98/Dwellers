import random

from characters.attacks.attack_nibble import AttackNibble
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class Bugling(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bugling"
        self.role = "A meat shield."
        self.type = Type.INSECT
        self.stats = {
            STag.STR: 3,
            STag.VIT: 5,
            STag.INT: 1,
            STag.SRD: 1,
            STag.AGL: 1,
            STag.FTN: 1
        }
        self.attacks = [AttackNibble()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
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
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()
            else:
                return outcome, hit
