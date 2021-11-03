import random

from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_maul import AttackMaul
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class Ghoul(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Ghoul"
        self.role = "An equalizer that takes care of the healthiest party members."
        self.type = Type.ABOMINATION
        self.stats = {
            STag.STR: 8,
            STag.VIT: 7,
            STag.INT: 2,
            STag.SRD: 1,
            STag.AGL: 2,
            STag.FTN: 1
        }
        self.base_hp = 65
        self.base_energy = 20
        self.strength = 8
        self.attacks = [AttackMaul(), AttackCrush()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Ghouls are tough and hit hard, but they get tired fast
        # They tend to weaken the party by dealing with players with most HP at hand
        target_ind = self.get_index_of_strongest_target(targets)

        attack = random.randint(0, len(self.attacks) - 1)  # -1 byczq
        outcome, hit = self.use_skill_on(self.attacks[attack], targets[target_ind])
        if outcome == "":
            return self.rest()

        return outcome, hit
