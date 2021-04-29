from logic.lobby import Lobby
from logic.participant import Participant
import socket
import context
from network import communication
from network import utility
from views import views_context
from views.concrete.view_menu import ViewMenu
import jsonpickle
from os import name
import time
from config import config
import msvcrt


class Game:
    def __init__(self):
        self.lobby = None
        context.PLAYER = Participant()

        views_context.MENU = ViewMenu()
        self.view = views_context.MENU
        self.view.print_screen()

    def tick(self):
        # Windows
        if name == 'nt':
            # If key is waiting to be read then read it
            if msvcrt.kbhit():
                inp = msvcrt.getch()

            # If you are not a host then check for any incoming messages from the host


        # Linux/Mac
        else:
            exit(0)
            # TODO: https://stackoverflow.com/questions/6179537/python-wait-x-secs-for-a-key-and-continue-execution-if-not-pressed
        time.sleep(config["TICK_WAIT_TIME"])

    def create_lobby(self):
        # Create lobby
        self.lobby = Lobby()

        # Create a participant for host and add it
        host_participant = Participant()
        host_participant.isHost = True
        self.lobby.add_participant(host_participant)

        # Update screen
        self.screen.update()

    def join_external_lobby(self, ip: str, port: int) -> str:
        """
        Create a new lobby by joining to a hosted lobby.

        :return: error message if unsuccesful (empty string if otherwise)
        """
        # Send request for a lobby
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_socket.connect((ip, port))

        participant_json = jsonpickle.encode(context.PLAYER)

        header = [
            "REQUEST_GENERAL:JOIN",
            "CONTENT_LENGTH:" + str(len(participant_json))
        ]

        response = communication.communicate_and_get_answer(local_socket, header, participant_json)
        if utility.get_value_of_argument(response, "STATUS") != "OK":
            return utility.get_value_of_argument(response, "REASON")

        # If host responded with a json of a lobby create lobby from json
        self.lobby = jsonpickle.decode(utility.get_content_from_frame(response))
        return ""

    def add_to_lobby(self, participant):
        """
        This is called when a players from the outside joins the lobby.

        :param participant: object representing the joining player
        """
        if self.lobby is None:
            return False

        self.lobby.add_participant(participant)
        return True

    def remove_from_lobby(self, participant):
        """
        This is called when a player from the outside leaves the lobby.

        :param participant: object representing the leaving player
        """
        if self.lobby is None:
            return False

        self.lobby.remove_participant(participant)
        return True

    def abandon_lobby(self):
        """
        Player leaves current lobby.

        :return:
        """
        context.LOBBY = None

    @staticmethod
    def close():
        # TODO: proper closing
        exit(0)

