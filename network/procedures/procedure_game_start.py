import socket
import context
import jsonpickle
from network import utility
from network.communication import communicate


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Receive a map object to start a game.
    Returns a log.
    """
    content_length = utility.get_content_length_from_header(frame)

    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate(sckt, ["GAME_START", "STATUS:ERR"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "GAME START REFUSED: NO CONNECTION " \
                                                                   "ESTABLISHED "

    lobby_json = jsonpickle.encode(context.GAME.lobby)
    communicate(sckt, ["200", "CONTENT-LENGTH:" + str(len(lobby_json))], lobby_json)
    return utility.get_ip_and_address_of_client_socket(sckt) + " GAME STARTED"
