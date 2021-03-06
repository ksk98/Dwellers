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

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = user.strength

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
