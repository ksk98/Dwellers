from characters.character import Character
from characters.character_config import config
from characters.enums.stats_enum import Stat
from characters.saved_characters import saved_characters


class Player(Character):
    def __init__(self, name: str):
        super().__init__()
        if name in saved_characters:
            self.name = name
            self._load_stats(name)
        else:
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
        self.refresh()

    def _load_stats(self, name: str):
        self.base_hp = saved_characters[name][Stat.HEALTH]
        self.base_energy = saved_characters[name][Stat.ENERGY]
        self.strength = saved_characters[name][Stat.STRENGTH]
        self.points = saved_characters[name]["points"]

    def overwrite_stats(self, old_name: str) -> bool:
        if saved_characters.get(old_name):
            saved_characters.pop(old_name)
        saved_characters[self.name] = {
            Stat.HEALTH: self.base_hp,
            Stat.ENERGY: self.base_energy,
            Stat.STRENGTH: self.strength,
            "points": self.points,
        }
        return True

    def save_stats(self):
        saved_characters[self.name] = {
            Stat.HEALTH: self.base_hp,
            Stat.ENERGY: self.base_energy,
            Stat.STRENGTH: self.strength,
            "points": self.points,
        }

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
            # TODO Exception?
            return False

        return True
