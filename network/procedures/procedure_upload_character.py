import socket
import context
import jsonpickle
from logic import participant
from network.communication import communicate_and_get_answer
from network import utility


def carry_out(sckt: socket.socket, frame: str):
    sckt_id = context.GAME.get_id_of_socket(sckt)
    if sckt_id == -1:
        communicate_and_get_answer(sckt, ["404"])

    clength = utility.get_content_length_from_header(frame)
    if clength == 0:
        communicate_and_get_answer(sckt, ["400"])

    body = utility.get_specific_amount_of_data(sckt, clength)
    if body == "":
        communicate_and_get_answer(sckt, ["400"])

    charct = jsonpickle.decode(body)
    partcp = participant.Participant(sckt_id)

    # TODO: VALIDATE CHARACTER, SEND 409 IF INVALID

    context.GAME.add_to_lobby(partcp)

