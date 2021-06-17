from __future__ import annotations

from random import randint

from characters.character_config import config


class Character:
    """
    Class representing characters of player.
    """
    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.hp = self.energy = self.strength = 0

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
