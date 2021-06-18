import socket
import context
import jsonpickle
from network import utility
from network.communication import communicate
from views.view_enum import Views


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Gameplay procedure
    Returns a log.
    """
    action = utility.get_value_of_argument(frame, "ACTION")
    sckt_id = context.GAME.get_id_of_socket(sckt)

    if sckt_id == -1 and context.GAME.lobby.local_lobby:
        communicate(sckt, ["GAME_START", "STATUS:ERR"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "GAMEPLAY RUINED: NO CONNECTION " \
                                                                   "ESTABLISHED "
    if action == "NEXT_ROOM":
        context.GAME.go_to_the_next_room()
        return utility.get_ip_and_address_of_client_socket(sckt) + " GOING TO NEXT ROOM "

    return utility.get_ip_and_address_of_client_socket(sckt) + " GAME STARTED"
