from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class SkeletonLazy(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Lazy Skeleton"
        self.role = "A lazy meat shield. Or a bone shield, if you will."
        self.type = Type.UNDEAD
        self.stats = {
            STag.STR: 2,
            STag.VIT: 2,
            STag.INT: 1,
            STag.SRD: 1,
            STag.AGL: 1,
            STag.FTN: 1
        }
        self.attacks = [AttackSlash()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Lazy boy likes to rest whenever he can
        if self.energy < self.get_base_energy():
            return self.rest()

        # If at full energy, the lazy boy tends to pick a random target to smack
        target_ind = self.get_index_of_random_target(targets)

        outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
        if outcome == "":
            line = self.name + " could not do anything!"
            return line, None
        else:
            return outcome, hit
