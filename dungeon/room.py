from random import randint

from dungeon.room_config import config
from dungeon.room_type_enum import RoomType


class Enemy(object):
    pass


class Room:
    def __init__(self, room_type: RoomType):
        self._gold = 0
        self._enemies: list[Enemy] = []
        self._next = None
        self._room_type = room_type
        self.generate_content()

    def to_string(self):
        print("Type:", self._room_type, "Gold:", self._gold, "Enemies:", len(self._enemies), end=' ')
        if self._next is not None:
            print("Next:", self._next.get_type())

    def generate_content(self):
        rand_range_dict = self.get_from_config()    # get a dictionary containing all min / max values

        # Generate enemies
        enemy_count = randint(rand_range_dict["enemies_min"], rand_range_dict["enemies_max"])
        for x in range(0, enemy_count):
            self.add_enemy(Enemy())

        # Generate gold
        self._gold = randint(rand_range_dict["gold_min"], rand_range_dict["gold_max"])

    def get_from_config(self) -> dict:
        values = {
            "enemies_min": config[self._room_type]["enemies_min"],
            "enemies_max": config[self._room_type]["enemies_max"],
            "gold_min": config[self._room_type]["gold_min"],
            "gold_max": config[self._room_type]["gold_max"]
        }
        return values

    def set_next(self, next_room):
        self._next = next_room

    def get_enemies(self) -> list[Enemy]:
        return self._enemies

    def get_type(self) -> RoomType:
        return self._room_type

    def get_next(self):
        return self._next

    def add_enemy(self, enemy: Enemy):
        self._enemies.append(enemy)
