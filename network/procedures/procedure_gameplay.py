import socket

import context
from network import utility
from network.communication import communicate
from views.concrete.view_game_summary import ViewGameSummary
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
        if context.GAME.combat is None:
            communicate(context.GAME.host_socket, ["GAMEPLAY", "ACTION:NEXT_ROOM", "STATUS:OK"])
            context.GAME.go_to_the_next_room()
        return utility.get_ip_and_address_of_client_socket(sckt) + " GOING TO NEXT ROOM "

    elif action == "DUNGEON_END":
        take = utility.get_value_of_argument(frame, "TAKE")
        host_take = utility.get_value_of_argument(frame, "HOST_TAKE")

        if take == "" and host_take == "":
            communicate(context.GAME.host_socket, ["GAMEPLAY", "ACTION:DUNGEON_END", "STATUS:ERR"])

        take = float(take)
        host_take = float(host_take)
        communicate(context.GAME.host_socket, ["GAMEPLAY", "ACTION:DUNGEON_END", "STATUS:OK"])
        context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary(take, host_take))
        context.GAME.view_manager.set_current(Views.SUMMARY)

    return utility.get_ip_and_address_of_client_socket(sckt) + " GAME STARTED"
