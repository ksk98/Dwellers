from __future__ import annotations

from random import randint

from characters.attacks.attack_base import AttackBase
from characters.character_config import config
from characters.enums.character_type_enum import Type as CharType
from characters.enums.attack_type_enum import Type as AttType


class Character:
    """
    Class representing characters of player.
    """
    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.base_hp = self.base_energy = self.strength = 0
        self.hp = self.energy = 0
        self.name = "KAROLEK, PRZELADUJ TO NA NICK GRACZA JAK BEDZIESZ WCHODZIC DO GRY"
        self.type: CharType = CharType.HUMAN

    # def attack(self, target: Character) -> bool:
    #     attack_cost = config["base"]["attack_cost"]
    #
    #     if self.energy >= attack_cost:
    #         self.energy -= attack_cost
    #         # TODO more advanced calculating of attack_value
    #         attack_value = randint(0, self.strength)
    #         if target.hp > attack_value:
    #             target.hp -= attack_value
    #         else:
    #             # TODO dead
    #             target.hp = 0
    #             pass
    #         return True
    #
    #     return False

    def refresh(self):
        self.hp = self.base_hp
        self.energy = self.base_energy

    def get_hit(self, damage: int, damage_type: AttType, attacker: str, attack: str) -> str:
        if damage_type == AttType.SLASH:
            if self.type == CharType.UNDEAD:
                damage = int(damage/3)
        elif damage_type == AttType.CRUSH:
            if self.type == CharType.UNDEAD:
                damage *= 2
            elif self.type == CharType.ABOMINATION:
                damage = int(damage / 2)
        elif damage_type == AttType.FIRE:
            if self.type == CharType.UNDEAD:
                damage = 0

        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            return self.name + " was killed by " + attacker + "[" + str(damage) + " " + attack + "]"
        if self.hp > self.base_hp:
            self.hp = self.base_hp
            return self.name + " was healed by " + attacker + "[" + str(damage * -1) + " " + attack + "]"

        return self.name + " was attacked by " + attacker + "[" + str(damage) + " " + attack + "]"

    def use_skill_on(self, skill: AttackBase, target: Character) -> str:
        """
        Returns empty string if user has not enough energy.
        """
        if skill.cost > self.energy:
            return ""

        self.energy -= skill.cost
        return skill.use_on(self, target)

    def rest(self) -> str:
        #rest_efficiency = config["base"]["rest_efficiency"]
        rest_efficiency = self.strength * 5
        self.base_energy += rest_efficiency
        return self.name + " rests"
