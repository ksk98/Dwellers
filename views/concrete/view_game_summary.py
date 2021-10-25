import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char
from views.view_enum import Views


class ViewGameSummary(ViewBase):
    def __init__(self):
        super().__init__()
        # Save looted gold amount
        # TODO DIVIDE BY PLAYER COUNT
        self.gold = context.GAME.tmp_gold
        # Collect it
        context.GAME.total_gold += self.gold
        # Reset
        context.GAME.tmp_gold = 0

        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        # TODO Looted gold sent by server?
        # TODO Number of defeated creatures?
        print()
        print_whole_line_of_char('=')
        self.print_multiline_text(
            "\nCONGRATULATIONS!\n "
            "\n"
            "YOU HAVE REACHED THE END OF A DUNGEON!\n"
            "LOOTED GOLD: {0}\n"
            "DEFEATED CREATURES: {1}\n".format(
                str(self.gold), str(context.GAME.defeated_creatures)))
        print_whole_line_of_char('=')
        print()
        self._print_options()

