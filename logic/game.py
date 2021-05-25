from logic.lobby import Lobby
from logic.participant import Participant
import socket
from network import communication
from network import utility
import jsonpickle
from os import name
from config import config
import msvcrt
from network import frame_handler
from views.view_manager import ViewManager
from settings import settings


class Game:
    def __init__(self):
        self.running = True

        self.lobby = None
        self.player_id = -1

        self.host_socket: socket.socket = None
        self.__sockets: dict[int, socket.socket] = {}
        self.__free_id = 0

        self.view_manager: ViewManager = ViewManager()
        self.view_manager.get_current().print_screen()

    def view(self):
        return self.view_manager.get_current()

    def tick(self):
        # Windows
        if name == 'nt':
            # If key is waiting to be read then read it
            if msvcrt.kbhit():
                inp = ord(msvcrt.getch())
                if inp == 13:   # Enter
                    self.view_manager.set_current(self.view().execute_current_option())
                elif inp == 8:  # Backspace
                    if self.view_manager.get_current().typing_mode:
                        self.view_manager.get_current().remove_character_from_current_text_input()
                        self.view_manager.refresh()
                elif inp == 224:  # Special keys that require using getch() a second time
                    inp = ord(msvcrt.getch())
                    if inp == 80:  # Arrowkey Down
                        self.view().scroll_down()
                        self.view().refresh_view()
                    elif inp == 72:  # Arrowkey Up
                        self.view().scroll_up()
                        self.view().refresh_view()
                else:
                    if self.view_manager.get_current().typing_mode:
                        self.view_manager.get_current().add_to_current_text_input(chr(inp))
                        self.view_manager.refresh()

            # TODO: LOGGING
            if self.host_socket is not None:
                frame_handler.handle(self.host_socket, utility.get_data(self.host_socket))
            for sckt in self.__sockets.values():
                frame_handler.handle(sckt, utility.get_data(sckt))

        # Linux/Mac
        else:
            exit(0)
            # TODO: this shouldn't require too much work and is a nice bonus
            # https://stackoverflow.com/questions/6179537/python-wait-x-secs-for-a-key-and-continue-execution-if-not-pressed

    def host_lobby(self, password: str = ""):
        self.lobby = Lobby(password)

        # Create host
        host_participant = Participant(self.get_new_id())
        self.player_id = host_participant.player_id
        self.lobby.add_participant(host_participant)

        # Create host socket that listens for joining players
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_socket.bind((utility.get_host_ip(), settings["HOSTING_PORT"]))
        self.host_socket.settimeout(config["TICK_WAIT_TIME"])

    def join_external_lobby(self, ip: str, port: int, password: str = "") -> str:
        """
        Create a new lobby by joining a hosted lobby.

        :return: error message if unsuccesful (empty string if otherwise)
        """
        # Create a temporary socket and request for address of stable socket connection with host
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.settimeout(config["CONNECTION_TIMEOUT_TIME"])
        try:
            temp_socket.connect((ip, port))
            answer = communication.communicate_and_get_answer(temp_socket, ["REQUEST_CONNECTION"])

            if answer.startswith("409"):
                return "LOBBY FULL"

            if answer.startswith("PASSWORD?"):
                answer = communication.communicate_and_get_answer(temp_socket, [password])

                if answer.startswith("401"):
                    return "WRONG PASSWORD"

            if answer.startswith("500"):
                return "SERVER ERROR"

            if not answer.startswith("200"):
                return "UNKNOWN ERROR"

            # Create new connection from given address
            new_port = utility.get_value_of_argument(answer, "PORT")
            if new_port == "":
                return "CONNECTION RESPONSE INVALID: EMPTY PORT"
            new_id = utility.get_value_of_argument(answer, "ID")
            if new_id == "":
                return "CONNECTION RESPONSE INVALID: EMPTY ID"

            self.player_id = new_id

            host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_socket.settimeout(config["CONNECTION_TIMEOUT_TIME"])
            host_socket.connect((ip, int(new_port)))

            # Get the lobby object from host
            answer = communication.communicate_and_get_answer(host_socket, ["REQUEST_LOBBY"])

            if answer.startswith("500"):
                return "SERVER ERROR"
            elif not answer.startswith("200"):
                return "UNKNOWN ERROR"

            content_length = utility.get_content_length_from_header(answer)
            if content_length == "":
                return "NO CONTENT LENGTH PROVIDED FOR LOBBY OBJECT"

            lobby_object = utility.get_specific_amount_of_data(host_socket, content_length)
            self.lobby = jsonpickle.decode(lobby_object)

            self.__sockets[int(new_id)] = host_socket
            return ""
        except socket.error as e:
            return str(e)

    def add_to_lobby(self, participant):
        """
        This is called when a player from the outside joins the lobby.

        :param participant: object representing the joining player
        """
        if self.lobby is None:
            return False

        self.lobby.add_participant(participant)

        participant_json = jsonpickle.encode(participant)

        for sckt in self.__sockets.values():
            communication.communicate_and_get_answer(sckt,
                                                     ["LOBBY_UPDATE",
                                                      "ACTION:PLAYER_JOINED",
                                                      "CONTENT-LENGTH:" + str(len(participant_json))],
                                                     participant_json)
        return True

    def remove_from_lobby(self, participant):
        """
        This is called when a player from the outside leaves the lobby.

        :param participant: object representing the leaving player
        """
        if self.lobby is None:
            return False

        self.lobby.remove_participant(participant)

        for sckt in self.__sockets.values():
            communication.communicate_and_get_answer(sckt,
                                                     ["LOBBY_UPDATE",
                                                      "ACTION:PLAYER_LEFT",
                                                      "ID:" + participant.player_id])

        return True

    def abandon_lobby(self):
        """
        Player leaves current lobby.

        :return:
        """
        self.lobby = None

        if self.player_id == 0:
            for sckt in self.__sockets.values():
                communication.communicate_and_get_answer(sckt, ["LOBBY_UPDATE", "ACTION:LOBBY_CLOSE"])
                sckt.close()
        else:
            self.host_socket.close()

    def get_new_id(self):
        self.__free_id += 1
        return self.__free_id - 1

    def get_occupied_ports_list(self) -> list[int]:
        ports = []
        for sckt in self.__sockets.values():
            ports.append(sckt.getsockname()[1])

        return ports

    def add_socket(self, sckt: socket.socket) -> int:
        new_id = self.get_new_id()
        self.__sockets[new_id] = sckt
        return new_id

    def get_id_of_socket(self, sckt: socket.socket) -> int:
        if sckt in self.__sockets.values():
            return list(self.__sockets.keys())[list(self.__sockets.values()).index(sckt)]
        return -1

    def close(self):
        self.running = False
