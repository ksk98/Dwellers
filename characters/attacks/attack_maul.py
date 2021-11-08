from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackMaul(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Maul"
        self.use_name = "mauled"
        self.desc = "Costly crush attack, scales greatly with strength."
        self.cost = 40
        self.type = Type.CRUSH
        self.gold_cost = 340

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.STR] * 3)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
