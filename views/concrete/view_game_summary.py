import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char
from views.view_enum import Views


class ViewGameSummary(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        # TODO Looted gold sent by server?
        # TODO Number of defeated creatures?
        print()
        print_whole_line_of_char('=')
        self.print_multiline_text(
            "\nCONGRATULATIONS!\n \nYOU HAVE REACHED THE END OF A DUNGEON!\nLOOTED GOLD: {0}\n".format(
                str(context.GAME.gold)))
        print_whole_line_of_char('=')
        print()
        self._print_options()

