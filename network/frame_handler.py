from network.procedures import procedure_connection as connection_procedure
from network.procedures import procedure_get_lobby as get_lobby_procedure
from network.procedures import procedure_lobby_update as update_lobby_procedure
from network.procedures import procedure_upload_character as upload_character_procedure
from network.communication import communicate_and_get_answer
import socket


def handle(sckt: socket.socket, frame: str):
    try:
        frame_action = frame.split("\r\n")[0]

        if frame_action == "REQUEST_CONNECTION":
            connection_procedure.carry_out(sckt)
        elif frame_action == "REQUEST_LOBBY":
            get_lobby_procedure.carry_out(sckt)
        elif frame_action == "UPLOAD_CHARACTER":
            upload_character_procedure.carry_out(sckt, frame)
        elif frame_action == "LOBBY_UPDATE":
            update_lobby_procedure.carry_out(sckt, frame)

        else:
            communicate_and_get_answer(sckt, ["400"])
    except socket.error as e:
        communicate_and_get_answer(sckt, ["500"])
        return "SOCKET ERROR: " + str(e)
