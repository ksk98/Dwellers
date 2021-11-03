import random

from characters.attacks.attack_base import AttackBase
from characters.character import Character
from characters.enums.attack_type_enum import Type
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag


class AttackDrinkBlood(AttackBase):
    """
    Made specifically to work with bloodsuckers role. Keep that in mind before reusing the attack.
    """
    def __init__(self):
        super().__init__()
        self.name = "Drink Blood"
        self.use_name = "drank from"
        self.desc = "Bite into your succulent enemy and absorb their life and energy."
        self.cost = 10
        self.type = Type.SLASH

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        damage_out = user.stats[STag.STR]
        user_hp = user.get_base_hp()
        hp_in = random.randint(int(user_hp/2), user_hp)
        energy_damage_out = random.randint(0, 8)

        return target.get_hit(damage=damage_out,
                              user=user,
                              attack=self,
                              energy_damage=energy_damage_out,
                              user_damage=(hp_in * -1))
