import context
from characters.attacks.repo import all_attacks
from characters.character_config import config
from characters.player import Player
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewShop(ViewBase):
    """
    View used to buy new things
    """

    def __init__(self, character: Player):
        super().__init__()

        # Character that is shopping
        self._character = character

        # Used to display message
        self._not_enough_gold = False

        # Used to display message
        self._no_more_skills_to_buy = False

        # Prepare names for option
        skills_to_buy = self._prepare_list_for_option()
        self.inputs = {
            "SELECT ATTACK": [0, skills_to_buy]
        }

        self.options = [
            ["BUY 1 STAT POINT [{0} GOLD]".format(config["base"]["skill_point_cost"]), Views.SHOP, lambda: self._buy_point(), Input.SELECT],
            ["SELECT ATTACK", Views.SHOP, lambda: None, Input.MULTI_TOGGLE],
            ["BUY SELECTED ATTACK", Views.SHOP, lambda: self._buy_skill(), Input.SELECT],
            ["BACK", Views.CHARACTER_POINTS, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        print()
        print_whole_line_of_char('=')
        # Print table of contents
        print_in_two_columns(self._prepare_table())

        print_whole_line_of_char('=')
        # Gold amount
        self.print_text("You have {0} gold to spend!".format(context.GAME.total_gold))

        # Not enough gold
        if self._not_enough_gold:
            self.print_text("You don't have enough gold to do that!")
            self._not_enough_gold = False

        # All skills purchased
        if self._no_more_skills_to_buy:
            self.print_text("All attacks have been purchased!")

        print()

        self._print_options()

    def _buy_point(self):
        """
        Try to buy 1 stat point
        :return:
        """
        if self._take_gold(config['base']['skill_point_cost']):
            self._character.points += 1

    def _buy_skill(self):
        """
        Try to buy selected skill
        """
        skill_name = self.get_input_of_option("SELECT ATTACK")

        # All skills have been purchased
        if skill_name is None:
            self._no_more_skills_to_buy = True
            return

        # Search for attack
        for attack in all_attacks:
            # Found it
            if attack.name in skill_name:
                # Try to buy it
                if self._take_gold(attack.gold_cost):
                    self._character.attacks.append(attack)
                    context.GAME.view_manager.set_new_view_for_enum(Views.SHOP, ViewShop(self._character))
                    return

    def _get_characters_skills(self):
        """
        Get a list of character's skills names
        :return: list[str] containing skill names that character own
        """
        character_attacks = []
        for character_attack in self._character.attacks:
            character_attacks.append(character_attack.name)
        return character_attacks

    def _prepare_list_for_option(self):
        """
        Prepares names for multiselect option
        :return: list[str] with names
        """
        skills_to_buy = []
        for attack in all_attacks:
            if attack.name not in self._get_characters_skills():
                option_str = "{name} [{amount} GOLD]".format(name=attack.name, amount=attack.gold_cost)
                skills_to_buy.append(option_str)
        return skills_to_buy

    def _prepare_table(self):
        """
        Creates list[ list[str], list[str] ].
        The first list contains attack names, the second one descriptions of those attacks.
        Those list will be displayed as a nice table with two columns.
        :return: list[ list[str], list[str] ]
        """
        attack_names = ["ATTACK:"]
        attack_descriptions = ["DESCRIPTION:"]
        for attack in all_attacks:

            # Take only attacks that character doesn't already have
            if attack.name not in self._get_characters_skills():
                attack_str = "{name}".format(name=attack.name)
                attack_names.append(attack_str)

                desc_str = "{desc}".format(desc=attack.desc)
                attack_descriptions.append(desc_str)

        return [attack_names, attack_descriptions]

    def _take_gold(self, amount):
        """
        Try to take given amount of gold from player
        :param amount: to be taken
        :return: False when player has not enough gold, True when succeed
        """
        if amount > context.GAME.total_gold:
            self._not_enough_gold = True
            return False
        else:
            context.GAME.total_gold -= amount
            return True
