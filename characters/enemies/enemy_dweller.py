import random

from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_fist import AttackFist
from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type


class Dweller(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Crazy Dweller"
        self.type = Type.HUMAN
        self.base_hp = 20
        self.base_energy = 15
        self.strength = 3
        self.attacks = [AttackSlash(), AttackCrush(), AttackFist()]

        self.refresh()

    def act(self, targets: list[Character]) -> str:
        # Crazy dwellers are adventurers that are no longer capable of logical thining
        # They tend to act *very* randomly
        target_ind = self.get_index_of_random_target(targets)
        nonsense_roll = random.randint(0, 1)
        if nonsense_roll == 0:
            line = self.name + " yells angrily at " + targets[target_ind].name + " about " + self.get_nonsense()
            self.send_miss(line)
            return line
        else:
            attack = random.randint(0, len(self.attacks) - 1)
            outcome = self.use_skill_on(self.attacks[attack], targets[target_ind])
            if outcome == "":
                return self.rest()

            return outcome

    @staticmethod
    def get_nonsense() -> str:
        nonsense = ["horses in pajamas", "toddlers eating dynamite", "devilish teddy bears",
                    "monty python jokes", "the superiority of the number 8", "the latest Tool album"]
        index = random.randint(0, len(nonsense) - 1)
        return nonsense[index]
