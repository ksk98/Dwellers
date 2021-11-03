import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class AttackHeal(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Heal"
        self.use_name = "healed"
        self.cost = 20
        self.type = Type.HEALING

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = random.randint(-27, -14)
        if user is not target:
            energy_damage_out = random.randint(-10, -5)
        else:
            energy_damage_out = 0

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out)
