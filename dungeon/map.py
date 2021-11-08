from random import randint

from dungeon.map_size_enum import MapSize
from dungeon.room import Room
from dungeon.room_type_enum import RoomType


class Map:
    """
    Generates all rooms, holds first
    """
    def __init__(self):
        self.room_count = 0
        self.non_hostile_room_streak = 0
        self._first_room = None

    def generate(self, map_size: MapSize):
        """
        Used to randomize room count and initiate a rooms creation
        :param map_size: Specifies a target size of generated map
        :return:
        """
        if map_size == MapSize.SMALL:
            self.room_count = randint(4, 6)
        elif map_size == MapSize.MEDIUM:
            self.room_count = randint(6, 9)
        elif map_size == MapSize.LARGE:
            self.room_count = randint(10, 15)

        self._first_room = self._create_rooms(self.room_count)

    def _create_rooms(self, count: int) -> Room:
        """
        Creates a specified number of rooms. Rooms are connected to each other in linear graph.
        :param count: Number of rooms to generate.
        :return: First room
        """

        room = None
        for x in range(0, count):
            chance_roll = randint(1 + (self.non_hostile_room_streak * 33), 100)

            # First room has 1% chance to force a fight
            # The fourth room in a row without a prior fight has a 100 percent chance to be a fight
            force_room_with_enemy = True if chance_roll == 100 else False
            new_room = self._create_single_room(force_room_with_enemy)

            # creating graph
            if room is not None:
                new_room.set_next(room)

            # move to the next node
            room = new_room

        return room

    def get_first_room(self) -> Room:
        return self._first_room

    def _create_single_room(self, force_enemy=False) -> Room:
        """
        Creates single room of random type
        :return Created room
        """
        if not force_enemy:
            room_type = randint(1, 3)   # randomize room type
        else:
            room_type = RoomType.ENEMY

        if room_type != RoomType.ENEMY:
            self.non_hostile_room_streak += 1
        else:
            self.non_hostile_room_streak = 0

        # create room instance
        new_room = Room(RoomType(room_type))
        return new_room
