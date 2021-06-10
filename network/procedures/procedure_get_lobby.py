import socket
import context
import jsonpickle
from network.communication import communicate


def carry_out(sckt: socket.socket):
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate(sckt, ["401"])
        return

    if sckt_id not in context.GAME.sockets:
        communicate(sckt, ["404"])
        return

    lobby_json = jsonpickle.encode(context.GAME.lobby)
    communicate(sckt, ["200", "CONTENT-LENGTH:" + str(len(lobby_json))], lobby_json)
