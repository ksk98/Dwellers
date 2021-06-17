import context
from characters.saved_characters import saved_characters
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_character_points import ViewCharacterPoints
from views.input_enum import Input
from views.view_enum import Views


class ViewCharacters(ViewBase):
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
            ["BACK TO MENU", Views.MENU, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        self._character_names = self._get_names()
        self._option_names = self._get_option_names(self._character_names)

        print("To start a game you need to select a character.".center(settings["MAX_WIDTH"]))
        print("NOTE: to create a character, select an empty slot".center(settings["MAX_WIDTH"]))
        print("Available characters:".center(settings["MAX_WIDTH"]))
        indx = 0
        for option in self.options:
            if indx < len(self._option_names):
                option[0] = self._option_names[indx]
            indx += 1
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

    def _get_option_names(self, character_names: list):
        option_names = []
        for name in character_names:
            option_names.append(self._get_option_text(name))
        return option_names

    def _get_option_text(self, character_name: str) -> str:
        if character_name != "":
            return self._check_if_name_is_selected(character_name) + "[ " + character_name + " ]"
        else:
            return "- EMPTY -"

    def _select(self, name: str):
        if settings["SELECTED_CHARACTER"] == name:      # is selected
            context.GAME.view_manager.remove_view_for_enum(Views.CHARACTER_POINTS)
            context.GAME.view_manager.set_new_view_for_enum(Views.CHARACTER_POINTS, ViewCharacterPoints())
            context.GAME.view_manager.set_current(Views.CHARACTER_POINTS)
        else:
            settings["SELECTED_CHARACTER"] = name
            if name != "":
                context.GAME.view_manager.set_current(Views.CHARACTERS)
            else:
                context.GAME.view_manager.remove_view_for_enum(Views.CHARACTER_POINTS)
                context.GAME.view_manager.set_new_view_for_enum(Views.CHARACTER_POINTS, ViewCharacterPoints())
                context.GAME.view_manager.set_current(Views.CHARACTER_POINTS)

    @staticmethod
    def _get_names() -> list[str]:
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
