import socket

import jsonpickle

import context
from network import utility
from network.communication import communicate
from views.view_enum import Views


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Receive a map object to start a game.
    Returns a log.
    """
    status = utility.get_value_of_argument(frame, "STATUS")
    sckt_id = context.GAME.get_id_of_socket(sckt)

    if sckt_id == -1 and context.GAME.lobby.local_lobby:
        communicate(sckt, ["GAME_START", "STATUS:ERR"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "GAME START REFUSED: NO CONNECTION " \
                                                                   "ESTABLISHED "
    if status == "INFO":
        clength = utility.get_content_length_from_header(frame)
        if clength == 0:
            communicate(sckt, ["GAME_START", "STATUS:ERR"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO RECEIVE A GAME MAP BUT " \
                                                                       "CONTENT LENGTH INDICATES NO BODY"

        body = utility.get_specific_amount_of_data(sckt, clength)
        if body == "":
            communicate(sckt, ["GAME_START", "STATUS:ERR"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO RECEIVE A GAME MAP BUT " \
                                                                       "NO BODY WAS PROVIDED"

        map_json = jsonpickle.decode(body)

        context.GAME.map = map_json
        communicate(sckt, ["GAME_START", "STATUS:OK"])

    elif status == "OK":
        all_players_ready = True
        context.GAME.lobby.get_participant_of_id(sckt_id).ready = True
        for participant in context.GAME.lobby.participants:
            if participant.ready is False:
                all_players_ready = False
                break
        if all_players_ready:
            for client in context.GAME.sockets.values():
                communicate(client, ["GAME_START", "STATUS:READY"])
            context.GAME.start_game()

    elif status == "ERR":
        context.GAME.sockets[sckt_id].close()
        context.GAME.remove_from_lobby(sckt_id)
        context.GAME.view_manager.display_error_and_go_to("Player reported an error while starting a game.", Views.LOBBY)

    elif status == "READY":
        context.GAME.start_game()

    return utility.get_ip_and_address_of_client_socket(sckt) + " GAME STARTED"
