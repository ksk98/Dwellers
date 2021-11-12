from random import randint

import context
from characters.enemies.enemy_repo import *
from dungeon.room_config import config
from dungeon.room_type_enum import RoomType


class Room:
    def __init__(self, room_type: RoomType, difficulty: Difficulty):
        self.gold_added = False
        self._gold = 0
        self._enemies: list[EnemyBase] = []
        self._next = None
        self._room_type: RoomType = room_type
        self._generate_content(difficulty)

    # public

    def clear_enemies(self):
        """
        Deletes all enemies in this room
        """
        self._enemies = []

    def has_next(self) -> bool:
        """
        Return true when this isn't the last room in the dungeon
        """
        if self._next is None:
            return False
        return True

    def set_next(self, next_room):
        """
        Sets the room after this one
        :param next_room: room to set as next
        """
        self._next = next_room

    # getters

    def get_enemies(self) -> list[EnemyBase]:
        """
        Returns the list of enemies in this room
        :return: list of enemies
        """
        return self._enemies

    def get_from_config(self) -> dict:
        """
        Loads values from config file
        """
        values = {
            "enemies_min": config[self._room_type]["enemies_min"],
            "enemies_max": config[self._room_type]["enemies_max"],
            "gold_min": config[self._room_type]["gold_min"],
            "gold_max": config[self._room_type]["gold_max"]
        }
        return values

    def get_gold(self) -> int:
        return self._gold

    def get_next(self):
        return self._next

    def get_type(self) -> RoomType:
        return self._room_type

    # private

    def _add_enemy(self, enemy: EnemyBase):
        """
        Adds enemy to the current room
        :param enemy: character object
        """
        self._enemies.append(enemy)

    # TODO: connect difficulty from somewhere, defaulting to an easy difficulty for now
    def _generate_content(self, difficulty=Difficulty.EASY):
        """
        Adds random amount of enemies and gold to the room
        """
        rand_range_dict = self.get_from_config()    # get a dictionary containing all min / max values

        gold_base = randint(rand_range_dict["gold_min"], rand_range_dict["gold_max"])
        if difficulty == Difficulty.EASY:
            self._gold = gold_base * 0.5
        elif difficulty == Difficulty.MEDIUM:
            self._gold = gold_base
        else:
            self._gold = gold_base * 1.25

        if self._room_type == RoomType.ENEMY:
            self._enemies = roll_an_enemy_party(difficulty, len(context.GAME.get_players()))
            for x in range(0, len(self._enemies)):
                self._enemies[x].id = x + 100
