import context
import socket
from network.communication import communicate_and_get_answer, communicate
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
    new_socket.listen(1)
    new_id = context.GAME.get_new_id()
    communicate(sckt, ["200", "PORT:" + str(new_port), "ID:" + str(new_id)])
    connection, addr = new_socket.accept()
    context.GAME.add_socket(connection, new_id)


