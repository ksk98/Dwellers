from views.concrete.view_base import ViewBase
from views.concrete.view_error import ViewError
from views.concrete.view_lobby import ViewLobby
from views.input_enum import Input
from views.view_enum import Views
from settings import settings
import context


class ViewJoin(ViewBase):
    def __init__(self, ip="", port=settings["HOSTING_PORT"], password=""):
        super().__init__()
        self.options = [
            ["IP", Views.JOIN, lambda: None, Input.TEXT_FIELD],
            ["PORT", Views.JOIN, lambda: None, Input.TEXT_FIELD],
            ["PASSWORD", Views.JOIN, lambda: None, Input.TEXT_FIELD],
            ["JOIN", Views.LOBBY, lambda: self._join_action(), Input.SELECT],
            ["CANCEL", Views.MENU, lambda: None, Input.SELECT]
        ]
        self.inputs = {
            "IP": ip,
            "PORT": port,
            "PASSWORD": password
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

    def _join_action(self):
        err = context.GAME.join_external_lobby(self.inputs.get("IP"),
                                               int(self.inputs.get("PORT")),
                                               self.inputs.get("PASSWORD"))
        if err != "":
            self.options[self.get_index_of_option("JOIN")][1] = Views.ERROR
            context.GAME.view_manager.set_new_view_for_enum(Views.JOIN, ViewJoin(self.inputs.get("IP"),
                                                                                 self.inputs.get("PORT"),
                                                                                 ""))
            context.GAME.view_manager.set_new_view_for_enum(Views.ERROR, ViewError(err, Views.JOIN))
        else:
            context.GAME.view_manager.set_new_view_for_enum(Views.LOBBY, ViewLobby())
