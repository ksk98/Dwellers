import socket
import context
import jsonpickle
from network import utility
from network.communication import communicate
from views.view_enum import Views


def carry_out(sckt: socket.socket, frame: str):
    action = utility.get_value_of_argument(frame, "ACTION")
    if action == "PLAYER_JOINED":
        clength = utility.get_content_length_from_header(frame)
        if clength == 0:
            return

        body = utility.get_specific_amount_of_data(sckt, clength)
        if not context.GAME.lobby.add_participant(jsonpickle.decode(body)):
            return

        context.GAME.view_manager.refresh()
    elif action == "PLAYER_LEFT":
        pid_text = utility.get_value_of_argument(frame, "ID")
        if pid_text == "":
            return

        if not context.GAME.lobby.has_participant_of_id(int(pid_text)):
            return

        if not context.GAME.lobby.remove_participant(int(pid_text)):
            return

        context.GAME.view_manager.refresh()
    elif action == "LOBBY_CLOSE":
        context.GAME.abandon_lobby()
        context.GAME.view_manager.display_error_and_go_to("Lobby was closed.", Views.MENU)
    else:
        communicate(sckt, ["400"])
        return
