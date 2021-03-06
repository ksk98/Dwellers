from characters.attacks.attack_bite import AttackBite
from characters.attacks.attack_drink_blood import AttackDrinkBlood
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.hit import Hit


class Bloodsucker(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bloodsucker"
        self.type = Type.INSECT
        self.base_hp = 25
        self.base_energy = 30
        self.strength = 2
        self.attacks = [AttackBite(), AttackDrinkBlood()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Bloodsuckers, although pretty weak, tend to prolong their lives by drinking blood of the players
        # They prefer juicy targets that are full of health
        target_ind = self.get_index_of_strongest_target(targets)
        if self.hp < self.base_hp:
            outcome, hit = self.use_skill_on(self.attacks[1], targets[target_ind])
            if outcome == "":
                return self.rest()
        else:
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()

        return outcome, hit
