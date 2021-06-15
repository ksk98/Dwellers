import socket
import context
import jsonpickle
from network import utility
from network.communication import communicate


def carry_out(sckt: socket.socket) -> str:
    """
    Pass the lobby to the player.
    Returns a log.
    """
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate(sckt, ["401"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "LOBBY OBJECT PASS REFUSED: NO CONNECTION " \
                                                                   "ESTABLISHED "

    lobby_json = jsonpickle.encode(context.GAME.lobby)
    communicate(sckt, ["200", "CONTENT-LENGTH:" + str(len(lobby_json))], lobby_json)
    return utility.get_ip_and_address_of_client_socket(sckt) + " LOBBY OBJECT PASSED"
