from characters.character import Character
from characters.enums.enemy_type_enum import EnemyType


class Enemy(Character):
    def __init__(self, e_type: EnemyType):
        super().__init__()
        self._enemy_type = e_type
