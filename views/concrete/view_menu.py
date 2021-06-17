import context
import title_ascii
from config import config
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_characters import ViewCharacters
from views.concrete.view_play import ViewPlay
from views.input_enum import Input
from views.view_enum import Views


class ViewMenu(ViewBase):
    def __init__(self):
        super().__init__()

        self.options = [
            ["PLAY", Views.PLAY,
             lambda: context.GAME.view_manager.set_new_view_for_enum(Views.PLAY, ViewPlay()),
             Input.SELECT],
            ["CHARACTERS", Views.CHARACTERS,
             lambda: context.GAME.view_manager.set_new_view_for_enum(Views.CHARACTERS, ViewCharacters()), Input.SELECT],
            ["SETTINGS", Views.SETTINGS, lambda: None, Input.SELECT],
            ["EXIT", None, lambda: context.GAME.close(), Input.SELECT]
        ]

    def print_screen(self):
        for line in title_ascii.title:
            if title_ascii.title.index(line) != len(title_ascii.title)-1:
                print(line.center(settings["MAX_WIDTH"]))
            else:
                ver = config["VERSION"]
                print((line + ver).center(settings["MAX_WIDTH"] + len(ver)-1))
        print("")
        self._print_options()
