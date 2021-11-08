import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackFist(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Fist"
        self.use_name = "punched"
        self.desc = "A solid punch to the guts. Deals crush and energy damage."
        self.cost = 8
        self.type = Type.CRUSH
        self.gold_cost = 35

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.STR])
        energy_damage_out = random.randint(
            int(user.stats[STag.STR] * 0.5),
            int((user.stats[STag.STR] + user.stats[STag.AGL]) * 0.7))

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out)
