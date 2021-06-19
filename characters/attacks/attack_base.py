from abc import ABC

import jsonpickle

import context
from characters.hit import Hit
from network.communication import communicate


class Character:
    pass


class AttackBase(ABC):
    def __init__(self):
        self.name = "???"
        self.cost = 0

    def use_on(self, user: Character, target: Character) -> str:
        return ""

    def send_hit(self, hit: Hit):
        pickled_hit = jsonpickle.encode(hit)
        headers = ["GAMEPLAY", "ACTION:ATTACK", "CONTENT-LENGTH:" + str(len(pickled_hit))]
        if context.GAME.lobby.local_lobby:
            for client in context.GAME.sockets.values():
                communicate(client, headers, pickled_hit)
        else:
            communicate(context.GAME.host_socket, headers, pickled_hit)
