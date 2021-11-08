from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackSlash(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Slash"
        self.use_name = "slashed"
        self.desc = "Cheap slash attack based on strength."
        self.cost = 5
        self.type = Type.SLASH
        self.gold_cost = 30

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = user.stats[STag.STR] * 1.15

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
