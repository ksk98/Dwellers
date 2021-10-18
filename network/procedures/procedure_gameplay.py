import socket

import jsonpickle

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
            context.GAME.go_to_the_next_room()
        return utility.get_ip_and_address_of_client_socket(sckt) + " GOING TO NEXT ROOM "

    elif action == "ATTACK":
        clength = utility.get_content_length_from_header(frame)

        if clength == 0:
            communicate(sckt, ["400"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " HIT RECEIVE ERROR " \
                                                                       "CONTENT LENGTH INDICATES NO BODY"

        body = utility.get_specific_amount_of_data(sckt, clength)
        if body == "":
            communicate(sckt, ["400"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " HIT RECEIVE ERROR " \
                                                                       "NO BODY WAS PROVIDED"

        hit = jsonpickle.decode(body)
        combat = context.GAME.combat
        if combat is not None:
            combat.make_hit(hit)

    elif action == "WIN":
        context.GAME.combat.win()

    elif action == "DEFEAT":
        context.GAME.combat.defeat()

    elif action == "REST":
        if context.GAME.combat is not None:
            id = utility.get_value_of_argument(frame, "ID")
            if context.GAME.combat.get_current_character_id() == int(id):
                context.GAME.combat.rest_current_character()

    elif action == "MISS":
        clength = utility.get_content_length_from_header(frame)

        if clength == 0:
            communicate(sckt, ["400"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " MISS RECEIVE ERROR " \
                                                                       "CONTENT LENGTH INDICATES NO BODY"

        body = utility.get_specific_amount_of_data(sckt, clength)
        if body == "":
            communicate(sckt, ["400"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " MISS RECEIVE ERROR " \
                                                                       "NO BODY WAS PROVIDED"

        hit = jsonpickle.decode(body)
        combat = context.GAME.combat
        if combat is not None:
            id = utility.get_value_of_argument(frame, "ID")
            if context.GAME.combat.get_current_character_id() == int(id):
                combat.current_character_missed(hit)

    elif action == "END":
        context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary())
        context.GAME.view_manager.set_current(Views.SUMMARY)

    return utility.get_ip_and_address_of_client_socket(sckt) + " GAME STARTED"
