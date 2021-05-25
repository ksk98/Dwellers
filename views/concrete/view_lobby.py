from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views
from config import config
from settings import settings
import context


class ViewLobby(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ("READY", None, lambda: None, Input.SELECT),
            ("EXIT", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT)
        ]

    def print_screen(self):
        players = context.GAME.lobby.participants
        for player in players:
            print((player.name + "[" + str(player.player_id) + "]").center(settings["MAX_WIDTH"]))
        for i in range(config["MAX_PLAYERS"] - len(players)):
            print("free".center(settings["MAX_WIDTH"]))
        print("")
        self._print_options()
