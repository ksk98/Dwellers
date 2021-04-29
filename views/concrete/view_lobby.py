from views.concrete.view_base import ViewBase
from views import views_context
from config import config
import context


class ViewLobby(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ("READY", None, lambda: None),
            ("EXIT", views_context.MENU, lambda: context.GAME.abandon_lobby())
        ]

    def print_screen(self):
        players = self.local_game.lobby.participants
        for player in players:
            print((player.name + "[" + player.id + "]").center(config["MAX_WIDTH"]))
        for i in range(config["MAX_PLAYERS"] - len(players)):
            print("free".center(config["MAX_WIDTH"]))
        print("")
        self._print_options()
