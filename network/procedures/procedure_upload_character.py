import socket
import context
import jsonpickle
from network.communication import communicate
from network import utility


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Add object of player to the lobby.
    Returns a log.
    """
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate(sckt, ["404"])
        return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO UPLOAD CHARACTER BUT " \
                                                                   "SOCKET IS NOT CONNECTED"

    clength = utility.get_content_length_from_header(frame)
    if clength == 0:
        communicate(sckt, ["400"])
        return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO UPLOAD CHARACTER BUT " \
                                                                   "CONTENT LENGTH INDICATES NO BODY"

    body = utility.get_specific_amount_of_data(sckt, clength)
    if body == "":
        communicate(sckt, ["400"])
        return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO UPLOAD CHARACTER BUT " \
                                                                   "NO BODY WAS PROVIDED"

    partcp = jsonpickle.decode(body)

    # TODO: VALIDATE CHARACTER, SEND 409 IF INVALID

    communicate(sckt, ["200"])

    context.GAME.add_to_lobby(partcp)
    return utility.get_ip_and_address_of_client_socket(sckt) + " ADDED TO LOBBY"
