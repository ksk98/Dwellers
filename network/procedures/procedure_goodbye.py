import socket

import context
from network import utility


def carry_out(sckt: socket.socket) -> str:
    """
    Remove player from lobby if he'she said goodbye.
    Returns a log.
    """
    pid = context.GAME.get_id_of_socket(sckt)
    if pid == -1:
        return utility.get_ip_and_address_of_client_socket(sckt) + " SAID GOODBYE, BUT NO PLAYER " \
                                                                   "OF ID " + str(pid) + "EXISTS"
    if not context.GAME.remove_from_lobby(pid):
        return utility.get_ip_and_address_of_client_socket(sckt) + "PLAYER OF ID " + str(pid) + " COULD NOT BE REMOVED"
    return utility.get_ip_and_address_of_client_socket(sckt) + " PLAYER OF ID " + str(pid) + " REMOVED"
