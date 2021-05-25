from network import procedures
from network.communication import communicate_and_get_answer
import socket


def handle(sckt: socket.socket, frame: str):
    try:
        frame_action = frame.split("\r\n")[0]

        if frame_action == "REQUEST_CONNECTION":
            procedures.procedure_connection.carry_out(sckt)
        elif frame_action == "REQUEST_LOBBY":
            procedures.procedure_get_lobby.carry_out(sckt)
        elif frame_action == "UPLOAD_CHARACTER":
            procedures.procedure_upload_character.carry_out(sckt, frame)
        elif frame_action == "LOBBY_UPDATE":
            procedures.procedure_lobby_update.carry_out(sckt, frame)

        else:
            communicate_and_get_answer(sckt, ["400"])
    except socket.error as e:
        communicate_and_get_answer(sckt, ["500"])
        return "SOCKET ERROR: " + e
