import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackFist(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Fist"
        self.cost = 5
        self.type = Type.CRUSH

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.strength * 0.5)
        energy_damage_out = random.randint(3, 9)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out)
