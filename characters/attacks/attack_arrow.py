from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackArrow(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Arrow"
        self.use_name = "shot"
        self.cost = 18
        self.type = Type.SLASH
        self.desc = "A powerful slash attack based on strength and agility. Requires some agility to work."
        self.gold_cost = 100

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.STR] * 1.6) - (5 - user.stats[STag.AGL])
        if damage_out < 1:
            damage_out = 0

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
