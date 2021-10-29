import context
import views.concrete.view_characters
from characters.saved_characters import saved_characters
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
        # Character check
        if self._check_if_character_exists():
            self._add_connection_buttons()

    def print_screen(self):
        self._print_logo()

        if not self._check_if_character_exists():
            self.print_text("YOU NEED TO SELECT A CHARACTER BEFORE STARTING A GAME!")

        self._print_options()

    def _check_if_character_exists(self):
        """
        Check if selected character is in file saved_characters
        :return: true if character exists
        """
        if settings["SELECTED_CHARACTER"] in saved_characters:
            return True
        return False

    def _add_connection_buttons(self):
        """
        Adds buttons used to host / join lobby
        """
        self.options.insert(0, ["JOIN LOBBY", Views.JOIN,
                                lambda: context.GAME.view_manager.set_new_view_for_enum(Views.JOIN, ViewJoin()),
                                Input.SELECT])
        self.options.insert(0, ["CREATE LOBBY", Views.HOST_PASSWORD,
                                lambda: context.GAME.view_manager.set_new_view_for_enum(Views.HOST_PASSWORD,
                                                                                        ViewHostPassword()),
                                Input.SELECT])
