import context
import socket
from network.communication import communicate_and_get_answer
from network import utility


def carry_out(sckt: socket.socket) -> str:
    if context.GAME.lobby.is_full():
        communicate_and_get_answer(sckt, ["409"])
        return "CONNECTION REFUSED FOR " + sckt.getpeername()[0] + ": LOBBY FULL"

    if context.GAME.lobby.has_password():
        password = communicate_and_get_answer(sckt, ["PASSWORD?"]).split("\r\n")[0]
        if not context.GAME.lobby.try_password(password):
            communicate_and_get_answer(sckt, ["401"])
            return "CONNECTION REFUSED FOR " + sckt.getpeername()[0] + ": WRONG PASSWORD"

    new_port = utility.get_free_port()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.bind((utility.get_host_ip(), new_port))
    new_id = context.GAME.add_socket(new_socket)

    communicate_and_get_answer(sckt, ["200", "PORT:" + new_port, "ID:" + new_id])

