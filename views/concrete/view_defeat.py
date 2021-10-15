from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewDefeat(ViewBase):
    """
    Screen telling that party has been wiped out
    """
    def __init__(self):
        super().__init__()
        self.options = [
            ["OK", Views.MENU, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        self.print_multiline_text("DEFEAT!\nYOU HAVE BEEN WIPED OUT!\n \n")
        self._print_options()
