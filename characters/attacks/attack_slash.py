from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackSlash(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Slash"
        self.cost = 5
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = user.strength
        hit = Hit(target.id, damage_out, self.type, user.name, self.name)
        self.send_hit(hit)
        return target.get_hit(damage_out, self.type, user.name, self.name)
