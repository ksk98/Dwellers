import context
from characters.character_config import config
from characters.enums.stats_enum import Stat
from characters.player import Player
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewCharacterPoints(ViewBase):
    def __init__(self):
        super().__init__()
        self.saved_character_name = settings["SELECTED_CHARACTER"]
        if self.saved_character_name == "":
            self._name = "Default"
        else:
            self._name = settings["SELECTED_CHARACTER"]

        self._character = Player(self._name)

        hp_button_string = "Health Points (+" + self.get_upgrade_amount_for(Stat.HEALTH) + ")"
        ep_button_string = "Energy Points (+" + self.get_upgrade_amount_for(Stat.ENERGY) + ")"
        sp_button_string = "Strength Points (+" + self.get_upgrade_amount_for(Stat.STRENGTH) + ")"
        self.options = [
            ["NAME", None, lambda: None, Input.TEXT_FIELD],
            [hp_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.HEALTH), Input.SELECT],
            [ep_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.ENERGY), Input.SELECT],
            [sp_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.STRENGTH),
             Input.SELECT],
            ["SAVE", Views.CHARACTERS, lambda: self.save(), Input.SELECT],
            ["RESET CHARACTER", Views.CHARACTER_POINTS, lambda: self._character.reset_stats(), Input.SELECT]
        ]
        self.inputs = {
            "NAME": self._name
        }

    def save(self):
        # TODO confirmation on overwriting another character
        self._character.name = self.inputs["NAME"]
        if self._character.name != self.saved_character_name:
            self._character.overwrite_stats(self.saved_character_name)
        else:
            self._character.save_stats()

    def print_screen(self):
        print("Current statistics:".center(settings["MAX_WIDTH"]))
        print(("Health Points: " + str(self._character.hp)).center(settings["MAX_WIDTH"]))
        print(("Energy Points: " + str(self._character.energy)).center(settings["MAX_WIDTH"]))
        print(("Strength Points: " + str(self._character.strength)).center(settings["MAX_WIDTH"]))
        print(("You have " + str(self._character.points) + " points to spend!").center(settings["MAX_WIDTH"]))
        print()
        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

    @staticmethod
    def get_upgrade_amount_for(stat: Stat) -> str:
        return str(config["upgrades"][stat])
