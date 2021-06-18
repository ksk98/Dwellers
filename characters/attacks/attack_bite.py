from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackBite(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Bite"
        self.cost = 5
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = user.strength
        return target.get_hit(damage_out, self.type, user.name, self.name)
