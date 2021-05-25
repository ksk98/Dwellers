import socket
import context
import jsonpickle
from network.communication import communicate_and_get_answer


def carry_out(sckt: socket.socket):
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate_and_get_answer(sckt, ["401"])
        return

    if not context.GAME.lobby.has_participant_of_id(sckt):
        communicate_and_get_answer(sckt, ["404"])
        return

    lobby_json = jsonpickle.encode(context.GAME.lobby)
    communicate_and_get_answer(sckt, ["200", "CONTENT-LENGTH:" + str(len(lobby_json))], lobby_json)
