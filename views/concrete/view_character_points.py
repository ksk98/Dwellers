from characters.character_config import config
from characters.enums.stats_enum import Stat
from characters.player import Player
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewCharacterPoints(ViewBase):
    """
    View used to create or modify character
    """
    def __init__(self):
        super().__init__()
        self.saved_character_name = settings["SELECTED_CHARACTER"]
        if self.saved_character_name == "":
            self._name = "Default"
        else:
            self._name = settings["SELECTED_CHARACTER"]

        self._character = Player(self._name)

        hp_button_string = "Health Points (+{0})".format(self.get_upgrade_amount_for(Stat.HEALTH))
        ep_button_string = "Energy Points (+{0})".format(self.get_upgrade_amount_for(Stat.ENERGY))
        sp_button_string = "Strength Points (+{0})".format(self.get_upgrade_amount_for(Stat.STRENGTH))

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

    def print_screen(self):
        self.print_multiline_text(
            "Current statistics:\n"
            "Health Points: {0}\n"
            "Energy Points: {1}\n"
            "Strength Points: {2}\n"
            "You have {3} points to spend!\n \n".format(
                str(self._character.base_hp), str(self._character.base_energy),
                str(self._character.strength), str(self._character.points)))

        self._print_options()

    def save(self):
        # TODO confirmation on overwriting another character
        self._character.name = self.inputs["NAME"]
        if self._character.name != self.saved_character_name:
            self._character.overwrite_stats(self.saved_character_name)
        else:
            self._character.save_stats()

    @staticmethod
    def get_upgrade_amount_for(stat: Stat) -> str:
        return str(config["upgrades"][stat])
