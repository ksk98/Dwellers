import socket

import jsonpickle

import context
from logic.client_combat import ClientCombat, end_battle
from network import utility
from network.communication import communicate


def carry_out(sckt: socket.socket, frame: str) -> str:
    """
    Combat procedure
    Returns a log.
    """
    action = utility.get_value_of_argument(frame, "ACTION")
    sckt_id = context.GAME.get_id_of_socket(sckt)

    if sckt_id == -1 and context.GAME.lobby.local_lobby:
        communicate(sckt, ["GAME_START", "STATUS:ERR"])
        return utility.get_ip_and_address_of_client_socket(sckt) + "GAMEPLAY RUINED: NO CONNECTION " \
                                                                   "ESTABLISHED "
    if action == "START":
        player_id = utility.get_value_of_argument(frame, "TURN")

        if player_id == "":
            communicate(context.GAME.host_socket, ["COMBAT", "STATUS:NO_ID"])
            return "EMPTY PLAYER ID WHILE STARTING COMBAT"

        player_id = int(player_id)
        communicate(context.GAME.host_socket, ["COMBAT", "ACTION:START", "STATUS:OK"])
        context.GAME.combat = ClientCombat(player_id)
        context.GAME.combat.start()

    elif action == "ATTACK":
        if context.GAME.lobby.local_lobby:
            user = utility.get_value_of_argument(frame, "USER")
            if user == "":
                return "USER EMPTY"

            target = utility.get_value_of_argument(frame, "TARGET")
            if target == "":
                return "TARGET EMPTY"

            type = utility.get_value_of_argument(frame, "TYPE")
            if type == "":
                return "TYPE EMPTY"

            user = int(user)
            target = int(target)
            outcome, hit, next_id = context.GAME.server_combat.attack(user, target, type)
            context.GAME.server_combat.send_outcome(outcome, hit, next_id, sckt)
            context.GAME.server_combat.act()

    elif action == "NO_ENERGY":
        context.GAME.combat.handle_outcome()

    elif action == "OUTCOME":
        clength = utility.get_content_length_from_header(frame)
        if clength == 0:
            communicate(sckt, ["COMBAT", "ACTION:OUTCOME_RECEIVE", "STATUS:ERR"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO RECEIVE AN OUTCOME BUT " \
                                                                       "CONTENT LENGTH INDICATES NO BODY"

        body = utility.get_specific_amount_of_data(sckt, clength)
        if body == "":
            communicate(sckt, ["COMBAT", "ACTION:OUTCOME_RECEIVE", "STATUS:ERR"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " TRIED TO RECEIVE AN OUTCOME BUT " \
                                                                       "NO BODY WAS PROVIDED"

        outcome, hit, turn_id = jsonpickle.decode(body)

        communicate(sckt, ["COMBAT", "ACTION:OUTCOME_RECEIVE", "STATUS:OK"])
        context.GAME.combat.handle_outcome(turn_id, outcome, hit)

    elif action == "REST":
        user = utility.get_value_of_argument(frame, "USER")
        if user == "":
            return "USER EMPTY"

        outcome, hit, next_id = context.GAME.server_combat.rest(int(user))
        context.GAME.server_combat.send_outcome(outcome, hit, next_id, sckt)

    elif action == "WIN":
        context.GAME.combat.restore_energy()
        communicate(context.GAME.host_socket, ["COMBAT", "ACTION:END_RECEIVE", "STATUS:OK"])
        end_battle(True)

    elif action == "DEFEAT":
        communicate(context.GAME.host_socket, ["COMBAT", "ACTION:END_RECEIVE", "STATUS:OK"])
        end_battle(False)