from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.hit import Hit


class SkeletonLazy(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Lazy Skeleton"
        self.type = Type.UNDEAD
        self.base_hp = 15
        self.base_energy = 10
        self.strength = 2
        self.attacks = [AttackSlash()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Lazy boy likes to rest whenever he can
        if self.energy < self.base_energy:
            return self.rest()

        # If at full energy, the lazy boy tends to pick a random target to smack
        target_ind = self.get_index_of_random_target(targets)

        outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
        if outcome == "":
            line = self.name + " could not do anything!"
            return line, None
        else:
            return outcome, hit
