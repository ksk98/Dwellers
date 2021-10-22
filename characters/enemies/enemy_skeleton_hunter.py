from characters.attacks.attack_arrow import AttackArrow
from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.hit import Hit


class SkeletonHunter(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Skeleton Hunter"
        self.type = Type.UNDEAD
        self.base_hp = 35
        self.base_energy = 20
        self.strength = 5
        self.attacks = [AttackSlash(), AttackArrow()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Skeleton hunter prioritizes shooting weakest targets, rests only if necessary
        target_ind = self.get_index_of_weakest_target(targets)

        outcome, hit = self.use_skill_on(self.attacks[1], targets[target_ind])
        if outcome == "":
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                outcome, hit = self.rest()

        return outcome, hit
