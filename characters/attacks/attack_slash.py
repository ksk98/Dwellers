from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackSlash(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Slash"
        self.cost = 5
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character):
        damage_out = user.strength
        target.get_hit(damage_out, self.type, user.name)
