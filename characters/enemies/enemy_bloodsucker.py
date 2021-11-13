from characters.attacks.attack_nibble import AttackNibble
from characters.attacks.attack_drink_blood import AttackDrinkBlood
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class Bloodsucker(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Bloodsucker"
        self.role = "A decoy that prolongs it's own life and harasses the party."
        self.type = Type.INSECT
        self.stats = {
            STag.STR: 3,
            STag.VIT: 1,
            STag.INT: 2,
            STag.SRD: 1,
            STag.AGL: 2,
            STag.FTN: 2
        }
        self.attacks = [AttackNibble(), AttackDrinkBlood()]

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Bloodsuckers, although pretty weak, tend to prolong their lives by drinking blood of the players
        # They prefer juicy targets that are full of health
        target_ind = self.get_index_of_strongest_target(targets)
        if self.hp < self.get_base_hp():
            outcome, hit = self.use_skill_on(self.attacks[1], targets[target_ind])
            if outcome == "":
                return self.rest()
        else:
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                return self.rest()

        return outcome, hit
