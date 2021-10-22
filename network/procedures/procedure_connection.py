import socket

import context
from network import utility
from network.communication import communicate_and_get_answer, communicate


def carry_out(sckt: socket.socket) -> str:
    """
    Carry out the connection procedure.
    Returns a log.
    """
    if context.GAME.lobby.is_full():
        communicate_and_get_answer(sckt, ["409"])
        return utility.get_ip_and_address_of_client_socket(sckt) + " CONNECTION REFUSED: LOBBY FULL"

    if context.GAME.lobby.has_password():
        password = communicate_and_get_answer(sckt, ["PASSWORD?"]).split("\r\n")[0]
        if not context.GAME.lobby.try_password(password):
            communicate_and_get_answer(sckt, ["401"])
            return utility.get_ip_and_address_of_client_socket(sckt) + " CONNECTION REFUSED: WRONG PASSWORD"

    # Establish new connection for player
    new_port = utility.get_free_port()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.bind((utility.get_hostname(), new_port))
    new_socket.listen(1)

    # Assign new ID for the socket and pass it to the player
    new_id = context.GAME.get_new_id()
    communicate(sckt, ["200", "PORT:" + str(new_port), "ID:" + str(new_id)])
    connection, addr = new_socket.accept()
    context.GAME.add_socket(connection, new_id)
    return utility.get_ip_and_address_of_client_socket(sckt) + " CONNECTION ESTABLISHED"
