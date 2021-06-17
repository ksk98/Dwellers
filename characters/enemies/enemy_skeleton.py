import random
from characters.character import Character
from characters.enums.character_type_enum import Type


class Enemy(Character):
    def __init__(self):
        super().__init__()
        self.name = "Skeleton"
        self.type = Type.UNDEAD
        self.base_hp = 25
        self.base_energy = 20
        self.strength = 2
        self.refresh()

    def act(self, targets: list[Character]) -> str:


