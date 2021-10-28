import msvcrt
import select
import socket
import threading
from os import name

import jsonpickle

from characters.player import Player
from config import config
from dungeon.map import Map
from dungeon.map_size_enum import MapSize
from dungeon.room import Room
from logic.client_combat import ClientCombat
from logic.lobby import Lobby
from logic.participant import Participant
from logic.server_combat import ServerCombat
from network import communication
from network import frame_handler
from network import utility
from settings import settings
from views.concrete.view_joining import ViewJoining
from views.concrete.view_lobby import ViewLobby
from views.concrete.view_room import ViewRoom
from views.view_enum import Views
from views.view_manager import ViewManager


class Game:
    """
    Main Game instance that holds everything together.
    """
    def __init__(self):
        # On False, the game will end
        self.running: bool = True

        # Lobby object alongside with id of local player
        # If id is 0, the player is a host of a lobby
        self.lobby = None
        # self.player_id: int = -1

        # For client: this is your communication with the host
        # For host: this is a socket you listen on for communication attempts
        self.host_socket: socket.socket = None

        # For host: those are sockets of other players you broadcast info to
        # Key - ID of player
        # Value - socket of player
        self.sockets: dict[int, socket.socket] = {}

        # This is the next available ID number for a hosted lobby
        self.__next_free_id: int = 0

        # This thread handles incoming connection attempts for the host
        self.connector_thread: threading.Thread = None

        # Instance of the view manager
        self.view_manager: ViewManager = ViewManager()

        # Instance of map object
        self.map: Map = None

        # Instance of current room
        self.current_room: Room = None

        # Instance of current combat
        self.combat: ClientCombat = None

        # Instance of server combat - only for host
        self.server_combat: ServerCombat = None

        # Collected gold
        self.total_gold = 0

        # Gold amount for one dungeon run
        self.tmp_gold = 0

        # Number of defeated creatures in current run
        self.defeated_creatures = 0

    def view(self):
        """
        A shorter way to reach self.view_manager.get_current().
        :return:
        """
        return self.view_manager.get_current()

    def tick(self):
        """
        Check for keyboard and network input and handle it accordingly. This function also handles unexpected
        socket disconnects.
        :return:
        """
        try:
            # Windows
            if name == 'nt':
                # If key is waiting to be read then read it
                if msvcrt.kbhit():
                    inp = ord(msvcrt.getch())
                    if inp == 13:               # Enter
                        self.view_manager.set_current(self.view().execute_current_option())
                    elif inp == 8:              # Backspace
                        if self.view_manager.get_current().typing_mode:
                            self.view().delete_letter()
                            self.view().refresh_view()
                    elif inp == 224:            # Special keys that require using getch() a second time
                        inp = ord(msvcrt.getch())
                        if inp == 80:           # Arrowkey Down
                            self.view().scroll_down()
                            self.view().refresh_view()
                        elif inp == 72:         # Arrowkey Up
                            self.view().scroll_up()
                            self.view().refresh_view()
                    else:                       # Anything the user types in. Currently no support for utf-8 characters.
                        if self.view_manager.get_current().typing_mode and chr(inp).isprintable():
                            self.view().write_letter(chr(inp))
                            self.view().refresh_view()

                # Don't handle socket input in the menu
                if self.host_socket is not None:
                    # If data is incoming pass it to the handler
                    ready = select.select([self.host_socket], [], [], 0.01)
                    if ready[0]:
                        frame_handler.handle(self.host_socket, utility.get_data(self.host_socket))

                    # Copy the dict in case it changes size during iteration, causing an exception
                    sockets = self.sockets.copy()
                    for sckt in sockets.values():
                        ready = select.select([sckt], [], [], 0.05)
                        if ready[0]:
                            frame_handler.handle(sckt, utility.get_data(sckt))

            # Linux/Mac
            else:
                print("Only windows is supported. :c")
                exit(0)
                # TODO: this shouldn't require too much work and is a nice bonus, no time for this now though
                # https://stackoverflow.com/questions/6179537/python-wait-x-secs-for-a-key-and-continue-execution-if-not-pressed
        except socket.error as e:
            # If the player is not a host and we are here, check if the host socket isn't closed
            if not self.is_local() and utility.is_socket_closed(self.host_socket):
                self.abandon_lobby()
                self.view_manager.display_error_and_go_to("Lobby was closed.", Views.MENU)
            # If socket close induced exception is caught, check who disconnected and remove him/her from the lobby
            dict_copy = self.sockets.copy()
            for pid in dict_copy.keys():
                if utility.is_socket_closed(self.sockets[pid]):
                    self.remove_from_lobby(pid)

    def connector(self):
        """
        Handle connection requests. Used in an external thread.
        :return:
        """
        while self.lobby is not None and self.map is None:
            try:
                sckt, addr = self.host_socket.accept()
                frame_handler.handle(sckt, utility.get_data(sckt))
                sckt.close()
            except socket.error:
                pass

    def host_lobby(self, password: str = ""):
        """
        Create a new lobby.
        """
        try:
            self.lobby = Lobby(password)
            self.lobby.address = utility.get_hostname()
            self.lobby.port = settings["HOSTING_PORT"]

            # Create player for host
            host_participant = Participant(self.get_new_id())
            self.lobby.local_player_id = host_participant.player_id
            self.lobby.add_participant(host_participant)

            # Create host socket that listens for joining players
            self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_socket.bind((utility.get_hostname(), settings["HOSTING_PORT"]))
            self.host_socket.listen(1)

            # Start the thread listening for connection requests
            self.view_manager.set_new_view_for_enum(Views.LOBBY, ViewLobby())
            self.connector_thread = threading.Thread(target=self.connector, args=())
            self.connector_thread.start()
        except socket.error as e:
            self.view_manager.display_error_and_go_to("Error on creating lobby: " + str(e))
            self.abandon_lobby()

    def close_connector_thread(self):
        # To stop the thread that listens for connection attempts we have to connect to it once
        if self.connector_thread is not None:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.connect((utility.get_hostname(), settings["HOSTING_PORT"]))
            temp_socket.sendall("IGNORE\r\n\r\n".encode("utf-8"))
            temp_socket.close()
            self.connector_thread.join()
            self.connector_thread = None

    def join_external_lobby(self, ip: str, port: int, password: str = "") -> str:
        """
        Create a new lobby by joining an external lobby.
        :return: error message if unsuccesful (empty string otherwise)
        """
        # Create a temporary socket and request for address of stable socket connection with host
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.settimeout(config["CONNECTION_TIMEOUT_TIME"])
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

            self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_socket.connect((ip, int(new_port)))

            self.view_manager.display_progress(Views.JOINING, ViewJoining("Synchronizing lobby..."))

            # Get the lobby object from host
            answer = communication.communicate_and_get_answer(self.host_socket, ["REQUEST_LOBBY"])

            if answer.startswith("500"):
                return "SERVER ERROR"
            elif not answer.startswith("200"):
                return "UNKNOWN ERROR: " + answer

            lobby_object = utility.get_content_from_frame(answer)
            self.lobby = jsonpickle.decode(lobby_object)
            self.lobby.local_lobby = False
            self.lobby.local_player_id = int(new_id)

            # Send instance of player to the host
            self.view_manager.display_progress(Views.JOINING, ViewJoining("Synchronizing character..."))
            player_character = Participant(int(new_id))
            player_character_json = jsonpickle.encode(player_character)

            answer = communication.communicate_and_get_answer(self.host_socket,
                                                              ["UPLOAD_CHARACTER",
                                                               "CONTENT-LENGTH:" +
                                                               str(len(str(player_character_json)))],
                                                              player_character_json)

            if not answer.startswith("200"):
                return "CHARACTER UPLOAD FAILED"

            return ""
        except socket.timeout:
            return "TIMED OUT"
        except socket.error as e:
            return str(e)

    def add_to_lobby(self, participant) -> bool:
        """
        This is called when a player from the outside joins the lobby.
        """
        if self.lobby is None:
            return False

        self.lobby.add_participant(participant)
        participant_json = jsonpickle.encode(participant)

        for sckt in self.sockets.values():
            communication.communicate(sckt,
                                      ["LOBBY_UPDATE",
                                       "ACTION:PLAYER_JOINED",
                                       "CONTENT-LENGTH:" + str(len(participant_json))],
                                      participant_json)

        self.view_manager.refresh()
        return True

    def remove_from_lobby(self, player_id: int) -> bool:
        """
        This is called when a player from the outside leaves the lobby.
        """
        if self.lobby is None:
            return False

        if not self.lobby.remove_participant(player_id) or not self.remove_socket(player_id):
            return False

        for sckt in self.sockets.values():
            communication.communicate(sckt,
                                      ["LOBBY_UPDATE",
                                       "ACTION:PLAYER_LEFT",
                                       "ID:" + str(player_id)])

        if self.combat is None:
            self.view_manager.refresh()
        else:
            self.server_combat.remove_player_from_queue(player_id)
            self.server_combat.check_if_player_exists()
            self.combat.create_new_view()
            self.server_combat.act()

        return True

    def abandon_lobby(self):
        """
        Leave/close a current lobby.
        :return:
        """
        if self.lobby is None:
            return

        player_id = self.lobby.local_player_id
        self.lobby = None
        self.view_manager.remove_view_for_enum(Views.LOBBY)
        self.__next_free_id = 0

        if player_id == 0:
            for sckt in self.sockets.values():
                communication.communicate(sckt, ["LOBBY_UPDATE", "ACTION:LOBBY_CLOSE"])
                sckt.close()
            self.sockets.clear()

            self.close_connector_thread()
            self.host_socket.close()
        else:
            communication.communicate(self.host_socket, ["GOODBYE"])

        self.tmp_gold = 0
        self.defeated_creatures = 0
        self.host_socket = None
        self.map = None
        self.current_room = None
        self.combat = None

    def get_new_id(self) -> int:
        """
        Take a next free ID value and increment it.
        """
        self.__next_free_id += 1
        return self.__next_free_id - 1

    def get_occupied_ports_list(self) -> list[int]:
        """
        Get a list of currently used player port numbers.
        """
        ports = []
        for sckt in self.sockets.values():
            ports.append(sckt.getsockname()[1])

        return ports

    def is_local(self):
        if self.lobby is None:
            return True

        return self.lobby.is_local()

    def add_socket(self, sckt: socket.socket, player_id: int) -> bool:
        """
        Add a new socket of player.
        """
        for pid in self.sockets.keys():
            if pid == player_id:
                return False

        self.sockets[player_id] = sckt
        return True

    def remove_socket(self, player_id: int) -> bool:
        """
        Remove socket of player.
        """
        if player_id in self.sockets.keys():
            self.sockets.pop(player_id)
            return True

        return False

    def get_id_of_socket(self, sckt: socket.socket) -> int:
        """
        Find id number of socket. Returns -1 if not found.
        """
        for ind in self.sockets.keys():
            if self.sockets[ind] == sckt:
                return ind

        return -1

    def close(self):
        """
        Close the running game instance.
        :return:
        """
        self.abandon_lobby()
        self.running = False

    def generate_map(self, size: MapSize):
        """
        Create a new map object
        :param size: enum for size of generated map
        :return:
        """
        self.map = Map()
        self.map.generate(size)
        self.current_room = self.map.get_first_room()

    def begin_game_start_procedure(self):
        """
        Communicates that the game is starting, sends the game map.
        """
        # Send map to clients
        map_json = jsonpickle.encode(self.map)
        for client in self.sockets.values():
            communication.communicate(client,
                                      ["GAME_START", "STATUS:INFO", "CONTENT-LENGTH:" + str(len(map_json))],
                                      map_json)
        # Reset ready status
        # Ready will now hold information that client received a valid information about starting game
        for participant in self.lobby.participants:
            participant.ready = False
        # Host is ready
        self.lobby.get_local_participant().ready = True

        if len(self.lobby.participants) == 1:
            self.start_game()

    def start_game(self):
        """
        Starts the game
        """
        # Close listening for connections
        self.close_connector_thread()

        # Set all values
        for participant in self.lobby.participants:
            char = participant.character
            char.name = participant.name
            char.id = participant.player_id
            char.hp = char.base_hp
            char.energy = char.base_energy

        # Change view
        self.current_room = self.map.get_first_room()
        self.view_manager.set_new_view_for_enum(Views.ROOM, ViewRoom(self.current_room))
        self.view_manager.set_current(Views.ROOM)

    def send_next_room_action(self):
        """
        Sends info to all clients that the party is going further.
        :return:
        """
        action = ""
        if self.current_room.has_next():
            action += "NEXT_ROOM"
        else:
            action += "DUNGEON_END"
        for client in self.sockets.values():
            answer = communication.communicate_and_get_answer(client, ["GAMEPLAY", "ACTION:" + action])
            received_action = utility.get_value_of_argument(answer, "ACTION")
            received_status = utility.get_value_of_argument(answer, "STATUS")

            if received_action != action or received_status != "OK":
                # TODO KICK PLAYER
                self.abandon_lobby()

    def go_to_the_next_room(self):
        """
        Gets the next room and changes the view
        """
        self.current_room = self.current_room.get_next()
        self.view_manager.set_new_view_for_enum(Views.ROOM, ViewRoom(self.current_room))
        self.view_manager.set_current(Views.ROOM)

    def get_players(self) -> list[Player]:
        """
        Returns player objects of the participants
        :return: list[player]
        """
        players = list[Player]()
        for participant in self.lobby.participants:
            players.append(participant.character)
        return players
