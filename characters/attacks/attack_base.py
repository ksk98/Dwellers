from abc import ABC

from characters.enums.attack_type_enum import Type
from characters.hit import Hit


class Character:
    pass


class AttackBase(ABC):
    def __init__(self):
        self.name = "???"
        self.cost = 0
        self.type = Type.SLASH
        self.desc = "The description of the attack... Info about how effective it is or whatever."
        self.gold_cost = 20

    def use_on(self, user: Character, target: Character) -> tuple[str, Hit]:
        """
        Calculates damage and uses target.get_hit()
        :param user: character that is using this attack
        :param target:  character that will be attacked
        :return:    tuple - string containing outcome and hit object containing all values
        """
        return "", None
