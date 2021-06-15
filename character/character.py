from config import config


class Character:
    """
    Class representing character of player.
    """
    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.hp = self.energy = self.points = 0
        self.reset_stats()

    def reset_stats(self):
        """
        Set stats to default.
        """
        self.hp = config["base"]["hp"]
        self.energy = config["base"]["energy"]
        self.points = config["base"]["points"]

    def upgrade_stat(self, stat: str) -> bool:
        """
        Upgrade a stat if skill points are available.
        """
        if self.points < 1:
            return False

        self.points -= 1
        self.hp += config["upgrades"][stat]

        return True
