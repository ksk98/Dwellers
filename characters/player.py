from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_slash import AttackSlash
from characters.character import Character
from characters.character_config import config
from characters.enums.stat_tags_enum import STag


class Player(Character):
    """
    Class representing player character.
    """
    def __init__(self, name: str):
        super().__init__()
        self.attacks = [AttackSlash(), AttackCrush()]
        self.name = name
        self.points = 0
        self.gold = 0
        self.reset_stats()

    def reset_stats(self):
        """
        Set stats to default.
        """
        self.set_stats_to_default()
        self.points = config["base"]["points"]
        self.restore()

    def upgrade_stat(self, stat: STag) -> bool:
        """
        Upgrade a stat if skill points are available.
        """
        if self.points < 1:
            return False

        self.points -= 1

        if stat not in self.stats:
            return False

        self.stats[stat] += 1

        return True
