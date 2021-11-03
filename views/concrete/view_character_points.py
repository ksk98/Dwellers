import context
from characters.character_config import config
from characters.enums.stats_enum import Stat
from characters.player_factory import PlayerFactory
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_shop import ViewShop
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewCharacterPoints(ViewBase):
    """
    View used to create or modify character
    """
    def __init__(self):
        super().__init__()
        # Do you really want to override?
        self.confirm_overwrite = False

        # Do you really want to delete?
        self.confirm_delete = False

        # Determine name for character
        self.saved_character_name = settings["SELECTED_CHARACTER"]
        if self.saved_character_name == "":
            self._name = "Default"
        else:
            self._name = settings["SELECTED_CHARACTER"]

        self._character = PlayerFactory.load_player(self._name)

        # Create names for options
        hp_button_string = "UPGRADE HEALTH (+{0})".format(self.get_upgrade_amount_for(Stat.HEALTH))
        ep_button_string = "UPGRADE ENERGY (+{0})".format(self.get_upgrade_amount_for(Stat.ENERGY))
        sp_button_string = "UPGRADE STRENGTH (+{0})".format(self.get_upgrade_amount_for(Stat.STRENGTH))

        self.options.insert(0, ["MAP SIZE", Views.LOBBY, lambda: None, Input.MULTI_TOGGLE])

        self.options = [
            ["NAME", None, lambda: None, Input.TEXT_FIELD],
            [hp_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.HEALTH), Input.SELECT],
            [ep_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.ENERGY), Input.SELECT],
            [sp_button_string, Views.CHARACTER_POINTS, lambda: self._character.upgrade_stat(Stat.STRENGTH),
             Input.SELECT],
            ["SHOP", Views.SHOP,
             lambda: context.GAME.view_manager.set_new_view_for_enum(Views.SHOP, ViewShop(self._character)),
             Input.SELECT],
            ["SAVE", None, lambda: self.save(), Input.SELECT],
            ["DELETE", None, lambda: self.delete(), Input.SELECT],
            ["RESET CHARACTER", Views.CHARACTER_POINTS, lambda: self._character.reset_stats(), Input.SELECT]
        ]

        self.inputs = {
            "NAME": self._name,
        }

    def print_screen(self):
        # Prepare columns
        statistics = self._prepare_statistics()
        attacks = self._prepare_skills()

        print()
        print_whole_line_of_char('=')

        print_in_two_columns([statistics, attacks])

        print_whole_line_of_char('=')
        self.print_text("You have {0} points to spend!".format(self._character.points))
        print()

        self._print_options()

        if self.confirm_overwrite:
            self.confirm_overwrite = False

        if self.confirm_overwrite:
            self.confirm_overwrite = False

    def _prepare_statistics(self):
        """
        Creates string with current statistics and returns list of lines
        :return: list[str]
        """
        stats = "STATS:\n" \
                "Health Points: {0}\n" \
                "Energy Points: {1}\n" \
                "Strength Points: {2}\n".format(
                    str(self._character.base_hp),
                    str(self._character.base_energy),
                    str(self._character.strength))

        return stats.splitlines()

    def _prepare_skills(self):
        """
        Prepares list of attacks that selected character have
        :return: list[str]
        """
        list = ["SKILLS:"]
        for attack in self._character.attacks:
            attack_str = "{name} [ENERGY COST: {cost}]".format(name=attack.name, cost=attack.cost)
            list.append(attack_str)

        return list

    def delete(self):
        if self.confirm_delete:
            PlayerFactory.delete(self._name)
            context.GAME.view_manager.set_current(Views.CHARACTERS)
        else:
            self.print_text("Do you really want to delete your precious character? Press again to confirm.")
            self.confirm_delete = True

    def save(self):
        self._character.name = self.inputs["NAME"]
        from characters.saved_characters import saved_characters  # because circular import
        if self._character.name != self.saved_character_name and saved_characters.get(self._character.name):
            if self.confirm_overwrite:
                PlayerFactory.save_player(self._character)
                context.GAME.view_manager.set_current(Views.CHARACTERS)
            else:
                self.confirm_overwrite = True
                self.print_text("This will overwrite existing character! Press again to confirm.")
        else:
            PlayerFactory.save_player(self._character)
            context.GAME.view_manager.set_current(Views.CHARACTERS)

    @staticmethod
    def get_upgrade_amount_for(stat: Stat) -> str:
        return str(config["upgrades"][stat])
