import socket
import context
import jsonpickle
from network import utility
from network.communication import communicate


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Pass the lobby to the player.
    Returns a log.
    """
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate(sckt, ["401"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "PLAYER STATUS CHANGE ERROR: NO CONNECTION " \
                                                                   "ESTABLISHED "
    player_status = bool(utility.get_value_of_argument(frame, "READY"))
    participant = context.GAME.lobby.get_participant_of_id(sckt_id)
    participant.ready = player_status
    for client in context.GAME.sockets.values():
        communicate(client, ["LOBBY_UPDATE", "PLAYER_READY", "STATUS:" + str(player_status), "PLAYER_ID:" + str(sckt_id)])

    return utility.get_ip_and_address_of_client_socket(sckt) + " LOBBY OBJECT PASSED"
