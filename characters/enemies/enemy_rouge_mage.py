from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_fist import AttackFist
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from characters.enums.character_type_enum import Type
from characters.enums.stat_tags_enum import STag
from characters.hit import Hit


class RogueMage(EnemyBase):
    def __init__(self):
        super().__init__()
        self.name = "Rogue Mage"
        self.role = "Hunts players that are hurt."
        self.type = Type.HUMAN
        self.stats = {
            STag.STR: 1,
            STag.VIT: 3,
            STag.INT: 11,
            STag.SRD: 7,
            STag.AGL: 3,
            STag.FTN: 2
        }
        self.attacks = [AttackFire(), AttackFist()]
        self.skip_turn = True

        self.restore()

    def act(self, targets: list[Character]) -> tuple[str, Hit]:
        # Smart enough to finish off hurt players, but if none are present the attacks are random
        # Not smart enough to rest often to keep fire damage high

        if self.skip_turn:
            self.skip_turn = False
            return self.name + " charges up", None

        target_ind = self.get_index_of_weakest_target(targets)
        if targets[target_ind].hp <= 8:
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                outcome, hit = self.use_skill_on(self.attacks[1], targets[target_ind])
                if outcome == "":
                    return self.rest()
        else:
            target_ind = self.get_index_of_random_target(targets)
            outcome, hit = self.use_skill_on(self.attacks[0], targets[target_ind])
            if outcome == "":
                outcome, hit = self.use_skill_on(self.attacks[1], targets[target_ind])
                if outcome == "":
                    return self.rest()

        return outcome, hit
