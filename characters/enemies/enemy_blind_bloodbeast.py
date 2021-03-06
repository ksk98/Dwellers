import random

from characters.attacks.attack_maul import AttackMaul
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.hit import Hit


class BlindBloodbeast(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Blind BLoodbeast"
        self.type = Type.ABOMINATION
        self.base_hp = 60
        self.base_energy = 60
        self.strength = 15
        self.attacks = [AttackMaul()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Ancient bloodbeast that fortunately for the players has become blind
        # It often misses but can strike a random player down with a single strike
        roll = random.randint(0, 20)
        if roll == 0:
            target_ind = self.get_index_of_random_target(targets)
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()

            return outcome, hit

        line = self.name + " swings at the air"
        return line, None
