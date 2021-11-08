import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackWhomp(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Whomp"
        self.use_name = "whomped"
        self.desc = "Utility move that deals energy damage based on agility and strength."
        self.cost = 16
        self.type = Type.CRUSH
        self.gold_cost = 70

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = random.randint(0, user.stats[STag.STR])
        energy_damage_out = random.randint(
            user.stats[STag.AGL],
            int((user.stats[STag.STR] + user.stats[STag.AGL]) * 1.5)
        )

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out)
