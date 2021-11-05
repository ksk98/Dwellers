import random

from characters.attacks.attack_nibble import AttackNibble
from characters.attacks.attack_spit import AttackSpit
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class BuglingSpitter(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bugling Spitter"
        self.role = "Randomly acting, energy sapping meat shield."
        self.type = Type.INSECT
        self.stats = {
            STag.STR: 3,
            STag.VIT: 2,
            STag.INT: 1,
            STag.SRD: 1,
            STag.AGL: 2,
            STag.FTN: 1
        }
        self.attacks = [AttackNibble(), AttackSpit()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Bugling spitters spit acid that saps energy
        # Their behavior is pretty random
        target_ind = self.get_index_of_random_target(targets)
        attack = random.randint(0, len(self.attacks) - 1)
        outcome, hit = self.use_skill_on(self.attacks[attack], targets[target_ind])
        if outcome == "":
            return self.rest()

        return outcome, hit
