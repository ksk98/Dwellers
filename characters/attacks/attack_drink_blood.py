from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackDrinkBlood(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Drink Blood"
        self.cost = 10
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = user.strength
        user.deal_damage(-7)
        return target.get_hit(damage_out, self.type, user.name, self.name, 7)