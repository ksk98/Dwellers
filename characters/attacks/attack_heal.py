from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackHeal(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Heal"
        self.cost = 20
        self.type = Type.HEALING

    def use_on(self, user: Character, target: Character):
        damage_out = -20
        target.get_hit(damage_out, self.type, user.name)
