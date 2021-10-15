import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewHostPassword(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["HOST", Views.LOBBY, lambda: context.GAME.host_lobby(self.inputs.get("PASSWORD")), Input.SELECT],
            ["PASSWORD", None, lambda: None, Input.TEXT_FIELD],
            ["CANCEL", Views.MENU, lambda: None, Input.SELECT]
        ]
        self.inputs = {
            "PASSWORD": ""
        }

    def print_screen(self):
        self._print_logo()
        self._print_options()