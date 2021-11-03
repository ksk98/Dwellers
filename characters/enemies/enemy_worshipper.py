import random

from characters.attacks.attack_impale import AttackImpale
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class Worshipper(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Worshipper"
        self.role = "Fragile damage dealer with random targeting."
        self.type = Type.HUMAN
        self.stats = {
            STag.STR: 7,
            STag.VIT: 3,
            STag.INT: 2,
            STag.SRD: 10,
            STag.AGL: 5,
            STag.FTN: 2
        }
        self.attacks = [AttackImpale()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Worshippers are glass cannons - easy to kill but very strong in terms of damage output
        # They attack and rest at random (like regular skeletons)
        target_ind = self.get_index_of_random_target(targets)
        roll = random.randint(0, 1)
        if roll == 0:
            if self.energy < self.get_base_energy():
                return self.rest()
            else:
                return self.use_skill_on(self.attacks[0], targets[target_ind])
        else:
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()
            else:
                return outcome, hit
