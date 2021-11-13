from __future__ import annotations

import context
from characters.attacks.attack_base import AttackBase
from characters.enums.attack_type_enum import Type as AttType
from characters.enums.character_type_enum import Type as CharType
from characters.hit import Hit
from characters.enums.stat_tags_enum import STag
from characters.character_config import config


class Character:
    """
    Class representing a character - either player or enemy.
    """

    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.id = -1
        # The base values are a reference on how a regular sunday dweller looks like
        self.stats = {
            # "base_hp": 24 + base,
            # "base_energy": 24 + base,
            STag.STR: 3,
            STag.VIT: 4,
            STag.INT: 2,
            STag.SRD: 1,
            STag.AGL: 2,
            STag.FTN: 2
        }
        self.hp = self.energy = 0
        self.name = "KAROLEK, PRZELADUJ TO NA NICK GRACZA JAK BEDZIESZ WCHODZIC DO GRY"  # XD
        self.type: CharType = CharType.HUMAN
        self.attacks = []

    def act(self, targets: list[Character]) -> str:
        """
        Make a character do something. Used when enemy needs to act during its turn.
        """
        return "Nothing happened..."

    def set_stats_to_default(self):
        self.stats = {
            STag.STR: 1,
            STag.VIT: 1,
            STag.INT: 1,
            STag.SRD: 1,
            STag.AGL: 1,
            STag.FTN: 1
        }

    def deal_damage(self, value: int):
        """
        Deal health damage to character. This only changes the value.
        """
        self.hp -= value
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.get_base_hp():
            self.hp = self.get_base_hp()

    def deal_energy_damage(self, value: int):
        """
        Deal energy damage to character. This only changes the value.
        """
        self.energy -= value
        if self.energy < 0:
            self.energy = 0
        elif self.energy > self.get_base_energy():
            self.energy = self.get_base_energy()

    def get_attack(self, name: str):
        """
        Search for an attack by it's name
        :param name: name of the attack
        :return: attack if found or None
        """
        for attack in self.attacks:
            if attack.name == name:
                return attack
        return None

    def get_hit(self, damage: int,
                user: Character,
                attack: AttackBase,
                energy_damage: int = 0,
                user_damage: int = 0) -> tuple[str, Hit]:
        """
        Final method while executing attack.
        Damage is calculated to it's final value.
        This method dealing damage / energy damage to target and user if necessary,
        takes energy for using attack. Generates string outcome and creates Hit object containing all values that
        might have been modified
        :param damage:          damage that will be dealt to target's hp (can be modified by multipliers)
        :param user:            Character's object
        :param attack:          attack that will be used
        :param energy_damage:   damage that will be dealt to target's energy
        :param user_damage:     damage that will be dealt to user's hp
        :return:    tuple - string containing description of what happened and Hit object containing all modified values
        """

        # Check energy
        if attack.cost > user.energy:
            return "", None

        # Damage can have multiplier when used on certain types of enemies
        damage_type = attack.type
        if damage_type == AttType.SLASH:
            if self.type == CharType.UNDEAD:
                damage = int(damage / 3)
            elif self.type == CharType.INSECT:
                damage = 0
            elif self.type == CharType.HUMAN:
                damage = int(damage * 1.5)
        elif damage_type == AttType.CRUSH:
            if self.type == CharType.UNDEAD:
                damage = int(damage * 1.3)
            elif self.type == CharType.ABOMINATION:
                damage = int(damage / 2)
            elif self.type == CharType.INSECT:
                damage = int(damage * 1.4)
        elif damage_type == AttType.FIRE:
            if self.type == CharType.UNDEAD:
                damage = 0
            elif self.type == CharType.INSECT:
                damage *= 2

        # Create hit object
        hit = Hit(user_id=user.id,
                  energy_cost=attack.cost,
                  target_id=self.id,
                  damage=damage,
                  energy_damage=energy_damage,
                  user_damage=user_damage)

        # Deal damage to target
        self.deal_damage(damage)
        self.deal_energy_damage(energy_damage)
        # and user
        user.deal_damage(user_damage)
        user.deal_energy_damage(attack.cost)

        # Create outcome text
        action = ""
        multiplier = 1
        if self.hp == 0:
            action = "killed"
        elif damage_type == AttType.HEALING:
            action = "healed"
            multiplier = -1
        else:
            action = "attacked"
        return \
            "{target} was {action} by {attacker} with {attack} [DMG: {damage}, Energy DMG: {energy}]".format(
                target=context.GAME.get_participant_name(self),
                action=action,
                attacker=context.GAME.get_participant_name(user),
                attack=attack.name,
                damage=str(damage * multiplier),
                energy=str(energy_damage * multiplier)), \
            hit

    def rest(self) -> (str, Hit):
        """
        Make a character rest for a turn.
        :return:
        """
        # Calculate
        rest_efficiency = self.stats[STag.STR] * 2 + \
                          self.stats[STag.VIT] * 2 + \
                          self.stats[STag.AGL] * 2

        if self.get_base_energy() - self.energy < rest_efficiency:
            rest_efficiency = self.get_base_energy() - self.energy

        # Restore energy
        self.energy += rest_efficiency

        hit = Hit(user_id=self.id,
                  energy_cost=0,
                  target_id=self.id,
                  damage=0,
                  user_damage=0,
                  energy_damage=rest_efficiency * -1)

        return context.GAME.get_participant_name(self) + " rests", hit

    def restore(self):
        """
        Restore characters health and energy to base values.
        """
        self.hp = self.get_base_hp()
        self.energy = self.get_base_energy()

    def use_skill_on(self, skill: AttackBase, target: Character) -> tuple[str, Hit]:
        """
        Returns empty string if user has not enough energy.
        """
        return skill.use_on(self, target)

    def get_base_hp(self):
        return self.stats[STag.VIT] * 6 + config["base"]["starting_hp"]

    def get_base_energy(self):
        return self.stats[STag.STR] * 4 + \
               self.stats[STag.INT] * 2 + \
               self.stats[STag.AGL] * 4 + \
               config["base"]["starting_en"]
