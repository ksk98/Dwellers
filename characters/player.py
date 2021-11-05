from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.character_config import config
from characters.enums.stats_enum import Stat


class Player(Character):
    """
    Class representing player character.
    """
    def __init__(self, name: str):
        super().__init__()
        self.attacks = [AttackSlash(), AttackCrush()]
        self.name = name
        self.base_hp = self.base_energy = self.strength = self.points = 0
        self.reset_stats()

    def reset_stats(self):
        """
        Set stats to default.
        """
        self.base_hp = config["base"][Stat.HEALTH]
        self.base_energy = config["base"][Stat.ENERGY]
        self.strength = config["base"][Stat.STRENGTH]
        self.points = config["base"]["points"]
        self.restore()

    def upgrade_stat(self, stat: Stat) -> bool:
        """
        Upgrade a stat if skill points are available.
        """
        if self.points < 1:
            return False

        self.points -= 1

        if stat == Stat.HEALTH:
            self.base_hp += config["upgrades"][stat]
        elif stat == Stat.ENERGY:
            self.base_energy += config["upgrades"][stat]
        elif stat == Stat.STRENGTH:
            self.strength += config["upgrades"][stat]
        else:
            return False

        return True
