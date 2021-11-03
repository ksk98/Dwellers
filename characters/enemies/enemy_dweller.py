import random

from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_fist import AttackFist
from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class Dweller(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Crazy Dweller"
        self.role = "Slightly entertaining meat shield."
        self.type = Type.HUMAN
        self.stats = {
            STag.STR: 3,
            STag.VIT: 4,
            STag.INT: 2,
            STag.SRD: 3,
            STag.AGL: 2,
            STag.FTN: 2
        }
        self.attacks = [AttackSlash(), AttackCrush(), AttackFist()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Crazy dwellers are adventurers that are no longer capable of logical thinking
        # They tend to act *very* randomly
        target_ind = self.get_index_of_random_target(targets)
        nonsense_roll = random.randint(0, 1)
        if nonsense_roll == 0:
            line = self.name + " yells angrily at " + targets[target_ind].name + " about " + self.get_nonsense()
            return line, None
        else:
            attack = random.randint(0, len(self.attacks) - 1)
            outcome, hit = self.use_skill_on(self.attacks[attack], targets[target_ind])
            if outcome == "":
                return self.rest()

            return outcome, hit

    @staticmethod
    def get_nonsense() -> str:
        nonsense = ["a local racoon comedian", "living in a simulation", "animated images of monkeys",
                    "a fake pandemic", "superiority of the number 8", "cleaning some cutlery"]
        index = random.randint(0, len(nonsense) - 1)
        return nonsense[index]
