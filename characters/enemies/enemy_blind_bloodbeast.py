import random

from characters.attacks.attack_maul import AttackMaul
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class BlindBloodbeast(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Blind Bloodbeast"
        self.role = "A ticking bomb that should not be ignored for too long."
        self.type = Type.ABOMINATION
        self.stats = {
            STag.STR: 15,
            STag.VIT: 10,
            STag.INT: 3,
            STag.SRD: 3,
            STag.AGL: 1,
            STag.FTN: 1
        }
        self.roll_boundary = 32
        self.attacks = [AttackMaul()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Ancient bloodbeast that fortunately for the players has become blind
        # It misses a lot at first, but with every turn it's not killed the chance to hit increases
        roll = random.randint(0, self.roll_boundary)
        if roll == 0:
            target_ind = self.get_index_of_random_target(targets)
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()

            return outcome, hit

        self._decrease_boundary()
        if self.roll_boundary <= 4:
            return self.name + " swings dangerously close", None
        else:
            return self.name + " swings at the air", None

    def _decrease_boundary(self):
        self.roll_boundary = int(self.roll_boundary / 2)
        if self.roll_boundary <= 1:
            self.roll_boundary = 2

