from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
import random

from characters.hit import Hit


class AttackHeal(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Heal"
        self.cost = 20
        self.type = Type.HEALING

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = random.randint(-27, -14)
        energy_damage_out = random.randint(-10, 0)
        hit = Hit(target.id, damage_out, self.type, user.name, self.name, energy_damage_out)
        self.send_hit(hit)
        return target.get_hit(damage_out, self.type, user.name, self.name, energy_damage_out)
