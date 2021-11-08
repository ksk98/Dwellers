from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackBatter(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Batter"
        self.use_name = "battered"
        self.desc = "Powerful crush attack based on strength."
        self.cost = 28
        self.type = Type.CRUSH
        self.cost = 170

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.STR] * 2.4)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
