from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class AttackFire(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Fireball"
        self.use_name = "burned"
        self.desc = "Fire attack that scales with intelligence. Less effective if you're tired."
        self.cost = 24
        self.type = Type.FIRE
        self.gold_cost = 110

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.INT] * 1.8 * (user.energy/user.get_base_energy()))

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self)
