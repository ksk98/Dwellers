import socket
from distutils.util import strtobool

import jsonpickle

import context
from network import utility
from network.communication import communicate
from views.view_enum import Views


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Update the lobby according to passed message.
    Returns a log.
    """
    action = utility.get_value_of_argument(frame, "ACTION")
    if action == "PLAYER_JOINED":
        clength = utility.get_content_length_from_header(frame)
        if clength == 0:
            return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (clength == 0)"

        body = utility.get_specific_amount_of_data(sckt, clength)
        if not context.GAME.lobby.add_participant(jsonpickle.decode(body)):
            return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (no participant)"

    elif action == "PLAYER_LEFT":
        pid_text = utility.get_value_of_argument(frame, "ID")
        if pid_text == "":
            return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (no ID)"

        if not context.GAME.lobby.has_participant_of_id(int(pid_text)):
            return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (ID not present)"

        if not context.GAME.lobby.remove_participant(int(pid_text)):
            return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (could not remove player)"

    elif action == "LOBBY_CLOSE":
        context.GAME.abandon_lobby()
        context.GAME.view_manager.display_error_and_go_to("Lobby was closed.", Views.MENU)

    elif action == "PLAYER_READY":
        player_status = strtobool(utility.get_value_of_argument(frame, "STATUS"))
        player_id = int(utility.get_value_of_argument(frame, "PLAYER_ID"))
        context.GAME.lobby.get_participant_of_id(player_id).ready = player_status

    else:
        communicate(sckt, ["400"])
        return utility.get_ip_and_address_of_client_socket(sckt) + " BAD UPDATE (no procedure for action " + action + ")"

    context.GAME.view_manager.refresh()
    return utility.get_ip_and_address_of_client_socket(sckt) + " LOBBY UPDATE"
