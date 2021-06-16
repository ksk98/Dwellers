from __future__ import annotations
from characters.enums.stats_enum import Stat
from config import config
from random import randint


class Character:
    """
    Class representing characters of player.
    """
    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.hp = self.energy = self.strength = self.points = 0
        self.reset_stats()

    def reset_stats(self):
        """
        Set stats to default.
        """
        self.hp = config["base"][Stat.HEALTH]
        self.energy = config["base"][Stat.ENERGY]
        self.strength = config["base"][Stat.STRENGTH]
        self.points = config["base"]["points"]

    def upgrade_stat(self, stat: Stat) -> bool:
        """
        Upgrade a stat if skill points are available.
        """
        if self.points < 1:
            return False

        self.points -= 1

        if stat == Stat.HEALTH:
            self.hp += config["upgrades"][stat]
        elif stat == Stat.ENERGY:
            self.energy += config["upgrades"][stat]
        elif stat == Stat.STRENGTH:
            self.strength += config["upgrades"][stat]
        else:
            # TODO Exception?
            return False

        return True

    def attack(self, target: Character) -> bool:
        attack_cost = config["base"]["attack_cost"]

        if self.energy >= attack_cost:
            self.energy -= attack_cost
            # TODO more advanced calculating of attack_value
            attack_value = randint(0, self.strength)
            if target.hp > attack_value:
                target.hp -= attack_value
            else:
                # TODO dead
                target.hp = 0
                pass
            return True

        return False

    def rest(self):
        rest_efficiency = config["base"]["rest_efficiency"]
        self.energy += rest_efficiency
