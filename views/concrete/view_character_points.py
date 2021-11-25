import context
from characters.player_factory import PlayerFactory
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_shop import ViewShop
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewCharacterPoints(ViewBase):
    """
    View used to create or modify character
    """
    def __init__(self):
        super().__init__()
        # Do you really want to override?
        self._confirm_overwrite = False

        # Do you really want to delete?
        self._confirm_delete = False

        # Do you really want to reset?
        self._confirm_reset = False

        # Determine name for character
        self.saved_character_name = settings["SELECTED_CHARACTER"]
        if self.saved_character_name == "":
            self._name = ""
        else:
            self._name = settings["SELECTED_CHARACTER"]

        self._character = PlayerFactory.load_player(self._name)

        self.options = [
            ["NAME", Views.CHARACTER_POINTS, lambda: None, Input.TEXT_FIELD],
            ["UPGRADE", Views.CHARACTER_POINTS,
             lambda: self._character.upgrade_stat(self.get_input_of_option("UPGRADE")), Input.LEFT_RIGHT_ENTER],
            ["SHOP", Views.SHOP,
             lambda: context.GAME.view_manager.set_new_view_for_enum(Views.SHOP, ViewShop(self._character)),
             Input.SELECT],
            ["SAVE", None, lambda: self.save(), Input.SELECT],
            ["DELETE", None, lambda: self.delete(), Input.SELECT],
            ["RESET CHARACTER", None, lambda: self.reset(), Input.SELECT]
        ]

        self.inputs = {
            "NAME": self._name,
            "UPGRADE": [0, list(self._character.stats.keys())]
        }

    def print_screen(self):
        # Prepare columns
        statistics = self._prepare_statistics()
        attacks = self._prepare_skills()

        print()
        PrintUtility.print_dividing_line()

        PrintUtility.print_in_columns([statistics, attacks], equal_size=True)

        PrintUtility.print_dividing_line()

        self.print_text("You have §g{0} points§0 to spend!".format(self._character.points))
        print()

        self._print_options()

        if self._confirm_overwrite:
            self._confirm_overwrite = False

        if self._confirm_reset:
            self._confirm_reset = False

    def _prepare_statistics(self):
        """
        Creates string with current statistics and returns list of lines
        :return: list[str]
        """

        stats_out = ["STATS:"]

        for stat in self._character.stats:
            stats_out.append(stat + ": " + str(self._character.stats[stat]))

        return stats_out

    def _prepare_skills(self):
        """
        Prepares list of attacks that selected character has
        :return: list[str]
        """
        list = ["SKILLS:"]
        for attack in self._character.attacks:
            attack_str = "{name} [§bENERGY COST: {cost}§0]".format(name=attack.name, cost=attack.cost)
            list.append(attack_str)

        return list

    def delete(self):
        if self._confirm_delete:
            PlayerFactory.delete(self._name)
            context.GAME.view_manager.set_current(Views.CHARACTERS)
        else:
            self.print_text("§rDo you really want to delete your precious character? Press again to confirm.§0")
            self._confirm_delete = True

    def reset(self):
        if self._confirm_reset:
            self._character.reset_stats()
            context.GAME.view_manager.set_current(Views.CHARACTERS)
        else:
            self.print_text("§rDo you really want to reset your precious character? Press again to confirm.§0")
            self._confirm_reset = True

    def save(self):
        name = self.inputs["NAME"]
        if name == "":
            context.GAME.view_manager.refresh()
            PrintUtility.print_with_dividing(PrintUtility.center("§rName of the character can't be empty!§0"))
            return

        self._character.name = name
        from characters.saved_characters import saved_characters  # because circular import
        if self._character.name != self.saved_character_name and saved_characters.get(self._character.name):
            if self._confirm_overwrite:
                PlayerFactory.save_player(self._character)
                context.GAME.view_manager.set_current(Views.CHARACTERS)
            else:
                self._confirm_overwrite = True
                self.print_text("§rThis will overwrite existing character! Press again to confirm.§0")
        else:
            PlayerFactory.save_player(self._character)
            context.GAME.view_manager.set_current(Views.CHARACTERS)
