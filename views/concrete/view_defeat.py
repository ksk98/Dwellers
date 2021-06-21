import context
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewDefeat(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["OK", Views.MENU, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        self.print_text("DEFEAT!".center(settings["MAX_WIDTH"]))
        self.print_text("YOU HAVE BEEN WIPED OUT!".center(settings["MAX_WIDTH"]))
        print()
        self._print_options()
