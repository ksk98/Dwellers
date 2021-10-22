import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackSpit(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Acid Spit"
        self.cost = 15
        self.type = Type.FIRE

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = random.randint(6, 13)
        energy_damage_out = random.randint(10, 20)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out)
