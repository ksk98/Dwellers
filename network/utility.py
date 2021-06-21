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

    return output.decode("utf-8")


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

    return local_output.decode("utf-8")


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


# https://stackoverflow.com/a/52872579
def is_port_in_use(port) -> bool:
    """
    Check if a local port is already occupied.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_free_port() -> int:
    """
    Find and return a free local port.
    """
    port = config["HIGH_PORTS_BASE"]+1
    occupied_ports = context.GAME.get_occupied_ports_list().sort()
    if occupied_ports is not None:
        for oport in occupied_ports:
            if port == oport:
                port += 1
            else:
                break

    return port


def get_hostname():
    """
    Return a valid hostname to use in hosting a lobby.
    """
    if settings["HOST_LOBBY_IS_LAN"]:
        return "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    return s.getsockname()[0]


# https://stackoverflow.com/a/62277798
def is_socket_closed(sock: socket.socket) -> bool:
    """
    Check if a given socket has been closed.
    """
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        sock.settimeout(0.05)
        data = sock.recv(16, socket.MSG_PEEK)
        sock.settimeout(0)
        if len(data) == 0:
            return True
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except socket.error:
        return True
    return False


def get_ip_and_address_of_client_socket(sckt: socket.socket) -> str:
    """
    Get a formatted string of address and port of a socket.
    Ex. 192.168.0.1:5050
    """
    return str(sckt.getsockname()[0]) + ":" + str(sckt.getsockname()[1])
