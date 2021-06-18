import socket
import context
from network.communication import communicate
from network.procedures import procedure_goodbye as goodbye
from network.procedures import procedure_get_lobby as get_lobby_procedure
from network.procedures import procedure_connection as connection_procedure
from network.procedures import procedure_game_start as game_start_procedure
from network.procedures import procedure_lobby_update as update_lobby_procedure
from network.procedures import procedure_upload_character as upload_character_procedure
from network.procedures import procedure_lobby_player_status as lobby_player_status_procedure


def handle(sckt: socket.socket, frame: str) -> bool:
    """
    Handle a given frame of data.
    """
    try:
        frame_action = frame.split("\r\n")[0]

        if frame_action == "REQUEST_CONNECTION":
            connection_procedure.carry_out(sckt)
        elif frame_action == "REQUEST_LOBBY":
            get_lobby_procedure.carry_out(sckt)
        elif frame_action == "UPLOAD_CHARACTER":
            upload_character_procedure.carry_out(sckt, frame)
        elif frame_action == "LOBBY_PLAYER_STATUS":
            lobby_player_status_procedure.carry_out(sckt, frame)
        elif frame_action == "LOBBY_UPDATE":
            update_lobby_procedure.carry_out(sckt, frame)
        elif frame_action == "GAME_START":
            game_start_procedure.carry_out(sckt, frame)
        elif frame_action == "GOODBYE":
            goodbye.carry_out(sckt)
        elif frame_action == "IGNORE":
            pass
        else:
            communicate(sckt, ["400"])
            return False

        return True
    except socket.error as e:
        communicate(sckt, ["500"])
        context.GAME.view_manager.display_error_and_return("Socket error: " + str(e))
        return False
