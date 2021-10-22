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

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.strength * 1.5)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
