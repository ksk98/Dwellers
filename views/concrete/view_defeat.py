import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char
from views.view_enum import Views


class ViewDefeat(ViewBase):
    """
    Screen telling that party has been wiped out
    """
    def __init__(self):
        super().__init__()

        # Reset looted gold and killed creatures
        context.GAME.tmp_gold = 0
        context.GAME.defeated_creatures = 0
        # TODO DELETE CHARACTER...

        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        print()
        print_whole_line_of_char('=')
        self.print_multiline_text("\nDEFEAT!\n \n"
                                  "YOU HAVE BEEN WIPED OUT!\n"
                                  "ALL LOOT HAS BEEN LOST... SAME AS YOU...")
        print_whole_line_of_char('=')
        print()
        self._print_options()
