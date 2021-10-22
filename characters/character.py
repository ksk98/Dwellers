from __future__ import annotations

from characters.attacks.attack_base import AttackBase
from characters.enums.attack_type_enum import Type as AttType
from characters.enums.character_type_enum import Type as CharType
from characters.hit import Hit


class Character:
    """
    Class representing characters of player.
    """

    def __init__(self):
        # If I don't do this, pycharm yells at me
        # for not setting the variables in the constructor >:C
        self.id = -1
        self.base_hp = self.base_energy = self.strength = 0
        self.hp = self.energy = 0
        self.name = "KAROLEK, PRZELADUJ TO NA NICK GRACZA JAK BEDZIESZ WCHODZIC DO GRY"  # XD
        self.type: CharType = CharType.HUMAN
        self.attacks = []

    def act(self, targets: list[Character]) -> str:
        return "Nothing happened..."

    def deal_damage(self, value: int):
        self.hp -= value
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.base_hp:
            self.hp = self.base_hp

    def deal_energy_damage(self, value: int):
        self.energy -= value
        if self.energy < 0:
            self.energy = 0
        elif self.energy > self.base_energy:
            self.energy = self.base_energy

    def get_attack(self, type: str):
        for attack in self.attacks:
            if attack.name == type:
                return attack
        return None

    def get_hit(self, damage: int,
                user: Character,
                attack: AttackBase,
                energy_damage: int = 0,
                user_damage: int = 0) -> tuple[str, Hit]:

        # Take energy
        if attack.cost > user.energy:
            return "", None

        damage_type = attack.type
        if damage_type == AttType.SLASH:
            if self.type == CharType.UNDEAD:
                damage = int(damage / 3)
            if self.type == CharType.INSECT:
                damage = 0
        elif damage_type == AttType.CRUSH:
            if self.type == CharType.UNDEAD:
                damage *= 2
            elif self.type == CharType.ABOMINATION:
                damage = int(damage / 2)
            elif self.type == CharType.INSECT:
                damage = int(damage * 1.5)
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
                  energy_damage=energy_damage)

        # Deal damage
        self.deal_damage(damage)
        self.deal_energy_damage(energy_damage)
        user.take_energy(attack.cost)
        user.deal_damage(user_damage)

        # Create outcome text
        action = ""
        multiplier = 1  # TODO decide - is it necessary? DMG: -20 looks weird...
        if self.hp == 0:
            action = "killed"
        elif damage_type == AttType.HEALING:
            action = "healed"
            inverse = -1
        else:
            action = "attacked"
        return \
            "{target} was {action} by {attacker} with {attack} [DMG: {damage}, Energy DMG: {energy}]".format(
                target=self.name,
                action=action,
                attacker=user.name,
                attack=attack.name,
                damage=str(damage * multiplier),
                energy=str(energy_damage * multiplier)), \
            hit

    def rest(self) -> (str, Hit):
        # Calculate
        rest_efficiency = self.strength * 5

        if self.base_energy - self.energy < rest_efficiency:
            rest_efficiency = self.base_energy - self.energy

        # Restore energy
        self.energy += rest_efficiency

        hit = Hit(user_id=self.id,
                  energy_cost=0,
                  target_id=self.id,
                  damage=0,
                  user_damage=0,
                  energy_damage=rest_efficiency * -1)

        return self.name + " rests", hit

    def restore(self):
        self.hp = self.base_hp
        self.energy = self.base_energy

    def take_energy(self, value: int):
        self.energy -= value
        if self.energy < 0:
            self.energy = 0
        elif self.energy > self.base_hp:
            self.energy = self.base_hp

    def use_skill_on(self, skill: AttackBase, target: Character) -> tuple[str, Hit]:
        """
        Returns empty string if user has not enough energy.
        """
        return skill.use_on(self, target)
