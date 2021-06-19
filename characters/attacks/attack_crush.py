from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackCrush(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Crush"
        self.cost = 10
        self.type = Type.CRUSH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = int(user.strength * 1.5)
        hit = Hit(target.id, damage_out, self.type, user.name, self.name)
        self.send_hit(hit)
        return target.get_hit(damage_out, self.type, user.name, self.name)
