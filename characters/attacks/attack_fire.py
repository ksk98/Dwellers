from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type


class AttackFire(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Fireball"
        self.cost = 10
        self.type = Type.FIRE

    def use_on(self, user: Character, target: Character):
        damage_out = int(user.energy / 2)
        target.get_hit(damage_out, self.type, user.name)
