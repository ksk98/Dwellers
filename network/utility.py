import socket
from config import config
import context
from settings import settings


def get_data(source_socket: socket.socket, delimiter: str = "\r\n\r\n") -> str:
    """
    Read bytes from a socket until a delimiter is met.
    """
    output = b''
    while delimiter.encode("utf-8") not in output:
        incoming = source_socket.recv(1)
        if not incoming:
            break

        output = output + incoming

    output = output.replace(delimiter.encode("utf-8"), b'')
    return output.decode('utf-8')


def get_specific_amount_of_data(source_socket: socket.socket, byte_count: int) -> str:
    """
    Read a given amount of bytes from a socket.
    """
    local_output = b''
    data_received = 0
    while data_received < byte_count:
        incoming = source_socket.recv(1)
        if not incoming:
            break
        data_received += 1
        local_output = local_output + incoming

    return local_output


def get_value_of_argument(header: str, arg_name: str) -> str:
    """
    Extract value of argument from a given header.
    """
    lines = header.splitlines()
    for line in lines:
        if line.startswith(arg_name):
            value = line.replace(arg_name+":", "").lstrip().replace("\r", "").replace("\n", "")
            return value
    return ""


def get_content_length_from_header(header: str) -> int:
    """
    Extract the value of CONTENT-LENGTH from a given header. If
    no value is present, return 0.
    """
    val = get_value_of_argument(header, "CONTENT-LENGTH")
    if val == "":
        return 0
    else:
        return int(val)


def get_content_from_frame(frame: str) -> str:
    """
    Extract content of a frame separated from the header by a double CRLF.
    """
    split = frame.split("\r\n\r\n")
    return split[1]


def is_port_in_use(port):
    """
    https://stackoverflow.com/a/52872579
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_free_port():
    port = config["HIGH_PORTS_BASE"]
    occupied_ports = context.GAME.get_occupied_ports_list().sort()
    if occupied_ports is not None:
        for oport in occupied_ports:
            if port == oport:
                port += 1
            else:
                break

    return port


def get_host_ip():
    if settings["HOST_LOBBY_IS_LAN"]:
        return "localhost"
    return "0.0.0.0"
    # return socket.gethostbyname(socket.gethostname())
