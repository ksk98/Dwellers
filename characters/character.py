from __future__ import annotations

import context
from characters.attacks.attack_base import AttackBase
from characters.enums.attack_type_enum import Type as AttType
from characters.enums.character_type_enum import Type as CharType
from network.communication import communicate


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

    def act(self, targets: list[Character]) -> str:
        return "Nothing happened..."

    def refresh(self):
        self.hp = self.base_hp
        self.energy = self.base_energy

    def get_hit(self, damage: int, damage_type: AttType, attacker: str, attack: str, energy_damage: int = 0) -> str:
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

        self.deal_damage(damage)
        self.deal_energy_damage(energy_damage)

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
        return "{target} was {action} by {attacker} with {attack} [DMG: {damage}, Energy DMG: {energy}]" \
            .format(
            target=self.name,
            action=action,
            attacker=attacker,
            attack=attack,
            damage=str(damage * multiplier),
            energy=str(energy_damage * multiplier))

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

    def use_skill_on(self, skill: AttackBase, target: Character) -> str:
        """
        Returns empty string if user has not enough energy.
        """
        if skill.cost > self.energy:
            return ""

        self.energy -= skill.cost
        return skill.use_on(self, target)

    def rest(self, send: bool = True) -> str:
        if send:
            if context.GAME.lobby.local_lobby:
                for client in context.GAME.sockets.values():
                    communicate(client, ["GAMEPLAY", "ACTION:REST", "ID:" + str(self.id)])
            else:
                communicate(context.GAME.host_socket, ["GAMEPLAY", "ACTION:REST", "ID:" + str(self.id)])
        rest_efficiency = self.strength * 5
        self.energy += rest_efficiency
        if self.energy > self.base_energy:
            self.energy = self.base_energy
        return self.name + " rests"
