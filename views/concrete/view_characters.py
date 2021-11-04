import context
import views.concrete.view_play
from characters.saved_characters import saved_characters
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_character_points import ViewCharacterPoints
from views.input_enum import Input
from views.view_enum import Views


class ViewCharacters(ViewBase):
    """
    Displays currently saved characters and is used to select one
    """
    def __init__(self):
        super().__init__()
        self._character_names = self._get_names()
        self._option_names = self._get_option_names(self._character_names)

        self.options = [
            [self._option_names[0], None,
                lambda: self._select(self._character_names[0]), Input.SELECT],
            [self._option_names[1], None,
                lambda: self._select(self._character_names[1]), Input.SELECT],
            [self._option_names[2], None,
                lambda: self._select(self._character_names[2]), Input.SELECT],
            [self._option_names[3], None,
                lambda: self._select(self._character_names[3]), Input.SELECT],
            ["PLAY", Views.PLAY,
                lambda: context.GAME.view_manager.set_new_view_for_enum
                (Views.PLAY, views.concrete.view_play.ViewPlay()), Input.SELECT],
            ["BACK TO MENU", Views.MENU, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        self._character_names = self._get_names()
        self._option_names = self._get_option_names(self._character_names)

        self._print_logo()
        self.print_multiline_text("NOTE: to create a character, select an empty slot\n" +
                                  "Available characters:\n")

        self._set_options_text()

        self._print_options()

    def _set_options_text(self):
        """
        Sets the text for options
        """
        indx = 0
        for option in self.options:
            if indx < len(self._option_names):
                option[0] = self._option_names[indx]
            indx += 1

    def _get_option_names(self, character_names: list):
        """
        Prepare a list of names for options using available characters
        :param character_names: list of available characters
        :return: list containing strings - names for options representing available characters
        """
        option_names = []
        for name in character_names:
            option_names.append(self._get_option_text(name))
        return option_names

    def _get_option_text(self, character_name: str) -> str:
        """
        Returns text for one option - character's name with all necessary brackets or info about slot being empty
        :param character_name: string containing character's name
        :return: string for use as option text
        """
        if character_name != "":
            return self._check_if_name_is_selected(character_name) + "[ " + character_name + " ]"
        else:
            return "- EMPTY -"

    @staticmethod
    def _select(name: str):
        """
        Sets character's name as selected
        :param name: name of the character to be selected
        """
        if settings["SELECTED_CHARACTER"] != name:
            settings["SELECTED_CHARACTER"] = name
            context.GAME.view_manager.set_current(Views.CHARACTERS)
        else:
            # Create new character
            context.GAME.view_manager.remove_view_for_enum(Views.CHARACTER_POINTS)
            context.GAME.view_manager.set_new_view_for_enum(Views.CHARACTER_POINTS, ViewCharacterPoints())
            context.GAME.view_manager.set_current(Views.CHARACTER_POINTS)

        # Update settings - save which character is selected
        context.GAME.save_settings()

    @staticmethod
    def _get_names() -> list[str]:
        """
        Creates 4-element list containing character names / empty strings
        """
        character_names = ["", "", "", ""]
        indx = 0
        for key in saved_characters:
            character_names[indx] += key
            indx += 1
        return character_names

    @staticmethod
    def _check_if_name_is_selected(name: str) -> str:
        if settings["SELECTED_CHARACTER"] == name:
            return "[*]"
        return "[ ]"
