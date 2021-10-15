import context
import views.concrete.view_characters
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_host_password import ViewHostPassword
from views.concrete.view_join import ViewJoin
from views.input_enum import Input
from views.view_enum import Views


class ViewPlay(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["SELECT A CHARACTER", Views.CHARACTERS,
             lambda: context.GAME.view_manager.set_new_view_for_enum(Views.CHARACTERS, views.concrete.view_characters.ViewCharacters()), Input.SELECT],
            ["BACK TO MENU", Views.MENU, lambda: context.GAME.view_manager.remove_view_for_enum(Views.PLAY), Input.SELECT]
        ]
        if settings["SELECTED_CHARACTER"] != "":
            self.add_connection_buttons()

    def print_screen(self):
        self._print_logo()

        if settings["SELECTED_CHARACTER"] == "":
            self.print_text("YOU NEED TO SELECT A CHARACTER BEFORE STARTING A GAME!")

        self._print_options()

    def add_connection_buttons(self):
        self.options.insert(0, ["JOIN LOBBY", Views.JOIN,
                                lambda: context.GAME.view_manager.set_new_view_for_enum(Views.JOIN, ViewJoin()),
                                Input.SELECT])
        self.options.insert(0, ["CREATE LOBBY", Views.HOST_PASSWORD,
                                lambda: context.GAME.view_manager.set_new_view_for_enum(Views.HOST_PASSWORD,
                                                                                        ViewHostPassword()),
                                Input.SELECT])
