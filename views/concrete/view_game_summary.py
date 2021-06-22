import context
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewGameSummary(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        self.print_text("CONGRATULATIONS!".center(settings["MAX_WIDTH"]))
        self.print_text("YOU HAVE REACHED THE END OF A DUNGEON!".center(settings["MAX_WIDTH"]))
        line = "LOOTED GOLD: " + str(context.GAME.gold)
        self.print_text(line.center(settings["MAX_WIDTH"]))
        print()
        self._print_options()

