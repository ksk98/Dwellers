import title_ascii
from views.concrete.view_base import ViewBase
from views.concrete.view_lobby import ViewLobby
from config import config


class ViewMenu(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ("CREATE LOBBY", ViewLobby(), lambda: None),
            ("JOIN LOBBY", None, lambda: None),
            ("CHARACTERS", None, lambda: None),
            ("SETTINGS", None, lambda: None),
            ("EXIT", None, lambda: self.local_game.close())
        ]

    def print_screen(self):
        for line in title_ascii.title:
            if title_ascii.title.index(line) != len(title_ascii.title)-1:
                print(line.center(config["MAX_WIDTH"]))
            else:
                ver = config["VERSION"]
                print((line + ver).center(config["MAX_WIDTH"] + len(ver)-1))
        print("")
        self._print_options()
