from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackImpale(AttackBase):
    def __init__(self):
        super().__init__()
        self.name = "Impale"
        self.use_name = "impaled"
        self.desc = "Powerful slash/stamina attack based on strength and agility."
        self.cost = 20
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = int(user.stats[STag.STR] * 1.6 + user.stats[STag.AGL] * 1.6)
        energy_damage_out = int(damage_out/3)

        return target.get_hit(damage=damage_out,
                              energy_damage=energy_damage_out,
                              user=user,
                              attack=self)
