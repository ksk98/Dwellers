import context
import title_ascii
from config import config
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_characters import ViewCharacters
from views.concrete.view_play import ViewPlay
from views.input_enum import Input
from views.view_enum import Views


class ViewTest1(ViewBase):
    def __init__(self):
        super().__init__()

        self.options = [
            ["MULTITOGGLE", Views.TEST, lambda: None, Input.MULTI_TOGGLE]
        ]

        self.inputs = {
            "MULTITOGGLE": [1, ["TWOJA", "BABCIA", "WCISKA", "KAPCIA"]]
        }

    def print_screen(self):
        for option in self.options:
            to_print = option[0]
            value = self.get_input_of_option(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))
