import random

import jsonpickle

import context
from characters.character import Character
from characters.enums.character_type_enum import Type
from network.communication import communicate


class EnemyBase(Character):
    def __init__(self):
        super().__init__()
        self.name = "???"
        self.type = Type.HUMAN
        self.base_hp = 1
        self.base_energy = 1
        self.strength = 1
        self.attacks = []

        self.refresh()

    def send_miss(self, miss: str):
        pickled = jsonpickle.encode(miss)
        headers = ["GAMEPLAY", "ACTION:MISS", "CONTENT-LENGTH:" + str(len(pickled)), "ID:" + str(self.id)]
        if context.GAME.lobby.local_lobby:
            for client in context.GAME.sockets.values():
                communicate(client, headers, pickled)
        else:
            communicate(context.GAME.host_socket, headers, pickled)

    @staticmethod
    def get_index_of_weakest_target(targets: list[Character]) -> int:
        target_ind = 0
        for ind in range(len(targets)):
            if targets[ind].hp < targets[target_ind].hp:
                target_ind = ind

        return target_ind

    @staticmethod
    def get_index_of_strongest_target(targets: list[Character]) -> int:
        target_ind = 0
        for ind in range(len(targets)):
            if targets[ind].hp > targets[target_ind].hp:
                target_ind = ind

        return target_ind

    @staticmethod
    def get_index_of_random_target(targets: list[Character]) -> int:
        return random.randint(0, len(targets) - 1)
