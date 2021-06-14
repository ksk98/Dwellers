import socket
import context


def carry_out(sckt: socket.socket):
    context.GAME.remove_from_lobby(context.GAME.get_id_of_socket(sckt))
