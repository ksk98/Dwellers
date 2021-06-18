from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackMaul(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Maul"
        self.cost = 20
        self.type = Type.CRUSH

    def use_on(self, user: Character, target: Character) -> str:
        damage_out = int(user.strength * 2)
        return target.get_hit(damage_out, self.type, user.name, self.name)
