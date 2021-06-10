import select
import threading

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
from views.concrete.view_error import ViewError
from views.view_manager import ViewManager
from settings import settings
from views.view_enum import Views
from views.concrete.view_lobby import ViewLobby
from views.concrete.view_joining import ViewJoining
import time


class Game:
    def __init__(self):
        self.running = True

        self.lobby = None
        self.player_id = -1

        # For client: this is your communication with the host
        # For host: this is a socket you listen on for communication attempts
        self.host_socket: socket.socket = None
        # For host: those are sockets of other players you broadcast info to
        self.__sockets: dict[int, socket.socket] = {}
        self.__free_id = 0

        self.connecter_thread = None

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
                        self.view().delete_letter()
                        self.view().refresh_view()
                elif inp == 224:  # Special keys that require using getch() a second time
                    inp = ord(msvcrt.getch())
                    if inp == 80:  # Arrowkey Down
                        self.view().scroll_down()
                        self.view().refresh_view()
                    elif inp == 72:  # Arrowkey Up
                        self.view().scroll_up()
                        self.view().refresh_view()
                else:
                    if self.view_manager.get_current().typing_mode and chr(inp).isprintable():
                        self.view().write_letter(chr(inp))
                        self.view().refresh_view()

            # TODO: LOGGING
            if self.host_socket is not None:
                ready = select.select([self.host_socket], [], [], 0.05)
                if ready[0]:
                    frame_handler.handle(self.host_socket, utility.get_data(self.host_socket))

                # Copy the dict in case it becomes bigger during iteration causing an exception
                sockets = self.__sockets.copy()
                for sckt in sockets.values():
                    ready = select.select([sckt], [], [], 0.05)
                    if ready[0]:
                        frame_handler.handle(sckt, utility.get_data(sckt))

        # Linux/Mac
        else:
            print("Only windows is supported. :c")
            exit(0)
            # TODO: this shouldn't require too much work and is a nice bonus
            # https://stackoverflow.com/questions/6179537/python-wait-x-secs-for-a-key-and-continue-execution-if-not-pressed

    def connecter(self):
        while True:
            try:
                sckt, addr = self.host_socket.accept()
                frame_handler.handle(sckt, utility.get_data(sckt))
                sckt.close()
            except socket.error:
                pass

    def host_lobby(self, password: str = ""):
        try:
            self.lobby = Lobby(password)
            self.lobby.address = utility.get_host_ip()
            self.lobby.port = settings["HOSTING_PORT"]

            # Create host
            host_participant = Participant(self.get_new_id())
            self.player_id = host_participant.player_id
            self.lobby.add_participant(host_participant)

            # Create host socket that listens for joining players
            self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_socket.bind((utility.get_host_ip(), settings["HOSTING_PORT"]))
            self.host_socket.listen(1)
            # self.host_socket.settimeout(config["TICK_WAIT_TIME"])

            self.view_manager.set_new_view_for_enum(Views.LOBBY, ViewLobby())
            self.connecter_thread = threading.Thread(target=self.connecter, args=())
            self.connecter_thread.start()
        except socket.error as e:
            self.view_manager.display_error(ViewError("Error on creating lobby: " + str(e)))

    def join_external_lobby(self, ip: str, port: int, password: str = "") -> str:
        """
        Create a new lobby by joining a hosted lobby.

        :return: error message if unsuccesful (empty string if otherwise)
        """
        # Create a temporary socket and request for address of stable socket connection with host
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #temp_socket.settimeout(config["CONNECTION_TIMEOUT_TIME"])
        try:
            self.view_manager.display_progress(Views.JOINING, ViewJoining("Initializing connection with " +
                                                                          ip + ":" + str(port) + "..."))

            temp_socket.connect((ip, port))

            self.view_manager.display_progress(Views.JOINING, ViewJoining("Requesting socket info..."))
            answer = communication.communicate_and_get_answer(temp_socket, ["REQUEST_CONNECTION"])

            if answer.startswith("409"):
                return "LOBBY FULL"

            if answer.startswith("PASSWORD?"):
                answer = communication.communicate_and_get_answer(temp_socket, [password])
                # TODO: ADD PROMPT FOR PASSWORD

                if answer.startswith("401"):
                    return "WRONG PASSWORD"

            if answer.startswith("500"):
                return "SERVER ERROR"

            if not answer.startswith("200"):
                return "UNKNOWN ERROR"

            self.view_manager.display_progress(Views.JOINING, ViewJoining("Establishing connection..."))

            # Create new connection from given address
            new_port = utility.get_value_of_argument(answer, "PORT")
            if new_port == "":
                return "CONNECTION RESPONSE INVALID: EMPTY PORT"
            new_id = utility.get_value_of_argument(answer, "ID")
            if new_id == "":
                return "CONNECTION RESPONSE INVALID: EMPTY ID"

            self.player_id = int(new_id)

            self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.host_socket.settimeout(config["CONNECTION_TIMEOUT_TIME"])
            self.host_socket.connect((ip, int(new_port)))

            self.view_manager.display_progress(Views.JOINING, ViewJoining("Synchronizing..."))

            # Get the lobby object from host
            answer = communication.communicate_and_get_answer(self.host_socket, ["REQUEST_LOBBY"])

            if answer.startswith("500"):
                return "SERVER ERROR"
            elif not answer.startswith("200"):
                return "UNKNOWN ERROR"

            content_length = utility.get_content_length_from_header(answer)
            if content_length == "":
                return "NO CONTENT LENGTH PROVIDED FOR LOBBY OBJECT"

            lobby_object = utility.get_specific_amount_of_data(self.host_socket, content_length)
            self.lobby = jsonpickle.decode(lobby_object)

            self.__sockets[int(new_id)] = self.host_socket
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

        self.view_manager.remove_view_for_enum(Views.LOBBY)
        self.__free_id = 0

        if self.player_id == 0:
            for sckt in self.__sockets.values():
                communication.communicate_and_get_answer(sckt, ["LOBBY_UPDATE", "ACTION:LOBBY_CLOSE"])
                sckt.close()
            self.__sockets.clear()
            self.connecter_thread.join()
        else:
            self.host_socket.close()

        self.host_socket = None

    def get_new_id(self):
        self.__free_id += 1
        return self.__free_id - 1

    def get_occupied_ports_list(self) -> list[int]:
        ports = []
        for sckt in self.__sockets.values():
            ports.append(sckt.getsockname()[1])

        return ports

    def add_socket(self, sckt: socket.socket, new_id: int):
        self.__sockets[new_id] = sckt

    def get_id_of_socket(self, sckt: socket.socket) -> int:
        if sckt in self.__sockets.values():
            return list(self.__sockets.keys())[list(self.__sockets.values()).index(sckt)]
        return -1

    def close(self):
        self.running = False
