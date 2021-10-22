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
        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        # TODO DELETE CHARACTER...
        # TODO Can't host next game after defeat...
        print()
        print_whole_line_of_char('=')
        self.print_multiline_text("\nDEFEAT!\n \nYOU HAVE BEEN WIPED OUT!\n")
        print_whole_line_of_char('=')
        print()
        self._print_options()
