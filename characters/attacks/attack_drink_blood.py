from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackDrinkBlood(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Drink Blood"
        self.cost = 10
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = user.strength

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=7,
                              user_damage=-7)
