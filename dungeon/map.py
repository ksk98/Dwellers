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
        self._first_room = None

    def generate(self, map_size: MapSize):
        """
        Used to randomize room count and initiate a rooms creation
        :param map_size: Specifies a target size of generated map
        :return:
        """
        if map_size == MapSize.SMALL:
            self._room_count = randint(3, 5)
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
            new_room = self._create_single_room()

            # creating graph
            if room is not None:
                new_room.set_next(room)

            # move to the next node
            room = new_room

        return room

    def get_first_room(self) -> Room:
        return self._first_room

    @staticmethod
    def _create_single_room() -> Room:
        """
        Creates single room of random type
        :return Created room
        """
        room_type = randint(1, 3)   # randomize room type

        # create room instance
        new_room = Room(RoomType(room_type))
        return new_room
