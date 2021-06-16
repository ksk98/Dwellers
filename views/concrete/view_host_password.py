import context
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewHostPassword(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["PASSWORD", None, lambda: None, Input.TEXT_FIELD],
            ["HOST", Views.LOBBY, lambda: context.GAME.host_lobby(self.inputs.get("PASSWORD")), Input.SELECT],
            ["CANCEL", Views.MENU, lambda: None, Input.SELECT]
        ]
        self.inputs = {
            "PASSWORD": ""
        }

    def print_screen(self):
        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))
