from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
import random


class AttackFist(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Fist"
        self.cost = 5
        self.type = Type.CRUSH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = int(user.strength * 0.5)
        energy_damage_out = random.randint(3, 9)
        return target.get_hit(damage_out, self.type, user.name, self.name, energy_damage_out)
