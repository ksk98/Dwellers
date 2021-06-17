from abc import ABC


class Character:
    pass


class AttackBase(ABC):
    def __init__(self):
        self.name = "???"
        self.cost = 0

    def use_on(self, user: Character, target: Character):
        pass
